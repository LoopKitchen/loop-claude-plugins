# PR review loop — mandatory before every merge

This loop is a hard gate: a PR is not mergeable until the loop reaches fixpoint,
even when the PR carries a label that lets it merge without human review (a
`skip-review`-style auto-merge label) — such labels remove the human gate, which
makes this loop the only quality gate left.

**Human-gated exception**: incident/data-fix PRs, draft PRs, and PRs the repo's
policy reserves for human review run the loop to clean and stop at "threads
resolved, ready for review" — a human merges those. Everything else in this file
applies unchanged; only step 8's merge is replaced by a handoff.

## The loop (run to fixpoint)

1. **Open the PR** (via `/git`). Do not merge yet.
2. **Wait for all bot reviewers to publish.** Use whatever review bots the repo
   runs (CodeRabbit, Qodo, gemini-code-assist and Copilot are common). They
   typically land within a few minutes of push; poll with
   `gh pr view <N> --json reviews,comments` (or a background Monitor) until the
   count stabilizes. A repo with no bots goes straight to step 4.
3. **Address bot comments** with technical rigor: verify each finding against the
   code before implementing; rebut false positives with evidence in a reply rather
   than blindly complying. Optional: the CodeRabbit and Qodo Claude Code plugins
   ship resolver skills — run them one at a time, never in parallel (they race on
   the same files).
4. **Run your own review**: `/code-review` (built into Claude Code; `/local-pr-review`
   from this plugin is the offline fallback) on `git diff origin/main...HEAD`
   (3-dot — this branch's changes only, excluding merge-from-main churn and
   unrelated in-flight work; substitute the repo's default branch for `main`).
5. **Fix, commit, push** (via `/git`). New pushes can trigger new bot comments.
6. **Repeat 2-5 until fixpoint**: zero unresolved GitHub review threads AND zero new
   substantive findings from your own pass. Convergence bound: if 3 consecutive
   rounds produce only non-substantive bot re-comments (style echoes, re-statements
   of dismissed findings), treat the loop as converged, note the dismissed residue
   in the PR body, and proceed.
7. **Resolve every thread.** Reply to each addressed comment and resolve it
   (GraphQL `resolveReviewThread`). Comment resolution is a precondition of merge,
   not cleanup after it.
8. **Merge** with the repo's merge convention and its auto-merge label if it uses
   one — except human-gated PRs (see exception above), and except PRs the repo's
   policy excludes from label-only merges (typical thresholds: more than ~20 files,
   auth/credential code, schema migrations): those also stop at "clean + resolved"
   and hand off for human review. Deploy labels are optional: apply them only from
   the repo's documented path-to-label mapping (this plugin's `/git` skill applies
   such a mapping when configured); never guess a label, and check the mapping
   yourself for code an automatic classifier tends to miss (shared libraries,
   background-worker code). A parent-repo submodule-bump PR merges only after the
   submodule's own PR; if the submodule is dirty mid-sweep, finish the submodule PR
   first. Then watch the deploy.

## Follow-on obligations

- **If a PR already merged unreviewed**, raise a follow-up PR addressing its review
  comments; do not leave threads rotting on merged PRs.
- **Follow-on work absorbs review deltas first.** Before building on a branch that
  went through review iterations, re-read what changed during those iterations, not
  just the original diff.
- **Integration/handler PRs** (code that calls third-party APIs) additionally get a
  pattern-check pass: fan-out bounds, auth handling, silent-empty-result paths,
  validation at serialization boundaries.

## Rationalizations that do not exempt the loop

| Excuse | Reality |
|---|---|
| "The PR has an auto-merge label, no one will look" | That is exactly why the loop is mandatory — it is the only gate left. |
| "Bots only leave nits" | Bots regularly catch real defects (pagination edge cases, off-by-one bounds). Verify, then dismiss with evidence if wrong. |
| "The change is tiny" | Small diffs still get steps 2-7; they just converge in one iteration. |
| "CI is green" | CI proves compilation and tests, not review findings. |
| "I already reviewed while writing" | The loop requires a fresh diff-vs-main pass after the PR exists. |
