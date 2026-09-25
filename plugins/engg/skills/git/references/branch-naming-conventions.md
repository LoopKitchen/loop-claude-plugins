# Branch Naming Conventions

## Primary format (with a Linear ticket)

```
{TICKET-ID}/{kebab-case-description}
```

`TICKET-ID` is the Linear issue identifier: the team **key** followed by the issue number (for example `ENG-123`). The team key is the short prefix Linear shows on every issue; the team's UUID, which the `issueCreate` mutation needs, is what `$LINEAR_TEAM_ID` holds. This format is only used when `LINEAR_API_KEY` is set and a ticket was fetched or created in Step 2.

**Examples:**
- `ENG-123/add-health-check-endpoint`
- `ENG-456/fix-order-sync-timeout`
- `ENG-789/update-rate-limit-defaults`

## Fallback format (no ticket)

```
{type}/{kebab-case-description}
```

Where `type` is one of:
- `feat` — new functionality
- `fix` — bug fix
- `chore` — maintenance, config, tooling

**Examples:**
- `feat/add-health-check-endpoint`
- `fix/null-pointer-in-order-parser`
- `chore/upgrade-orm-deps`

## Autonomous format (`/git --autonomous`)

```
claude/{kebab-case-task-slug}
```

Used when another skill or an unattended session invokes `/git --autonomous`. The slug is derived from the task description exactly as below. If a Linear ticket exists, the primary format still wins (`{TICKET-ID}/...`); the `claude/` prefix is the no-ticket fallback for unattended runs so reviewers can tell machine-opened branches apart.

## Deriving the description

1. Start from the conversation context and plan, the Linear ticket title, or a summary of the git diff
2. Convert to lowercase
3. Replace spaces and special characters with hyphens
4. Remove consecutive hyphens
5. Truncate to **50 characters** max
6. Strip any trailing hyphens

**Example:** `"Add Health Check Endpoint for the API"` → `add-health-check-endpoint-for-the-api`
