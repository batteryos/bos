---
name: bos
version: 0.5.0
description: |
  BatteryOS unified interface. 84 API endpoints across 6 domains.
  /bos with no args shows the primer. Use domain-specific skills for details:
  /bos-dispatch, /bos-prices, /bos-analysis, /bos-assets, /bos-dashboard, /bos-queue.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BatteryOS (`/bos`)

## Preamble (run first)

```bash
mkdir -p ~/.bos/state ~/.bos/analytics
echo '{"skill":"bos","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
~/.bos/bin/bos-auth-check 2>/dev/null || true
```

## Python API

All API calls use the `bos` Python library at `~/.claude/skills/bos/src/bos/`.

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Skills

| Skill | Client | Endpoints | Description |
|-------|--------|-----------|-------------|
| `/bos-dispatch` | `client.calc` | 20 | Calc/data CRUD, NS results, dragonet |
| `/bos-prices` | `client.prices` | 8 | Contracts, actuals, forwards, agg forwards |
| `/bos-analysis` | `client.analysis` | 11 | TBn, RPO, basis, EOn, aggregate, CycN, CRR |
| `/bos-assets` | `client.assets` | 28 | Revenue, volume, BOS index, availability, rankings, HSL |
| `/bos-dashboard` | `client.dashboard` | 7 | Rankings, dispatch, revenue index, TBn spreads |
| `/bos-queue` | `client.queue` | 10 | Projects, milestones, POIs, buses |

Route to the domain-specific skill when the user's question is about one domain.
Mention related skills when the question spans domains.

## Defaults

- **Refdate**: latest available from the API
- **Display**: annual results. Years in rows, scenarios/hubs/configs in columns
- **Hub**: HB_HOUSTON unless specified

## Concepts

- **Calc**: Calculation object with nodes x scenarios = node-scenarios
- **Node**: Pricing node (e.g., HB_HOUSTON)
- **Scenario**: Battery parameters (MW, hours, RTE, cycles)
- **Node-Scenario (NS)**: Cross product — one dispatch result per node x scenario
- **Dragon**: External dispatch optimization engine
- **Dragonet**: Lightweight optimization — upload your own CSV, get results
- **Refdate**: Reference date for forward curve pricing
- **TBn**: Time Block n spread = avg of n most expensive hours - avg of n cheapest hours
- **RPO**: Revenue Put Option — combines AS + TB revenue components
- **EOn**: Energy Only perfect dispatch (LP-based, SOC-feasible)
- **Basis**: Price differential between a node and its hub
- **CRR**: Congestion Revenue Rights basis
- **CycN**: Cycle revenue optimizer — optimal revenue given a cycle budget
- **INR**: Interconnection Request Number (e.g., 24INR0123)
- **POI**: Point of Interconnection
- **CO**: Commitment Optimal perfect dispatch (with ancillary services)
- **EO**: Energy Only perfect dispatch (energy arbitrage only)
