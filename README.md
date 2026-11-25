# Economics Research Crew

面向**税收经济学、公共经济学、计量经济学与因果推断**的 AI 科研协作与论文写作系统。它把研究者的一句话，经意图路由送进 S1–S12 的论证脊柱，一路走到终稿、复现包与投稿前审稿；每个阶段的产物都由确定性脚本做机械检查，再由研究者在关卡拍板。

支持 **Windows 11 与 macOS / Linux**，自适应 **Claude Code、Antigravity CLI（`agy`）与 Codex CLI**；零外部 Python 依赖，不覆盖既有配置，不自动运行任何回归。

---

## 全景图：从研究者提问到终稿审稿的一张网

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/architecture.svg">
  <img alt="Economics Research Crew — 从研究者提问到终稿审稿的一张网" src="docs/architecture.svg">
</picture>

> 上图为矢量动态图，随深/浅色主题切换。交互版 [docs/architecture.html](docs/architecture.html)（或[在线预览](https://htmlpreview.github.io/?https://github.com/shjzzzz/Economics-Research-Crew/blob/main/docs/architecture.html)）提供 4 个聚焦视图：**一张网**、**主线 A 证据面**、**主线 B 实证面**、**共享账本·关卡·验证**；点击节点可跳转到源码行，并可导出 PNG / SVG / WebM。

---

## 一、设计主线：一张网、两条主线、四个接口

本项目不是 Skill 合集，而是一条从输入到终稿的连通链路。设计只沿两条主线展开，其余能力都挂在这两条线上：

| 部分 | 做什么 | 落在哪里 |
|---|---|---|
| **入口** | 研究者一句自然语言 → `routing_hint` 匹配 18 组触发词 → 单项任务激活 `/skill`，多阶段任务走 `/research-pipeline` | `CLAUDE.md`、`.claude/routing-triggers.json`、`hooks/routing_hint.py` |
| **主线 A · RAG-wiki 证据面** | 两步摄入写入 wiki → `kb_search` 本地全文召回 → `/query-wiki` 带锚点问答、`/literature-review` 引文核验 → 把 `cite_key` 与 `locator` 送进设计与写作 | `/ingest-source`、`/query-wiki`、`/wiki-lint`、`kb_search.py` |
| **主线 B · AERS 实证面** | 冻结分析计划 → 按计划估计，每个规格登记入账 → 独立审稿查“试了多少、报告多少” → 只用已登记的数与引文写作 → 复现包与投稿前审计 | S1–S12 的 Skill 与 7 个隔离 Agent |
| **共享账本** | 两条主线之间只通过账本交接：`results-ledger.json`（`{{res:id}}`）、`spec-ledger.json`（每个规格）、`citation-map.json`（`[@key]` + 定位锚点）；账本也进入 `kb_search` 索引 | `Meta/` |
| **阶段关卡** | 上一阶段的产物变成下一阶段的机械检查；检查通过后仍由研究者 `gate` 拍板，AI 不能自判放行 | `orchestrator.py`、`paper_tools.py stage_check`、`orchestrator_guard` hook |
| **验证层** | 逐环检查这张网是否连通，并用正反例证明评分细则能区分对错；全部离线、不耗额度 | `tests/evals/run_evals.py`、`kb_search.py eval`、`tests/run.ps1` |

### 关卡机检一览

| 阶段 | 机械检查 | 检查内容 |
|---|---|---|
| S5 实证执行 | `specs_logged`（`results_reproduced` 仅提示） | 规格账本非空（每次估计都登记，含不报告的），且登记结果的 `--spec` 不指向不存在的规格；结果可重复检查在 S5 只提示不阻断 |
| S8 论文大纲 | `no_open_questions` | 不留未答的 `⟦问：…⟧` |
| S10 / S11 成稿与精修 | `citations_resolved`、`results_linked` | 引文都在引文表中，数字都来自结果登记簿 |
| S12 终检 | 以上全部 + `citations_verified`、`claims_aligned`、`package_ready`、`results_reproduced` | 引文已核实、主张与大纲一致、复现包审计通过（README 四节、主脚本、无绝对路径与隐藏字符、无 Office 作者元数据）；正文每个 `{{res:id}}` 经 `results verify` 重读或重跑后一致、输入数据 SHA256 未变，手填数值由研究者 `results confirm`，保密数据由研究者 `results waive` |

---

## 二、主线 B：经济学论文全周期论证脊柱（S1–S12）

| 阶段 | 负责 Skill | 内部 Agent | 核心产出 | 研究者关卡 |
|---|---|---|---|---|
| **S1 问题** | `/research-question` | — | `PROJECT.md`（问题、estimand、理想 vs 准实验、可行性） | 问题与 estimand 是否确定？ |
| **S2 文献** | `/literature-review` | `literature-agent` | 2–4 个争论簇文献矩阵、精确缺口、未核实清单 | 缺口是否真实、文献是否遗漏？ |
| **S3 机制与制度** | `/theory-modeling` + `/tax-policy-analysis` | `theory-agent`、`tax-policy-agent` | 竞争性假说与简化式映射；权威法源（含冲突适用）与政策冲击要素 | 假说能否推出？法源与冲击时点是否核实？ |
| **S4 识别设计** | `/causal-inference-audit` | `causal-inference-agent` | 威胁—检验—证伪矩阵、冻结 `analysis-plan.md`、因果措辞上限 | 识别假设是否可辩护？计划是否冻结？ |
| **S5 实证执行** | `/econometric-analysis` | `econometrics-agent`（唯一 Bash/PowerShell） | 8 步标准产出与 M1→M6 主表、样本瀑布、`analysis-log.md`、每个规格入 `spec-ledger.json`、结果入簿 `results-ledger.json`（机检 `specs_logged`） | 是否按计划执行、记录偏离并完成入簿？ |
| **S6 独立审查** | `/academic-review` | `academic-reviewer`（只读隔离） | 编辑初审三问 + 规格账本核查 + 已读清单 + `F1/M1/m1` + 5 维分 + 分配归宿 + 框架锁定 + 7 类 AI 失效 | 独立审查意见是否完整汇报？ |
| **S7 决策** | `/research-pipeline` | Research Director + 研究者 | 接受进入写作 / 退回某阶段 / 停止 | 致命问题是否解决？（`--fatal-resolved`） |
| **S8 论文大纲** | `/paper-outline` | — | `paper/outline.md`（主张清单、6 步引言蓝图、文献布局、一表一问） | **C1**：论证脊柱与主张清单是否确定？ |
| **S9 引文核验** | `/literature-review` + `paper_tools cite` | — | `Meta/citation-map.json`（Crossref/人工确认 + `locator`）、`citations.bib` | **C2**：引文核验与定位锚点是否可接受？ |
| **S10 受限成稿** | `/paper-draft` | `paper-writer-agent` | `paper/draft.md`（仅 `[@key]`、`{{res:id}}`、`<!-- claim -->`）与对照表 | **C3**：主张覆盖度与经济量级是否准确？ |
| **S11 精修与润色** | `/paper-refine`（+ 可选 `/paper-polish`） | `paper-writer-agent` + `academic-reviewer` | `review verify` 预检、`versions/`、`reviews.json`、`rebuttal-matrix.md`、`polished.md` | **C4**：精修结果与可选润色（`polish check`）是否可接受？ |
| **S12 终检回流** | `/research-pipeline` + `/replication-package` | Research Director + 研究者 | `paper/final.md`、`paper/ai-disclosure.md`、`replication/` 复现包（机检 `package_ready`）、7 类失效清零、`synthesis` 回流 | **C5**：投稿前清单、复现包与知识回流是否完成？ |

---

## 三、主线 A：RAG-wiki 证据面

| Skill / 工具 | 用途 | 核心机制 |
|---|---|---|
| `/ingest-source` | 两步摄入 `03-Literature/_sources/` 来源 | SHA256 去重 → 按 focus（默认项目研究问题）先分析并停下等确认 → 写文献卡（中英双语 tags，提议 `aliases.csv` 同义词）；换 focus 重摄入只追加小节 |
| `kb_search.py` | 全库本地全文召回 | SQLite FTS5 + BM25、中文 bigram、同义词展开、`--expand-links` 沿双链扩展；每条命中带锚点与 `coverage`，弱匹配会提示；结果与规格账本也可检索（`--scope meta`）；`eval` 计算 recall@k 与 MRR |
| `/query-wiki` | 基于知识库与决策记录作答 | 先召回、再读 `Meta/index.md` 与枢纽页、沿 `[[双链]]` 展开；命中只是线索，结论回到原文核对，零命中即答“库内证据不足” |
| `/wiki-lint` | 知识库确定性体检与语义审计 | `wiki_lint.py lint/map` + `paper_tools.py report` + 矛盾/过时/知识回流检查（批准后再修） |

S12 结项后，关键发现经研究者同意写回 `08-Research-Notes/`（`type: synthesis`），下一个项目从更厚的证据面起步。

---

## 四、确定性工具链与 Hooks

| 工具 / Hook | 核心命令或触发时机 | 解决的问题 |
|---|---|---|
| `orchestrator.py` | `init / status / next / artifact / verify / gate / fail / recover / enforce / log` | 机读项目状态机（`STATE.json`）与追加式运行账本（`Meta/run-ledger.jsonl`）；关卡仅由研究者决定 |
| `paper_tools.py` | `cite (add/from-note/import/zotero/zotero-note/open/verify/confirm/check/bib/ris/csl)`、`results (register/import/verify/confirm/waive/render/check)`、`spec (log/summary)`、`claim check`、`review verify`、`refine (start/record/status)`、`polish (scan/check)`、`package check`、`questions`、`report` | 引文与数字机械溯源、EndNote / Zotero 互通（RIS / BibTeX / CSL-JSON 导入导出，Zotero API 只读拉取，导入一律 `unverified`）、`--no-source-reason` 诚实空值、大纲主张覆盖度审计、NFC 审稿引述与推荐文献存在性核验、润色零内容变更证明（含否定词与语气强弱）、规格账本（试了多少 vs 报告多少，选择性报告信号）、结果可重复核对（每个数记下输出文件、单元格、输入数据 SHA256、软件与种子；`results verify` 重读输出，`--rerun --yes` 经研究者同意后用 Stata / R / Python 重跑脚本再比对）、对数点→百分比换算与误写检查、复现包审计（README 四节、主脚本、绝对路径、隐藏字符、Office 作者元数据） |
| `wiki_lint.py` | `lint`、`map [--check]`、`hash` | 确定性体检、生成双地图并刷新 `ERC:MAP`；自动过滤 `paper/versions/` 与多项目 `PROJECT.md` 误报 |
| `kb_search.py` | `index`、`search`、`stats`、`eval` | 全库**本地**全文召回（SQLite FTS5 + BM25，中文字 bigram，`Meta/aliases.csv` 中英同义展开，`--expand-links` 沿双链扩展）；纯标准库、不调用任何模型、不联网；命中带 `cite_key`/标题路径/行号锚点与 `coverage`（命中查询词比例，弱匹配会提示），供 `/query-wiki` 跨文献问答召回；结果登记簿与规格账本也进入索引（`--scope meta`，每条一节），可查“这个数来自哪个规格”；`eval` 用“问题 → 应命中来源”清单算 recall@k 与 MRR；索引放库内 `.erc-index/`（自忽略，可随时重建）；命中只是线索，结论须回到原文核对 |
| `tools/check_upstreams.py` | `list`、`check [--repo NAME] [--out FILE] [--json]`、`mark-audited --repo NAME --sha S [--tag T]` | **零 LLM 额度**一次检测 5 个上游（`academic-research-skills`、`paper-orchestra`、`obsidian-second-brain`、`research-superpowers`、`Auto-Empirical-Research-Skills`），按各自清单映射受影响模块并输出原生适配简报；清单在 `payload/Meta/upstream-ars.json` 与 `tools/upstreams/*.json`；GitHub Actions 每周一自动运行，有更新时开 issue，**只检测，不自动改库** |
| `tools/check_ars_updates.py` | `check [--out FILE] [--json]`、`mark-audited --tag T --sha S` | ARS 单上游检测（`check_upstreams.py` 的底层，保持兼容） |
| `tools/erc_cli.py` + `install.sh` | `install / test / sync / check-ars / check-upstreams` | Windows 11 与 macOS / Linux 跨平台安装、校验与同步，自动适配 `python` / `python3` hook 命令 |
| 7 个可选 Hooks（`-WithHooks`） | `session_context`、`protect_raw`、`orchestrator_guard`、`validate_frontmatter`、`validate_paper`、`routing_hint`、`orchestrator_record` | 会话启动/压缩后自动恢复项目阶段状态；拦截改写原始数据/机读账本/跳阶段/超并发；草稿未知引文/结果即时告警；确定性路由提示与派出记录（均设 `timeout: 10`） |

---

## 五、四层知识库与 Meta 控制面

| 层级 | 目录 | 职责与隔离边界 |
|---|---|---|
| **Tier 0 原始只读层** | `03-Literature/_sources/`、`06-Data/raw/`、库内既有笔记（文献库/知识库） | **不可变**（hook 拦写）；保持原位、按目录检索、不自动视为已核实结论 |
| **Tier 1 跨项目复利层** | `02-Areas/`、`03-Literature/`、`04-Theories/`、`05-Methods/`、`08-Research-Notes/`、`MOC/` | 跨项目复用的结构化文献卡（含 `cite_key` 与三层定位锚点）、机制页、方法页、综合页与枢纽页 |
| **Tier 2 项目执行层** | `01-Research-Projects/<项目>/`、`06-Data/{processed,metadata}/`、`07-Code/{stata,python,R}/` | 仅 `PROJECT.md` 进索引与双链图；`STATE.json`、`analysis-plan.md` 与 `paper/` 过程稿/版本快照不污染全库图谱 |
| **Tier 3 交付与归档层** | `09-Writing/`、`10-Archive/` | `09-Writing/` 仅放**非完整研究项目的独立文稿**（政策简报/评论/讲义）；`10-Archive/` 结项归档 |
| **Meta 控制面** | `Meta/` | **静态规范**（`purpose` / `research-standards` / `collaboration-protocol` / `style-guide` / `mechanism-library` / `ai-tells.json` / `upstream-ars.json`）、**协作账本**（`index` / `log` / `review-queue` / `decisions` / `constraints` / `source-registry`；另有 `aliases.csv` 术语别名表）、**脚本独占机读文件**（`citation-map.json` / `results-ledger.json` / `spec-ledger.json` / `run-ledger.jsonl` / `folder-map.md` / `link-map.md`） |

两张自动生成地图（`Meta/folder-map.md`、`Meta/link-map.md`）及其精简版写入 `CLAUDE.md` / `AGENTS.md` 的 `ERC:MAP` 标记之间，由 `wiki_lint.py map` 生成。

---

## 六、跨系统与多平台支持

| 维度 | 支持对象 | 规则与路径 | Hooks（`-WithHooks` / `--with-hooks`） | 状态 |
|---|---|---|---|---|
| **操作系统** | **Windows 11** | `Install-EconomicsResearchCrew.ps1`（PS 5.1 / 7）或 `python tools/erc_cli.py` | hook 命令优先 `py -3`（无 py 启动器时回退 `python`） | 已双宿主全量测试（475 项；本机安装 `claude` CLI 时 476 项） |
| **操作系统** | **macOS / Linux** | `./install.sh`（封装 `python3 tools/erc_cli.py`，纯 LF） | 自动适配为 `python3` | Python 模拟全量通过 + `bash -n` 通过；实体 macOS 未实机运行 |
| **AI CLI** | **Claude Code** | `CLAUDE.md` + `.claude/ECONOMICS-RESEARCH.md`、`.claude/{skills,agents,scripts,hooks}/`（原生 `effort`/`disallowedTools`/`PowerShell`） | `.claude/settings.json`（全 7 个 hooks，含 `SessionStart` 状态恢复与 `timeout: 10`） | 已测试（含 `claude plugin validate --strict`） |
| **AI CLI** | **Antigravity (`agy`)** | 根 `AGENTS.md`（`ERC:BEGIN…END`，≤24 KB）、`.agents/{skills,agents,scripts,hooks}/` | `.agents/hooks.json`（`protect_raw` + `routing_hint`） | 已冒烟测试 |
| **AI CLI** | **Codex CLI** | 同上 `AGENTS.md` + `.agents/{skills,agents,scripts}/` | 无（原始数据保护靠规则约束） | 仅结构生成，**未运行测试** |

---

## 七、安装与同步

先获取代码并进入仓库目录（以下命令都在仓库根目录运行）：
```bash
git clone https://github.com/shjzzzz/Economics-Research-Crew.git
cd Economics-Research-Crew
```

### Windows 11（PowerShell 5.1 / 7）
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\MyVault" -WhatIf                   # 预演（零写入）
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\MyVault" -Platform all -WithHooks  # 全平台 + hooks（项目名默认取目录名，可加 -ProjectName "名称"）
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\MyVault" -Update                   # 升级：差异写 .new，不覆盖
.\Sync-AgentsMd.ps1 -VaultPath "D:\MyVault"                                           # 同步 CLAUDE.md -> AGENTS.md
.\Test-EconomicsResearchCrew.ps1 -VaultPath "D:\MyVault"                              # 结构校验
```

### macOS / Linux（及跨平台 Python CLI）
```bash
chmod +x install.sh
./install.sh --vault ~/MyVault --dry-run                       # 预演（零写入）
./install.sh --vault ~/MyVault --platform all --with-hooks     # 全平台 + python3 hooks（--name "名称" 指定项目名，默认取目录名）
./install.sh --vault ~/MyVault --update                        # 升级：差异写 .new，不覆盖
./install.sh test --vault ~/MyVault                            # 结构校验
./install.sh sync --vault ~/MyVault                            # 同步 CLAUDE.md -> AGENTS.md
./install.sh check-ars                                                      # 检测 ARS 上游更新
./install.sh check-upstreams                                                # 检测全部 5 个上游更新
```

> 所有安装器只新增不覆盖，改动前自动备份 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`、`AGENTS.md`、`.agents/hooks.json` 至 `_erc-backups/<时间戳>/`。详细操作手册见 [docs/USAGE.md](docs/USAGE.md)。

---

## 八、验证

### 首次只读自检提示词
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```

### 回归与连通性验证
| 验证项 | 命令 | 说明 |
|---|---|---|
| 结构检查 | `.\Test-EconomicsResearchCrew.ps1 -VaultPath <库>` / `./install.sh test --vault <库>` | 校验 7 Agents、18 Skills、frontmatter、全部 `Meta/` 与 Hooks |
| 全量离线回归（Win11） | `pwsh -NoProfile -File tests\run.ps1` 与 `powershell -NoProfile -File tests\run.ps1` | `[1]`…`[20]` 共 475 项（本机安装 `claude` CLI 时 476 项；本地放有 `payload-extras/skills` 时再加 3 项）；`-Section 11,17,18` 按节调试并自动带上前置节；全在临时目录运行，不触碰真实知识库 |
| 网络连通性与评分细则 | `python tests/evals/run_evals.py --chain --selftest` | 清单与 payload 一致、路由覆盖全部 Skill、S1–S12 的负责人/Agent/检查名都存在、Skill 里引用的 CLI 子命令确实存在；7 个评分场景各有正反例 |
| 离线评分已保存回答 | `python tests/evals/run_evals.py --grade <目录>` | 只按评分细则判分，不调用模型 |
| 检索评测 | `python .claude/scripts/kb_search.py eval qrels.json --vault <库> --k 5,10` | “问题 → 应命中来源”清单算 recall@k、MRR 与漏检项 |
| 上游更新检查 | `python tools/check_upstreams.py check` | 零 LLM 额度；无更新返回 `0`，有更新返回 `2` 并输出适配简报，抓取失败返回 `1`；每周一由 GitHub Actions 自动运行 |
| 实机路由评测（可选） | `python tests/routing_eval.py --vault <临时库>` | **消耗 Claude 额度**；覆盖 `tests/routing_cases.json` 16 个路由用例 |

---

## 九、设计借鉴、可选扩展与合规边界

| 来源项目 | 许可证 | 本项目采用方式 | 明确边界 |
|---|---|---|---|
| `llm_wiki` | — | 借鉴“可积累 Wiki”思路（`purpose` / `index` / `log` / 两步摄入 / `lint`） | 原生实现，不引入桌面端或额外 MCP |
| `My-Brain-Is-Full-Crew` | — | 借鉴 hooks 强制执行与回归测试；可选 `-WithUpstream -RepoUrl <地址>` 隔离构建 | 默认不装上游；不自动导入会冲突的上游 dispatcher |
| `google-research/paper-orchestra` | Apache-2.0 | 借鉴受限输入写作、引文表、结果追溯与精修回退理念 | 原生重写，不含其代码（其流水线依赖外部 API 密钥与 LaTeX，与本项目零依赖原则冲突）；保留经济学研究者关卡；清单 `tools/upstreams/paper-orchestra.json` 持续追踪 |
| `Imbad0202/academic-research-skills`（截至 `v3.24.4`） | CC-BY-NC-4.0 | 借鉴苏格拉底防越位、让步门槛、框架锁定、L3 锚点、`data_access_level`、7 类 AI 失效闸门、R&R 矩阵、审稿引述/推荐文献核验、按稿件日期评判、分配归宿核查、`--no-source-reason` 诚实空值与 `Advisory` 分层 | **仅借设计模式并在本项目原生重写，绝不含其任何代码或提示词**；通过 `tools/check_ars_updates.py` 持续追踪 |
| `eugeniughelbur/obsidian-second-brain` | MIT | 已吸收（原生重写）：证据页新鲜度提示、带无答案用例的检索自测；摄入时更新已有页、共享日志等本项目已有对应 | 仅借设计模式；**排除**自主改写、定时自改和需密钥的研究集成，因其与只读层、先报告后修改、`constraints.md` 不得由 AI 自改的规则冲突；本机若已装其插件，项目 Skill 优先；清单 `tools/upstreams/obsidian-second-brain.json` 持续追踪 |
| `leiverkus/research-superpowers`（截至 `v0.49.0`） | MIT | 已吸收（原生重写）：闸门被绕过时记录未满足的条件，近 10 次放行中强制放行超过 30% 时 `wiki_lint` 告警；摄入文献按 focus（默认项目研究问题）阅读，换 focus 重摄入只追加小节 | 仅借设计模式、不拷代码；**排除**人文学科内容、OpenCode/MCP 集成与需密钥的服务；方法类型分关卡、Skill/Agent 契约、来源分级仍是候选；清单 `tools/upstreams/research-superpowers.json` 持续追踪 |
| `academic-humanizer` / `econ-writing-skill` / `humanizer-zh-academic` | MIT | 借鉴语言精修分层、经济学章节公式与中文学术套话分类（`Meta/ai-tells.json`） | 原生重写；**不采用**“降低 AIGC 检测率”目标，AI 参与须如实披露 |
| `brycewang-stanford/Auto-Empirical-Research-Skills`（截至 `e0f61306`） | CC-BY-SA-4.0（仓库默认） | 已吸收（原生重写）：规格账本与选择性报告信号、对数点换算一致性、润色三模式与否定词/语气保真、复现包审计与 `replication-package` Skill、M1→M6 渐进主表、编辑初审、评分细则评测（正反例） | 仅借设计模式，不拷文字与代码，故不受 ShareAlike 约束；**排除** StatsPAI 绑定、降 AIGC 与去水印、p-hacking 搜索引擎、70 余个社区合集与数值基准；清单 `tools/upstreams/aers.json` 持续追踪 |
| 2 个绘图 Skill（必装）：`thu-digitizer`、`scientific-visualization` | MIT（Rimagination；K-Dense Inc.，上游 `K-Dense-AI/scientific-agent-skills`） | 原样收录，各自目录内附上游 `LICENSE` | 未经本项目安全审计；按 MIT 条款保留版权声明 |
| `payload-extras/`（可选 `-WithExtras`） | 多为上游未附许可证 | 仅供用户本机自用的第三方 Skill（含 `publication-chart-skill` / `econ-visualization` / `copyplot` / `tikz`），**不随公开仓库分发**（已 gitignore） | 未经本项目审计、默认不安装、不配置任何 MCP |
