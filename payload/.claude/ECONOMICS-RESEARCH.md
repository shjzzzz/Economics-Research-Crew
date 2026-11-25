# Economics Research Crew — 核心研究与路由协议

> 路由、论证主线、编排、写作约束与证据标准的唯一正本；库结构与红线见 `CLAUDE.md`、`Meta/vault-map.md`。

## 1. 意图路由表（18 Skill，7 Agent）
| 阶段/角色 | 用户意图（示例） | 主 Skill | 授权 Agent |
|---|---|---|---|
| S1 选题 | 选题、收敛研究问题、定题、确定 estimand | `/research-question` | — |
| S2/S9 文献 | 文献综述、梳理文献、研究缺口、文献矩阵、找文献、Zotero/EndNote | `/literature-review` | `literature-agent` |
| S3 理论 | 理论模型、机制分析、均衡、比较静态、假说推导 | `/theory-modeling` | `theory-agent` |
| S3 税收政策 | 税法适用、税目、税制、征管、遵从、税负归宿、政策评估 | `/tax-policy-analysis` | `tax-policy-agent` |
| S4 识别 | 识别策略、DID/IV/RDD/聚束、平行趋势、内生性、稳健性设计 | `/causal-inference-audit` | `causal-inference-agent` |
| S5 计量 | 数据清洗、变量构造、回归、复现论文、代码审计、异质性 | `/econometric-analysis` | `econometrics-agent`（唯一可用 Bash/PS） |
| S6 审稿 | 审稿、匿名审稿、挑刺、审查研究设计或稿件 | `/academic-review` | `academic-reviewer`（隔离） |
| S8 大纲 | 论文大纲、论文框架、主张清单、贡献定位、引言布局 | `/paper-outline` | — |
| S10 起草 | 起草论文、写初稿、分节写作、把大纲写成正文 | `/paper-draft` | `paper-writer-agent` |
| S11 精修/R&R | 精修、按审稿意见修改、返修、R&R、多轮修改 | `/paper-refine` | `paper-writer-agent` / `academic-reviewer` |
| S11b 润色 | 润色、去 AI 味、语言精修、文风校准、消除套话 | `/paper-polish` | — |
| S12 复现 | 复现包、可得性声明、双盲清理 | `/replication-package` | — |
| 绘图（MIT） | 出版级期刊图（Python）、从图表图片/PDF 提取数据 | `/scientific-visualization`、`/thu-digitizer` | — |
| 知识库摄入 | 摄入文献/来源、处理 `00-Inbox`/`_sources` | `/ingest-source` | — |
| 知识库查询 | 知识库里有什么、根据知识库回答、查已有文献 | `/query-wiki` | — |
| 知识库体检 | 检查断链/孤立页/矛盾/过时 | `/wiki-lint` | — |
| 总控（S1–S12） | 完整做研究、规划并推进、继续上次的研究 | `/research-pipeline` | 按阶段授权（以上全部） |

## 2. 论证主线（S1–S12）
每篇实证/制度论文维持一条可追溯的因果主线（细则见 `Meta/research-standards.md`）：
S1 问题与 estimand → S2 文献争论与缺口 → S3 竞争机制与制度冲击 → S4 威胁-检验矩阵、冻结计划与措辞上限 → S5 可复现估计、样本瀑布与设定/结果账本 → S6 独立审稿 + 7 类 AI 失效关卡 → S7 研究者决定继续/返回/停止 → S8 主张驱动大纲 → S9 带定位的已核引文 → S10 受约束分节起草 → S11 清单式精修/R&R（可选 `/paper-polish`）→ S12 终检、复现包、AI 披露与知识库回写。

质量回路：研究 Agent 提出 → `econometrics-agent` 执行 → `academic-reviewer` 只凭产物独立质疑 → 总控与研究者裁决。Fatal 问题阻断通过；代码能跑不等于可跳过 S4。

## 3. 编排层
`/research-pipeline` 只经 `python .claude/scripts/orchestrator.py`（`init`、`status`、`next`、`artifact`、`verify`、`gate`、`fail`、`recover`、`enforce`、`log`）维护 `01-Research-Projects/<项目>/STATE.json` 与 `Meta/run-ledger.jsonl`。
- **研究者关卡**：不得凭 AI 判断执行 `gate --decision pass`；必须带 `--note`。
- **重试与并发**：每 Agent 每阶段最多重试 2 次，之后停止并报告；默认并发 1（S3 为 2，上限 3）。Claude Code 由 hooks 强制顺序、重试、并发与文件保护；agy/Codex 自觉遵守。

## 4. 论文写作与人机协作（S8–S12）
遵循 `Meta/collaboration-protocol.md`（A0–A3、C1–C5）与 `Meta/style-guide.md`（CLI 细节见 `/literature-review`、`/paper-draft`、`/paper-refine`、`/paper-polish`）：
- **受约束输入**：引文用 `Meta/citation-map.json` 的 `[@key]`（`locator` 与 `claim_scope` 防 L3 错配）；数字用 `Meta/results-ledger.json` 的 `{{res:id}}`（无来源须 `--no-source-reason`；对数点用 `:pct`），经 `--spec` 链到 `Meta/spec-ledger.json`（记录每个设定）；数字须能经 `results verify` 重现（手填由研究者 `results confirm`）；结果段带 `<!-- claim: Cn -->`；缺口写 `⟦问：…⟧`（答复 `⟦答：…⟧`），绝不编造。
- **文献管理**：`paper_tools.py cite import|zotero|ris|csl|bib|open|zotero-note` ↔ EndNote/Zotero（`ZOTERO_API_KEY` 只放环境变量，只做 GET 拉取，`zotero-note --yes` 须研究者同意）；导入一律 `unverified`（中文 `manual`），从不自动确认。
- **精修（`/paper-refine`）**：`academic-reviewer` 列出所读文件，按稿件日期评判文献，检查分配归宿、Frame-Lock 与让步阈值（≥4/5，不得连续让步），输出编号 `F1/M1/m1` 与 5 项评分（`ident, contrib, inst, consist, write`）。修改前先跑 `paper_tools.py review verify`。复审按清单计数（`--carried-*`/`--new-*`）；仅当 Fatal ≤ 上轮、Major 减少（或持平且总分不降）、维度一致且无单项降 ≥2 时接受。新增分析进 `Meta/review-queue.md`。
- **润色（`/paper-polish`）**：内容定稿后才做；`polish check` 证明引文、`{{res}}`、主张、问答标记、数字与否定词未变。不得用于规避 AI 检测；AI 使用披露写入 `paper/ai-disclosure.md`。
- **隔离与失效关卡**：每个 Skill/Agent 声明 `data_access_level`（`raw`/`redacted`/`verified_only`）；`Meta/mechanism-library.md` 只提供可检验假说而非证据；S6/S12 须通过 7 类 AI 失效关卡。

## 5. 计量、税法与证据纪律
- **计量**：区分相关、预测与因果；报告 estimand、假设、聚类层级、样本瀑布、经济量级（相对均值/标准差或弹性）与软件版本。做现代诊断：交错 DID（CS/SA/Bacon/HonestDiD）、IV（有效 F/AR/排他性/LATE）、RDD/聚束（连续性/操纵/带宽）。固定效应或前趋势不显著都不能证明因果；不得静默筛样本、缩尾或 p-hacking。
- **证据与税法**：区分事实、模型解释与假说；保留 DOI/URL 与页/表/式定位。中国税法须注明发文机关、文号、发布/生效日期、修订/废止状态、适用范围与冲突适用顺序（见 `tax-policy-agent`）。

## 6. 知识库维护
- 会话开始读 `Meta/purpose.md`（为空则提醒研究者，不得自定方向）、`Meta/decisions.md` 与 `Meta/constraints.md`。
- 路由与更新：`Meta/index.md` 同时路由文件系统（`Meta/folder-map.md`）与知识图谱（`Meta/link-map.md` 枢纽 → `[[双链]]`）；每次摄入/体检/整理都更新 `Meta/index.md` 并追加 `Meta/log.md`。既有笔记按文件夹检索，不走双链图。
- Tier 1 frontmatter：`type`（`literature|theory|method|synthesis|query|research-project|dataset|analysis-plan|analysis-log`）、`sources`、`updated`、`verification`（`verified|unverified`）；文献卡加 `cite_key`。
- 两步摄入（`/ingest-source`）：先分析并等批准 → 写入并交叉链接 → 更新 `Meta/index.md`、`Meta/source-registry.md`（SHA256）与 `Meta/log.md`；矛盾记入 `Meta/review-queue.md`。
- 确定性检查与地图：先 `python .claude/scripts/wiki_lint.py lint --vault .`，再 `map`。S12 后经研究者同意，把关键发现沉淀到 `08-Research-Notes/`（`type: synthesis`）。
