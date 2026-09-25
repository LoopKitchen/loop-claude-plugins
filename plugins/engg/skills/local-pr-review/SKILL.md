---
name: local-pr-review
description: Local code review of a PR with structured markdown report output. Use when the user wants an offline review with a downloadable report that an AI agent can use to implement fixes.
---

## Arguments

- `$ARGUMENTS` — PR number (e.g., `123`)

Perform a comprehensive local code review of PR $ARGUMENTS following the LEVER optimization principles. Generate a structured markdown report that an AI agent can use to implement fixes.

First, read and internalize the optimization principles from `/optimization-principles.md`.

**CRITICAL SETUP - Clean Checkout**:
1. Stash any current changes: `git stash -u`
2. Switch to main: `git checkout main`
3. Pull latest: `git pull`
4. Checkout PR: `gh pr checkout $ARGUMENTS`

**Ultrathink** about the code - look for deep optimization opportunities.

## Analysis Steps

1. **Fetch PR Details**:
   - Get PR info: `gh pr view $ARGUMENTS --json title,body,files,additions,deletions`
   - Get the diff: `gh pr diff $ARGUMENTS`

2. **Analyze Against LEVER Framework**:
   Read the LEVER framework from [../pr-review/references/lever-framework.md](../pr-review/references/lever-framework.md).

3. **Focus Areas**:
   See the Focus Areas section in [../pr-review/references/lever-framework.md](../pr-review/references/lever-framework.md).

## Report Generation

Create a markdown report at `./pr-review-$ARGUMENTS.md` with the following structure:

```markdown
# PR Review Report: #[PR_NUMBER]

**Title**: [PR Title]
**Branch**: [branch name]
**Files Changed**: [count]
**Lines Added/Removed**: +[additions] / -[deletions]

---

## Executive Summary

[2-3 sentence overview of the PR and main optimization opportunities]

**Potential Code Reduction**: X lines -> Y lines (Z% reduction possible)

---

## Issues Found

### Issue 1: [Brief Descriptive Title]

**Severity**: High | Medium | Low
**LEVER Principle**: [Which principle is violated]
**File**: `path/to/file.py`
**Lines**: [start_line]-[end_line]

#### Current Code (BEFORE)
```python
[Exact code from the PR that needs improvement]
```

#### Suggested Fix (AFTER)
```python
[Exact refactored code that should replace it]
```

#### Explanation
[Brief explanation of why this change improves the code]

#### Impact
- Lines reduced: X -> Y
- Complexity reduction: [description]

---

### Issue 2: [Next Issue Title]
[Same structure as above]

---

## Action Items Checklist

For an AI agent to implement these fixes, complete in order:

- [ ] **Issue 1**: [One-line actionable description]
  - File: `path/to/file.py`
  - Action: Replace lines X-Y with suggested code

- [ ] **Issue 2**: [One-line actionable description]
  - File: `path/to/file.py`
  - Action: [specific action]

---

## Files to Modify

| File | Issues | Priority |
|------|--------|----------|
| `path/to/file1.py` | #1, #3 | High |
| `path/to/file2.py` | #2 | Medium |

---

## LEVER Violations Summary

| Principle | Violations | Impact |
|-----------|------------|--------|
| **L**everage | X | [description] |
| **E**xtend | X | [description] |
| **V**erify | X | [description] |
| **E**liminate | X | [description] |
| **R**educe | X | [description] |
```

## Critical Requirements

1. **Be Specific**: Every issue must have exact file paths, line numbers, and complete code snippets
2. **Actionable**: The AFTER code must be copy-paste ready - no placeholders or "..."
3. **Complete Context**: Include enough surrounding code that the fix location is unambiguous
4. **Prioritized**: Order issues by impact (high-impact optimizations first)
5. **Measurable**: Include line count/complexity metrics for each issue

Think harder: Could this entire PR be achieved by modifying 10-20 lines of existing code instead of adding 100+ new lines? Look for existing patterns that could be reused.

Be a critic - focus on what can be improved, not what's good. Be specific with line numbers and concrete refactoring suggestions.

After creating the report, inform the user:
- Report location: `./pr-review-$ARGUMENTS.md`
- How to apply fixes: "Run an AI agent with this report to implement the suggested changes"
