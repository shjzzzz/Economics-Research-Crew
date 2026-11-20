#!/usr/bin/env python3
"""Cross-platform adaptive installer, checker and syncer for Economics Research Crew.

Supports macOS, Windows 11 and Linux using Python standard library only.
Auto-detects OS (adapting hook commands to `python3` on macOS/Linux and `python` on Windows)
and installed AI CLIs (`claude`, `agy`, `codex`). Never overwrites existing user files.

Usage:
  python3 tools/erc_cli.py install --vault PATH [--platform auto|claude|agy|codex|all]
                                   [--with-hooks] [--with-extras] [--update] [--dry-run]
  python3 tools/erc_cli.py test --vault PATH
  python3 tools/erc_cli.py sync --vault PATH [--check]
  python3 tools/erc_cli.py check-ars [--out FILE] [--json] [--mock JSON]
"""
import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.dirname(HERE)
PAYLOAD = os.path.join(PKG_ROOT, "payload")
sys.path.insert(0, HERE)
import build_platform as bp  # noqa: E402
import merge_hooks as mh  # noqa: E402

AGENTS = [
    "literature-agent", "theory-agent", "tax-policy-agent", "econometrics-agent",
    "causal-inference-agent", "academic-reviewer", "paper-writer-agent",
]
SKILLS = [
    "research-question", "literature-review", "theory-modeling", "tax-policy-analysis",
    "causal-inference-audit", "econometric-analysis", "academic-review",
    "ingest-source", "query-wiki", "wiki-lint", "research-pipeline",
    "paper-outline", "paper-draft", "paper-refine", "paper-polish",
    "publication-chart-skill", "econ-visualization", "scientific-visualization",
    "copyplot", "tikz", "thu-digitizer",
]
META_REQUIRED = [
    "Meta/purpose.md", "Meta/index.md", "Meta/review-queue.md", "Meta/vault-map.md",
    "Meta/research-standards.md", "Meta/source-registry.md", "Meta/log.md",
    "Meta/collaboration-protocol.md", "Meta/style-guide.md", "Meta/mechanism-library.md",
    "Meta/decisions.md", "Meta/ai-tells.json", "Meta/upstream-ars.json",
]
RESEARCH_DIRS = [
    "00-Inbox", "01-Research-Projects", "03-Literature", "03-Literature/_sources",
    "04-Theories", "05-Methods", "06-Data/raw", "06-Data/processed", "06-Data/metadata",
    "07-Code/python", "07-Code/R", "07-Code/stata", "08-Research-Notes",
    "09-Writing", "10-Archive", "MOC",
]
MAP_RE = re.compile(r"<!-- ERC:MAP:BEGIN.*?<!-- ERC:MAP:END -->", re.S)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_os_label(override=None):
    if override:
        return override
    s = platform.system().lower()
    if s == "darwin":
        return "macos"
    if s == "windows":
        return "windows"
    return s or "unix"


def resolve_python_cmd(os_label, explicit=None):
    if explicit:
        return explicit
    if os_label == "windows":
        return "python"
    return "python3" if shutil.which("python3") else "python"


def copy_no_overwrite(src_dir, dst_dir, update, dry_run, pending):
    if not os.path.isdir(src_dir):
        return
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in sorted(dirs) if d != "__pycache__"]
        for f in sorted(files):
            s = os.path.join(root, f)
            rel = os.path.relpath(s, src_dir)
            d = os.path.join(dst_dir, rel)
            if os.path.exists(d):
                if update and sha256_file(s) != sha256_file(d):
                    newp = d + ".new"
                    if not dry_run:
                        shutil.copyfile(s, newp)
                    pending.append(newp)
                    print("  有差异 -> %s.new" % rel.replace("\\", "/"))
                elif not update:
                    print("  跳过(已存在): %s" % rel.replace("\\", "/"))
                continue
            if not dry_run:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copyfile(s, d)


def cmd_install(a):
    vault = os.path.abspath(os.path.expanduser(a.vault))
    if not os.path.isdir(vault):
        sys.exit("知识库目录不存在：%s" % vault)
    if not os.path.isdir(PAYLOAD):
        sys.exit("未找到 payload 目录：%s" % PAYLOAD)

    os_label = detect_os_label(a.target_os)
    py_cmd = resolve_python_cmd(os_label, a.python_cmd)
    detected = [c for c in ("claude", "agy", "codex") if shutil.which(c)]
    if a.platform == "auto":
        platforms = detected if detected else ["claude"]
    elif a.platform == "all":
        platforms = ["claude", "agy", "codex"]
    else:
        platforms = [a.platform]
    do_claude = "claude" in platforms
    do_agents = ("agy" in platforms) or ("codex" in platforms)
    print("系统：%s（hook python=%s）；平台：%s（--platform %s；本机检测到：%s）" % (
        os_label, py_cmd, ", ".join(platforms), a.platform, ", ".join(detected) or "无"))

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(vault, "_erc-backups", stamp)
    pending = []

    # 1. Backup critical existing files
    for rel in ("CLAUDE.md", ".mcp.json", ".claude/settings.json", "AGENTS.md", ".agents/hooks.json"):
        src = os.path.join(vault, *rel.split("/"))
        if os.path.isfile(src) and not a.dry_run:
            dst = os.path.join(backup_dir, *rel.split("/"))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

    # 2. Core payload
    claude_dir = os.path.join(vault, ".claude")
    if do_claude:
        copy_no_overwrite(os.path.join(PAYLOAD, ".claude"), claude_dir, a.update, a.dry_run, pending)
    copy_no_overwrite(os.path.join(PAYLOAD, "Meta"), os.path.join(vault, "Meta"), a.update, a.dry_run, pending)
    copy_no_overwrite(os.path.join(PAYLOAD, "Templates"), os.path.join(vault, "Templates"), a.update, a.dry_run, pending)

    # 3. agy / Codex generated files
    if do_agents:
        stage = tempfile.mkdtemp(prefix="erc-platform-")
        try:
            agent_plats = {p for p in platforms if p != "claude"}
            bp.build(PAYLOAD, stage, agent_plats, py_cmd)
            copy_no_overwrite(os.path.join(stage, ".agents"), os.path.join(vault, ".agents"), a.update, a.dry_run, pending)
            agents_md = os.path.join(vault, "AGENTS.md")
            if not a.dry_run:
                old_exists = os.path.exists(agents_md + ".new")
                bp.merge_agents_md(agents_md, os.path.join(stage, "AGENTS.erc.md"), a.update)
                if os.path.exists(agents_md + ".new") and not old_exists:
                    pending.append(agents_md + ".new")
            if a.with_hooks and "agy" in platforms and not a.dry_run:
                agy_hooks = os.path.join(vault, ".agents", "hooks.json")
                os.makedirs(os.path.dirname(agy_hooks), exist_ok=True)
                bp.merge_agy_hooks(agy_hooks, os.path.join(stage, "hooks.erc.json"))
        finally:
            shutil.rmtree(stage, ignore_errors=True)

    # 4. Optional extras
    if a.with_extras:
        extras = os.path.join(PKG_ROOT, "payload-extras")
        if not os.path.isdir(extras):
            sys.exit("--with-extras 需要 payload-extras 目录。")
        if do_claude:
            copy_no_overwrite(os.path.join(extras, "skills"), os.path.join(claude_dir, "skills"), a.update, a.dry_run, pending)
            copy_no_overwrite(os.path.join(extras, "agents"), os.path.join(claude_dir, "agents"), a.update, a.dry_run, pending)
        if do_agents:
            copy_no_overwrite(os.path.join(extras, "skills"), os.path.join(vault, ".agents", "skills"), a.update, a.dry_run, pending)
        copy_no_overwrite(os.path.join(extras, "extras"), os.path.join(vault, "Meta", "extras"), a.update, a.dry_run, pending)

    # 5. Claude hooks
    if a.with_hooks and do_claude and not a.dry_run:
        rc = mh.main(os.path.join(claude_dir, "settings.json"),
                     os.path.join(PAYLOAD, ".claude", "settings.hooks.json"), py_cmd)
        if rc != 0:
            sys.exit(rc)

    # 6. Root CLAUDE.md
    import_line = "@.claude/ECONOMICS-RESEARCH.md"
    root_claude = os.path.join(vault, "CLAUDE.md")
    tpl_path = os.path.join(PAYLOAD, "CLAUDE.template.md")
    if do_claude and not a.dry_run:
        tpl_body = bp.rd(tpl_path).rstrip()
        if not os.path.exists(root_claude):
            body = tpl_body if import_line in tpl_body else (tpl_body + "\n\n" + import_line)
            bp.wr(root_claude, body + "\n")
        else:
            cur = bp.rd(root_claude)
            if a.update:
                if MAP_RE.sub("MAP", cur).rstrip() != MAP_RE.sub("MAP", tpl_body).rstrip():
                    bp.wr(root_claude + ".new", tpl_body + "\n")
                    pending.append(root_claude + ".new")
            if import_line not in cur:
                bp.wr(root_claude, cur.rstrip() + "\n\n" + import_line + "\n")

    # 7. Research directories
    if not a.dry_run:
        for d in RESEARCH_DIRS:
            os.makedirs(os.path.join(vault, *d.split("/")), exist_ok=True)

    # 8. Refresh maps
    if not a.dry_run:
        lint_py = os.path.join(vault, ".claude", "scripts", "wiki_lint.py")
        if not os.path.isfile(lint_py):
            lint_py = os.path.join(vault, ".agents", "scripts", "wiki_lint.py")
        if os.path.isfile(lint_py):
            subprocess.run([sys.executable, lint_py, "map", "--vault", vault], check=False)

    if pending:
        print("以下文件与新版不同，已生成 .new 副本（未覆盖原文件）：")
        for p in pending:
            print("  " + p)
    print("完成。%s" % ("（dry-run，未写入文件）" if a.dry_run else
                        ("备份：" + backup_dir if os.path.isdir(backup_dir) else "无需备份")))
    return 0


def parse_frontmatter_simple(path):
    txt = bp.rd(path)
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    out = {}
    for ln in m.group(1).splitlines():
        kv = re.match(r"^([\w-]+):\s*(.*)$", ln)
        if kv:
            out[kv.group(1)] = kv.group(2).strip().strip('"')
    return out


def cmd_test(a):
    vault = os.path.abspath(os.path.expanduser(a.vault))
    errors = []
    valid_access = {"raw", "redacted", "verified_only"}
    valid_task = {"open-ended", "outcome-gradable"}

    def req_files(paths):
        for rel in paths:
            if not os.path.exists(os.path.join(vault, *rel.split("/"))):
                errors.append("缺少文件: " + rel)

    def check_defs(root):
        for ag in AGENTS:
            p = os.path.join(vault, root, "agents", ag + ".md")
            if not os.path.isfile(p):
                errors.append("缺少 agent: %s/agents/%s.md" % (root, ag))
                continue
            fm = parse_frontmatter_simple(p)
            if not fm or fm.get("name") != ag or not fm.get("description"):
                errors.append("agent frontmatter 无效: %s/agents/%s.md" % (root, ag))
            if fm and (fm.get("data_access_level") not in valid_access or fm.get("task_type") not in valid_task):
                errors.append("agent 缺少或无效的 data_access_level/task_type: %s/agents/%s.md" % (root, ag))
        for sk in SKILLS:
            p = os.path.join(vault, root, "skills", sk, "SKILL.md")
            if not os.path.isfile(p):
                errors.append("缺少 skill: %s/skills/%s" % (root, sk))
                continue
            fm = parse_frontmatter_simple(p)
            if not fm or fm.get("name") != sk or not fm.get("description"):
                errors.append("skill frontmatter 无效: %s/skills/%s" % (root, sk))
            if fm and (fm.get("data_access_level") not in valid_access or fm.get("task_type") not in valid_task):
                errors.append("skill 缺少或无效的 data_access_level/task_type: %s/skills/%s" % (root, sk))

    has_claude = os.path.isdir(os.path.join(vault, ".claude", "skills")) or os.path.isfile(os.path.join(vault, "CLAUDE.md"))
    has_agents = os.path.isdir(os.path.join(vault, ".agents", "skills")) or os.path.isfile(os.path.join(vault, "AGENTS.md"))
    if not (has_claude or has_agents):
        errors.append("未发现任何平台的安装（.claude/ 或 .agents/）")

    req_files(META_REQUIRED)
    for d in ("06-Data/raw", "06-Data/processed", "07-Code"):
        if not os.path.isdir(os.path.join(vault, *d.split("/"))):
            errors.append("缺少目录: " + d)

    if has_claude:
        check_defs(".claude")
        req_files([".claude/ECONOMICS-RESEARCH.md", ".claude/scripts/wiki_lint.py",
                   ".claude/scripts/orchestrator.py", ".claude/scripts/paper_tools.py",
                   ".claude/hooks/validate_paper.py", ".claude/pipeline-stages.json",
                   "Templates/handoff.md", "Templates/paper-outline.md", "Templates/rebuttal-matrix.md"])
        rc = os.path.join(vault, "CLAUDE.md")
        if not os.path.isfile(rc) or "@.claude/ECONOMICS-RESEARCH.md" not in bp.rd(rc):
            errors.append("根 CLAUDE.md 未 import ECONOMICS-RESEARCH.md")
        sj = os.path.join(vault, ".claude", "settings.json")
        if os.path.isfile(sj):
            st = bp.rd(sj)
            for h in ("protect_raw.py", "validate_frontmatter.py", "validate_paper.py",
                      "routing_hint.py", "orchestrator_guard.py", "orchestrator_record.py"):
                if h in st and not os.path.isfile(os.path.join(vault, ".claude", "hooks", h)):
                    errors.append("settings.json 引用了 hook 但文件缺失: " + h)

    if has_agents:
        check_defs(".agents")
        req_files([".agents/scripts/wiki_lint.py", ".agents/scripts/orchestrator.py",
                   ".agents/scripts/paper_tools.py", ".agents/pipeline-stages.json"])
        am = os.path.join(vault, "AGENTS.md")
        if not os.path.isfile(am):
            errors.append("缺少根 AGENTS.md")
        else:
            sz = os.path.getsize(am)
            if "ERC:BEGIN" not in bp.rd(am):
                errors.append("AGENTS.md 中没有 Economics Research Crew 区块")
            if sz > bp.AGENTS_MD_LIMIT:
                errors.append("AGENTS.md 为 %d 字节，超过上限 %d" % (sz, bp.AGENTS_MD_LIMIT))
        hj = os.path.join(vault, ".agents", "hooks.json")
        if os.path.isfile(hj):
            try:
                json.loads(bp.rd(hj))
            except ValueError:
                errors.append(".agents/hooks.json 不是有效 JSON")

    if errors:
        for e in errors:
            print(" x " + e)
        return 1
    where = ([] if not has_claude else ["Claude Code(.claude)"]) + ([] if not has_agents else ["Antigravity/Codex(.agents + AGENTS.md)"])
    print("结构检查通过（%d agents, %d skills；平台：%s）。" % (len(AGENTS), len(SKILLS), "、".join(where)))
    return 0


def cmd_sync(a):
    vault = os.path.abspath(os.path.expanduser(a.vault))
    bp.sync_vault(vault, a.check)
    return 0


def cmd_check_ars(a):
    import check_ars_updates as cau
    argv = ["check"]
    if a.out:
        argv += ["--out", a.out]
    if a.json:
        argv += ["--json"]
    if a.mock:
        argv += ["--mock", a.mock]
    return cau.main(argv)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("install")
    pi.add_argument("--vault", required=True)
    pi.add_argument("--platform", default="auto", choices=["auto", "claude", "agy", "codex", "all"])
    pi.add_argument("--with-hooks", action="store_true")
    pi.add_argument("--with-extras", action="store_true")
    pi.add_argument("--update", action="store_true")
    pi.add_argument("--dry-run", action="store_true")
    pi.add_argument("--target-os", choices=["macos", "windows", "linux"], help="Override OS detection (for testing)")
    pi.add_argument("--python-cmd", help="Override hook python command (e.g. python3 or python)")
    pi.set_defaults(f=cmd_install)

    pt = sub.add_parser("test")
    pt.add_argument("--vault", required=True)
    pt.set_defaults(f=cmd_test)

    ps = sub.add_parser("sync")
    ps.add_argument("--vault", required=True)
    ps.add_argument("--check", action="store_true")
    ps.set_defaults(f=cmd_sync)

    pa = sub.add_parser("check-ars")
    pa.add_argument("--out")
    pa.add_argument("--json", action="store_true")
    pa.add_argument("--mock")
    pa.set_defaults(f=cmd_check_ars)

    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8")
    sys.exit(main())
