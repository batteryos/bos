"""Queue API client -- ERCOT interconnection queue."""

from bos.base import BaseClient
from bos.gridqueue.models import Bus, POI, POIBus, Project


class QueueClient(BaseClient):
    """Client for /api/v1/queue endpoints.

    Write operations take typed request dataclasses::

        from bos.gridqueue.models import BusCreate
        client.queue.add_bus(BusCreate(bus_name="NEW_345KV", bus_number=99999))
    """

    # --- Projects ---

    def list_projects(self, iso="ercot", **filters):
        """GET /{iso}/projects/ -- List all queue projects."""
        data = self.get(f"/{iso}/projects/", params=filters or None)
        if isinstance(data, list):
            return [Project.from_dict(d) for d in data]
        return data

    def get_project_milestones(self, iso="ercot", **filters):
        """GET /{iso}/projects/milestones/ -- Project milestones."""
        return self.get(f"/{iso}/projects/milestones/", params=filters or None)

    def get_project(self, iso, inr):
        """GET /{iso}/project/{inr}/ -- Single project detail by INR."""
        return self.get(f"/{iso}/project/{inr}/")

    # --- Infrastructure ---

    def list_pois(self):
        """GET /pois/ -- List all points of interconnection."""
        data = self.get("/pois/")
        if isinstance(data, list):
            return [POI.from_dict(d) for d in data]
        return data

    def list_buses(self):
        """GET /buses/ -- List all transmission buses."""
        data = self.get("/buses/")
        if isinstance(data, list):
            return [Bus.from_dict(d) for d in data]
        return data

    def get_bus(self, iso, slug):
        """GET /{iso}/bus/{slug}/ -- Bus detail with associated projects."""
        return self.get(f"/{iso}/bus/{slug}/")

    def list_poi_buses(self):
        """GET /poi_buses/ -- POI-to-bus mappings."""
        data = self.get("/poi_buses/")
        if isinstance(data, list):
            return [POIBus.from_dict(d) for d in data]
        return data

    # --- Write operations ---

    def add_bus(self, req=None, **kwargs):
        """POST /add/bus/ -- Add a new bus."""
        return self.post("/add/bus/", self.serialize(req, kwargs))

    def update_bus(self, req=None, **kwargs):
        """POST /update/bus/ -- Update an existing bus."""
        return self.post("/update/bus/", self.serialize(req, kwargs))

    def add_poi_bus(self, req=None, **kwargs):
        """POST /add/poibus/ -- Add a POI-bus mapping."""
        return self.post("/add/poibus/", self.serialize(req, kwargs))
