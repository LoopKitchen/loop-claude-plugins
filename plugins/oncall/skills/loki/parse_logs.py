#!/usr/bin/env python3
"""Parse Loki JSON response from stdin and format log entries."""
import sys
import json
from datetime import datetime, timezone

raw = sys.stdin.read()
if not raw.strip():
    print("ERROR: Empty response from Loki")
    sys.exit(1)

data = json.loads(raw)

if data.get("status") != "success":
    print(f"Loki query failed: {data}")
    sys.exit(1)

results = data.get("data", {}).get("result", [])
if not results:
    print("No logs found for the given query and time range.")
    sys.exit(0)

entries = []
for stream in results:
    labels = stream.get("stream", {})
    svc = labels.get("service_name", "unknown")
    sev = labels.get("severity", "UNKNOWN")
    for ts_ns, line in stream.get("values", []):
        ts_s = int(ts_ns) / 1e9
        dt = datetime.fromtimestamp(ts_s, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        # Try to parse JSON log lines for structured output
        try:
            log = json.loads(line)
            msg = log.get("message") or log.get("textPayload") or log.get("msg") or line[:500]
            src = log.get("sourceLocation", {})
            src_str = ""
            if src:
                src_str = f' [{src.get("file", "")}:{src.get("line", "")}]'
        except (json.JSONDecodeError, TypeError):
            msg = line[:500]
            src_str = ""
        entries.append((dt, svc, sev, msg, src_str))

# Sort by timestamp descending (most recent first)
entries.sort(key=lambda x: x[0], reverse=True)

print(f"Found {len(entries)} log entries:\n")
for dt, svc, sev, msg, src in entries:
    print(f"[{dt}] [{svc}] [{sev}]{src}")
    print(f"  {msg}")
    print()
