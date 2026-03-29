---
name: bos-queue
version: 0.1.0
description: |
  ERCOT interconnection queue from BatteryOS: projects, milestones, GIS stages,
  POIs, transmission buses, POI-bus mappings. 10 endpoints.
  Use when asked about interconnection projects, queue capacity, or grid infrastructure.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS Queue (`/bos-queue`)

ERCOT interconnection queue data.

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-queue","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Related skills
- `/bos` — Primer and skill router
- `/bos-dashboard` — Queue capacity dashboard

## Python API

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Examples

```python
projects = client.queue.list_projects()
projects = client.queue.list_projects(fuel="BESS", refdate="2026-03-25")
milestones = client.queue.get_project_milestones()
detail = client.queue.get_project("ercot", "24INR0123")
pois = client.queue.list_pois()
buses = client.queue.list_buses()
poi_buses = client.queue.list_poi_buses()

from bos.gridqueue.models import BusCreate
client.queue.add_bus(BusCreate(bus_name="NEW_345KV", bus_number=99999))
```

## Endpoint reference

| Method | Path | Python method |
|--------|------|---------------|
| GET | `/{iso}/projects/` | `client.queue.list_projects()` |
| GET | `/{iso}/projects/milestones/` | `client.queue.get_project_milestones()` |
| GET | `/{iso}/project/{inr}/` | `client.queue.get_project(iso, inr)` |
| GET | `/pois/` | `client.queue.list_pois()` |
| GET | `/buses/` | `client.queue.list_buses()` |
| GET | `/{iso}/bus/{slug}/` | `client.queue.get_bus(iso, slug)` |
| GET | `/poi_buses/` | `client.queue.list_poi_buses()` |
| POST | `/add/bus/` | `client.queue.add_bus(BusCreate(...))` |
| POST | `/update/bus/` | `client.queue.update_bus(BusUpdate(...))` |
| POST | `/add/poibus/` | `client.queue.add_poi_bus(POIBusCreate(...))` |
