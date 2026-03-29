---
name: bos-prices
version: 0.3.0
description: |
  Electricity prices from BatteryOS: ICE forward contracts, historical
  actuals, forward curves, cross-exchange comparison. 8 endpoints.
  Use when asked about electricity prices, forwards, contracts, or settlements.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS Prices (`/bos-prices`)

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-prices","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Related skills
- `/bos` — Primer and skill router
- `/bos-analysis` — TBn, RPO, EOn calculations derived from these prices
- `/bos-dispatch` — Dragon dispatch using forward curves

## Python API

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Hub-to-contract symbol mapping (ERCOT)

```
         peak   2x16   7x8    he1017  he1822
NORTH    ERN    ER2    ECI    ED7     ERC
HOUSTON  ERH    EDB    ECJ    ERM     ERB
SOUTH    ERS    EDA    ECK    ERQ     ERD
WEST     ERW    EDC    ECL    ERT     ERE
```

## Examples

```python
# Exchanges
exchanges = client.prices.list_exchanges()

# Contracts (default IFED, supports any exchange)
contracts = client.prices.list_contracts()
contracts = client.prices.list_contracts("IFED", iso="ercot", node="HB_NORTH")

# Contract prices / available dates
dates = client.prices.get_contract("ERH")                          # available dates
prices = client.prices.get_contract("ERH", refdate="2026-03-25")   # prices
prices = client.prices.get_contract("ERH", strip="NQ25", freq="som", step=True)

# Available refdates
refdates = client.prices.get_available_refdates("ERH")

# Cross-exchange comparison
comparison = client.prices.compare_prices("ERH", "IFED", "BOS", "2026-03-25")

# Historical actuals
actuals = client.prices.get_actuals("ercot", "HB_HOUSTON", curves=["dam", "rtm"], years=[2024])

# Forward curves
forwards = client.prices.get_forwards("ercot", "HB_HOUSTON", "2026-03-25")

# Aggregated forwards
agg = client.prices.get_agg_forwards("IFED", "ercot", "HB_HOUSTON", "dam", "mean")
```

## Endpoint reference

| Method | Path | Python method |
|--------|------|---------------|
| GET | `/kronos/contracts/` | `client.prices.list_exchanges()` |
| GET | `/kronos/contracts/{exchange}/` | `client.prices.list_contracts(exchange_code, **filters)` |
| GET | `/kronos/contracts/{exchange}/{symbol}/` | `client.prices.get_contract(symbol, exchange_code, ...)` |
| GET | `/kronos/contracts/{exchange}/{symbol}/available_dates/` | `client.prices.get_available_refdates(symbol, exchange_code)` |
| GET | `/kronos/compare/{exc1}/{symbol}/{exc2}/{refdate}/` | `client.prices.compare_prices(symbol, exc1, exc2, refdate)` |
| POST | `/prices/history/{iso}/{node}/` | `client.prices.get_actuals(iso, node, **params)` |
| POST | `/prices/futures/{iso}/{node}/{refdate}/` | `client.prices.get_forwards(iso, node, refdate, **params)` |
| GET | `/prices/futures/{exc}/{iso}/{node}/{curve}/{agg}/` | `client.prices.get_agg_forwards(exc, iso, node, curve, agg)` |

## Concepts

- **Exchange code**: MIC code identifying the exchange (e.g. IFED for ICE Futures, BOS for BatteryOS curves)
- **refdate / fordate**: Reference date (when observed) vs forward date (delivery month)
- **strip**: Forward curve strip pattern (e.g. `NQ25` = July-Aug 2025, `CAL26`). ICE month codes: F G H J K M N Q U V X Z
- **freq**: Date frequency filter (sow, eow, som, eom, soq, eoq, soy, eoy)
- **step**: Step-function interpolation for forward curves
