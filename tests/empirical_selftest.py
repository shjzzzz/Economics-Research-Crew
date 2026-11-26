#!/usr/bin/env python3
"""Offline self-test for the empirical line of paper_tools.py (spec ledger, log-point conversion, polish fidelity,
replication package, stage checks specs_logged / package_ready).

Usage: python empirical_selftest.py <path-to-paper_tools.py>
Builds a throw-away vault, prints "  PASS <name>" / "  FAIL <name>" lines (parsed by tests/run.ps1).
Exit 0 only if every check passes. No network, no models.
"""
import json, os, shutil, subprocess, sys, tempfile, zipfile
pt = os.path.abspath(sys.argv[1])
v = tempfile.mkdtemp(prefix="emptest-")
proj = "01-Research-Projects/demo"


def w(rel, text):
    p = os.path.join(v, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(text)
    return p


def run(*a):
    r = subprocess.run([sys.executable, "-X", "utf8", pt, "--vault", v] + list(a), capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout + r.stderr


ok = True


def chk(c, n):
    global ok
    print(("  PASS " if c else "  FAIL ") + n)
    ok = ok and c


os.makedirs(os.path.join(v, "Meta"))
code = w(proj + "/replication/code/03_main.do", "reghdfe y d, absorb(id)\n")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(pt))
import paper_tools as P  # noqa: E402

chk(P.stage_check(v, "specs_logged", []) != [], "specs_logged blocks while the spec ledger is empty")
rc, out = run("spec", "log", "--id", "d.s1", "--purpose", "baseline", "--planned", "--estimate", "0.25", "--p", "0.01",
              "--script", proj + "/replication/code/03_main.do")
chk(rc == 0, "spec log baseline")
for i in range(2, 7):
    run("spec", "log", "--id", "d.s%d" % i, "--purpose", "exploration", "--p", "0.02" if i == 2 else "0.5")
rc, out = run("results", "register", "--id", "t2.b", "--value", "0.25", "--spec", "d.s1", "--source", proj + "/replication/code/03_main.do")
chk(rc == 0, "results register --spec links a number to its specification")
rc, out = run("results", "register", "--id", "t2.x", "--value", "1", "--spec", "nope")
chk(rc != 0, "results register refuses an unknown spec")
run("results", "register", "--id", "t2.c", "--value", "0.1", "--spec", "d.s2", "--no-source-reason", "test")
rc, out = run("spec", "summary", "--json")
j = json.loads(out[:out.rindex("}") + 1])
chk(j["logged"] == 6 and j["reported"] == 2 and j["reported_unplanned"] == ["d.s2"], "spec summary: tried 6, reported 2, unplanned d.s2")
chk(any("选择性报告" in x for x in j["warnings"]), "spec summary raises the selective-reporting signal")
chk(P.stage_check(v, "specs_logged", []) == [], "specs_logged passes once specs are logged")

d = w(proj + "/paper/draft.md", "税收增加 {{res:t2.b}}，即 25%。\n\n换算为 {{res:t2.b:pct}}%。\n")
rc, out = run("results", "check", d)
chk("28.4" in out and "{{res:t2.b:pct}}" in out, "results check catches a log point written as a percentage")
rc, out = run("results", "render", d, "-o", os.path.join(v, "r.md"))
chk("换算为 28.4%" in open(os.path.join(v, "r.md"), encoding="utf-8").read(), "{{res:id:pct}} renders (e^b-1)*100")

a = w("a.md", "改革可能提高了税收 {{res:t2.b}}，但并非所有地区都不显著。This may not hold.\n")
b = w("b.md", "改革证明提高了税收 {{res:t2.b}}，但并非所有地区都显著。This clearly holds.\n")
c = w("c.md", "改革或许提高了税收 {{res:t2.b}}，但并非所有地区都不显著。This may not hold.\n")
rc, out = run("polish", "check", "--before", a, "--after", b)
chk(rc != 0 and "否定词" in out and "语气变强" in out, "polish check fails on a dropped negation and warns on stronger tone")
rc, out = run("polish", "check", "--before", a, "--after", c)
chk(rc == 0, "polish check passes a meaning-preserving rewrite")

chk(any("README" in e for e in P.stage_check(v, "package_ready", [], project="demo")), "package_ready blocks without README")
w(proj + "/replication/README.md", "# R\n## 数据可得性\n保密\n## 计算环境\nStata 18\n## 运行说明\nrun main.do\n")
rc, out = run("package", "check", os.path.join(v, proj, "replication"))
chk(rc != 0 and "表图对照" in out and "主脚本" in out, "package check lists the missing section and master script")
w(proj + "/replication/README.md", "# R\n## 数据可得性\n保密\n## 计算环境\nStata 18\n## 运行说明\nrun main.do\n## 表图对照\n表1 03_main\n")
w(proj + "/replication/main.do", 'do "code/03_main.do"\ncd "C:\\Users\\me"\n')
w(proj + "/replication/notes.md", "zero\u200bwidth\n")
docx = os.path.join(v, proj, "replication", "paper.docx")
with zipfile.ZipFile(docx, "w") as z:
    z.writestr("docProps/core.xml", "<cp:coreProperties><dc:creator>Zhou</dc:creator><cp:lastModifiedBy>Zhou</cp:lastModifiedBy></cp:coreProperties>")
    z.writestr("word/document.xml", "<w:document/>")
rc, out = run("package", "check", os.path.join(v, proj, "replication"))
chk(rc == 0 and "绝对路径" in out and "隐藏字符" in out and "Zhou" in out, "package check passes with warnings for paths, hidden characters, author metadata")
rc, out = run("package", "check", os.path.join(v, proj, "replication"), "--fix")
core = zipfile.ZipFile(docx).read("docProps/core.xml").decode()
chk("Zhou" not in core and "\u200b" not in open(os.path.join(v, proj, "replication", "notes.md"), encoding="utf-8").read(),
    "package check --fix strips hidden characters and Office author fields")
chk(P.stage_check(v, "package_ready", [], project="demo") == [], "package_ready passes")

shutil.rmtree(v, ignore_errors=True)
print("empirical selftest: " + ("ALL OK" if ok else "SOME FAILED"))
sys.exit(0 if ok else 1)
