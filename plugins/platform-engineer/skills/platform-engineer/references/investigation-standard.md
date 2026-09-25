# Investigation standard

## WHAT
For production and incident work, anchor every claim to ground-truth data. Treat
any existing root-cause account as a hypothesis that still needs testing.

## WHY
- The strongest past outcomes came from grounding each conclusion in real data
  and disproving stale explanations. Two recurring shapes: an upstream API
  contract change that had been misread as a data-quality issue in the
  consumer, and a trailing-edge lag artifact that had been reported as a 0%
  failure rate. In both, the accepted story was wrong and the data showed it.
- A diagnosis that names its evidence source is reviewable and defensible. One
  that asserts a cause without a source is a guess that reviewers cannot check.

## HOW
- Pull ground truth before accepting any diagnosis: warehouse ledgers, document
  stores, raw report tables, transformation models, git history, deploy
  timelines, and cache-bypassing live probes. State the source next to each
  conclusion.
- When a prior RCA, an alert summary, or institutional memory already names a
  cause, test it directly and try to disprove it before building on it.
  Recalled memories reflect what was true when written, so verify a named file,
  flag, or table still exists before relying on it.
- For a mystery that spans several data stores or code paths, dispatch parallel
  agents (one per store, one per code path, one per deploy timeline), have each
  return cited findings, then reconcile and flag contradictions. This is the
  highest-value pattern in past incident work.
- Express a data or credential fix as a concrete assertion (this credential
  returns a valid lease, this store maps correctly, this backlog is under N).
  Apply the fix, then re-run the assertion against live production, not cached
  data. If it still fails, diagnose and retry before declaring it done.
- Use the existing entry points for this: `/rca` and `/loki` (oncall plugin).
  This standard is the standing discipline they run under. It does not replace
  them.
- Prefer CLI surfaces (your warehouse CLI, your cloud CLI, `/loki`) over MCP
  equivalents for these queries where both exist; CLI output is reproducible
  and quotable in the diagnosis.
