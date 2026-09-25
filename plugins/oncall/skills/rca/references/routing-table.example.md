# Backend 5xx ownership and routing (example)

Copy this file to `references/routing-table.md` and fill in your own domains, channels, and on-call groups. The `rca` skill loads it before assigning an owner or posting an automated 5xx RCA. Channel names, channel ids, and group handles below are placeholders.

## Routing rules

1. **Route by the code that raised the error.** Identify the business domain from the raising file and the caller path, never from the browser client, the monitor that fired, or the gateway service that happened to serve the request.
2. **Map the domain to a channel and an on-call group** using the table below. Resolve channel ids against your chat tool before posting; if a channel was renamed, use the id and record the current name in the RCA.
3. **Apply path overrides for shared services.** When one service hosts several products, route by the longest matching business path (for example `/billing/` to the billing owners, `/reports/` to the reporting owners) rather than by the service's default owner.
4. **Shared utilities route to their caller.** When a shared helper (a database client, a cache wrapper) raises, the product that called it owns the impact; the helper's maintainer may be named only as the likely regression owner.
5. **Name an individual only with evidence.** Confirm the raising file and line from logs, run `git blame` and `git log -L`, resolve the commit to its PR, and check that the failure began after that PR deployed. Otherwise tag the product on-call group. A refactor author is not blamed for older defective logic.
6. **One post, one ownership line.** Every automated RCA post carries exactly one of the two lines below, goes to exactly one channel, and never tags the frontend group merely because a browser observed a backend 5xx.

```text
Likely regression owner: @<person> via <repo>#<pr>; response owner: @<on-call-group>.
Response owner: @<on-call-group>. No causal PR or individual owner was proven.
```

## Domain to channel map (example rows)

| Domain or service | Channel | Channel id | On-call group |
|---|---|---|---|
| Billing, `billing-service` | `#team-billing` | `<channel-id>` | `@billing-oncall` |
| Reporting, `reports-service`, paths `/reports/`, `/exports/` | `#team-reporting` | `<channel-id>` | `@reporting-oncall` |
| Shared backend or unresolved ownership | `#backend` | `<channel-id>` | `@backend-oncall` |
