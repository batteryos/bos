"""Tests for bos.prices -- Prices API client."""

from io import BytesIO
from unittest.mock import patch

import pytest

from bos.prices.client import PricesClient
from bos.prices.config import ENDPOINTS
from bos.prices.models import (
    ERCOT_HUBS,
    HUB_CONTRACT_MAP,
    AvailableDate,
    Contract,
    ContractPrice,
    Exchange,
)


class TestPricesClient:
    @pytest.fixture
    def client(self, mock_session):
        return PricesClient({"BOS_API": "test-token"}, ENDPOINTS)

    # -- list_exchanges ---------------------------------------------------

    def test_list_exchanges(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"mic": "IFED", "name": "ICE Futures", "url": "https://ice.com"}]
        )
        result = client.list_exchanges()
        assert len(result) == 1
        assert isinstance(result[0], Exchange)
        assert result[0].mic == "IFED"

    # -- list_contracts ---------------------------------------------------

    def test_list_contracts(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"symbol": "ERH", "node": "HB_HOUSTON", "shape": "peak"}]
        )
        result = client.list_contracts()
        assert len(result) == 1
        assert isinstance(result[0], Contract)
        assert result[0].symbol == "ERH"
        call_url = mock_session.get.call_args[0][0]
        assert "/kronos/contracts/IFED/" in call_url

    def test_list_contracts_custom_exchange(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.list_contracts("BOS")
        call_url = mock_session.get.call_args[0][0]
        assert "/kronos/contracts/BOS/" in call_url

    def test_list_contracts_with_filters(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.list_contracts("IFED", shape="peak", iso="ERCOT")
        call_kwargs = mock_session.get.call_args
        assert "shape" in str(call_kwargs)

    # -- get_contract -----------------------------------------------------

    def test_get_contract_available_dates(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "refdate": "2026-03-25",
                    "min_fordate": "2026-04-01",
                    "max_fordate": "2028-12-01",
                }
            ]
        )
        result = client.get_contract("ERH")
        assert len(result) == 1
        assert isinstance(result[0], AvailableDate)
        assert result[0].refdate == "2026-03-25"

    def test_get_contract_prices(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "exchange": "IFED",
                    "symbol": "ERH",
                    "refdate": "2026-03-25",
                    "fordate": "2026-06-01",
                    "price": 42.5,
                    "open": 41.0,
                    "high": 43.0,
                    "low": 40.5,
                    "close": 42.5,
                    "volume": 100,
                    "open_interest": 500,
                }
            ]
        )
        result = client.get_contract("ERH", refdate="2026-03-25")
        assert len(result) == 1
        assert isinstance(result[0], ContractPrice)
        assert result[0].price == 42.5
        assert result[0].volume == 100

    def test_get_contract_with_refdate(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"symbol": "ERH", "settlements": []}
        )
        client.get_contract("ERH", refdate="2025-03-25")
        call_args = mock_session.get.call_args
        assert "refdate" in str(call_args)

    def test_get_contract_with_fordate(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.get_contract("ERH", refdate="2026-03-25", fordate="2026-06-01")
        call_args = mock_session.get.call_args
        assert "fordate" in str(call_args)

    def test_get_contract_with_date_range(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.get_contract("ERH", startref="2026-01-01", endref="2026-03-25")
        call_args = mock_session.get.call_args
        assert "startref" in str(call_args)
        assert "endref" in str(call_args)

    def test_get_contract_with_strip(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.get_contract("ERH", refdate="2026-03-25", strip="CAL26")
        call_args = mock_session.get.call_args
        assert "strip" in str(call_args)

    def test_get_contract_custom_exchange(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data=[])
        client.get_contract("ERH", exchange_code="BOS")
        call_url = mock_session.get.call_args[0][0]
        assert "/kronos/contracts/BOS/ERH/" in call_url

    # -- get_available_refdates -------------------------------------------

    def test_get_available_refdates(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=["2026-03-25", "2026-03-24", "2026-03-21"]
        )
        result = client.get_available_refdates("ERH")
        assert len(result) == 3
        call_url = mock_session.get.call_args[0][0]
        assert "/available_dates/" in call_url

    def test_get_available_refdates_custom_exchange(
        self, client, mock_session, mock_response
    ):
        mock_session.get.return_value = mock_response(json_data=[])
        client.get_available_refdates("ERH", exchange_code="BOS")
        call_url = mock_session.get.call_args[0][0]
        assert "/kronos/contracts/BOS/ERH/available_dates/" in call_url

    # -- compare_prices ---------------------------------------------------

    def test_compare_prices(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"data": "comparison"})
        result = client.compare_prices("ERH", "IFED", "BOS", "2026-03-25")
        call_url = mock_session.get.call_args[0][0]
        assert "/kronos/compare/IFED/ERH/BOS/2026-03-25/" in call_url

    # -- Prices data endpoints --------------------------------------------

    def test_get_actuals(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(json_data={"data": "actuals"})
        result = client.get_actuals("ercot", "HB_HOUSTON", curves=["dam"])
        call_url = mock_session.post.call_args[0][0]
        assert "/prices/history/ercot/HB_HOUSTON/" in call_url

    def test_get_forwards(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(json_data={"data": "forwards"})
        result = client.get_forwards("ercot", "HB_HOUSTON", "2026-03-25")
        call_url = mock_session.post.call_args[0][0]
        assert "/prices/futures/ercot/HB_HOUSTON/2026-03-25/" in call_url

    def test_get_agg_forwards(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"data": "agg"})
        client.get_agg_forwards("IFED", "ercot", "HB_HOUSTON", "dam", "monthly")
        call_url = mock_session.get.call_args[0][0]
        assert "/prices/futures/IFED/ercot/HB_HOUSTON/dam/monthly/" in call_url

    # -- Constants --------------------------------------------------------

    def test_ercot_hubs_constant(self):
        assert "HB_HOUSTON" in ERCOT_HUBS
        assert len(ERCOT_HUBS) == 7

    def test_hub_contract_map(self):
        assert HUB_CONTRACT_MAP["HB_HOUSTON"]["peak"] == "ERH"
        assert HUB_CONTRACT_MAP["HB_NORTH"]["7x8"] == "ECI"

    # -- Model dataclasses ------------------------------------------------

    def test_contract_hub_node_alias(self):
        c = Contract.from_dict({"symbol": "ERH", "node": "HB_HOUSTON"})
        assert c.hub == "HB_HOUSTON"
        assert c.node == "HB_HOUSTON"

    def test_contract_backward_compat(self):
        c = Contract(symbol="ERH", hub="HB_HOUSTON", shape="peak")
        assert c.hub == "HB_HOUSTON"
        assert c.node == "HB_HOUSTON"

    def test_contract_price_from_dict(self):
        cp = ContractPrice.from_dict(
            {
                "exchange": "IFED",
                "symbol": "ERH",
                "refdate": "2026-03-25",
                "fordate": "2026-06-01",
                "price": 42.5,
                "volume": 100,
            }
        )
        assert cp.price == 42.5
        assert cp.volume == 100
        assert cp.open is None

    def test_available_date_from_dict(self):
        ad = AvailableDate.from_dict(
            {
                "refdate": "2026-03-25",
                "min_fordate": "2026-04-01",
                "max_fordate": "2028-12-01",
            }
        )
        assert ad.refdate == "2026-03-25"
        assert ad.min_fordate == "2026-04-01"

    def test_exchange_from_dict(self):
        ex = Exchange.from_dict(
            {"mic": "IFED", "name": "ICE Futures", "url": "https://ice.com"}
        )
        assert ex.mic == "IFED"
        assert ex.name == "ICE Futures"
