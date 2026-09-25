# Contributing

Thanks for helping improve these plugins. This file covers the repository
layout, the checks every change must pass, and how to add a skill.

## Layout

```
.claude-plugin/marketplace.json            # marketplace "loop-plugins": lists the plugins below
plugins/<plugin>/.claude-plugin/plugin.json # plugin manifest: name, description, version, license, keywords
plugins/<plugin>/README.md                  # what the plugin's skills do and the variables they read
plugins/<plugin>/skills/<skill>/SKILL.md    # the skill (frontmatter + procedure)
plugins/<plugin>/skills/<skill>/references/ # optional supporting docs the skill loads
plugins/<plugin>/skills/<skill>/*.py|*.sh   # optional helper scripts
plugins/<plugin>/skills/<skill>/*.example.* # optional config templates users copy and fill in
plugins/<plugin>/agents/<agent>.md          # optional subagents
.github/scripts/skill-lint.sh               # static lint (secrets, absolute paths, frontmatter, script syntax)
.github/scripts/identifier-gate.sh          # internal-identifier gate
.github/workflows/                          # CI: skill-lint and identifier-gate
```

## SKILL.md conventions

- Frontmatter must have `name:` and `description:`; `argument-hint:` and
  `allowed-tools:` are optional. Do not add a `version:` key (versions live in
  `plugin.json`). The description is what makes the skill trigger, so include
  the phrases a user would say.
- Add a **Configuration** section near the top that lists every variable the
  skill reads, one line each, with its meaning and default. Use the shared
  names from the root README's configuration table; do not invent parallel
  names for the same thing. Mark Linear as optional and skip it when
  `LINEAR_API_KEY` is unset.
- Reference bundled scripts and files through the plugin root:
  `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/<file>`. Never use absolute paths, a
  home directory, or a path into another repository.
- Config that users must fill in ships as `<name>.example.<ext>` with
  placeholder values; the skill reads the real file from a variable with the
  example file's location as the documented default.
- List only tools that exist in a standard Claude Code install (or the MCP
  servers the README names) under `allowed-tools`.
- Keep the procedure portable: prefer `python3 -c` for date arithmetic over
  GNU- or BSD-only `date` flags, and `gh` over raw GitHub API calls where it
  reads the same.

## No internal identifiers

This is a public mirror of an internal toolset. Nothing that identifies a
specific company's infrastructure, people or customers may be committed:

- cloud project ids and numbers, Sentry org slugs, PostHog / Vercel /
  Cloudflare project ids
- chat channel, user or group ids (`C0...`, `U0...`, `S0...`)
- internal hostnames, IP addresses, `nip.io` / `sslip.io` hosts
- private repository names
- employee or customer names and email addresses (other than the two contact
  addresses in `marketplace.json` and `SECURITY.md`)
- tokens, keys or credentials of any kind, including "expired" ones

Use the configuration variables instead, and `example.com` / `acme` style
placeholders in examples.

Two checks enforce this and run in CI on every pull request and push to
`main`:

```bash
bash .github/scripts/skill-lint.sh                       # every file under plugins/
bash .github/scripts/skill-lint.sh plugins/oncall/skills/loki/SKILL.md   # one file
bash .github/scripts/identifier-gate.sh                  # whole tree
```

`skill-lint.sh` blocks embedded credentials, non-portable absolute paths,
malformed frontmatter, and Python or shell scripts that do not compile.
`identifier-gate.sh` greps for the shape of internal identifiers (chat ids,
home-directory paths, org-scoped hosts, project-id-looking strings, email
addresses outside `example.com`). In this repository's own CI the gate also
runs an extended, non-public pattern supplied through the
`IDENTIFIER_GATE_PATTERNS` repository secret; pull requests from forks run
the generic pattern only, and a maintainer re-runs the full gate before
merging. Both scripts exit non-zero on a hit and print the file and line.

## Adding a skill

1. Pick the plugin (`oncall` for incident and observability work, `engg` for
   development workflow, `platform-engineer` for orchestration) or propose a
   new one in an issue first.
2. Create `plugins/<plugin>/skills/<skill>/SKILL.md` following the
   conventions above. Put helper scripts and reference docs next to it.
3. Add a one-line entry to `plugins/<plugin>/README.md` and to the plugin
   table in the root `README.md`. If the skill reads a new variable, add it
   to both configuration tables with its meaning and default.
4. Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json`
   (patch for fixes, minor for a new skill).
5. Run both scripts locally, then test the skill from a clean install:

   ```bash
   claude plugin marketplace add ./            # from the repo root
   claude plugin install <plugin>@loop-plugins
   ```

6. Open a pull request. Describe what the skill does, what it reads, and
   what you ran to verify it. Keep unrelated changes out.

## Editing an existing skill

Keep the procedure intact unless the change is the point. Skills are read by
a model, so wording matters: state steps as instructions, keep decision
tables explicit, and prefer one clear path over several optional ones.
