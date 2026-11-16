#!/usr/bin/env python3
"""PreToolUse hook: protect immutable raw material.

Blocks (exit 2) modification of anything under 06-Data/raw and
03-Literature/_sources. Creating a NEW file via Write is allowed (importing
new raw material); overwriting/editing/deleting existing files is blocked.

Limits (be honest): Write/Edit/MultiEdit/NotebookEdit are checked exactly.
Bash is checked heuristically (destructive verbs, redirects, copy-to-dest
that mention a protected path); it cannot catch every shell construct.
Fails open (exit 0) on malformed hook input.
"""
import json
import os
import re
import sys

PROTECTED = ["06-data/raw", "03-literature/_sources"]
FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
DESTRUCTIVE = re.compile(
    r"(?i)(?:^|[\s;&|(])(rm|rmdir|mv|move|del|erase|ren|rename|truncate|shred|"
    r"remove-item|move-item|rename-item|set-content|add-content|clear-content|out-file|tee)\b"
    r"|sed\s+-[a-z]*i"
)
COPYLIKE = re.compile(r"(?i)(?:^|[\s;&|(])(cp|copy|xcopy|robocopy|copy-item)\b")
REDIRECT = re.compile(r"(?:^|[^<\d])>>?\s*[\"']?([^\s\"'|;&]+)")


def norm(p):
    return p.replace("\\", "/").lower()


def is_protected(path):
    n = norm(path)
    return any(("/" + pr + "/") in ("/" + n + "/") or n.startswith(pr + "/") or n.endswith("/" + pr)
               or ("/" + pr + "/") in n for pr in PROTECTED)


def block(msg):
    sys.stderr.write("BLOCKED by protect_raw hook: " + msg + "\n")
    sys.exit(2)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    cwd = data.get("cwd") or os.getcwd()

    if tool in FILE_TOOLS:
        fp = ti.get("file_path") or ti.get("notebook_path") or ""
        if not fp:
            sys.exit(0)
        absp = os.path.normpath(fp if os.path.isabs(fp) else os.path.join(cwd, fp))
        if is_protected(absp):
            if tool == "Write" and not os.path.exists(absp):
                sys.exit(0)
            block("%s targets immutable raw material (%s). Raw data/sources are read-only; "
                  "write derived output to 06-Data/processed or a note instead." % (tool, fp))
        sys.exit(0)

    if tool == "Bash":
        cmd = ti.get("command", "") or ""
        n = norm(cmd)
        if not any(pr in n for pr in PROTECTED):
            sys.exit(0)
        if DESTRUCTIVE.search(cmd):
            # only block when a protected path is part of the same command
            block("command appears to modify/delete files and mentions a protected raw path.")
        for m in REDIRECT.finditer(cmd):
            if is_protected(m.group(1)):
                block("shell redirect writes into a protected raw path.")
        if COPYLIKE.search(cmd):
            tokens = cmd.strip().split()
            if tokens and is_protected(tokens[-1].strip("\"'")):
                block("copy destination is a protected raw path.")
    sys.exit(0)


if __name__ == "__main__":
    main()
