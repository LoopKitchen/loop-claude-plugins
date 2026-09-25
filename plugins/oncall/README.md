# oncall

On-call and incident response skills for Claude Code.

```bash
claude plugin marketplace add LoopKitchen/loop-claude-plugins
claude plugin install oncall@loop-plugins
```

## Skills

| Skill | What it does |
|---|---|
| `loki` | Query production logs from Grafana Loki by service, time range, severity and search text. `/loki services` and `/loki labels` discover what exists before you query; results are summarised by the bundled `parse_logs.py`. Triggers on "check logs", "production errors", "search logs", "what's failing". |
| `rca` | Root cause analysis for production issues: data mismatches, blank pages, missing data, API latency, page load and waterfall problems. Correlates Sentry, PostHog session replays, cloud logs, Vercel deployments and GitHub history using the request's traceparent, then writes an RCA document from `references/rca-template.md` into `RCA_DOCS_DIR`. Routing of findings to owners follows `references/routing-table.md`, which you create from `routing-table.example.md`; the Sentry alert inventory lives in `references/alerts.md`, created from `alerts.example.md`. |
| `on-call-report` | On-call health report. Scans a tiered list of Slack channels (`channels.example.json` shows the shape; copy it to `channels.json` or point `ONCALL_CHANNELS_FILE` at your copy), Sentry issues, GitHub issues and PRs, and PostHog errors; categorises everything as Frontend / Backend / Infra / Customer impact and emits task briefs an agent can pick up. Triggers on "on-call report", "health report", "what's broken", "system health". |

## Configuration

Set these as environment variables (or in the `env` block of
`.claude/settings.json`). Each skill's `SKILL.md` repeats the subset it reads.

| Variable | Required | Default | Meaning | Read by |
|---|---|---|---|---|
| `LOKI_URL` | yes, for `loki` | none | Base URL of the Loki gateway (`/loki/api/v1/...` is appended) | `loki` |
| `LOKI_AUTH_HEADER` | no | none | Full header string for authenticated gateways, e.g. `Authorization: Bearer <token>` or `X-Scope-OrgID: <tenant>` | `loki` |
| `GCP_PROJECT` | for `rca` | none | Production Google Cloud project id | `rca` |
| `GCP_STAGING_PROJECT` | no | none | Staging Google Cloud project id | `rca` |
| `SENTRY_ORG` | for `rca`, `on-call-report` | none | Sentry organisation slug | `rca`, `on-call-report` |
| `SENTRY_REGION_URL` | no | `https://us.sentry.io` | Sentry API base for your region | `rca`, `on-call-report` |
| `SENTRY_PROJECTS` | for `rca`, `on-call-report` | none | Comma-separated Sentry project slugs | `rca`, `on-call-report` |
| `SENTRY_AUTH_TOKEN` | for `rca` step 4 | none | Sentry API token (a secret) for the alert-inventory check | `rca` |
| `GITHUB_ORG` | for `on-call-report` | none | GitHub organisation to scan for issues and PRs | `on-call-report` |
| `GITHUB_REPO` | for `rca`, `on-call-report` | none | `owner/name` of the primary repository | `rca`, `on-call-report` |
| `POSTHOG_PROJECT_ID` | no | none | PostHog project id for replay and error links; `on-call-report` skips its PostHog phase when unset | `rca`, `on-call-report` |
| `APP_URL` | for `rca` | none | Public URL of the main web app | `rca` |
| `ADMIN_URL` | no | none | URL of the admin app, if separate | `rca` |
| `API_URL` | no | none | URL of the API host | `rca` |
| `VERCEL_PROJECTS` | no | none | Comma-separated Vercel project names | `rca` |
| `RCA_DOCS_DIR` | no | `docs/rca/` | Where RCA documents are written; `on-call-report` saves reports to the sibling `reports/` directory | `rca`, `on-call-report` |
| `ONCALL_CHANNELS_FILE` | no | `${CLAUDE_PLUGIN_ROOT}/skills/on-call-report/channels.json` | Tiered Slack channel config (copy `channels.example.json`) | `on-call-report` |
| `COMPANY_NAME` | no | `GITHUB_ORG` | Name used in report titles | `on-call-report` |

Filled-in copies (`channels.json`, `references/routing-table.md`,
`references/alerts.md`) carry real channel and alert ids; the repository's
`.gitignore` keeps them out of version control.

## Requirements

- `curl` and `python3` for `loki`.
- `gh` (authenticated) and `gcloud` (authenticated against `GCP_PROJECT`) for `rca`.
- MCP servers registered as `slack`, `sentry` and `posthog` for
  `on-call-report` and the Sentry / PostHog steps of `rca`; `rca` can also use
  `vercel` and `firebase` servers when present. Without them the skills fall
  back to CLI and manual steps where they can.

## Notes

- `loki` assumes a Loki HTTP API (`/loki/api/v1/query_range`, `/labels`,
  `/label/<name>/values`) reachable at `LOKI_URL`. Grafana Cloud and
  self-hosted Loki both work; put the auth header in `LOKI_AUTH_HEADER`.
- `rca` never edits production. It reads, correlates, and writes a document.
- `on-call-report` posts nothing to Slack unless you ask it to; it reads
  channels and drafts a report.
