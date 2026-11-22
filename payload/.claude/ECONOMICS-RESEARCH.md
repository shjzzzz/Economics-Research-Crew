# Economics Research Crew — Core Research & Routing Protocol

> Single source of truth for routing, economics argument spine, orchestration, writing constraints and evidence standards. Workspace layout and hard red lines live in `CLAUDE.md` / `Meta/vault-map.md`.

## 1. Intent Routing Table (17 Skills, 7 Agents)
| Stage / Role | User intent (examples) | Primary Skill | Authorized Agent |
|---|---|---|---|
| S1 Question | 选题、收敛研究问题、定题、确定 estimand | `/research-question` | — |
| S2/S9 Literature | 文献综述、梳理文献、研究缺口、文献矩阵、找文献、Zotero/EndNote | `/literature-review` | `literature-agent` |
| S3 Theory | 理论模型、机制分析、均衡、比较静态、假说推导 | `/theory-modeling` | `theory-agent` |
| S3 Tax Policy | 税法适用、税目、税制、征管、遵从、税负归宿、政策评估 | `/tax-policy-analysis` | `tax-policy-agent` |
| S4 Identification | 识别策略、DID/IV/RDD/聚束、平行趋势、内生性、稳健性设计 | `/causal-inference-audit` | `causal-inference-agent` |
| S5 Econometrics | 数据清洗、变量构造、回归、复现论文、代码审计、异质性 | `/econometric-analysis` | `econometrics-agent` (only Bash/PS) |
| S6 Review | 审稿、匿名审稿、挑刺、审查研究设计或稿件 | `/academic-review` | `academic-reviewer` (isolated) |
| S8 Outline | 论文大纲、论文框架、主张清单、贡献定位、引言布局 | `/paper-outline` | — |
| S10 Draft | 起草论文、写初稿、分节写作、把大纲写成正文 | `/paper-draft` | `paper-writer-agent` |
| S11 Refine / R&R | 精修、按审稿意见修改、返修、R&R、多轮修改 | `/paper-refine` | `paper-writer-agent` / `academic-reviewer` |
| S11b Polish | 润色、去 AI 味、语言精修、文风校准、消除套话 | `/paper-polish` | — |
| Plots (MIT) | 出版级期刊图（Python）、从图表图片/PDF 提取数据 | `/scientific-visualization`, `/thu-digitizer` | — |
| Wiki Ingest | 摄入文献/来源到知识库、处理 `00-Inbox`/`_sources` | `/ingest-source` | — |
| Wiki Query | 知识库里有什么、根据知识库回答、查已有文献 | `/query-wiki` | — |
| Wiki Lint | 知识库体检、检查断链/孤立页/矛盾/过时 | `/wiki-lint` | — |
| Director (S1–S12) | 完整做研究、规划并推进、继续上次的研究 | `/research-pipeline` | stage-gated (all above) |

## 2. Economics Argument Spine (S1–S12)
Maintain one traceable causal spine across every empirical/institutional paper (details in `Meta/research-standards.md`):
`S1 Question & Estimand` → `S2 Literature Debate & Gap` → `S3 Competing Mechanisms & Institutional Shock` → `S4 Threat-to-Test Matrix, Frozen Plan & Wording Ceiling` → `S5 Reproducible Estimation, Sample Waterfall & Results Ledger` → `S6 Independent Review + 7-Mode AI Failure Gate` → `S7 Researcher Go/Return/Stop` → `S8 Claim-Driven Outline` → `S9 Verified Citations with Locators` → `S10 Constrained Section Drafting` → `S11 Checklist Refinement / R&R (+ optional /paper-polish)` → `S12 Final Gate, AI Disclosure & Wiki Write-back`.

Quality loop: research agents propose → `econometrics-agent` executes → `academic-reviewer` challenges independently (artifacts only) → Director + researcher decide. A Fatal Flaw blocks acceptance; never skip S4 just because code runs.

## 3. Orchestration Layer
`/research-pipeline` maintains `01-Research-Projects/<project>/STATE.json` and `Meta/run-ledger.jsonl` **only** via `python .claude/scripts/orchestrator.py` (`init`, `status`, `next`, `artifact`, `verify`, `gate`, `fail`, `recover`, `enforce`, `log`).
- **Researcher gates**: never run `gate --decision pass` on AI judgment; always supply `--note`.
- **Retries & concurrency**: max 2 retries per agent per stage, then stop and report. Default concurrency 1 (S3: 2; cap 3). Claude Code hooks enforce order, retries, concurrency and file protection; follow voluntarily on agy/Codex.

## 4. Paper Writing & Human–AI Collaboration (S8–S12)
Follow `Meta/collaboration-protocol.md` (A0–A3, C1–C5) and `Meta/style-guide.md` (detailed CLI workflows live in `/literature-review`, `/paper-draft`, `/paper-refine`, `/paper-polish`):
- **Constrained inputs**: citations use `[@key]` from `Meta/citation-map.json` (with `locator` & `claim_scope` against L3 mismatch); numbers use `{{res:id}}` from `Meta/results-ledger.json` (honest null `--no-source-reason` when confidential/manual); result blocks carry `<!-- claim: Cn -->`; gaps become `⟦问：…⟧` (answered `⟦答：…⟧`), never invention.
- **Reference managers**: `paper_tools.py cite import|zotero|ris|csl|bib|open|zotero-note` exchanges with EndNote/Zotero (`ZOTERO_API_KEY` env-only, GET-only pulls; `zotero-note --yes` requires researcher approval). Imported items always start `unverified` (`manual` for Chinese) and are never auto-confirmed.
- **Refinement (`/paper-refine`)**: `academic-reviewer` lists read files, judges literature by manuscript date, checks distributional incidence, Frame-Lock and Concession Threshold (≥4/5, no consecutive concessions), and emits numbered `F1/M1/m1` + 5 scores (`ident, contrib, inst, consist, write`). Run `paper_tools.py review verify` before revising. Re-reviews use checklist counts (`--carried-*`/`--new-*`); accept only if Fatal ≤ prev, (Major < prev or tied Major with total ≥ prev), identical dimensions and no drop ≥2. New analysis goes to `Meta/review-queue.md`.
- **Language polish (`/paper-polish`)**: runs only after content settles; `polish check` proves citations, `{{res}}`, claim tags, Q/A markers and numbers are invariant. Never used to evade AI detection; disclose AI use in `paper/ai-disclosure.md`.
- **Isolation & failure gate**: every Skill/Agent declares `data_access_level` (`raw`/`redacted`/`verified_only`); `Meta/mechanism-library.md` offers testable hypotheses, not evidence; S6/S12 must clear the 7-mode AI failure gate.

## 5. Econometric, Tax-Law & Evidence Discipline
- **Econometrics**: separate association, prediction, causality; report estimand, assumptions, clustering level, sample waterfall, economic magnitude (vs. mean/SD or elasticity) and software versions. Run modern diagnostics: staggered DID (CS/SA/Bacon/HonestDiD), IV (effective F/AR/exclusion/LATE), RDD/Bunching (continuity/sorting/bandwidth). Fixed effects or insignificant pre-trends never prove causality; no silent filtering, winsorizing or p-hacking.
- **Evidence & Tax Law**: separate facts, model interpretation and hypotheses; keep DOI/URL and page/table/equation anchors. Chinese tax law requires issuing authority, doc number, promulgation/effective dates, amendment/repeal status, scope and conflict-resolution ordering (see `tax-policy-agent`).

## 6. Knowledge Base & Wiki Maintenance
- Session start: read `Meta/purpose.md` (if blank, remind researcher; never invent direction), `Meta/decisions.md` and `Meta/constraints.md`.
- Routing & updates: `Meta/index.md` routes both filesystem (`Meta/folder-map.md`) and knowledge graph (`Meta/link-map.md` hubs → `[[wikilinks]]`); every ingest/lint/organization pass updates `Meta/index.md` and appends to `Meta/log.md`. Search legacy notes by folder, not the link graph.
- Tier 1 frontmatter: `type` (`literature|theory|method|synthesis|query|research-project|dataset|analysis-plan|analysis-log`), `sources`, `updated`, `verification` (`verified|unverified`); literature notes add `cite_key`.
- Two-step ingest (`/ingest-source`): analyze & await approval → write/cross-link pages → update `Meta/index.md`, `Meta/source-registry.md` (SHA256) and `Meta/log.md`; log contradictions in `Meta/review-queue.md`.
- Deterministic checks & maps: run `python .claude/scripts/wiki_lint.py lint --vault .` and `python .claude/scripts/wiki_lint.py map --vault .`. After S12, compound key findings into `08-Research-Notes/` (`type: synthesis`) with researcher consent.
