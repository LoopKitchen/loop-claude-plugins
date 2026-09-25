# Sentry alert inventory (example)

Copy this file to `references/alerts.md` and keep it current. The `rca` skill checks it in Step 4 so that no RCA claims "no alerting exists" for a path that already has an alert. Every row below is a placeholder.

Regenerate the rows from the Sentry API (requires `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, and `SENTRY_REGION_URL`):

```bash
curl -s -H "Authorization: Bearer ${SENTRY_AUTH_TOKEN}" \
  "${SENTRY_REGION_URL:-https://us.sentry.io}/api/0/organizations/${SENTRY_ORG}/alert-rules/" \
  | python3 -c "
import json, sys
for r in json.load(sys.stdin):
    trig = ', '.join(f\"{t.get('label','')}={t.get('alertThreshold','')}\" for t in r.get('triggers', []))
    print(f\"| {r.get('id','')} | {r.get('name','')} | \`{r.get('aggregate','')}\` | {trig} | |\")
"
```

| Alert ID | Name | Metric | Warning | Critical | Channel |
|----------|------|--------|---------|----------|---------|
| `<id>` | `<product> API latency - p95` | `p95(span.duration)` | 4,000ms | 6,000ms | `#<alerts-channel>` |
| `<id>` | `Top 3 slow APIs - p99` | `p99(span.duration)` | - | - | `#<alerts-channel>` |
| `<id>` | `Failed API - 5xx count` | `count()` | - | - | `#<alerts-channel>` |
| `<id>` | `401 Unauthorized - APIs` | `count()` | - | - | `#<alerts-channel>` |

Columns: Warning and Critical are the trigger thresholds; Channel is where the alert posts. Add a row per alert rule; delete rows for rules that no longer exist.
