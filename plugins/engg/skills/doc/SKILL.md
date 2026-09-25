---
name: doc
description: Search the codebase and create comprehensive documentation as a GitHub issue. Use when the user wants to understand, trace, and document a system feature, module, or architectural pattern as an engineering design doc.
---

## Arguments

- `$ARGUMENTS` — Search query or topic to document (e.g., `order validation flow`, `notification delivery pipeline`)

## Configuration

This skill reads no environment variables and needs no setup beyond an authenticated `gh`.

Search for files and logic related to the user's query. Trace through dependencies and implementations. Create comprehensive documentation including: architecture overview, data flows, corner cases, business logic, and assumptions. Include a tests2write.md section if applicable. Use code references like file_path:line_number.

Key locations: start from the repository's README, `CLAUDE.md` / `AGENTS.md`, and top-level directory layout (services, shared packages, data models, migrations) to find where the topic lives; `/codebase-investigator` helps when the entry point is not obvious.

Ultrathink about the full system architecture and create a GitHub issue using gh issue create with the plan as an engineering design doc. Output the issue URL at the end.
