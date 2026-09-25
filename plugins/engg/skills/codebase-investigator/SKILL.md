---
name: codebase-investigator
description: Investigate codebases to find where features are implemented, trace data flows, understand existing patterns, and explain how things work. Use when asked to find code, locate implementations, understand how a feature works, trace the flow of data, or explore unfamiliar parts of the codebase. Triggers on "where is", "how does", "find the code", "trace the flow", "what PR added", "explain the implementation".
---

# Codebase Investigator

## Overview
Expert at navigating and understanding codebases. Can find implementations, trace data flows, identify patterns, and explain how features work with specific file:line references.

## Configuration

This skill reads no environment variables and needs no setup. It works with `grep` (or `rg`), `find`, and `git` against the current working tree.

| Variable | Meaning | Default |
|----------|---------|---------|
| (none) | — | — |

Optional: if a code-graph MCP server is configured in your session (one that indexes a repository and answers caller/callee, path-tracing, or graph-search questions), Strategy 5 below uses it. Nothing has to be set for the skill to fall back to text search.

## When to Use
- "Where is [feature] implemented?"
- "How does [X] work?"
- "Find the code that handles [Y]"
- "Trace the data flow for [process]"
- "What PR added [feature]?"
- "Explain the [module] architecture"
- "Find all usages of [function/class]"

## Investigation Strategies

The examples below use Python globs; swap `--include="*.py"` for `*.go`, `*.ts`, `*.rb`, etc. to match the language you are investigating. Prefer `rg` (ripgrep) over `grep -r` when it is installed — same patterns, faster, and it respects `.gitignore`.

### Strategy 1: Keyword Search (Fast)
Best for: Finding specific functions, classes, or unique strings

```bash
# Find function definitions
grep -r "def function_name" --include="*.py"
grep -r "class ClassName" --include="*.py"

# Find usages
grep -r "function_name(" --include="*.py"
```

### Strategy 2: File Pattern Search (Medium)
Best for: Finding files related to a feature

```bash
# Find files by name pattern
find . -name "*validation*" -type f
find . -name "*payment*" -type f

# Find files containing keyword
grep -l "order_validation" -r --include="*.py"
```

### Strategy 3: Import Tracing (Thorough)
Best for: Understanding dependencies and data flow

1. Find the entry point
2. Read the imports
3. Follow each import to understand the chain
4. Build a dependency map

### Strategy 4: Git History (Historical)
Best for: Understanding why something exists

```bash
# Find commits that touched a file
git log --oneline -- path/to/file.py

# Find PR that added a feature
git log --oneline --grep="feature name"

# See who last modified each line
git blame path/to/file.py
```

### Strategy 5: Code-Graph MCP (Structural, when available)
Best for: "Who calls this?", "What does this call?", impact analysis, dead-code checks

If a code-graph MCP is available in the session, use it before hand-tracing imports:

1. Check that the current repository is indexed (most graph servers expose an index-status or list-projects call; index it if not).
2. Search the graph for the symbol by name to get its canonical node.
3. Ask for callers / callees / a path between two symbols instead of grepping for call sites by hand.
4. Confirm each graph hit by reading the file at the reported line — the graph is a map, the source is the territory.

If no code-graph MCP is configured, Strategies 1-4 cover the same ground; it just takes more hops.

## Instructions

### Step 0: Orient in an Unfamiliar Repository
If you have not worked in this repository before, spend two minutes on layout before searching:

```bash
# Top-level shape
ls
cat README.md | head -80

# Package/workspace manifests reveal the module boundaries
ls go.work go.mod pyproject.toml package.json pnpm-workspace.yaml Cargo.toml 2>/dev/null

# Ownership and docs often map features to directories
cat CODEOWNERS .github/CODEOWNERS 2>/dev/null
ls docs 2>/dev/null
```

Typical monorepo shapes you will meet — treat these as hints, not rules:

```
repo/
├── apps/ or services/     # Deployable services, one directory each
├── packages/ or libs/     # Shared libraries (schemas, utilities, clients)
├── cmd/                   # Go binaries, one main package each
├── workflows/ or jobs/    # Scheduled or orchestrated background work
├── migrations/            # Database schema history
├── scripts/               # One-off and operational scripts
├── infra/ or deploy/      # Infrastructure and deployment configs
└── docs/                  # Design docs, ADRs, runbooks
```

### Step 1: Clarify the Target
Before searching, understand:
- What exactly are we looking for?
- Is it a feature, function, class, or concept?
- What keywords might be used?

### Step 2: Start Broad, Then Narrow
```
1. grep for obvious keywords → find candidate files
2. Read file structure → identify likely locations
3. Read specific functions → understand implementation
4. Trace imports → understand dependencies
```

### Step 3: Document the Trail
As you investigate, note:
- **Entry points**: Where the feature is triggered
- **Core logic**: Where the main work happens
- **Data sources**: Where data comes from
- **Side effects**: What else gets affected

### Step 4: Summarize Findings
Always provide:
- File paths with line numbers (e.g., `src/services/orders/validation.py:142`)
- A brief explanation of what each part does
- How the pieces connect together

## Where to Start, by Question Shape

| You are looking for | Start looking in |
|---------------------|------------------|
| An HTTP/gRPC endpoint | Route registration: `main.py`, `routes.py`, `router.*`, `handlers/`, `*_handler.go`, `controllers/` |
| A background job or workflow | `workflows/`, `jobs/`, `tasks/`, scheduler or cron definitions, queue consumers |
| A data model or table | `models/`, `schemas/`, `migrations/`, ORM definitions, `.proto` / OpenAPI specs |
| A feature flag or config switch | Config loaders, `settings.*`, `config/`, env-var reads (`os.environ`, `os.Getenv`, `process.env`) |
| A CLI command | `cmd/`, `bin/`, `cli.py`, `__main__.py`, argument-parser setup |
| Business rule or validation | Search the domain noun (`order`, `invoice`, `plan`) next to `validate`, `check`, `verify`, `enforce` |
| An integration with an external system | Client wrappers named after the system, `integrations/`, `providers/`, `clients/` |
| Why something exists | `git log --grep`, `git blame`, linked PR/issue, `docs/` and ADRs |

**Cross-cutting patterns worth knowing**:
- **Services** usually own their own entry point, models, and routes in one directory; start there.
- **Shared code** lives in a common package that many services import; when a search returns hits in both a service and a shared package, the shared package is usually the implementation and the service is the caller.
- **Tests** mirror the source tree; the test file next to a module is the fastest documentation of how it is used.

## Output Format

### For "Where is X?" Questions
```
## [Feature Name] Implementation

### Entry Point
- `path/to/file.py:123` - [Brief description]

### Core Logic
- `path/to/core.py:45-89` - [What it does]

### Related Files
- `path/to/helper.py` - [Supporting functionality]
- `path/to/model.py` - [Data models used]

### Data Flow
1. Request comes in at [entry point]
2. Calls [function] which queries [source]
3. Results processed by [logic]
4. Returns [output]
```

### For "How does X work?" Questions
```
## How [Feature] Works

### Overview
[1-2 sentence summary]

### Step-by-Step Flow
1. **Trigger**: [What starts the process]
2. **Input**: [What data is needed]
3. **Processing**: [What happens to the data]
4. **Output**: [What gets returned/saved]

### Key Files
- `file1.py:100` - [Purpose]
- `file2.py:50` - [Purpose]

### Diagram
[ASCII diagram if helpful]
```

## Example Investigation

**User**: "Where is order validation implemented?"

**Investigation**:
1. Search: `grep -r "order_validation\|validate_order" --include="*.py"`
2. Find: candidate files under `services/orders/` and a shared `packages/schemas/` hit
3. Read: the route that calls the validator, then the validator itself
4. Trace: Imports and dependencies (which models, which data sources)

**Response**:
```
## Order Validation Implementation

### Entry Point
- `services/orders/routes.py:88` - `POST /orders/{id}/validate` endpoint

### Core Logic
- `services/orders/validation.py:41-130` - `validate_order()`
  - Checks: line items match catalog, dates within fulfilment window, total within credit limit

### Data Sources
- `services/orders/models.py`
  - `Order` model - Order definition (Postgres via the ORM)
- `packages/schemas/catalog.py`
  - `CatalogItem` schema - shared with the catalog service
- Warehouse tables: `orders`, `catalog_snapshot` (read through the analytics client)

### Data Flow
1. API request triggers validation
2. Service fetches the order from Postgres and the catalog snapshot from the warehouse
3. Compares order line items against the catalog and the customer's credit limit
4. Returns validation result with a list of errors
```

## Tips

1. **Start with obvious names**: Most code uses descriptive names
2. **Check tests**: Test files often show how things are used
3. **Read docstrings**: Good code has documentation
4. **Use git blame**: Find who wrote it and the PR context
5. **Look for config**: Feature flags and configs reveal entry points
6. **Ask the graph first, then read**: When a code-graph MCP is available, use it for callers/callees and confirm by reading the source
