"""Tests for bos.analysis -- Analysis API client."""

from io import BytesIO
from unittest.mock import patch

import pytest

from bos.analysis.client import AnalysisClient
from bos.analysis.config import ENDPOINTS


class TestAnalysisClient:
    @pytest.fixture
    def client(self, mock_session):
        return AnalysisClient({"BOS_API": "test-token"}, ENDPOINTS)

    # -- Actuals ----------------------------------------------------------

    def test_get_actuals_tbn(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"tbn": 10.5})
        client.get_actuals_tbn("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/history/ercot/HB_HOUSTON/tbn/" in call_url

    def test_get_actuals_tbn_with_params(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_actuals_tbn(
            "ercot",
            "HB_HOUSTON",
            start_date="2025-01-01",
            end_date="2025-12-31",
            data_format="csv",
        )
        call_args = mock_session.get.call_args
        assert "start_date" in str(call_args)

    def test_get_actuals_rpo(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"rpo": 5.2})
        client.get_actuals_rpo("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/history/ercot/HB_HOUSTON/rpo/" in call_url

    def test_get_actuals_basis(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_actuals_basis("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/history/ercot/HB_HOUSTON/basis/" in call_url

    def test_get_actuals_eon(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"eon": 8.3})
        client.get_actuals_eon("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/history/ercot/HB_HOUSTON/eon/" in call_url

    def test_get_actuals_aggregate(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_actuals_aggregate("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/history/ercot/HB_HOUSTON/aggregate/" in call_url

    # -- Forwards ---------------------------------------------------------

    def test_get_forwards_tbn(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_forwards_tbn("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/futures/ercot/HB_HOUSTON/tbn/" in call_url

    def test_get_forwards_rpo(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_forwards_rpo("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/futures/ercot/HB_HOUSTON/rpo/" in call_url

    def test_get_forwards_eon(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_forwards_eon("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/futures/ercot/HB_HOUSTON/eon/" in call_url

    def test_get_forwards_aggregate(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={})
        client.get_forwards_aggregate("ercot", "HB_HOUSTON")
        call_url = mock_session.get.call_args[0][0]
        assert "/analysis/futures/ercot/HB_HOUSTON/aggregate/" in call_url

    # -- CycN -------------------------------------------------------------

    @patch("bos.base.requests.post")
    def test_get_cycle_revenue(self, mock_post, client, mock_response):
        resp = mock_response(json_data={"revenue": 100})
        resp.headers = {"Content-Type": "application/json"}
        mock_post.return_value = resp
        fake_file = BytesIO(b"date,revenue,cycles\n2025-01-01,50,1")
        client.get_cycle_revenue(365, fake_file)
        call_url = mock_post.call_args[0][0]
        assert "/analysis/cycn/365/" in call_url

    # -- CRR basis --------------------------------------------------------

    def test_get_crr_basis(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"basis": 2.5})
        result = client.get_crr_basis("ercot", "HB_HOUSTON", "HB_NORTH")
        assert result["basis"] == 2.5
        call_url = mock_session.get.call_args[0][0]
        assert "/chukar/ercot/HB_HOUSTON/basis/HB_NORTH/" in call_url
