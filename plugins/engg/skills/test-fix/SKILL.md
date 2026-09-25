---
name: test-fix
description: Run pytest and fix failing tests iteratively. Use when the user asks to run tests, debug test failures, or ensure tests pass after code changes.
---

Run pytest with whatever environment the repository's test suite documents (for example a cloud project id exported as an environment variable, `GCP_PROJECT_ID=$GCP_PROJECT`, when the tests talk to Google Cloud). If tests fail, debug the failures by examining error messages and tracing to root causes. Fix the issues and re-run tests until all pass. Update test documentation if logic changes.

Think harder about test failures - are they real bugs or test assumption issues? What is the pattern across multiple failures?
