"""Tests for bos.gridqueue -- Queue API client."""

import pytest

from bos.exceptions import NotFoundError
from bos.gridqueue.client import QueueClient
from bos.gridqueue.config import ENDPOINTS
from bos.gridqueue.models import Bus, POI, POIBus, Project


class TestQueueClient:
    @pytest.fixture
    def client(self, mock_session):
        return QueueClient({"BOS_API": "test-token"}, ENDPOINTS)

    def test_list_projects(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "inr": "24INR0001",
                    "entered_queue": "2024-01-15",
                    "name": "Solar Farm",
                    "fuel": "Solar",
                    "status": "Planned",
                }
            ]
        )
        result = client.list_projects()
        assert len(result) == 1
        assert isinstance(result[0], Project)
        assert result[0].inr == "24INR0001"

    def test_get_project(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data={"inr": "24INR0001", "name": "Test"}
        )
        result = client.get_project("ercot", "24INR0001")
        assert result["inr"] == "24INR0001"

    def test_list_pois(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "poi1", "name": "substation_a"}]
        )
        result = client.list_pois()
        assert isinstance(result[0], POI)

    def test_list_buses(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"slug": "bus1", "name": "BUS_345KV", "number": 12345}]
        )
        result = client.list_buses()
        assert isinstance(result[0], Bus)
        assert result[0].number == 12345

    def test_list_poi_buses(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[
                {
                    "poi_location_slug": "poi1",
                    "poi_location_name": "sub_a",
                    "bus_slug": "bus1",
                    "bus_name": "BUS_1",
                    "bus_number": 100,
                }
            ]
        )
        result = client.list_poi_buses()
        assert isinstance(result[0], POIBus)
        assert result[0].bus_number == 100

    def test_get_project_milestones(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(
            json_data=[{"inr": "24INR0001", "gim_study_phase": "Phase 2"}]
        )
        result = client.get_project_milestones()
        assert result[0]["gim_study_phase"] == "Phase 2"

    def test_add_bus(self, client, mock_session, mock_response):
        mock_session.post.return_value = mock_response(json_data={})
        result = client.add_bus(bus_name="NEW_BUS", bus_number=99999)
        assert result == {}

    def test_not_found(self, client, mock_session, mock_response):
        mock_session.get.return_value = mock_response(status_code=404, ok=False)
        with pytest.raises(NotFoundError):
            client.get_project("ercot", "INVALID")
