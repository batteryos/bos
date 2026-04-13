---
name: bos-dispatch
version: 0.4.0
description: |
  Dragon dispatch workflow via BatteryOS: calc CRUD, data objects,
  node-scenario results, and Dragonet. 20 endpoints on client.calc.
  Use when asked to run dispatch, create a calc, get results, or dragonet.
allowed-tools:
  - Bash
  - Read
  - Agent
---

# BOS Dispatch (`/bos-dispatch`)

Calc CRUD, data objects, node-scenario results, and Dragonet.

## Preamble (run first)

```bash
mkdir -p ~/.bos/analytics
echo '{"skill":"bos-dispatch","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> ~/.bos/analytics/skill-usage.jsonl 2>/dev/null || true
~/.bos/bin/bos-auth-check 2>/dev/null || true
```

## Related skills
- `/bos` — Primer and skill router
- `/bos-assets` — BESS asset performance (actual revenue to compare against dispatch)
- `/bos-analysis` — TBn, RPO, EOn calculations
- `/bos-prices` — Price data and forward contracts

## Python API

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Examples

```python
# Data objects
data_objects = client.calc.list_data_objects()
obj = client.calc.create_data_object(iso="ercot", node="HB_HOUSTON",
                                      fromdate="2022-01-01", todate="2023-12-31")
detail = client.calc.get_data_object("SLUG")
calcs = client.calc.get_data_object_calcs("SLUG")

# Create and run a calc
calc = client.calc.create_calc(iso="ercot", node="HB_HOUSTON", name="Houston Test",
                                startdate="2022-01-01", enddate="2023-12-31")

# Poll status
status = client.calc.get_calc_status(calc.slug)

# Browse results
summary = client.calc.get_calc_summary(calc.slug)
nodes = client.calc.list_calc_nodes(calc.slug)
scenarios = client.calc.list_calc_scenarios(calc.slug)
ns_list = client.calc.list_node_scenarios(calc.slug)

# Node-scenario results
ns = ns_list[0]
detail = client.calc.get_node_scenario(calc.slug, ns.slug)
result = client.calc.get_ns_result(calc.slug, ns.slug)
daily = client.calc.get_ns_daily_result(calc.slug, ns.slug)
params = client.calc.get_ns_params(calc.slug, ns.slug)
ns_status = client.calc.get_ns_status(calc.slug, ns.slug)

# Dragonet (quick optimization with your own data)
result = client.calc.run_dragonet("ercot", "HB_HOUSTON", open("data.csv", "rb"))
```

## Endpoint reference

### Data objects
| Method | Path | Python method |
|--------|------|---------------|
| GET | `/data/` | `client.calc.list_data_objects()` |
| POST | `/data/` | `client.calc.create_data_object(...)` |
| GET | `/data/{slug}/` | `client.calc.get_data_object(slug)` |
| GET | `/data/{slug}/calc/` | `client.calc.get_data_object_calcs(slug)` |

### Calc CRUD
| Method | Path | Python method |
|--------|------|---------------|
| GET | `/calc/` | `client.calc.list_calcs()` |
| POST | `/calc/` | `client.calc.create_calc(...)` |
| GET | `/calc/{slug}/` | `client.calc.get_calc(slug)` |
| GET | `/calc/{slug}/status/` | `client.calc.get_calc_status(slug)` |
| GET | `/calc/{slug}/summary/` | `client.calc.get_calc_summary(slug)` |

### Calc nodes / scenarios
| Method | Path | Python method |
|--------|------|---------------|
| GET | `/calc/{slug}/nodes/` | `client.calc.list_calc_nodes(slug)` |
| GET | `/calc/{slug}/nodes/{node}/` | `client.calc.get_calc_node(slug, node)` |
| GET | `/calc/{slug}/scenarios/` | `client.calc.list_calc_scenarios(slug)` |
| GET | `/calc/{slug}/scenarios/{scenario}/` | `client.calc.get_calc_scenario(slug, scenario)` |

### Node-scenario results
| Method | Path | Python method |
|--------|------|---------------|
| GET | `/calc/{slug}/nodescenarios/` | `client.calc.list_node_scenarios(slug)` |
| GET | `/calc/{slug}/nodescenarios/{ns}/` | `client.calc.get_node_scenario(slug, ns)` |
| GET | `/calc/{slug}/nodescenarios/{ns}/result/` | `client.calc.get_ns_result(slug, ns)` |
| GET | `/calc/{slug}/nodescenarios/{ns}/daily_result/` | `client.calc.get_ns_daily_result(slug, ns)` |
| GET | `/calc/{slug}/nodescenarios/{ns}/params/` | `client.calc.get_ns_params(slug, ns)` |
| GET | `/calc/{slug}/nodescenarios/{ns}/status/` | `client.calc.get_ns_status(slug, ns)` |

### Dragonet
| Method | Path | Python method |
|--------|------|---------------|
| POST | `/dragonet/calc/` | `client.calc.run_dragonet(iso, node, file)` |

## Concepts

- **Calc**: A calculation containing nodes x scenarios = node-scenarios
- **Node**: A pricing node (e.g., HB_HOUSTON)
- **Scenario**: Battery parameters — MW, hours, RTE, cycle cap
- **Node-Scenario (NS)**: One dispatch result per node x scenario pair
- **Dragonet**: Lightweight optimization engine — upload your own price CSV, get results back
- **COn**: Commitment Optimal perfect dispatch (with ancillary services)
