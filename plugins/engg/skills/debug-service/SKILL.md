---
name: debug-service
description: Debug why a local development service isn't starting or responding. Use when a service fails to launch, shows port conflicts, import errors, missing dependencies, or configuration problems.
---

Debug why the service isn't running. Check for: poetry environment issues, port conflicts (8080/8000), missing dependencies, import errors, or configuration problems. Look at error logs carefully. Fix any issues found and get the service running.

Service locations: the repository's README or `CLAUDE.md` names the service directories and how each one is started (`make`, `poetry run`, `uv run`, `npm run dev`, `go run`); `poetry env info --path` / `uv venv` locate the virtual environment when the service is Python.

Think harder about the error messages - what is the root cause versus symptoms? Are there cascading failures?
