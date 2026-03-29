"""Tests for bos.calc -- Calc API client."""

from unittest.mock import patch

import pytest

from bos.calc.client import CalcClient
from bos.calc.config import ENDPOINTS, TITAN
from bos.calc.models import (
    Calc,
    CalcNode,
    CalcScenario,
    DataObject,
    NodeScenario,
)


class TestCalcClient:
    @pytest.fixture
    def client(self, mock_session):
        return CalcClient({"BOS_API": "test-token"}, ENDPOINTS)

    # -- Data objects -----------------------------------------------------

    def test_list_data_objects(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "data1", "name": "Test Data"}]
        )
        result = client.list_data_objects()
        assert isinstance(result[0], DataObject)

    def test_create_data_object(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(
            json_data={"slug": "data2", "name": "New Data"}
        )
        result = client.create_data_object(name="New Data")
        assert isinstance(result, DataObject)
        assert result.slug == "data2"

    def test_get_data_object(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"slug": "data1", "name": "Test Data"}
        )
        result = client.get_data_object("data1")
        assert isinstance(result, DataObject)
        assert result.slug == "data1"

    def test_get_data_object_calcs(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "slug": "calc1",
                    "name": "Houston 100MW",
                    "iso": "ERCOT",
                    "node": "HB_HOUSTON",
                    "capacity": 100.0,
                    "duration": 2.0,
                }
            ]
        )
        result = client.get_data_object_calcs("data1")
        assert isinstance(result[0], Calc)
        assert result[0].slug == "calc1"

    # -- Calc CRUD --------------------------------------------------------

    def test_list_calcs(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "slug": "calc1",
                    "name": "Houston 100MW",
                    "iso": "ERCOT",
                    "node": "HB_HOUSTON",
                    "capacity": 100.0,
                    "duration": 2.0,
                    "status": {"slug": "done", "name": "Done"},
                }
            ]
        )
        result = client.list_calcs()
        assert len(result) == 1
        assert isinstance(result[0], Calc)
        assert result[0].slug == "calc1"
        assert result[0].status == "done"

    def test_create_calc(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(
            json_data={
                "slug": "newcalc",
                "name": "New Calc",
                "iso": "ERCOT",
                "node": "HB_HOUSTON",
                "capacity": 50.0,
                "duration": 1.0,
            }
        )
        result = client.create_calc(name="New Calc", iso="ERCOT", node="HB_HOUSTON")
        assert isinstance(result, Calc)
        assert result.slug == "newcalc"

    def test_get_calc(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "slug": "calc1",
                "name": "Houston 100MW",
                "iso": "ERCOT",
                "node": "HB_HOUSTON",
                "capacity": 100.0,
                "duration": 2.0,
            }
        )
        result = client.get_calc("calc1")
        assert isinstance(result, Calc)
        assert result.slug == "calc1"

    def test_get_calc_status(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"slug": "done", "name": "Done"}
        )
        result = client.get_calc_status("calc1")
        assert result["slug"] == "done"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/status/" in call_url

    def test_get_calc_summary(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"total_revenue": 1000.0}
        )
        result = client.get_calc_summary("calc1")
        assert result["total_revenue"] == 1000.0
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/summary/" in call_url

    # -- Calc nodes/scenarios ---------------------------------------------

    def test_list_calc_nodes(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "node1", "calc": "calc1", "node": "HB_HOUSTON"}]
        )
        result = client.list_calc_nodes("calc1")
        assert isinstance(result[0], CalcNode)
        assert result[0].node == "HB_HOUSTON"

    def test_get_calc_node(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"slug": "node1", "calc": "calc1", "node": "HB_HOUSTON"}
        )
        result = client.get_calc_node("calc1", "node1")
        assert isinstance(result, CalcNode)
        assert result.slug == "node1"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/nodes/node1/" in call_url

    def test_list_calc_scenarios(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "slug": "scen1",
                    "calc": "calc1",
                    "name": "Base Case",
                    "params": [{"name": "capacity", "value": 100}],
                }
            ]
        )
        result = client.list_calc_scenarios("calc1")
        assert isinstance(result[0], CalcScenario)
        assert result[0].params[0]["name"] == "capacity"

    def test_get_calc_scenario(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "slug": "scen1",
                "calc": "calc1",
                "name": "Base Case",
                "params": [{"name": "capacity", "value": 100}],
            }
        )
        result = client.get_calc_scenario("calc1", "scen1")
        assert isinstance(result, CalcScenario)
        assert result.slug == "scen1"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/scenarios/scen1/" in call_url

    # -- Node-scenario results --------------------------------------------

    def test_list_node_scenarios(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "slug": "ns1",
                    "node": "node1",
                    "scenario": "scen1",
                    "status": {"slug": "done", "name": "Done"},
                    "refdate": "2025-03-25",
                    "exchange": "ice",
                }
            ]
        )
        result = client.list_node_scenarios("calc1")
        assert isinstance(result[0], NodeScenario)
        assert result[0].refdate == "2025-03-25"

    def test_get_node_scenario(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "slug": "ns1",
                "node": "node1",
                "scenario": "scen1",
                "status": {"slug": "done", "name": "Done"},
                "refdate": "2025-03-25",
                "exchange": "ice",
            }
        )
        result = client.get_node_scenario("calc1", "ns1")
        assert isinstance(result, NodeScenario)
        assert result.slug == "ns1"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/nodescenarios/ns1/" in call_url

    def test_get_ns_result(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"revenue": 42.5, "year": 2025}
        )
        result = client.get_ns_result("calc1", "ns1")
        assert result["revenue"] == 42.5

    def test_get_ns_daily_result(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"daily": [{"date": "2025-01-01", "revenue": 5.0}]}
        )
        result = client.get_ns_daily_result("calc1", "ns1")
        assert result["daily"][0]["date"] == "2025-01-01"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/nodescenarios/ns1/daily_result/" in call_url

    def test_get_ns_params(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"capacity": 100, "duration": 2}
        )
        result = client.get_ns_params("calc1", "ns1")
        assert result["capacity"] == 100
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/nodescenarios/ns1/params/" in call_url

    def test_get_ns_status(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"slug": "done", "name": "Done"}
        )
        result = client.get_ns_status("calc1", "ns1")
        assert result["slug"] == "done"
        call_url = mock_session.get.call_args[0][0]
        assert "/calc1/nodescenarios/ns1/status/" in call_url

    # -- Dragonet ---------------------------------------------------------

    @patch("bos.base.requests.post")
    def test_run_dragonet(self, mock_post, client, mock_response):
        resp = mock_response(json_data={"status": "complete"})
        resp.headers = {"Content-Type": "application/json"}
        mock_post.return_value = resp
        from io import BytesIO

        fake_file = BytesIO(b"hour,price\n1,50.0")
        client.run_dragonet("ercot", "HB_HOUSTON", fake_file)
        call_url = mock_post.call_args[0][0]
        assert call_url.startswith(TITAN)
        assert "/dragonet/calc/" in call_url
