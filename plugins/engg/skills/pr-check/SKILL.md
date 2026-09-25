---
name: pr-check
description: Check PR status after /git — fetches review comments, plans fixes, and checks CI. Use when the user wants to read reviewer feedback, plan fixes for review comments, or check CI status.
allowed-tools:
  - Bash(gh *)
---

1. **Find the PR**: Run `gh pr view --json number,url,title,statusCheckRollup,reviews,comments` for the current branch. If no PR exists, tell the user to run `/git` first.
2. **Read review comments**: Parse `reviews` and `comments` from step 1 for PR-level feedback. Also fetch inline review comments with `gh api repos/{owner}/{repo}/pulls/{number}/comments`. Summarize all feedback.
3. **Plan fixes**: Think hard about the feedback. Create a prioritized fix plan for any issues found.
4. **Check CI** _(skip if step 3 identified fixes to implement — CI will re-run after those fixes are pushed)_: Inspect GitHub Actions status checks. If any are still running, wait and re-check (up to 2 retries with 30s delay). Report pass/fail results. If any checks failed, fetch the failed job logs and include suggested fixes in the output.
