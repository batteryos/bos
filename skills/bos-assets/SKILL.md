---
name: bos-assets
version: 0.2.0
description: |
  BESS asset data from BatteryOS: revenue (actual, CO perfect, EO perfect), volume
  (actual, perfect, dispatch, download), BOS Index, availability, performance, percentiles,
  rankings, HSL, cycles. ISO-wide and per-asset/component/resource granularity.
  Use when asked about battery asset performance, revenue, volume, cycles, or availability.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS BESS Assets API

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-assets","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
~/.bos/bin/bos-auth-check 2>/dev/null || true
```

## Related skills
- `/bos` — Prices, calcs, queue, dashboard (59 endpoints)
- `/bos-calcs` — Read-only calc results, node-scenario data
- `/bos-dispatch` — Create calcs, dispatch to Dragon

BESS asset performance data. 30 endpoints.

## Python API

All API calls use the `bos` Python library.

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
from bos.assets.models import AssetFilter, NewAsset, NewResourceName
client = BOSClient()
```

## Examples

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
from bos.assets.models import AssetFilter
client = BOSClient()

# List all ERCOT BESS assets
assets = client.assets.list_assets()
for a in assets[:5]:
    print(f"{a.slug}: {a.name} ({a.capacity}MW/{a.duration}hr, owner={a.owner})")

# Filter by owner
vistra = client.assets.list_assets(AssetFilter(owner_name="Vistra"))

# Revenue: actual vs CO perfect vs EO perfect
revenue = client.assets.get_revenue()
perfect_co = client.assets.get_perfect_revenue()
perfect_eo = client.assets.get_eo_perfect_revenue()

# Revenue filtered by owner
rev_filtered = client.assets.get_revenue(AssetFilter(owner_name="Vistra"))

# Rankings
ranking = client.assets.get_ranking()

# Cycles
cycles = client.assets.get_cycles()

# Availability
avail = client.assets.get_availability()

# HSL
hsl = client.assets.get_hsl()
asset_hsl = client.assets.get_asset_hsl("ercot", "ASSET_SLUG")

# BOS Index
idx = client.assets.get_bos_index()
idx_perfect = client.assets.get_perfect_bos_index()

# Performance
perf = client.assets.get_performance()

# Percentiles
pct = client.assets.get_percentiles()

# Volume
vol = client.assets.get_volume()
vol_perfect = client.assets.get_perfect_volume()
vol_eo = client.assets.get_eo_perfect_volume()
vol_dl = client.assets.download_volume()
vol_dispatch = client.assets.get_dispatch_volume()

# Per-asset volume download
asset_vol = client.assets.download_asset_volume("ercot", "ASSET_SLUG")

# Per-resource volume download
res_vol = client.assets.download_resource_volume(
    "ercot", "ASSET_SLUG", "COMPONENT_SLUG", "RESOURCE_SLUG"
)

# Owners and QSEs
owners = client.assets.list_owners()
qses = client.assets.list_qses()

# Asset detail and timeline
detail = client.assets.get_asset("ercot", "ASSET_SLUG")
timeline = client.assets.get_asset_timeline("ercot", "ASSET_SLUG")
```

## Endpoint reference

| Method | Path | Python method |
|--------|------|---------------|
| POST | `/{iso}/` | `client.assets.list_assets()` |
| GET | `/{iso}/{slug}/` | `client.assets.get_asset(iso, slug)` |
| GET | `/{iso}/{slug}/timeline/` | `client.assets.get_asset_timeline(iso, slug)` |
| GET | `/{iso}/owners/` | `client.assets.list_owners()` |
| GET | `/{iso}/qse/` | `client.assets.list_qses()` |
| POST | `/{iso}/revenue/` | `client.assets.get_revenue()` |
| POST | `/{iso}/revenue/perfect/` | `client.assets.get_perfect_revenue()` |
| POST | `/{iso}/revenue/perfect/eo/` | `client.assets.get_eo_perfect_revenue()` |
| POST | `/{iso}/volume/` | `client.assets.get_volume()` |
| POST | `/{iso}/volume/perfect/` | `client.assets.get_perfect_volume()` |
| POST | `/{iso}/volume/perfect/eo/` | `client.assets.get_eo_perfect_volume()` |
| POST | `/{iso}/volume/dl/` | `client.assets.download_volume()` |
| POST | `/{iso}/volume/dispatch/` | `client.assets.get_dispatch_volume()` |
| POST | `/{iso}/{slug}/volume/dl/` | `client.assets.download_asset_volume(iso, slug)` |
| POST | `/{iso}/asset/{a}/component/{c}/resource/{r}/volume/dl/` | `client.assets.download_resource_volume(iso, a, c, r)` |
| POST | `/{iso}/bosindex/` | `client.assets.get_bos_index()` |
| POST | `/{iso}/bosindex/perfect/` | `client.assets.get_perfect_bos_index()` |
| POST | `/{iso}/availability/` | `client.assets.get_availability()` |
| POST | `/{iso}/performance/` | `client.assets.get_performance()` |
| POST | `/{iso}/percentiles/` | `client.assets.get_percentiles()` |
| POST | `/{iso}/ranking/` | `client.assets.get_ranking()` |
| POST | `/{iso}/hsl/` | `client.assets.get_hsl()` |
| POST | `/{iso}/{slug}/hsl/` | `client.assets.get_asset_hsl(iso, slug)` |
| POST | `/{iso}/cycles/` | `client.assets.get_cycles()` |
| POST | `/fixtures/` | `client.assets.dump_fixtures()` |
| POST | `/new/asset/` | `client.assets.add_asset(NewAsset(...))` |
| POST | `/new/res_name/` | `client.assets.add_resource_name(NewResourceName(...))` |
| GET | `/analysis/{slug}/toggle_favorite_status/` | `client.assets.toggle_analysis_favorite(slug)` |

All POST endpoints accept an `AssetFilter` dataclass for filtering:
```python
from bos.assets.models import AssetFilter
client.assets.get_revenue(AssetFilter(owner_name="Vistra", category="standalone"))
```

## Concepts

- **CO (Commitment Optimal)**: Perfect dispatch with ancillary service co-optimization
- **EO (Energy Only)**: Perfect dispatch on energy arbitrage only (no AS)
- **BOS Index**: Composite performance score normalized across fleet
- **HSL**: High Sustained Limit — max sustained output registered with ERCOT
- **QSE**: Qualified Scheduling Entity — the entity that schedules the asset in ERCOT
