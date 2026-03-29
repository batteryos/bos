"""Tests for bos.assets -- Assets API client."""

import pytest

from bos.assets.client import AssetsClient
from bos.assets.config import ENDPOINTS
from bos.assets.models import Asset, Owner, QSE


class TestAssetsClient:
    @pytest.fixture
    def client(self, mock_session):
        return AssetsClient({"BOS_API": "test-token"}, ENDPOINTS)

    def test_list_assets(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(
            json_data=[
                {
                    "slug": "asset1",
                    "name": "Test Battery",
                    "node": "HB_HOUSTON",
                    "owner": "Owner Co",
                    "qse": "QSE Corp",
                    "capacity": 100.0,
                    "duration": 2.0,
                    "category": "standalone",
                    "cod": "2023-06-01",
                }
            ]
        )
        result = client.list_assets()
        assert len(result) == 1
        assert isinstance(result[0], Asset)
        assert result[0].slug == "asset1"
        assert result[0].capacity == 100.0
        assert result[0].owner == "Owner Co"

    def test_list_owners(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "own1", "name": "Owner Co"}]
        )
        result = client.list_owners()
        assert isinstance(result[0], Owner)
        assert result[0].name == "Owner Co"

    def test_list_qses(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "qse1", "name": "QSE Corp", "code": "QSEC"}]
        )
        result = client.list_qses()
        assert isinstance(result[0], QSE)
        assert result[0].code == "QSEC"

    def test_get_revenue(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(json_data={"revenue": 500000})
        result = client.get_revenue()
        assert result["revenue"] == 500000

    def test_get_cycles(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(
            json_data=[{"asset": "test", "cycles": 365}]
        )
        result = client.get_cycles()
        assert result[0]["cycles"] == 365

    def test_get_asset_detail(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"slug": "asset1", "name": "Test"}
        )
        result = client.get_asset("ercot", "asset1")
        assert result["slug"] == "asset1"

    def test_get_availability(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(
            json_data=[{"asset": "test", "availability": 0.95}]
        )
        result = client.get_availability()
        assert result[0]["availability"] == 0.95

    def test_download_resource_volume(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(json_data=[{"volume": 123}])
        result = client.download_resource_volume("ercot", "asset1", "comp1", "res1")
        assert result[0]["volume"] == 123
