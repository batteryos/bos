# BOS — BatteryOS Skills for Claude Code

Terminal-native access to [BatteryOS](https://batteryos.com): ERCOT electricity prices,
BESS asset analytics, dispatch optimization, interconnection queue, and market reports —
through Claude Code.

BatteryOS is a battery storage analytics platform. These skills expose its
[API](https://batteryos.com/api/v1/) (84 endpoints across 6 domains) as Claude Code
commands, backed by a typed Python client library.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **bos** | `/bos` | Primer and skill router |
| **bos-assets** | `/bos-assets` | BESS asset performance: revenue, volume, cycles (30 endpoints) |
| **bos-prices** | `/bos-prices` | DAM/RTM hub prices, ICE forwards, contracts (7 endpoints) |
| **bos-calcs** | `/bos-calcs` | Dispatch calc results: nodes, scenarios, NS output (35 endpoints) |
| **bos-dispatch** | `/bos-dispatch` | Create calcs, dispatch to Dragon (4 endpoints) |
| **bos-queue** | `/bos-queue` | ERCOT interconnection projects, milestones (10 endpoints) |
| **bos-dashboard** | `/bos-dashboard` | Market reports, TBn spreads, rankings (7 endpoints) |

## Install — 30 seconds

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Git](https://git-scm.com/), [Python 3.10+](https://www.python.org/)

### Step 1: Install on your machine

Open Claude Code and paste this. Claude does the rest.

> Install BOS skills: run **`git clone https://github.com/batteryos/bos.git ~/.claude/skills/bos && cd ~/.claude/skills/bos && ./setup`** then add a "bos" section to CLAUDE.md that lists the available skills: /bos, /bos-assets, /bos-prices, /bos-calcs, /bos-dispatch, /bos-queue, /bos-dashboard.

Or do it manually:

```bash
# Clone into Claude Code skills directory
cd ~/.claude/skills
git clone https://github.com/batteryos/bos.git bos

# Run setup (creates ~/.bos, installs Python lib, symlinks skills)
cd bos && ./setup
```

### Step 2: Set your API token

```bash
echo "your-token-here" > ~/.bos/credentials
```

Or set the `BOS_API` environment variable.

### What setup does

1. Creates `~/.bos/` directories (bin, state, analytics)
2. Copies CLI tools to `~/.bos/bin/`
3. Creates a Python virtualenv and installs `requests` + `pytest`
4. Runs the test suite to verify everything works
5. Symlinks all 6 sub-skills into `~/.claude/skills/`
6. Checks for API token

### Step 3: Verify

```bash
/bos
```

You should see the primer table with all 6 domain skills.

## Auth

BOS API token, resolved in order:
1. Explicit: `BOSClient(token="...")`
2. Environment: `BOS_API` env var
3. File: `~/.bos/credentials` (token as plain text)

## Hosts

| Host | Services |
|------|----------|
| `titan.batteryos.com` | Prices, Kronos (contracts), Analysis, Dragonet |
| `batteryos.com` | Calc, Assets, Queue, Dashboard |

## Quick Start

```bash
/bos                    # Show all capabilities
/bos-assets             # BESS fleet performance
/bos-prices             # Electricity prices and forwards
/bos-dispatch           # Run a Dragon dispatch
/bos-queue              # Interconnection queue
/bos-dashboard          # Market dashboards
```

## Python API

The skills are backed by a typed Python client library at `src/bos/`.
You can use it directly:

```python
from bos import BOSClient
from bos.assets.models import AssetFilter

client = BOSClient()

# Typed path — autocomplete shows every field
assets = client.assets.list_assets(AssetFilter(owner_name=["Vistra"], duration=[2]))

# All domains
calcs = client.calc.list_calcs()
prices = client.prices.list_contracts()
projects = client.queue.list_projects()
ranking = client.dashboard.get_ranking()
```

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- BOS API token
- Python 3.10+

## Structure

```
bos/
  SKILL.md                          # /bos — primer and router
  CLAUDE.md                         # Instructions for Claude Code
  README.md                         # This file
  setup                             # One-command install
  bin/                              # CLI tools
  skills/
    bos-assets/SKILL.md
    bos-prices/SKILL.md
    bos-calcs/SKILL.md
    bos-dispatch/SKILL.md
    bos-queue/SKILL.md
    bos-dashboard/SKILL.md
  src/bos/                          # Python API wrapper library
    assets/   calc/   prices/   gridqueue/   dashboard/
```
