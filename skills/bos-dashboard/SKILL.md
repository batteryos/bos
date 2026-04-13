---
name: bos-dashboard
version: 0.1.0
description: |
  Pre-computed market dashboards from BatteryOS: owner performance rankings,
  fleet dispatch, revenue index, TBn spreads (ERCOT and US), queue capacity.
  7 GET endpoints, no required params.
  Use when asked about market reports, rankings, TBn spreads, or fleet performance.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS Dashboard (`/bos-dashboard`)

Pre-computed market intelligence dashboards. All GET, no required params.

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-dashboard","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
~/.bos/bin/bos-auth-check 2>/dev/null || true
```

## Related skills
- `/bos` — Primer and skill router
- `/bos-assets` — Detailed per-asset data behind the rankings
- `/bos-queue` — Queue project data behind queue capacity

## Python API

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Examples

```python
ranking = client.dashboard.get_ranking()
ranking = client.dashboard.get_ranking(owner="vistra")
dispatch = client.dashboard.get_dispatch()
revenue = client.dashboard.get_revenue()
tbn_ercot = client.dashboard.get_tbn_ercot(year="2025", n="2")
tbn_us = client.dashboard.get_tbn_us(year="2025", n="2")
queue_cap = client.dashboard.get_queue_capacity()
data_key = client.dashboard.get_data_key()
```

## Endpoint reference

| Method | Path | Python method |
|--------|------|---------------|
| GET | `/ranking/` | `client.dashboard.get_ranking()` |
| GET | `/dispatch/` | `client.dashboard.get_dispatch()` |
| GET | `/revenue/` | `client.dashboard.get_revenue()` |
| GET | `/tbn_ercot/` | `client.dashboard.get_tbn_ercot()` |
| GET | `/tbn_us/` | `client.dashboard.get_tbn_us()` |
| GET | `/data/` | `client.dashboard.get_data_key()` |
| GET | `/queue_capacity/` | `client.dashboard.get_queue_capacity()` |
