# bos — Python wrapper for the BatteryOS API

Typed Python client covering 84 BatteryOS API endpoints across 6 domains.
Dataclasses aligned with the BatteryOS API response shapes.

## Install

```bash
pip install -e src/bos
```

Requires Python 3.10+ and `requests`.

## Usage

```python
from bos import BOSClient

client = BOSClient()  # reads BOS_API env var or ~/.bos/credentials

# Assets
assets = client.assets.list_assets()
owners = client.assets.list_owners()
revenue = client.assets.get_revenue()
cycles = client.assets.get_cycles()

# Calc / Dragon dispatch
calcs = client.calc.list_calcs()
calc = client.calc.create_calc(name="Test", iso="ERCOT", node="HB_HOUSTON")
result = client.calc.get_ns_result("calc-slug", "ns-slug")

# Prices
contracts = client.prices.list_contracts()
actuals = client.prices.get_actuals("ercot", "HB_HOUSTON")

# Analysis
tbn = client.analysis.get_actuals_tbn("ercot", "HB_HOUSTON")

# Queue
projects = client.queue.list_projects()
buses = client.queue.list_buses()

# Dashboard
ranking = client.dashboard.get_ranking()
tbn_ercot = client.dashboard.get_tbn_ercot()
```

## Auth

Token resolved in order:

1. Explicit: `BOSClient(token="...")`
2. Environment: `BOS_API` env var
3. File: `~/.bos/credentials`

## Domains

| Domain | Client | Host | Endpoints |
|--------|--------|------|-----------|
| Calc | `client.calc` | batteryos.com | 18 |
| Assets | `client.assets` | batteryos.com | 28 |
| Prices | `client.prices` | titan.batteryos.com | 8 |
| Analysis | `client.analysis` | titan.batteryos.com | 11 |
| Queue | `client.queue` | batteryos.com | 10 |
| Dashboard | `client.dashboard` | batteryos.com | 7 |

## Models

Typed dataclasses for API responses:

| Module | Classes |
|--------|---------|
| `bos.assets.models` | `Asset`, `Owner`, `QSE` |
| `bos.calc.models` | `Calc`, `CalcNode`, `CalcScenario`, `NodeScenario`, `DataObject`, `CalcStatus` |
| `bos.prices.models` | `Contract`, `ContractPrice`, `AvailableDate`, `Exchange`, `ERCOT_HUBS`, `HUB_CONTRACT_MAP` |
| `bos.gridqueue.models` | `Project`, `POI`, `Bus`, `POIBus` |
| `bos.dashboard.models` | `RankingEntry`, `DispatchEntry`, `RevenueEntry` |

All dataclasses have a `from_dict(data)` classmethod for JSON parsing.

## Structure

```
src/bos/
  __init__.py           # BOSClient re-export
  auth.py               # Token resolution
  base.py               # BaseClient (shared session, error handling)
  client.py             # BOSClient entry point
  exceptions.py         # BOSError, AuthError, APIError, NotFoundError
  calc/                 # CalcClient (18 endpoints)
    client.py  config.py  models.py  tests.py  examples.py
  assets/               # AssetsClient (28 endpoints)
    client.py  config.py  models.py  tests.py  examples.py
  prices/               # PricesClient (8 endpoints)
    client.py  config.py  models.py  tests.py
  analysis/             # AnalysisClient (11 endpoints)
    client.py  config.py  tests.py
  dashboard/            # DashboardClient (7 endpoints)
    client.py  config.py  models.py  tests.py  examples.py
  gridqueue/            # QueueClient (10 endpoints)
    client.py  config.py  models.py  tests.py  examples.py
  tests/                # 94 tests, all mocked (no live API)
```

## Tests

```bash
cd ~/.claude/skills/bos
source .venv/bin/activate
PYTHONPATH=src/bos:src python3 -m pytest src/bos/tests/ -v
```

## Quality

- black: formatted
- pylint: 10.00/10
- No circular imports
- No duplicate classes or methods
- `__future__.annotations` only where needed (self-referencing return types)
