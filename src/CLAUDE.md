# src/ — Python Library CLAUDE.md

## What This Is

`src/bos/` is a Python API wrapper for BatteryOS. It provides typed access to all
84 API endpoints via `BOSClient`. Dataclass field names are aligned with the actual
API JSON response shapes.

## Architecture

```
BOSClient
  ├── calc: CalcClient           → batteryos.com/api/v1 (+ dragonet on batteryos.com)
  ├── assets: AssetsClient       → batteryos.com/api/v1/asset
  ├── prices: PricesClient       → batteryos.com/api/v1
  ├── analysis: AnalysisClient   → batteryos.com/api/v1
  ├── queue: QueueClient         → batteryos.com/api/v1/queue
  └── dashboard: DashboardClient → batteryos.com/api/v1/bridge
```

All domain clients inherit from `BaseClient` which owns the `requests.Session`,
auth header, and error handling. No circular imports. No lazy imports.

## Conventions

- **Dataclasses for known shapes**, raw dicts for variable shapes (revenue aggregations,
  proxy endpoints). Every dataclass has `from_dict(cls, data: dict)`.
- **Field names match API JSON output**. For example, `Asset.owner` is a `str`
  (the owner name as returned by the API), not an FK integer.
- **POST for reads** on asset/BESS endpoints (mirrors API behavior). The client
  handles this transparently — callers don't need to know.
- **ISO defaults to `"ercot"`** on all asset and queue methods.
- Methods that return binary (XLS downloads) use `get_bytes()` and return `bytes`.

## Dependencies

- `requests>=2.28` (only external dependency)
- Python 3.10+

## Running Tests

```bash
source .venv/bin/activate
PYTHONPATH=src/bos:src python3 -m pytest src/bos/tests/ -v
```

94 tests, all mocked. No live API calls.

## Lint

```bash
source .venv/bin/activate
black --check src/bos/
PYTHONPATH=src/bos:src pylint src/bos/
```

Target: black clean, pylint 10.00/10.

## Key Files

| File | What It Does |
|------|-------------|
| `auth.py` | Token resolution: explicit > `BOS_API` env > `~/.bos/credentials` |
| `client.py` | `BOSClient` — wires all 6 domain clients |
| `base.py` | `BaseClient` — shared session, host routing, `_handle_response()`, error mapping |
| `calc/client.py` | Largest client (20 methods) — Dragon dispatch, NS results |
| `assets/client.py` | 28 methods — revenue, volume, analytics, admin |
| `calc/models.py` | `Calc`, `NodeScenario` — most complex `from_dict` (nested status objects) |
| `gridqueue/models.py` | `Project` — 24 fields matching API response |
| `*/config.py` | Per-domain endpoint declarations (host, auth key per endpoint) |

## Adding an Endpoint

1. Add the endpoint to the domain's `config.py` ENDPOINTS list
2. Add the method to the domain's `client.py`
3. If the response has a known shape, add or reuse a dataclass in `models.py`
4. Add a test in the domain's `tests.py`
5. Run `black`, `pylint`, `pytest`
