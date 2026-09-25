---
name: test-fix
description: Run pytest and fix failing tests iteratively. Use when the user asks to run tests, debug test failures, or ensure tests pass after code changes.
---

## Configuration

This skill reads no environment variables of its own; export whatever the repository's test docs require before running it.

Run pytest with whatever environment the repository's test suite documents. If tests fail, debug the failures by examining error messages and tracing to root causes. Fix the issues and re-run tests until all pass. Update test documentation if logic changes.

Think harder about test failures - are they real bugs or test assumption issues? What is the pattern across multiple failures?
