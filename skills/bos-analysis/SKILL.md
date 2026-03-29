---
name: bos-analysis
version: 0.2.0
description: |
  Analysis calculations from BatteryOS: TBn, RPO, basis, EOn for actuals
  and forwards. CycN cycle revenue optimizer. CRR basis. 11 endpoints.
  Use when asked about TBn, RPO, basis, EOn, CRR, or cycle revenue.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS Analysis (`/bos-analysis`)

Node-level analytics — TBn, RPO, basis, EOn, CycN, CRR basis.

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-analysis","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
```

## Related skills
- `/bos` — Primer and skill router
- `/bos-prices` — Raw price data, contracts, forwards
- `/bos-dispatch` — Dragon dispatch (COn)

## Python API

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Examples

```python
# Actuals
tbn = client.analysis.get_actuals_tbn("ercot", "HB_HOUSTON", start_date="2025-01-01", end_date="2025-12-31")
rpo = client.analysis.get_actuals_rpo("ercot", "HB_HOUSTON")
basis = client.analysis.get_actuals_basis("ercot", "HB_HOUSTON")
eon = client.analysis.get_actuals_eon("ercot", "HB_HOUSTON")
agg = client.analysis.get_actuals_aggregate("ercot", "HB_HOUSTON")

# Forwards
fwd_tbn = client.analysis.get_forwards_tbn("ercot", "HB_HOUSTON")
fwd_rpo = client.analysis.get_forwards_rpo("ercot", "HB_HOUSTON")
fwd_eon = client.analysis.get_forwards_eon("ercot", "HB_HOUSTON")
fwd_agg = client.analysis.get_forwards_aggregate("ercot", "HB_HOUSTON")

# CycN (POST with file)
cycn = client.analysis.get_cycle_revenue(365, open("cycle_data.csv", "rb"))

# CRR basis
crr = client.analysis.get_crr_basis("ercot", "HB_HOUSTON", "HB_NORTH")
```

## Endpoint reference

| Method | Path | Python method |
|--------|------|---------------|
| GET | `/analysis/history/{iso}/{node}/tbn/` | `client.analysis.get_actuals_tbn(iso, node, **params)` |
| GET | `/analysis/history/{iso}/{node}/rpo/` | `client.analysis.get_actuals_rpo(iso, node, **params)` |
| GET | `/analysis/history/{iso}/{node}/basis/` | `client.analysis.get_actuals_basis(iso, node, **params)` |
| GET | `/analysis/history/{iso}/{node}/eon/` | `client.analysis.get_actuals_eon(iso, node, **params)` |
| GET | `/analysis/history/{iso}/{node}/aggregate/` | `client.analysis.get_actuals_aggregate(iso, node, **params)` |
| GET | `/analysis/futures/{iso}/{node}/tbn/` | `client.analysis.get_forwards_tbn(iso, node, **params)` |
| GET | `/analysis/futures/{iso}/{node}/rpo/` | `client.analysis.get_forwards_rpo(iso, node, **params)` |
| GET | `/analysis/futures/{iso}/{node}/eon/` | `client.analysis.get_forwards_eon(iso, node, **params)` |
| GET | `/analysis/futures/{iso}/{node}/aggregate/` | `client.analysis.get_forwards_aggregate(iso, node, **params)` |
| POST | `/analysis/cycn/{annual_cycles}/` | `client.analysis.get_cycle_revenue(annual_cycles, file)` |
| GET | `/chukar/{iso}/{node}/basis/{hub}/` | `client.analysis.get_crr_basis(iso, node, hub, **params)` |

## Concepts

- **TBn**: Time Block n spread — avg of n most expensive hours minus avg of n cheapest hours
- **RPO**: Revenue Put Option — combines AS + TB revenue components
- **Basis**: Price differential between a node and its hub
- **EOn**: Energy Only perfect dispatch (LP-based, SOC-feasible)
- **CycN**: Annual cycle revenue optimizer — maximizes revenue within a cycle budget
- **CRR**: Congestion Revenue Rights basis between node and hub
