# Linear GraphQL API Reference

All Linear API calls use the GraphQL endpoint at `https://api.linear.app/graphql`.
Auth is via the `LINEAR_API_KEY` environment variable.

## Unique file paths

Before making Linear API calls, generate a unique suffix to avoid file collisions:
```bash
date +%s
```
Capture the command's stdout and store it in an internal variable named `LINEAR_REQ_ID` (for example, if the command prints `1773257185`, treat that as `LINEAR_REQ_ID`) and use it in all subsequent file paths: `/tmp/linear-payload-$LINEAR_REQ_ID.json` and `/tmp/linear-result-$LINEAR_REQ_ID.json`

## Command pattern

1. **Write** the JSON payload to `/tmp/linear-payload-$LINEAR_REQ_ID.json` using the Write tool.
2. **Run curl** in a single line with `-o` to save the response (no `\` continuations, no pipes):
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```
3. **Read** `/tmp/linear-result-$LINEAR_REQ_ID.json` using the Read tool to get the response. Parse the JSON from the result.

---

## 0. List teams (only when `LINEAR_TEAM_ID` is unset)

```graphql
{ teams { nodes { id key name } } }
```

Write `/tmp/linear-payload-$LINEAR_REQ_ID.json`:
```json
{"query": "{ teams { nodes { id key name } } }"}
```

Then run:
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```

Then read `/tmp/linear-result-$LINEAR_REQ_ID.json` and extract `.data.teams.nodes`. Use `id` (a UUID) as `teamId`; `key` is the prefix that appears in issue identifiers such as `ENG-123`. Once chosen, suggest the user export it as `LINEAR_TEAM_ID` so this query is not needed again.

---

## 1. Fetch issue by identifier

```graphql
query($id: String!) {
  issue(id: $id) {
    id
    identifier
    title
    description
    state { name }
    assignee { name }
    team { id key name }
    cycle { id name }
  }
}
```

**Example:**

Write `/tmp/linear-payload-$LINEAR_REQ_ID.json`:
```json
{"query": "query($id: String!) { issue(id: $id) { id identifier title description state { name } assignee { name } team { id key name } cycle { id name } } }", "variables": {"id": "ENG-123"}}
```

Then run:
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```

Then read `/tmp/linear-result-$LINEAR_REQ_ID.json` and extract `.data.issue`.

---

## 2. Get active cycle for a team

```graphql
query($teamId: String!) {
  team(id: $teamId) {
    activeCycle {
      id
      name
      number
      startsAt
      endsAt
    }
  }
}
```

**Example:**

Write `/tmp/linear-payload-$LINEAR_REQ_ID.json`:
```json
{"query": "query($teamId: String!) { team(id: $teamId) { activeCycle { id name number startsAt endsAt } } }", "variables": {"teamId": "TEAM_ID"}}
```

Then run:
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```

Then read `/tmp/linear-result-$LINEAR_REQ_ID.json` and extract `.data.team.activeCycle`.

---

## 3. Create issue

```graphql
mutation($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
      url
    }
  }
}
```

**Variables (`$input`):**
```json
{
  "teamId": "TEAM_UUID ($LINEAR_TEAM_ID)",
  "assigneeId": "USER_UUID",
  "cycleId": "CYCLE_UUID (omit if no active cycle)",
  "title": "Issue title",
  "description": "## Summary\n- bullet points"
}
```

To assign to the authenticated user, first fetch your user ID.

Write `/tmp/linear-payload-$LINEAR_REQ_ID.json`:
```json
{"query": "{ viewer { id name } }"}
```

Then run:
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```

Then read `/tmp/linear-result-$LINEAR_REQ_ID.json` and extract `.data.viewer`.

**Full create example:**

Write `/tmp/linear-payload-$LINEAR_REQ_ID.json`:
```json
{"query": "mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }", "variables": {"input": {"teamId": "TEAM_UUID", "title": "Add health check endpoint", "description": "## Summary\n- Add /health endpoint", "assigneeId": "USER_UUID", "cycleId": "CYCLE_UUID"}}}
```

Then run:
```bash
curl -s -X POST https://api.linear.app/graphql -H "Content-Type: application/json" -H "Authorization: $LINEAR_API_KEY" -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json
```

Then read `/tmp/linear-result-$LINEAR_REQ_ID.json` and extract `.data.issueCreate.issue`.

---

## Notes

- **All commands must be single-line.** Claude Code's Bash tool inserts empty string arguments (`''`) at `\` line continuation points, breaking curl. Heredocs (`<< 'EOF'`) also fail because glob patterns like `Bash(cat *)` cannot match across newlines ([#11932](https://github.com/anthropics/claude-code/issues/11932)).
- **Do not pipe curl output.** `$LINEAR_API_KEY` becomes empty when the command contains a pipe `|`. Use `-o /tmp/linear-result-$LINEAR_REQ_ID.json` to save the response to a file, then read it with the Read tool.
- Use the **Write tool** to create `/tmp/linear-payload-$LINEAR_REQ_ID.json`, then run `curl -d @/tmp/linear-payload-$LINEAR_REQ_ID.json -o /tmp/linear-result-$LINEAR_REQ_ID.json` in a **separate single-line Bash call**. Read the result with the **Read tool**.
- The `$id` parameter in `issue(id:)` accepts both UUID and identifier format (e.g. `ENG-123`).
- Always check `.data` and `.errors` in the response; Linear returns HTTP 200 even for GraphQL errors.
- Rate limit: 1500 requests per hour per API key.
