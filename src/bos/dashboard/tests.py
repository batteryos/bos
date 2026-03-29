"""Tests for bos.dashboard -- Dashboard API client."""

import pytest

from bos.dashboard.client import DashboardClient
from bos.dashboard.config import ENDPOINTS
from bos.dashboard.models import DispatchEntry, RankingEntry, RevenueEntry
from bos.exceptions import APIError


class TestDashboardClient:
    @pytest.fixture
    def client(self, mock_session):
        return DashboardClient({"BOS_API": "test-token"}, ENDPOINTS)

    def test_get_ranking(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "results": [
                    {
                        "date": "2025-01",
                        "label": "Owner A",
                        "value": 42.5,
                        "min": 10.0,
                        "max": 80.0,
                        "rank": 1,
                        "selected": True,
                    }
                ]
            }
        )
        result = client.get_ranking()
        assert len(result) == 1
        assert isinstance(result[0], RankingEntry)
        assert result[0].value == 42.5
        assert result[0].rank == 1

    def test_get_dispatch(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "results": [
                    {
                        "timestamp": "2025-01-01T00:00:00Z",
                        "charging": 100.0,
                        "discharging": 200.0,
                    }
                ]
            }
        )
        result = client.get_dispatch()
        assert len(result) == 1
        assert isinstance(result[0], DispatchEntry)
        assert result[0].charging == 100.0

    def test_get_revenue(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={
                "results": [{"date": "2025-01", "actual": 500.0, "perfect": 800.0}]
            }
        )
        result = client.get_revenue()
        assert len(result) == 1
        assert isinstance(result[0], RevenueEntry)
        assert result[0].actual == 500.0

    def test_get_tbn_ercot(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"2025_2": {"nodes": []}}
        )
        result = client.get_tbn_ercot()
        assert "2025_2" in result

    def test_get_data_key(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(json_data={"key": "value"})
        result = client.get_data_key()
        assert result == {"key": "value"}

    def test_get_queue_capacity(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"results": [{"fuel": "BESS", "mw": 1000}]}
        )
        result = client.get_queue_capacity()
        assert result[0]["fuel"] == "BESS"

    def test_error_handling(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            status_code=500, ok=False, json_data={"error": "Server error"}
        )
        with pytest.raises(APIError) as exc_info:
            client.get_ranking()
        assert exc_info.value.status_code == 500
