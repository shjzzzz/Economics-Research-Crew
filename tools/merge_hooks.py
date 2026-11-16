#!/usr/bin/env python3
"""Merge the Crew hook snippet into a Claude Code settings.json, idempotently.

Usage: python merge_hooks.py SETTINGS_JSON SNIPPET_JSON

- Creates SETTINGS_JSON if missing.
- Refuses (exit 1, file untouched) if SETTINGS_JSON is not valid JSON.
- A hook is considered present if some command in the same event already
  references the same script file name; present hooks are never duplicated.
- Preserves every other key. Writes only when something changed.
"""
import json
import os
import re
import sys


def script_names(group):
    names = set()
    for h in group.get("hooks", []):
        m = re.search(r"([\w.-]+\.py)", h.get("command", ""))
        if m:
            names.add(m.group(1))
    return names


def main(settings_path, snippet_path):
    with open(snippet_path, encoding="utf-8-sig") as fh:
        snippet = json.load(fh)
    if os.path.exists(settings_path):
        try:
            with open(settings_path, encoding="utf-8-sig") as fh:
                settings = json.load(fh)
        except ValueError as e:
            sys.stderr.write("settings.json is not valid JSON, left untouched: %s\n" % e)
            return 1
        if not isinstance(settings, dict):
            sys.stderr.write("settings.json top level is not an object, left untouched\n")
            return 1
    else:
        settings = {}
    changed = False
    hooks = settings.setdefault("hooks", {})
    for event, groups in snippet.get("hooks", {}).items():
        existing = hooks.setdefault(event, [])
        have = set()
        for g in existing:
            have |= script_names(g)
        for g in groups:
            if script_names(g) <= have and script_names(g):
                continue
            existing.append(g)
            changed = True
    if changed or not os.path.exists(settings_path):
        os.makedirs(os.path.dirname(os.path.abspath(settings_path)), exist_ok=True)
        with open(settings_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(settings, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("hooks merged into " + settings_path)
    else:
        print("hooks already present; no change")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
