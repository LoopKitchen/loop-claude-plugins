---
name: share-session
description: >-
  Share a Claude Code session transcript as an interactive HTML page with a public
  URL. Use when the user wants to share, export, or replay a session, or when they
  mention "share session", "session link", or "replay".
argument-hint: "[session_id | path | description] [--local]"
allowed-tools:
  - Bash(ls *)
  - Bash(grep *)
  - Bash(python3 *)
  - Bash(open *)
  - Bash(xargs *)
  - Read
---

Share a Claude Code session transcript as an interactive HTML page. Default behavior uploads to GCS and returns a public URL.

## Argument Parsing

Parse `$ARGUMENTS` to determine the input type:

| Pattern | Meaning | Example |
|---------|---------|---------|
| UUID (hex with dashes) | Session ID — use directly | `a1b2c3d4-...` |
| Path ending in `.jsonl` | Session file path — use directly | `~/.claude/projects/.../foo.jsonl` |
| `--local` | Skip upload, open locally | `--local` |
| Other text | Natural language description — search for matching session | `"the balance dashboard session"` |
| Empty | No args — use most recent session | |

## Step 1: Find the Session

**A) UUID or path** — use directly.

**B) Empty / no args** — find the most recent session:

```bash
PROJECT_DIR=$(echo "$PWD" | sed 's/[\/.]/-/g' | sed 's/^-//')
ls -t ~/.claude/projects/-${PROJECT_DIR}/*.jsonl | head -1
```

**C) Natural language description** — search for a matching session:

1. Extract 2-3 keywords from the description.
2. Search session files for matches:
   ```bash
   PROJECT_DIR=$(echo "$PWD" | sed 's/[\/.]/-/g' | sed 's/^-//')
   grep -l "keyword1" ~/.claude/projects/-${PROJECT_DIR}/*.jsonl | xargs grep -l "keyword2"
   ```
3. For each matching file, show a summary:
   ```bash
   for f in <matched_files>; do
     echo "=== $(basename $f .jsonl) ==="
     echo "Size: $(ls -lh $f | awk '{print $5}')"
     python3 -c "
   import json
   with open('$f') as fh:
       for line in fh:
           d = json.loads(line)
           if d.get('type') == 'user' and not d.get('toolUseResult'):
               msg = d.get('message', {})
               content = msg.get('content', '') if isinstance(msg, dict) else str(msg)
               if '<task-notification>' not in str(content) and '<command-name>' not in str(content):
                   print('First prompt:', str(content)[:200])
                   print('Date:', d.get('timestamp', '')[:10])
                   break
   "
   done
   ```
4. If multiple matches, present options and ask the user to pick. If one clear match, use it.

## Step 2: Generate and Upload

Run the session replayer script at `scripts/session_replayer.py`:

```bash
python3 scripts/session_replayer.py <session_id_or_path> -o /tmp/session_replay.html --upload
```

If `--local` is in `$ARGUMENTS`, skip `--upload` and open locally instead:

```bash
python3 scripts/session_replayer.py <session_id_or_path> -o /tmp/session_replay.html
open /tmp/session_replay.html
```

## Step 3: Report

Return the public URL (or local path if `--local`) to the user.
