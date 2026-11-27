#!/usr/bin/env python3
"""Offline verification layer: chain integrity of the S1-S12 network and rubric scenarios for the skills.

  python tests/evals/run_evals.py --chain        every link from user prompt to final review exists and runs:
                                                 manifest == payload, every routing target is a real skill and every
                                                 skill is routable, S1-S12 owners/agents/checks exist, and every
                                                 paper_tools / kb_search / orchestrator command cited in a skill or
                                                 agent file is a real subcommand (checked with -h)
  python tests/evals/run_evals.py --selftest     each scenario's rubric passes its pass.md and fails its fail.md
  python tests/evals/run_evals.py --grade DIR    grade saved answers DIR/<scenario-id>.md (no model is called)

Rubric checks: regex_any, regex_all, regex_none, manual (never auto-passes; reported as needs-manual).
A failed required item fails the scenario. Passing every regex is necessary, not sufficient: it proves an answer
did not trip a known wire, not that it is right. Prints "  PASS <name>" / "  FAIL <name>" lines.
"""
import argparse, json, os, re, subprocess, sys

sys.dont_write_bytecode = True  # importing paper_tools must not leave __pycache__ in payload/
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
CLAUDE = os.path.join(PKG, "payload", ".claude")
ok = True


def chk(c, n):
    global ok
    print(("  PASS " if c else "  FAIL ") + n)
    ok = ok and c


def read(p):
    return open(p, encoding="utf-8-sig").read()


def chain():
    man = json.loads(read(os.path.join(PKG, "tools", "manifest.json")))
    skills, agents = set(man["skills"]), set(man["agents"])
    chk(skills == {d for d in os.listdir(os.path.join(CLAUDE, "skills")) if os.path.isfile(os.path.join(CLAUDE, "skills", d, "SKILL.md"))},
        "manifest skills == payload skill folders (%d)" % len(skills))
    chk(agents == {f[:-3] for f in os.listdir(os.path.join(CLAUDE, "agents")) if f.endswith(".md")},
        "manifest agents == payload agent files (%d)" % len(agents))
    routes = {r["skill"] for r in json.loads(read(os.path.join(CLAUDE, "routing-triggers.json")))["routes"]}
    chk(routes <= skills, "every routing target is a real skill: %s" % sorted(routes - skills))
    chk(skills <= routes, "every skill is reachable from a user prompt: missing %s" % sorted(skills - routes))
    table = read(os.path.join(CLAUDE, "ECONOMICS-RESEARCH.md"))
    named = set(re.findall(r"\x60/([a-z][a-z-]+)\x60", table))
    chk(skills <= named and named <= skills, "routing protocol table lists exactly the manifest skills: %s" % sorted(skills ^ named))
    stages = json.loads(read(os.path.join(CLAUDE, "pipeline-stages.json")))["stages"]
    chk([s["id"] for s in stages] == ["S%d" % i for i in range(1, 13)], "stages S1..S12 contiguous")
    sys.path.insert(0, os.path.join(CLAUDE, "scripts"))
    import paper_tools  # noqa: E402
    for s in stages:
        owners = set(re.findall(r"/([a-z][a-z-]+)", s["owner"]))
        chk(owners <= skills and set(s.get("agents", [])) <= agents and set(s.get("checks", [])) <= set(paper_tools.STAGE_CHECKS),
            "%s %s: owners %s, agents and checks exist" % (s["id"], s["name"], sorted(owners)))
    cited = set()
    for root in (os.path.join(CLAUDE, "skills"), os.path.join(CLAUDE, "agents")):
        for dp, _, fs in os.walk(root):
            for f in fs:
                if f.endswith(".md"):
                    for m in re.finditer(r"(paper_tools|kb_search|orchestrator|wiki_lint)\.py\x60? ([a-z][a-z-]+)(?: ([a-z][a-z-]+))?", read(os.path.join(dp, f))):
                        cited.add(m.groups())
    bad = []
    for script, cmd, sub in sorted(cited, key=str):
        base = [sys.executable, "-X", "utf8", os.path.join(CLAUDE, "scripts", script + ".py"), cmd]
        r = subprocess.run(base + ([sub, "-h"] if sub else ["-h"]), capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0 and sub:  # "<cmd> <word>" where <word> is prose, not a subcommand
            r = subprocess.run(base + ["-h"], capture_output=True, text=True, encoding="utf-8")
            if r.returncode == 0 and re.search(r"\{([^}]*)\}", r.stdout) and sub not in re.search(r"\{([^}]*)\}", r.stdout).group(1).split(","):
                r.returncode = 1
        if r.returncode != 0:
            bad.append(" ".join(x for x in (script, cmd, sub) if x))
    chk(cited and not bad, "%d CLI commands cited in skills/agents all exist: bad %s" % (len(cited), bad))


def grade(sc, text):
    """-> (status, failed_required, open_manual)."""
    failed, manual, partial = [], [], False
    for it in sc["rubric"]:
        kind, pats = it["check"], it.get("patterns", [])
        if kind == "manual":
            manual.append(it["id"])
            continue
        hits = [bool(re.search(p, text)) for p in pats]
        good = any(hits) if kind == "regex_any" else all(hits) if kind == "regex_all" else not any(hits)
        if not good:
            failed.append(it["id"]) if it.get("required") else None
            partial = partial or not it.get("required")
    if failed:
        return "fail", failed, manual
    return ("needs-manual" if manual else "partial" if partial else "pass"), [], manual


def scenarios():
    data = json.loads(read(os.path.join(HERE, "scenarios.json")))
    man = set(json.loads(read(os.path.join(PKG, "tools", "manifest.json")))["skills"])
    for sc in data:
        chk(sc["skill"] in man and any(i.get("required") and i["check"] != "manual" for i in sc["rubric"]),
            "scenario %s targets a real skill and has a required machine check" % sc["id"])
    return data


def selftest():
    for sc in scenarios():
        d = os.path.join(HERE, "fixtures", sc["id"])
        st_pass, _, _ = grade(sc, read(os.path.join(d, "pass.md")))
        st_fail, failed, _ = grade(sc, read(os.path.join(d, "fail.md")))
        chk(st_pass in ("pass", "needs-manual") and st_fail == "fail",
            "%s discriminates (pass.md -> %s, fail.md -> %s %s)" % (sc["id"], st_pass, st_fail, failed))


def grade_dir(path):
    for sc in scenarios():
        f = os.path.join(path, sc["id"] + ".md")
        if not os.path.isfile(f):
            print("  SKIP %s (no answer file)" % sc["id"])
            continue
        st, failed, manual = grade(sc, read(f))
        print("  %s %s%s%s" % ("FAIL" if st == "fail" else "PASS", sc["id"], " failed " + ",".join(failed) if failed else "",
                              " needs-manual " + ",".join(manual) if manual and st != "fail" else ""))


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chain", action="store_true"); ap.add_argument("--selftest", action="store_true"); ap.add_argument("--grade")
    a = ap.parse_args()
    if not (a.chain or a.selftest or a.grade):
        ap.error("choose --chain, --selftest or --grade DIR")
    if a.chain:
        chain()
    if a.selftest:
        selftest()
    if a.grade:
        grade_dir(a.grade)
    print("run_evals: " + ("ALL OK" if ok else "SOME FAILED"))
    sys.exit(0 if ok else 1)
