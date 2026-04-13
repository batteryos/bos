# BOS Skills — CLAUDE.md

## What is BatteryOS?

[BatteryOS](https://batteryos.com) is a battery energy storage analytics platform
covering the ERCOT market. It provides dispatch optimization (Dragon engine), asset
performance tracking, forward price curves, interconnection queue data, and market reports.

## API

Two hosts, one auth token:

| Host | Base URL | Services |
|------|----------|----------|
| batteryos.com | `https://batteryos.com/api/v1` | All Services |

**84 endpoints** total across 6 domains.

Auth: `Authorization: Token <token>` header on every request.
Token source: `active_token` in `src/bos/auth.py` (explicit) > `BOS_API` env var > `~/.bos/credentials` file.

## Authentication Workflow (CLI OTP)

If a valid token is missing and an `AuthError` occurs:

1. **Prompt for Email**: Ask the user for their work email address.
2. **Request OTP**: Call `POST https://batteryos.com/api/v1/auth/cli/request/` with `{"email": "user@company.com"}`.
   - If 403, inform the user about the work email requirement and ask again.
3. **Prompt for OTP**: Tell the user to check their inbox and provide the 6-digit code.
4. **Verify OTP**: Call `POST https://batteryos.com/api/v1/auth/cli/verify/` with `{"email": "user@company.com", "otp": "123456"}`.
5. **Store Token**: On success (200 OK), extract the token and save it to `~/.bos/credentials`:
   `echo -n "TOKEN_HERE" > ~/.bos/credentials`
   Then proceed with the original request.

## Working with the API

All API calls go through the `bos` Python library at `src/bos/`. No curl.

```python
import sys; sys.path.insert(0, "/Users/vishal/.claude/skills/bos/src")
from bos import BOSClient
client = BOSClient()
```

## Repo Structure

```
bos/
  SKILL.md                          # /bos — primer and skill router
  CLAUDE.md                         # This file
  README.md
  openapi.json                      # Consolidated OpenAPI spec
  bin/                              # CLI tools: bos-data-check, bos-config
  skills/
    bos-dispatch/SKILL.md           # /bos-dispatch — 20 calc/data/dragonet endpoints
    bos-prices/SKILL.md             # /bos-prices — 8 contract/price endpoints
    bos-analysis/SKILL.md           # /bos-analysis — 11 TBn/RPO/EOn/CRR endpoints
    bos-calcs/SKILL.md              # /bos-calcs — alias for bos-analysis
    bos-assets/SKILL.md             # /bos-assets — 28 asset endpoints
    bos-dashboard/SKILL.md          # /bos-dashboard — 7 dashboard endpoints
    bos-queue/SKILL.md              # /bos-queue — 10 queue endpoints
  src/bos/                          # Python API wrapper library
    calc/      models.py client.py config.py tests.py examples.py
    prices/    models.py client.py config.py tests.py
    analysis/  client.py config.py tests.py
    assets/    models.py client.py config.py tests.py examples.py
    dashboard/ models.py client.py config.py tests.py examples.py
    gridqueue/ models.py client.py config.py tests.py examples.py
```

Skills are symlinked into `~/.claude/skills/`:
```
~/.claude/skills/bos              -> this repo
~/.claude/skills/bos-dispatch     -> bos/skills/bos-dispatch/
~/.claude/skills/bos-prices       -> bos/skills/bos-prices/
~/.claude/skills/bos-analysis     -> bos/skills/bos-analysis/
~/.claude/skills/bos-calcs        -> bos/skills/bos-calcs/
~/.claude/skills/bos-assets       -> bos/skills/bos-assets/
~/.claude/skills/bos-dashboard    -> bos/skills/bos-dashboard/
~/.claude/skills/bos-queue        -> bos/skills/bos-queue/
```


## Conventions

- **SKILL.md** (uppercase) for skill files
- All skills share the same preamble pattern (analytics logging)
- Usage is logged to `~/.bos/analytics/skill-usage.jsonl`
- Config at `~/.bos/config.yaml`, managed via `~/.bos/bin/bos-config`

## Output Rules
- Combine preamble (mkdir, logging, bos-data-check) and the actual command into a single bash call so the user sees only one output. Suppress preamble output with `>/dev/null 2>&1`. Only surface preamble results if DATA_STALE or error requiring user action.
- Show raw command output. Do not summarize, paraphrase, or editorialize unless the user asks for interpretation.

## Adding a New Skill

1. Create `skills/bos-<name>/SKILL.md` with frontmatter (`name`, `version`, `description`, `allowed-tools`)
2. Include the preamble (analytics logging)
3. Add related skills cross-references
4. Symlink: `cd ~/.claude/skills && ln -sf bos/skills/bos-<name> bos-<name>`
5. Update the primer table in `bos/SKILL.md`
