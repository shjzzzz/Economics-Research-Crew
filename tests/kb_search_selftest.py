#!/usr/bin/env python3
"""Offline self-test for payload/.claude/scripts/kb_search.py.

Usage: python kb_search_selftest.py <path-to-kb_search.py>
Builds a throw-away vault in the temp dir, runs index/search/stats through the CLI and prints
"  PASS <name>" / "  FAIL <name>" lines (parsed by tests/run.ps1). Exit 0 only if every check passes.
No network, no models.
"""
import os, sys, json, subprocess, tempfile, shutil
kb = sys.argv[1]
v = tempfile.mkdtemp(prefix="kbtest-")
def w(rel, text):
    p = os.path.join(v, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(text)
w("03-Literature/smith2020.md", "---\ntype: literature\ncite_key: smith2020\ntitle: Tax Compliance and Audit Threats\nauthors: [Smith, Jones]\nyear: 2020\nkeywords: [tax compliance, 纳税遵从]\nverification: verified\n---\n# 研究问题\n本文研究税收遵从度与稽查威慑的关系，使用双重差分设计。\n\n## Identification\nWe use staggered DID. See [[chen2018]].\n\n"+("填充文字。\n"*10))
w("03-Literature/chen2018.md", "---\ntype: literature\ncite_key: chen2018\ntitle: 增值税改革与企业投资\nyear: 2018\nclaim_scope: 独特样本口径甲乙\nverification: unverified\n---\n# 摘要\n增值税转型显著提高了企业投资，识别策略为断点回归。 back to [[smith2020]]\n")
w("04-Theories/mech.md", "---\ntype: theory\ntitle: Deterrence mechanism\n---\n# Mechanism\nAudit probability raises compliance. See [[smith2020]].\n")
w("旧税法笔记.md", "增值税暂行条例 legacy note\n")
w("03-Literature/_sources/raw.md", "raw source about 稽查威慑\n")
w("06-Data/raw/x.md", "稽查威慑 should not be indexed\n")
w(".claude/skills/a.md", "稽查威慑 hidden\n")
w("Meta/aliases.csv", "canonical,alias\n纳税遵从,tax compliance\n税收遵从,纳税遵从\n")
def run(*a):
    r = subprocess.run([sys.executable, "-X", "utf8", kb] + list(a) + ["--vault", v], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr
ok = True
def chk(c, n):
    global ok
    print(("  PASS " if c else "  FAIL ") + n); ok = ok and c
rc, out, err = run("index"); chk(rc == 0 and "indexed 5" in out, "index first run: " + out.strip())
rc, out, err = run("index"); chk("indexed 0, unchanged 5" in out, "incremental no-op: " + out.strip())
rc, out, _ = run("search", "遵从"); j = json.loads(out)
chk(rc == 0 and any(h["cite_key"] == "smith2020" for h in j["hits"]), "2-char CJK hit")
chk(all(h["path"] != "旧税法笔记.md" for h in j["hits"]), "legacy not in default scope")
rc, out, _ = run("search", "tax", "compliance"); j = json.loads(out)
chk(j["hits"] and j["hits"][0]["cite_key"] == "smith2020", "english hit ranks smith2020 first")
rc, out, _ = run("search", "样本口径"); j = json.loads(out)
chk(any(h["cite_key"] == "chen2018" and h["heading_path"] == "(frontmatter)" for h in j["hits"]), "claim_scope in frontmatter is searchable")
rc, out, _ = run("search", "纳税遵从"); j = json.loads(out)
chk(any(h["cite_key"] == "smith2020" for h in j["hits"]) and "tax compliance" in j["expanded"], "alias expansion zh->en: " + str(j["expanded"]))
rc, out, _ = run("search", "稽查威慑"); j = json.loads(out)
paths = [h["path"] for h in j["hits"]]
chk("06-Data/raw/x.md" not in paths and ".claude/skills/a.md" not in paths and "03-Literature/_sources/raw.md" not in paths, "excluded dirs / raw tier not returned: " + str(paths))
rc, out, _ = run("search", "稽查威慑", "--scope", "all"); j = json.loads(out)
paths = [h["path"] for h in j["hits"]]
chk("03-Literature/_sources/raw.md" in paths and "06-Data/raw/x.md" not in paths, "scope all includes raw, still excludes 06-Data")
rc, out, _ = run("search", "增值税", "--scope", "legacy"); j = json.loads(out)
chk(any(h["path"] == "旧税法笔记.md" for h in j["hits"]), "scope legacy finds root note")
h = j["hits"][0]
chk(all(k in h for k in ("cite_key","path","heading_path","line_start","line_end","score","verification","snippet","tier")), "anchor fields present")
rc, out, _ = run("search", "断点回归", "--year", "2015-2019"); j = json.loads(out)
chk(len(j["hits"]) == 1 and j["hits"][0]["cite_key"] == "chen2018", "year filter keeps 2018")
rc, out, _ = run("search", "断点回归", "--year", "2020"); j = json.loads(out)
chk(j["hits"] == [] and j.get("note") == "no match", "year filter excludes -> no match note")
rc, out, _ = run("search", "断点回归", "--type", "theory"); j = json.loads(out)
chk(j["hits"] == [], "type filter")
rc, out, _ = run("search", "断点回归", "--expand-links", "1"); j = json.loads(out)
links = [h for h in j["hits"] if h["via"] == "link"]
chk(any(h["cite_key"] == "smith2020" for h in links), "expand-links adds neighbour: " + str([h["path"] for h in links]))
rc, out, _ = run("search", "遵从", "火星", "殖民"); j = json.loads(out)
chk(j["hits"] and j["hits"][0]["coverage"] < 0.5 and j.get("note", "").startswith("weak match"), "partial match reports low coverage and a weak-match note")
rc, out, _ = run("search", "税收遵从", "稽查威慑"); j = json.loads(out)
chk(j["hits"] and j["hits"][0]["coverage"] == 1.0 and "note" not in j, "full match has coverage 1.0 and no note")
rc, out, _ = run("search", "完全不存在的词语"); j = json.loads(out)
chk(rc == 0 and j["hits"] == [] and j["note"] == "no match", "no match output")
rc, out, _ = run("search", "Callaway Sant'Anna Wooldridge" ); chk(rc == 0, "odd query does not crash")
rc, out, _ = run("search", '"staggered DID"', "--mode", "all"); j = json.loads(out); chk(len(j["hits"]) >= 1, "quoted phrase")
v2 = tempfile.mkdtemp(prefix="kbtest2-")
os.makedirs(os.path.join(v2, "03-Literature"))
for i in range(30):
    open(os.path.join(v2, "03-Literature", "n%d.md" % i), "w", encoding="utf-8").write("# t%d\n共同词汇 并发测试 %d\n" % (i, i))
procs = [subprocess.Popen([sys.executable, "-X", "utf8", kb, "search", "并发测试", "--vault", v2], stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(4)]
res = [(p.communicate(), p.returncode) for p in procs]
chk(all(rc == 0 and json.loads(o.decode("utf-8"))["total"] > 0 for (o, e), rc in res), "4 concurrent first-time searches all succeed")
out5 = subprocess.run([sys.executable, "-X", "utf8", kb, "search", "并发测试", "--vault", v2, "--limit", "5"], capture_output=True, text=True, encoding="utf-8").stdout
chk(len({h["path"] for h in json.loads(out5)["hits"]}) == 5, "--limit counts documents, not chunks")
shutil.rmtree(v2, ignore_errors=True)
w("02-Areas/fresh.md", "---\ntype: area\n---\n# 新页\n独特词汇甲乙丙丁。\n")
rc, out, _ = run("search", "甲乙丙丁"); j = json.loads(out)
chk(any(h["path"] == "02-Areas/fresh.md" for h in j["hits"]), "search sees a new note without a separate index run")
os.remove(os.path.join(v, "02-Areas/fresh.md"))
run("index")
# incremental: change one file
w("03-Literature/chen2018.md", "---\ntype: literature\ncite_key: chen2018\nyear: 2018\n---\n# 摘要\n全新内容 工具变量。\n")
rc, out, _ = run("index"); chk("indexed 1, unchanged 4" in out, "changed file re-indexed only: " + out.strip())
rc, out, _ = run("search", "断点回归"); chk(json.loads(out)["hits"] == [], "old content gone after reindex")
os.remove(os.path.join(v, "04-Theories/mech.md"))
rc, out, _ = run("index"); chk("removed 1" in out, "deleted file removed: " + out.strip())
rc, out, _ = run("stats"); s = json.loads(out); chk(s["docs"] == 4 and "wiki" in s["by_tier"], "stats")
chk(os.path.exists(os.path.join(v, ".erc-index", ".gitignore")), ".erc-index/.gitignore written")
w("Meta/spec-ledger.json", json.dumps({"version": 1, "entries": {"p.s1": {"id": "p.s1", "purpose": "baseline", "outcome": "ln_vat", "treatment": "merger"}}}))
rc, out, _ = run("search", "ln_vat", "--scope", "meta"); j = json.loads(out)
chk(any(h["path"] == "Meta/spec-ledger.json" and h["heading_path"] == "p.s1" for h in j["hits"]), "spec ledger indexed one section per entry")
q = os.path.join(v, "qrels.json")
open(q, "w", encoding="utf-8").write(json.dumps([
    {"q": "稽查威慑", "expect": ["smith2020"]},
    {"q": "tax compliance", "expect": ["smith2020"]},
    {"q": "火星殖民", "expect": ["smith2020"]},
    {"q": "完全不存在的外星税制", "expect": [], "trap": True},
    {"q": "遵从 火星 殖民", "expect": [], "trap": True},
], ensure_ascii=False))
rc, out, _ = run("eval", q, "--k", "1,5"); j = json.loads(out)
chk(rc == 0 and j["cases"] == 3 and j["recall"]["@5"] == 0.667 and j["misses"] == ["火星殖民"], "eval: recall@5 = 2/3 and the miss is listed")
chk(j.get("trap_cases") == 2 and j.get("trap_refused") == 2 and j.get("trap_refusal_rate") == 1.0, "eval: trap cases refused (no match + weak match)")
w("MOC/tax-moc.md", "---\ntype: moc\ntitle: 税收遵从总览\n---\n# MOC\n[[smith2020]] [[chen2018]]\n")
rc, out, _ = run("orient", "纳税遵从", "工具变量"); j = json.loads(out)
years = [x["year"] for x in j["timeline"] if x["year"] is not None]
chk(rc == 0 and j["matched_aliases"] and any(m["path"] == "MOC/tax-moc.md" for m in j["mocs"]) and years == sorted(years) and len(years) >= 2,
    "orient: returns matched aliases, MOCs, and chronological timeline")
ans_ok = os.path.join(v, "ans_ok.md")
open(ans_ok, "w", encoding="utf-8").write("- 稽查威慑提高遵从 [source: smith2020 | as-of: 2026-11-27]\n见 [@chen2018]。\n")
rc, out, _ = run("check-cites", ans_ok); j = json.loads(out)
chk(rc == 0 and j["ok"] and set(j["valid"]) == {"smith2020", "chen2018"}, "check-cites passes on valid vault sources")
ans_bad = os.path.join(v, "ans_bad.md")
open(ans_bad, "w", encoding="utf-8").write("- 幻觉引用 [source: ghost9999 | as-of: 2026-11-27]\n见 [@missing2025]。\n")
rc, out, _ = run("check-cites", ans_bad); j = json.loads(out)
chk(rc == 1 and not j["ok"] and set(j["unknown"]) == {"ghost9999", "missing2025"}, "check-cites fails on unknown sources")
shutil.rmtree(v, ignore_errors=True)
print("kb_search selftest: " + ("ALL OK" if ok else "SOME FAILED"))
sys.exit(0 if ok else 1)
