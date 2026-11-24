#!/usr/bin/env python3
"""Local full-text retrieval over the research vault. No embeddings, no models, no network.

    python kb_search.py search QUERY... [--vault PATH] [--scope wiki|legacy|raw|project|meta|all]
                        [--type T[,T]] [--year Y|Y1-Y2] [--cite-key K] [--limit N]
                        [--mode any|all] [--expand-links HOPS]
    python kb_search.py index  [--vault PATH] [--rebuild]
    python kb_search.py stats  [--vault PATH]

Every command first brings <vault>/.erc-index/kb.sqlite up to date (stat-based, incremental), so
results never lag behind the notes. Notes are split into heading-level chunks; Chinese is indexed as
character bigrams, English as lowercase words. Ranking is BM25 (title/heading 5, keywords/tags/authors 4,
body 1). Meta/aliases.csv (canonical,alias) is expanded both ways at query time. --expand-links adds
wikilink neighbours of the hits. Hits carry cite_key, path, heading path and line range; they are leads,
never conclusions: re-read the page before citing. No hit -> {"hits": [], "note": "no match"}, exit 0.
Use keywords rather than sentences; Chinese terms need >= 2 characters; "quotes" keep a phrase together.
Scopes: wiki (default: Tier 1 folders, MOC, PROJECT.md), legacy (other notes), raw (03-Literature/_sources),
project (project drafts/logs), meta (Meta/). Never indexed: dot-folders, _erc*, _vendor, node_modules,
Templates, 06-Data, 07-Code, paper/versions, root CLAUDE.md/AGENTS.md.
"""
import argparse
import csv
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wiki_lint as wl  # parse_frontmatter, WIKILINK, CODE_FENCE, INLINE_CODE, SCOPE, project helpers

VERSION = 2  # bump when schema or tokenizer changes (stored in PRAGMA user_version)
DB = ".erc-index/kb.sqlite"
WIKI_DIRS = set(wl.SCOPE) | {"MOC"}
SKIP_DIRS, TOP_SKIP = {"node_modules", "_vendor", "Templates"}, {"06-Data", "07-Code"}
TIERS = ("wiki", "legacy", "raw", "project", "meta")
KEYWORD_FIELDS = ("keywords", "tags", "method", "focus", "research_field", "authors", "journal", "type")
CHUNK = 1500
CJK = "[㐀-䶿一-鿿豈-﫿]+"
CJK_RE = re.compile(CJK)
WORD = re.compile("[0-9A-Za-zÀ-ɏ]+|" + CJK)
HEAD = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCES = ("\x60\x60\x60", "~~~")
STOP = {"the", "an", "of", "in", "on", "and", "or", "to", "for", "is", "are", "was", "were", "what", "how",
        "why", "which", "with", "by", "at", "from", "that", "this", "be", "as", "do", "does"}
SCHEMA = """
CREATE TABLE docs(id INTEGER PRIMARY KEY, path TEXT UNIQUE, stamp TEXT, tier TEXT, type TEXT, cite_key TEXT,
                  title TEXT, year INTEGER, verification TEXT, stem TEXT);
CREATE TABLE chunks(id INTEGER PRIMARY KEY, doc_id INTEGER, heading TEXT, l1 INTEGER, l2 INTEGER, text TEXT);
CREATE TABLE links(doc_id INTEGER, target TEXT);
CREATE INDEX ix_chunks ON chunks(doc_id);
CREATE INDEX ix_links ON links(doc_id);
CREATE INDEX ix_stem ON docs(stem);
CREATE VIRTUAL TABLE fts USING fts5(title, keywords, body, tokenize='unicode61 remove_diacritics 2');
"""
COLS = ("d.path, d.tier, d.type, d.cite_key, d.title, d.year, d.verification, "
        "c.heading, c.l1, c.l2, c.text")
JOIN = " JOIN chunks c ON c.id = fts.rowid JOIN docs d ON d.id = c.doc_id"


def tokenize(text):
    out = []
    for w in WORD.findall(text):
        if CJK_RE.fullmatch(w):
            out += [w] if len(w) == 1 else [w[i:i + 2] for i in range(len(w) - 1)]
        else:
            out.append(w.lower())
    return out


def as_list(v):
    return [str(x) for x in (v if isinstance(v, list) else [v]) if x and str(x).strip()]


# ---------------------------------------------------------------- index
def connect(vault, rebuild=False):
    path = vault / DB
    path.parent.mkdir(exist_ok=True)
    if rebuild:
        path.unlink(missing_ok=True)
    gi = path.parent / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")
    con = sqlite3.connect(str(path), timeout=60)
    con.row_factory = sqlite3.Row
    return con


def tier_of(rel):
    top = rel.parts[0]
    if top == "Meta":
        return "meta"
    if top == "03-Literature" and "_sources" in rel.parts:
        return "raw"
    if top == "01-Research-Projects":
        return "wiki" if wl._is_project_entry(rel) else "project"
    return "wiki" if top in WIKI_DIRS else "legacy"


def notes(vault):
    for root, dirs, files in os.walk(str(vault)):
        top = Path(root) == vault
        dirs[:] = sorted(d for d in dirs if not (d.startswith((".", "_erc")) or d in SKIP_DIRS
                                                  or (top and d in TOP_SKIP)))
        for f in sorted(files):
            p = Path(root) / f
            rel = p.relative_to(vault)
            if (f.lower().endswith(".md") and not wl._is_paper_version(rel)
                    and not (top and f.lower() in ("claude.md", "agents.md"))):
                yield rel, p


def make_chunks(lines, start):
    """Heading-level sections, long ones cut at blank lines -> (heading_path, l1, l2, text), 1-based lines."""
    sections, stack, heading, a, fenced = [], [], "(top)", start, False
    for i in range(start, len(lines)):
        fenced ^= lines[i].lstrip().startswith(FENCES)
        m = None if fenced else HEAD.match(lines[i])
        if m:
            sections.append((heading, a, i))
            stack = [s for s in stack if s[0] < len(m[1])] + [(len(m[1]), m[2].strip())]
            heading, a = " > ".join(t for _, t in stack), i
    sections.append((heading, a, len(lines)))
    out = []
    for heading, a, b in sections:
        s, size = a, 0
        for i in range(a, b):
            size += len(lines[i]) + 1
            if i == b - 1 or size >= 2 * CHUNK or (size >= CHUNK and not lines[i].strip()):
                seg = lines[s:i + 1]
                nz = [k for k, ln in enumerate(seg) if ln.strip()]
                if nz and tokenize("\n".join(ln for ln in seg if not HEAD.match(ln))):
                    out.append((heading, s + nz[0] + 1, s + nz[-1] + 1, "\n".join(seg[nz[0]:nz[-1] + 1])))
                s, size = i + 1, 0
    return out


def link_targets(text):
    text = wl.INLINE_CODE.sub("", wl.CODE_FENCE.sub("", text))
    names = (re.sub(r"\.md$", "", raw.strip().replace("\\", "/").split("/")[-1], flags=re.I).lower()
             for raw in wl.WIKILINK.findall(text))
    return set(names) - {""}


def drop_doc(con, doc_id):
    con.execute("DELETE FROM fts WHERE rowid IN (SELECT id FROM chunks WHERE doc_id = ?)", (doc_id,))
    for t, col in (("chunks", "doc_id"), ("links", "doc_id"), ("docs", "id")):
        con.execute("DELETE FROM %s WHERE %s = ?" % (t, col), (doc_id,))


def add_doc(con, rel, tier, stamp, text):
    fm = wl.parse_frontmatter(text)[0] or {}
    lines = text.lstrip("﻿").splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        start = next((i + 1 for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
    stem, cite_key = rel.stem, str(fm.get("cite_key") or "").strip()
    title = str(fm.get("title") or "").strip() or stem
    year = re.search(r"\d{4}", str(fm.get("year", "")))
    keywords = " ".join(tokenize(" ".join([x for f in KEYWORD_FIELDS for x in as_list(fm.get(f))]
                                          + [cite_key, str(fm.get("year", ""))])))
    doc_id = con.execute(
        "INSERT INTO docs(path, stamp, tier, type, cite_key, title, year, verification, stem) VALUES(?,?,?,?,?,?,?,?,?)",
        (rel.as_posix(), stamp, tier, str(fm.get("type") or "").strip().lower(), cite_key, title,
         int(year[0]) if year else None, str(fm.get("verification") or "").strip().lower(), stem.lower())).lastrowid
    for heading, l1, l2, body in make_chunks(lines, start):
        cid = con.execute("INSERT INTO chunks(doc_id, heading, l1, l2, text) VALUES(?,?,?,?,?)",
                          (doc_id, heading, l1, l2, body)).lastrowid
        con.execute("INSERT INTO fts(rowid, title, keywords, body) VALUES(?,?,?,?)",
                    (cid, " ".join(tokenize(title + " " + heading)), keywords, " ".join(tokenize(body))))
    con.executemany("INSERT INTO links VALUES(?,?)",
                    [(doc_id, t) for t in sorted(link_targets("\n".join(lines[start:])))])


def update_index(vault, rebuild=False):
    """Bring the index up to date (a file is re-read only when its size/mtime/tier changed)."""
    con = connect(vault, rebuild)
    con.execute("BEGIN IMMEDIATE")  # one writer at a time: concurrent searches queue instead of colliding
    if con.execute("PRAGMA user_version").fetchone()[0] != VERSION:
        for t in ("fts", "links", "chunks", "docs"):
            con.execute("DROP TABLE IF EXISTS " + t)
        for stmt in filter(str.strip, SCHEMA.split(";")):
            con.execute(stmt)
        con.execute("PRAGMA user_version = %d" % VERSION)
    known = {r["path"]: (r["id"], r["stamp"]) for r in con.execute("SELECT id, path, stamp FROM docs")}
    keep, changed = set(), 0
    for rel, p in notes(vault):
        key, tier, st = rel.as_posix(), tier_of(rel), p.stat()
        stamp = "%d:%d:%s" % (st.st_size, st.st_mtime_ns, tier)
        keep.add(key)
        if key in known and known[key][1] == stamp:
            continue
        if key in known:
            drop_doc(con, known[key][0])
        add_doc(con, rel, tier, stamp, p.read_text(encoding="utf-8-sig", errors="replace"))
        changed += 1
    gone = [v[0] for k, v in known.items() if k not in keep]
    for doc_id in gone:
        drop_doc(con, doc_id)
    con.commit()
    return con, changed, len(keep) - changed, len(gone)


# ---------------------------------------------------------------- query
def load_aliases(vault):
    """Synonym groups from Meta/aliases.csv; rows sharing a term are merged (transitive)."""
    p, groups = vault / "Meta" / "aliases.csv", []
    for row in (csv.reader(p.open(encoding="utf-8-sig", newline="")) if p.exists() else []):
        pair = {x.strip().lower() for x in row[:2] if x.strip()}
        if len(pair) == 2 and pair != {"canonical", "alias"}:
            hit = [g for g in groups if g & pair]
            groups = [g for g in groups if g not in hit] + [pair.union(*hit)]
    return groups


def term_in(term, text):
    if CJK_RE.search(term):
        return term in text
    return re.search(r"(?<![0-9a-z])%s(?![0-9a-z])" % re.escape(term), text) is not None


def phrase(s):
    toks = tokenize(s)
    if len(toks) <= 6:
        return '"%s"' % " ".join(toks) if toks else None
    return "(" + " OR ".join('"%s"' % t for t in dict.fromkeys(toks)) + ")"


def build_match(q, alias_groups, mode):
    """FTS5 MATCH expression, every alternative spelling (for snippets) and the aliases that were added."""
    qlow = q.lower()
    words = [w.lower() for w in WORD.findall(re.sub(r'"[^"]*"', " ", q))]
    units = [s.strip().lower() for s in re.findall(r'"([^"]+)"', q)]
    units += [w for w in words if CJK_RE.fullmatch(w) or (len(w) > 1 and w not in STOP)] or words
    groups, added = [[u] for u in dict.fromkeys(units)], []
    for g in alias_groups:
        if any(len(t) > 1 and term_in(t, qlow) for t in g):
            groups = [x for x in groups if not (len(x) == 1 and x[0] in g)] + [sorted(g)]
            added += [t for t in sorted(g) if not term_in(t, qlow)]
    clauses = [c for c in ("(" + " OR ".join(filter(None, map(phrase, g))) + ")" for g in groups) if c != "()"]
    terms = [t for g in groups for t in g]
    return (" AND " if mode == "all" else " OR ").join(clauses), terms, added


def filters(a):
    tiers = TIERS if a.scope == "all" else [t.strip() for t in a.scope.split(",")]
    if any(t not in TIERS for t in tiers):
        raise SystemExit("bad --scope %r (use %s or all)" % (a.scope, "|".join(TIERS)))
    where, args = ["d.tier IN (%s)" % ",".join("?" * len(tiers))], list(tiers)
    if a.type:
        types = [t.strip().lower() for t in a.type.split(",")]
        where.append("d.type IN (%s)" % ",".join("?" * len(types)))
        args += types
    if a.year:
        m = re.fullmatch(r"(\d{4})?(-(\d{4})?)?", a.year.strip())
        if not m or not (m[1] or m[3]):
            raise SystemExit("bad --year %r (use 2020 or 2015-2020)" % a.year)
        lo, hi = m[1], (m[3] if m[2] else m[1])
        for col, v in (("d.year >= ?", lo), ("d.year <= ?", hi)):
            if v:
                where.append(col)
                args.append(int(v))
    if a.cite_key:
        where.append("d.cite_key = ?")
        args.append(a.cite_key)
    return " AND ".join(where), args


def snippet(text, terms):
    flat = re.sub(r"\s+", " ", text).strip()
    pos = min((i for i in (flat.lower().find(t) for t in terms) if i >= 0), default=-1)
    if pos < 0:
        return flat[:180]
    a = max(0, pos - 70)
    return ("…" if a else "") + flat[a:a + 190] + ("…" if a + 190 < len(flat) else "")


def hit(r, terms, score=0.0, origin=None):
    return {"cite_key": r["cite_key"], "title": r["title"], "path": r["path"], "heading_path": r["heading"],
            "line_start": r["l1"], "line_end": r["l2"], "score": round(score, 3), "tier": r["tier"],
            "type": r["type"], "year": r["year"], "verification": r["verification"],
            "via": "link" if origin else "match", "via_path": origin, "snippet": snippet(r["text"], terms)}


NEIGHBOURS = ("SELECT d2.id FROM links l JOIN docs d2 ON d2.stem = l.target WHERE l.doc_id = ?1 "
              "UNION SELECT l.doc_id FROM links l JOIN docs d1 ON d1.stem = l.target WHERE d1.id = ?1")


def expand_links(con, hits, hops, where, args, terms):
    """Wikilink neighbours (in or out, up to hops) of the hits that pass the same filters."""
    paths = sorted({h["path"] for h in hits})
    seen = {r["id"]: r["path"] for r in con.execute(
        "SELECT id, path FROM docs WHERE path IN (%s)" % ",".join("?" * len(paths)), paths)}
    frontier, out = dict(seen), []
    for _ in range(hops):
        nxt = {}
        for did, origin in frontier.items():
            nxt.update({r[0]: origin for r in con.execute(NEIGHBOURS, (did,)) if r[0] not in seen})
        seen.update(nxt)
        for did, origin in nxt.items():
            r = con.execute("SELECT %s FROM chunks c JOIN docs d ON d.id = c.doc_id WHERE d.id = ? AND %s "
                            "ORDER BY c.id LIMIT 1" % (COLS, where), [did] + args).fetchone()
            out += [hit(r, terms, origin=origin)] if r else []
        frontier = nxt
    return out


def search(vault, a):
    con = update_index(vault)[0]
    q = " ".join(a.query).strip()
    match, terms, added = build_match(q, load_aliases(vault), a.mode)
    where, args = filters(a)
    hits, per_doc = [], Counter()
    if match:
        sql = ("SELECT %s, bm25(fts, 5.0, 4.0, 1.0) AS s FROM fts%s WHERE fts MATCH ? AND %s ORDER BY s LIMIT ?"
               % (COLS, JOIN, where))
        for r in con.execute(sql, [match] + args + [a.limit * 10]):
            if per_doc[r["path"]] < 2:
                per_doc[r["path"]] += 1
                hits.append(hit(r, terms, -r["s"]))
        hits = hits[:a.limit]
        if hits and a.expand_links:
            hits += expand_links(con, hits, a.expand_links, where, args, terms)[:a.limit]
    res = {"query": q, "mode": a.mode, "scope": a.scope, "expanded": added, "total": len(hits), "hits": hits}
    if not hits:
        res["note"] = "no match"
    print(json.dumps(res, ensure_ascii=False, indent=2))


def stats(vault):
    con = update_index(vault)[0]
    count = lambda sql: {r[0] or "(none)": r[1] for r in con.execute(sql)}
    print(json.dumps({
        "docs": con.execute("SELECT COUNT(*) FROM docs").fetchone()[0],
        "chunks": con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0],
        "by_tier": count("SELECT tier, COUNT(*) FROM docs GROUP BY tier"),
        "by_type": count("SELECT type, COUNT(*) FROM docs GROUP BY type")}, ensure_ascii=False, indent=2))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("index", "search", "stats"):
        p = sub.add_parser(name)
        p.add_argument("--vault", default=".")
        if name == "index":
            p.add_argument("--rebuild", action="store_true")
        if name == "search":
            p.add_argument("query", nargs="+")
            p.add_argument("--scope", default="wiki")
            p.add_argument("--type")
            p.add_argument("--year")
            p.add_argument("--cite-key", dest="cite_key")
            p.add_argument("--limit", type=int, default=10)
            p.add_argument("--mode", choices=("any", "all"), default="any")
            p.add_argument("--expand-links", dest="expand_links", type=int, default=0)
    a = ap.parse_args(argv)
    vault = Path(a.vault).resolve()
    try:
        if a.cmd == "search":
            search(vault, a)
        elif a.cmd == "stats":
            stats(vault)
        else:
            con, new, same, gone = update_index(vault, a.rebuild)
            print("indexed %d, unchanged %d, removed %d | %d docs, %d chunks" % (
                new, same, gone, con.execute("SELECT COUNT(*) FROM docs").fetchone()[0],
                con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]))
    except sqlite3.OperationalError as e:
        sys.stderr.write("kb_search: SQLite error (%s); FTS5 is required\n" % e)
        return 2
    return 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    sys.exit(main())
