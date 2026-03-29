"""Exhaustive examples for every QueueClient endpoint and parameter config.

10 endpoints. Covers:
  GET no args (list), GET iso default, GET iso+filters, GET iso+id
  POST with BusCreate/BusUpdate/POIBusCreate dataclass, POST kwargs escape hatch

Usage:
    export BOS_API=your-token
    python -m bos.gridqueue.examples
"""

from bos import BOSClient
from bos.gridqueue.models import BusCreate, BusUpdate, POIBusCreate

client = BOSClient()
q = client.queue


# ============================================================
# GET — no args (static paths)
# ============================================================

pois = q.list_pois()
buses = q.list_buses()
poi_buses = q.list_poi_buses()


# ============================================================
# GET — iso only (default "ercot")
# ============================================================

projects_bare = q.list_projects()
projects_explicit = q.list_projects(iso="ercot")
milestones_bare = q.get_project_milestones()


# ============================================================
# GET — iso + kwargs filters
# ============================================================

projects_fuel = q.list_projects(fuel="Solar")
projects_multi = q.list_projects(fuel="BESS", technology="Battery")
projects_inr = q.list_projects(inr="24INR0001")
projects_ref = q.list_projects(refdate="2026-03-25")
milestones_filtered = q.get_project_milestones(fuel="Solar")
milestones_combo = q.get_project_milestones(
    iso="ercot", fuel="BESS", refdate="2026-03-25"
)


# ============================================================
# GET — iso + identifier
# ============================================================

project = q.get_project("ercot", "24INR0001")
bus = q.get_bus("ercot", "BUS_SLUG")


# ============================================================
# POST — with typed dataclass
# ============================================================

q.add_bus(BusCreate(bus_name="NEW_345KV", bus_number=99999))
q.update_bus(BusUpdate(bus_slug="BUS_SLUG", bus_name="UPDATED", bus_number=99998))
q.add_poi_bus(POIBusCreate(poi_location_slug="POI_SLUG", bus_slug="BUS_SLUG"))


# ============================================================
# POST — kwargs escape hatch
# ============================================================

q.add_bus(bus_name="RAW_BUS", bus_number=11111)
