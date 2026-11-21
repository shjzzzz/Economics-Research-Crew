# Economics Research Crew — Core Research & Routing Protocol

> Single source of truth for routing, economics argument spine, orchestration, writing collaboration and evidence standards. Workspace layout and hard red lines live in `CLAUDE.md` / `Meta/vault-map.md`.

## 1. Intent Routing Table (17 Skills)
| User intent (examples) | Primary Skill | Authorized Agent |
|---|---|---|
| 选题、收敛研究问题、定题、确定 estimand | `/research-question` | — |
| 文献综述、梳理文献、研究缺口、文献矩阵、找文献 | `/literature-review` | `literature-agent` |
| 理论模型、机制分析、均衡、比较静态、假说推导 | `/theory-modeling` | `theory-agent` |
| 税法适用、税目、税制、征管、遵从、税负归宿、政策评估 | `/tax-policy-analysis` | `tax-policy-agent` |
| 识别策略、DID/IV/RDD/聚束、平行趋势、内生性、稳健性设计 | `/causal-inference-audit` | `causal-inference-agent` |
| 数据清洗、变量构造、回归、复现论文、代码审计、异质性 | `/econometric-analysis` | `econometrics-agent` |
| 审稿、匿名审稿、挑刺、审查研究设计或稿件 | `/academic-review` | `academic-reviewer` |
| 论文大纲、论文框架、主张清单、贡献定位、引言布局 | `/paper-outline` | — |
| 起草论文、写初稿、分节写作、把大纲写成正文 | `/paper-draft` | `paper-writer-agent` |
| 精修、按审稿意见修改、返修、R&R、多轮修改 | `/paper-refine` | `paper-writer-agent` / `academic-reviewer` |
| 润色、去 AI 味、语言精修、文风校准、消除套话 | `/paper-polish` | — |
| 出版级期刊图（Python 多子图、误差棒、显著性标注）、从图表图片/PDF 提取数据 | `/scientific-visualization`, `/thu-digitizer` | — |
| 摄入文献/来源到知识库、处理 `_sources` | `/ingest-source` | — |
| 知识库里有什么、根据知识库回答、查已有文献 | `/query-wiki` | — |
| 知识库体检、检查断链/孤立页/矛盾/过时 | `/wiki-lint` | — |
| 完整做研究、规划并推进、继续上次的研究 | `/research-pipeline` | stage-gated (all above) |

### Role Mapping (Director + 8 Roles)
Director: `/research-pipeline` | 01 Literature: `/literature-review`, `literature-agent`, `/ingest-source` | 02 Theory: `/theory-modeling`, `theory-agent` | 03 Data & 04 Econometrics & 06 Replication: `/econometric-analysis`, `econometrics-agent`; identification audited by `/causal-inference-audit`, `causal-inference-agent` | 05 Tax: `/tax-policy-analysis`, `tax-policy-agent` | 07 Writing: `/paper-outline`, `/paper-draft`, `/paper-refine`, `/paper-polish`, `paper-writer-agent` | 08 Review: `/academic-review`, `academic-reviewer` (isolated context).

## 2. Economics Argument Spine (S1–S12)
Every empirical/institutional paper maintains one traceable causal spine (see `Meta/research-standards.md`):
`S1 Question & Estimand` → `S2 Literature Debate & Gap` → `S3 Competing Mechanisms (H1..Hk) & Institutional Shock` → `S4 Threat-to-Test Matrix, Frozen Plan & Wording Ceiling` → `S5 Reproducible Estimation, Sample Waterfall & Registered Results (res:*)` → `S6 Independent Review + 7-Mode AI Failure Gate` → `S7 Researcher Go/Return/Stop` → `S8 Claim-Driven Outline & 6-Move Intro` → `S9 Verified Citations with Locators` → `S10 Constrained Section Drafting` → `S11 Checklist Refinement / R&R (+ optional /paper-polish)` → `S12 Final Gate, AI Disclosure & Wiki Synthesis Write-back`.

Quality loop: proposal (research agents) → execution (`econometrics-agent`) → independent challenge (`academic-reviewer`, artifacts only) → decision (Director + researcher). A Fatal Flaw blocks acceptance. Do not skip S4 identification design merely because a regression runs.

## 3. Orchestration Layer
`/research-pipeline` tracks state in `01-Research-Projects/<project>/STATE.json` and logs in `Meta/run-ledger.jsonl`, modified **only** via `python .claude/scripts/orchestrator.py` (`init`, `status`, `next`, `artifact`, `verify`, `gate`, `fail`, `recover`, `enforce`, `log`).
- **Gates belong to the researcher**: never run `gate --decision pass` on AI judgment; always supply `--note`.
- **Retries & parallelism**: max 2 retries per agent per stage, then stop and report. Default concurrency 1 (S3: 2; hard cap 3). Claude Code hooks enforce stage order, retry budget, concurrency and file protection; on agy/Codex follow the same rules voluntarily.

## 4. Paper Writing & Human–AI Collaboration (S8–S12)
Follow `Meta/collaboration-protocol.md` (autonomy A0–A3, checkpoints C1–C5) and `Meta/style-guide.md`.
- **Constrained inputs**: draft citations use `[@key]` from `Meta/citation-map.json` (with `--locator` & `--claim-scope` to prevent L3 mismatch; bridge from `03-Literature/` via `paper_tools.py cite from-note`); numbers use `{{res:id}}` from `Meta/results-ledger.json` (honest null `--no-source-reason` when confidential/manual); result blocks carry `<!-- claim: Cn -->`; gaps become `⟦问：…⟧` (answered `⟦答：…⟧`), never invention.
- **Reference managers (EndNote / Zotero)**: `paper_tools.py cite import FILE` reads RIS / BibTeX / CSL-JSON exports (or `cite zotero` pulls via the Zotero API, GET only, key only from env `ZOTERO_API_KEY`); `cite ris|csl|bib` export. The citation table stays the single source of truth: imports start `unverified` (`manual` for Chinese items), never auto-confirmed, add literature notes + index rows; `--attach` copies PDFs into `03-Literature/_sources/` (copy, never move). `cite zotero-note KEY` writes a new Zotero child note (preview unless `--yes`; researcher approval).
- **Refinement (`/paper-refine`)**: `academic-reviewer` lists read files first, judges literature by manuscript date, checks distributional/stakeholder incidence and unsupported core premises, never guesses unconfirmed venues, and outputs numbered `F1/M1/m1` (+ optional `Advisory/Watchlist`) + 5 scores (`ident, contrib, inst, consist, write`, 1–10) + Frame-Lock + Concession Threshold (≥4/5, no consecutive concessions). Run `paper_tools.py review verify` to check reviewer quotes (NFC) and suggested references before revising. Re-reviews use `--carried-*`/`--new-*` against baseline; accept only if Fatal ≤ prev AND (Major < prev OR (Major == prev AND total ≥ prev)), with identical dimensions and no dimension drop ≥2. Requests for new analysis go to `Meta/review-queue.md`. External R&R uses `Templates/rebuttal-matrix.md`.
- **Language polish (`/paper-polish`)**: runs only after content settles; `paper_tools.py polish scan` flags tells from `Meta/ai-tells.json`; `polish check` proves citations, `{{res}}`, claim tags, Q/A markers and numbers are invariant. Never used to evade AI detection; AI involvement is disclosed in `paper/ai-disclosure.md`.
- **Data isolation & mechanisms**: every Skill/Agent declares `data_access_level` (`raw`/`redacted`/`verified_only`). `Meta/mechanism-library.md` provides testable starting points, not evidence. S6/S12 must clear the 7-mode AI failure gate.

## 5. Econometric, Tax-Law & Evidence Discipline
- **Econometrics**: separate association, prediction, causality; report estimand, assumptions, clustering level (at assignment/shock), sample waterfall, economic magnitude (vs. mean/SD or elasticity), software versions. Check modern diagnostics: staggered DID (CS/SA/Bacon/HonestDiD), IV (effective F/AR/exclusion/LATE), RDD/Bunching (continuity/sorting/bandwidth). Fixed effects or insignificant pre-trends do not prove causality. No silent filtering, winsorizing or p-hacking.
- **Evidence & Tax Law**: separate source facts, model interpretation, researcher hypotheses. Keep DOI/URL and page/table/equation anchors; Chinese tax law requires issuing authority, doc number, promulgation/effective dates, amendment/repeal status, scope, and conflict-resolution ordering (see `tax-policy-agent`).

## 6. Knowledge Base & Wiki Maintenance
- Session start: read `Meta/purpose.md` (if blank, remind researcher; never invent direction) and `Meta/decisions.md`.
- Retrieval & organization: `Meta/index.md` routes both the filesystem (directories/boundaries + `Meta/folder-map.md`) and the knowledge system (`Meta/link-map.md` hubs → `[[wikilinks]]`); every wiki organization/ingest/lint pass updates `Meta/index.md` and appends to `Meta/log.md`. Legacy tax-law notes are searched by folder, not through the link graph.
- Frontmatter for Tier 1 wiki pages: `type` (`literature|theory|method|synthesis|query|research-project|dataset|analysis-plan|analysis-log`), `sources`, `updated`, `verification` (`verified|unverified`); literature notes add `cite_key`.
- Two-step ingest (`/ingest-source`): analyze & await approval → write/update pages + cross-link `04-Theories`/`05-Methods` → update `Meta/index.md`, `Meta/source-registry.md` (SHA256), `Meta/log.md` (`## [YYYY-MM-DD] <type> | <title>`). Log source contradictions side-by-side in `Meta/review-queue.md`.
- Deterministic checks & maps: run `python .claude/scripts/wiki_lint.py lint --vault .` and `python .claude/scripts/wiki_lint.py map --vault .` (refreshes `Meta/folder-map.md`, `Meta/link-map.md`, and `ERC:MAP` in `CLAUDE.md`/`AGENTS.md`). After S12 completion, compound key findings back into `08-Research-Notes/` (`type: synthesis`) with researcher consent.
