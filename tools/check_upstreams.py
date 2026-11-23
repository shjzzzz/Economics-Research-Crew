#!/usr/bin/env python3
"""Multi-upstream update tracker for Economics Research Crew (ERC).

Pure standard library, zero LLM quota. Runs the same adaptive check as
check_ars_updates.py over every tracked upstream and emits one design-pattern
adoption brief. Detection only: adopting a change is always a reviewed, native
rewrite (see each manifest's license and policy fields).

Tracked upstreams:
  ars                    payload/Meta/upstream-ars.json            (CC-BY-NC-4.0)
  paper-orchestra        tools/upstreams/paper-orchestra.json      (Apache-2.0)
  obsidian-second-brain  tools/upstreams/obsidian-second-brain.json (MIT)
  research-superpowers   tools/upstreams/research-superpowers.json  (MIT)
  (any extra tools/upstreams/*.json is picked up automatically)

Usage:
  python tools/check_upstreams.py list
  python tools/check_upstreams.py check [--repo NAME] [--mock JSON] [--out FILE] [--json]
  python tools/check_upstreams.py mark-audited --repo NAME --sha SHA [--tag TAG] [--note TEXT]

Exit codes:
  0  every checked upstream is up to date (or mark-audited succeeded)
  1  a fetch failed and nothing else was found (transient; do not open an issue)
  2  at least one upstream has updates (brief emitted)
"""
import argparse
import glob
import json
import os
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_ars_updates as cau  # noqa: E402

ROOT = os.path.dirname(HERE)
ARS_MANIFEST = os.path.join(ROOT, "payload", "Meta", "upstream-ars.json")
EXTRA_DIR = os.path.join(HERE, "upstreams")


def manifests():
    out = {"ars": ARS_MANIFEST}
    for p in sorted(glob.glob(os.path.join(EXTRA_DIR, "*.json"))):
        out[os.path.splitext(os.path.basename(p))[0]] = p
    return out


def pick(repo):
    allm = manifests()
    if not repo:
        return allm
    if repo not in allm:
        sys.exit("未知上游 %r；可选：%s" % (repo, ", ".join(sorted(allm))))
    return {repo: allm[repo]}


def cmd_list(a):
    for name, path in manifests().items():
        m = cau.load_json(path)
        print("%-22s %-14s 基线 %s %s  %s" % (name, m.get("license", ""), m.get("last_audited_tag") or "-",
                                             m.get("last_audited_sha", "")[:8], m["repo"]))
    return 0


def cmd_check(a):
    chosen = pick(a.repo)
    if a.mock and len(chosen) != 1:
        sys.exit("--mock 只能与 --repo 同用")
    results, briefs, errors = {}, [], {}
    for name, path in chosen.items():
        m = cau.load_json(path)
        try:
            res, md = cau.evaluate(m, a.mock)
        except SystemExit as exc:  # fetch_upstream exits on network errors
            errors[name] = str(exc)
            continue
        results[name] = res
        if md:
            briefs.append(md)
    any_updates = bool(briefs)
    if briefs and errors:
        briefs.append("## 抓取失败的上游（本次未检查）\n" + "\n".join("- `%s`：%s" % (n, msg) for n, msg in errors.items()))
    if a.out and briefs:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n\n---\n\n".join(briefs))
    if a.json:
        print(json.dumps({"any_updates": any_updates, "upstreams": results, "errors": errors},
                         ensure_ascii=False, indent=2))
    else:
        for name, res in results.items():
            if res["up_to_date"]:
                print("已是最新：%s（基线 %s %s）" % (name, res["baseline_tag"] or "-", res["baseline_sha"][:8]))
        if briefs:
            print("\n\n---\n\n".join(briefs))
        for name, msg in errors.items():
            print("获取失败：%s：%s" % (name, msg), file=sys.stderr)
    if any_updates:
        return 2
    return 1 if errors else 0


def cmd_mark(a):
    path = pick(a.repo)[a.repo]
    return cau.cmd_mark(SimpleNamespace(manifest=path, tag=a.tag, sha=a.sha, note=a.note))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("list")
    pl.set_defaults(f=cmd_list)
    pc = sub.add_parser("check")
    pc.add_argument("--repo", help="check one upstream by name; default is all")
    pc.add_argument("--mock", help="Offline JSON fixture with {releases:[], commits:[]} (needs --repo)")
    pc.add_argument("--out", help="Write the combined Markdown brief to this path")
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(f=cmd_check)
    pm = sub.add_parser("mark-audited")
    pm.add_argument("--repo", required=True)
    pm.add_argument("--sha", required=True)
    pm.add_argument("--tag", default=None, help="release tag; omit for upstreams without releases")
    pm.add_argument("--note")
    pm.set_defaults(f=cmd_mark)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8")
    sys.exit(main())
