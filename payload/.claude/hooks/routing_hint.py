#!/usr/bin/env python3
"""UserPromptSubmit hook: deterministic routing hint.

Matches the user's prompt against .claude/routing-triggers.json and, when an
intent matches, prints a one-paragraph hint that Claude Code adds to the
context ("this request maps to /skill; invoke it first"). It never blocks.

- Prompts that already start with "/" (explicit command) get no hint.
- No match -> no output (conceptual questions are answered directly).
- Fails open (exit 0, no output) on any error.
"""
import json
import os
import re
import sys


def load_routes():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.dirname(here), "routing-triggers.json")
    with open(path, encoding="utf-8-sig") as fh:
        return json.load(fh).get("routes", [])


def match(prompt, routes):
    hits = []
    for r in routes:
        for pat in r.get("patterns", []):
            m = re.search(pat, prompt, re.IGNORECASE)
            if m:
                hits.append((r["skill"], m.group(0)))
                break
    return hits


def main():
    try:
        data = json.load(sys.stdin)
        prompt = (data.get("prompt") or "").strip()
        if not prompt or prompt.startswith("/"):
            return 0
        hits = match(prompt, load_routes())
    except Exception:
        return 0
    if not hits:
        return 0
    primary, trigger = hits[0]
    others = [h[0] for h in hits[1:]]
    msg = ("[routing] 本请求匹配项目 Skill `/%s`（触发词：%s）。按 CLAUDE.md 路由规则：先用 Skill 工具调用 `%s`，"
           "再按它的步骤执行；不要在主会话里自行完成该流程。" % (primary, trigger, primary))
    if others:
        msg += "该 Skill 执行中可能还涉及：%s（按需在流程内调用，不要同时启动）。" % "、".join("/" + o for o in others)
    msg += "若请求其实只是概念性短问题，可直接回答。"
    sys.stdout.write(msg + "\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
