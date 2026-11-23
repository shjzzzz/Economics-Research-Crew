#!/usr/bin/env python3
"""SubagentStart / SubagentStop hook: record sub-agent lifecycle in Meta/run-ledger.jsonl.

Never blocks and never prints; fails open. The ledger stores ids, agent type, project/stage and the
size of the final message, not its content.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8-sig", "replace"))
        import orchestrator as orc
        vault = orc.find_vault(data.get("cwd"))
        if not vault:
            return
        ev = {"SubagentStart": "start", "SubagentStop": "stop"}.get(data.get("hook_event_name"))
        if not ev:
            return
        ap = orc.active_project(vault)
        extra = {}
        if ev == "stop":
            extra["final_chars"] = len(data.get("last_assistant_message") or "")
            aid = data.get("agent_id")
            if aid:
                for prev in reversed(orc.ledger_read(vault)):
                    if prev.get("event") == "start" and prev.get("agent_id") == aid and prev.get("ts"):
                        try:
                            t0 = datetime.datetime.fromisoformat(prev["ts"])
                            t1 = datetime.datetime.now().astimezone()
                            extra["duration_ms"] = max(0, int((t1 - t0).total_seconds() * 1000))
                        except ValueError:
                            pass
                        break
        orc.ledger_append(vault, ev, agent=data.get("agent_type"), agent_id=data.get("agent_id"),
                          project=ap[1]["project"] if ap else None, stage=ap[1]["stage"] if ap else None, **extra)
    except Exception:
        return


if __name__ == "__main__":
    main()
    sys.exit(0)
