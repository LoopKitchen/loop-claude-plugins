# RCA: [short title]

Copy this file to `$RCA_DOCS_DIR/RCA-<YYYY-MM-DD>-<slug>.md` (default `docs/rca/`) and replace every `[placeholder]`. Keep every section and every table column; write "N/A" rather than deleting a row. Write the Summary last.

## 1. Metadata

| Field | Value |
|-------|-------|
| RCA ID | `RCA-[YYYY-MM-DD]-[NNN]` |
| Title | [short title] |
| Incident date | [YYYY-MM-DD] |
| RCA date | [YYYY-MM-DD] |
| Severity | SEV-[1/2/3/4] (see matrix below) |
| Status | [Investigating / Root cause identified / Resolved / Closed] |
| GitHub issue | [`owner/name#NNN`](https://github.com/owner/name/issues/NNN) |
| Incident commander | [name] |
| Investigator | [name] |
| Backend owner | [name or on-call group] |
| Frontend owner | [name or on-call group] |
| Reviewer | [name] |

| Severity | Criteria | RCA due |
|----------|----------|---------|
| SEV-1 | Revenue-impacting outage, data loss, security breach, or more than 50% of users affected | 24 hours |
| SEV-2 | Major feature degradation, more than 10% of users affected, or an SLA breach | 3 business days |
| SEV-3 | Minor feature degradation, performance regression, or fewer than 10% of users affected | 5 business days |
| SEV-4 | Cosmetic issue, intermittent bug, or single-user impact | 10 business days |

## 2. Summary

[Two or three sentences for non-technical readers: what broke, who it affected, for how long, and what fixed it. Write this section last.]

## 3. Customer Impact

| Metric | Value |
|--------|-------|
| Duration | [start to end, UTC; total minutes] |
| Users affected | [count or estimate, with how it was measured] |
| Organizations affected | [count or list] |
| Pages / endpoints affected | [list] |
| Revenue impact | [amount or "none identified"] |
| Data loss | [yes/no; scope] |
| SLA breach | [yes/no; which SLA] |
| Support tickets | [count and links] |

**User experience:** [What the user saw, in one paragraph. Include what did load and what did not.]

[Screenshot placeholder: user-facing symptom]

## 4. Timeline

All times in UTC. The local column uses the reporter's or the on-call engineer's timezone; state which one: [timezone, e.g. America/Los_Angeles].

| Time (UTC) | Time (local, [TZ]) | Event | Source |
|------------|--------------------|-------|--------|
| [YYYY-MM-DD HH:MM:SS] | [HH:MM] | [Deploy / first error / user report / alert fired / mitigation / resolved] | [clickable, time-scoped link: logs, Sentry, PostHog, deploy, PR] |
| | | | |

## 5. Detection

| Field | Value |
|-------|-------|
| How detected | [alert / customer report / internal report / automated sweep] |
| Time to detect (TTD) | [minutes from first impact to detection] |
| Who detected it | [person, alert name, or channel] |
| Existing alerts covering this path | [alert names and links, or "none"; verify against the alert inventory before writing "none"] |
| Alerting gap | [what alert would have caught this earlier, or "none"] |

> If the incident was customer-reported, call that out here and add a Detect action item in section 9.

## 6. Root Cause

**What happened:** [One paragraph describing the failing mechanism, with the raising file and line where known.]

**5 Whys:**

1. Why did [symptom]? Because [cause 1].
2. Why did [cause 1]? Because [cause 2].
3. Why did [cause 2]? Because [cause 3].
4. Why did [cause 3]? Because [cause 4].
5. Why did [cause 4]? Because [root cause].

| | Description |
|---|-------------|
| Trigger | [the event that exposed the defect, e.g. a deploy, a traffic spike, a filter selection] |
| Root cause | [the underlying defect that made the trigger harmful] |

| Category | Choose one |
|----------|-----------|
| [Data Gap / API Error / Frontend Bug / Backend Bug / User Config / Infra Issue / Auth Issue / Deploy Regression / Feature Flag / Performance / Third-Party] | |

## 7. Contributing Factors

- [Factor 1: something that made the incident more likely, wider, or longer, e.g. a missing empty-state check, a missing alert, a shared code path]
- [Factor 2]
- [What went well / where we got lucky, if relevant]

## 8. Resolution

| Field | Value |
|-------|-------|
| Mitigation | [what stopped the bleeding, and when (UTC)] |
| Fix | [PR link and deploy time (UTC)] |
| Verification | [how the fix was confirmed: log query, replay, metric, with links] |
| Rollback plan | [if applicable] |

## 9. Action Items

Types: Prevent (stops recurrence), Mitigate (limits impact), Detect (finds it faster), Process (changes how we work).

| # | Action | Type | Owner | Issue | Priority | Due date | Status |
|---|--------|------|-------|-------|----------|----------|--------|
| 1 | [action] | [Prevent/Mitigate/Detect/Process] | [name] | [`owner/name#NNN`] | [P0/P1/P2] | [YYYY-MM-DD] | TODO |
| 2 | | | | | | | |

## 10. Evidence Links

Every link must be time-scoped to the incident window and filter-specific (service, endpoint, status, trace id). No generic dashboard links.

| System | What it shows | Link |
|--------|---------------|------|
| Cloud Logging (HTTP logs) | [requests for trace `<trace_id>`] | [link with `;startTime=;endTime=`] |
| Cloud Logging (app logs) | [request body for trace `<trace_id>`] | [link] |
| Cloud Run metrics | [service latency / error rate in window] | [link] |
| Sentry (trace or issue) | [trace waterfall / issue] | [link] |
| Sentry (alerts) | [alert rule that fired or should have] | [link] |
| PostHog (events) | [API_latency events for the user] | [link] |
| PostHog (session replay) | [session `<session_id>`] | [link] |
| Deployment | [deploy that preceded the incident] | [link] |
| GitHub | [issue, causal PR, fix PR] | [links] |

**Key log snippets:**

```text
[paste the critical log lines with timestamps]
```

**Trace waterfall:**

[Screenshot placeholder: trace waterfall]

| Span | Duration | Description |
|------|----------|-------------|
| [span] | [ms] | [what it did and why it matters] |

**Infrastructure state at the time:**

| Setting | Value |
|---------|-------|
| [service revision / instance count / memory / concurrency / feature flags] | [value] |

## 11. Lessons Learned (optional)

- What went well: [bullet]
- What went wrong: [bullet]
- Where we got lucky: [bullet]

## 12. Sign-off (optional)

| Role | Name | Date | Approved |
|------|------|------|----------|
| RCA owner | [name] | [YYYY-MM-DD] | [yes/no] |
| Engineering lead | [name] | [YYYY-MM-DD] | [yes/no] |

Post-RCA checklist:

- [ ] All action items have an owner, an issue, and a due date
- [ ] Every evidence link opens directly to the evidence
- [ ] GitHub issue updated with the RCA link and final state
- [ ] Alert inventory updated if a Detect action item added an alert
