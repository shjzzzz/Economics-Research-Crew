---
name: wiki-lint
description: "Health-check the research wiki: run deterministic lint and map refresh, check active paper report and project synthesis write-back, then audit contradictions, stale claims and missing concept pages. Reports first; fixes only after approval. Use for 知识库体检、检查知识库、断链、孤立页、矛盾、过时内容."
argument-hint: "[optional: folder or topic to focus on]"
data_access_level: redacted
task_type: open-ended
---

# Wiki Lint（知识库确定性体检与语义审计）

## 1. 目标与边界
保障 Tier 1 跨项目知识库与项目入口页的结构健康、双链完整、溯源清晰与语义一致。**默认只报告不修改**，经研究者逐项批准后再执行修复。

## 2. 前置读取
- 读取 `Meta/purpose.md`、`Meta/index.md`、`Meta/review-queue.md`、`Meta/decisions.md`、`Meta/constraints.md`。

## 3. 核心体检流程
1. **确定性结构检查**：运行 `python .claude/scripts/wiki_lint.py lint --vault .`（若库在 git 管控下且需审计既有事实是否被静默删改，可加 `--against <git-ref>`）。
   - 扫描范围：Tier 1 知识目录（`03-Literature`、`04-Theories`、`05-Methods`、`08-Research-Notes`）、`01-Research-Projects/<项目>/PROJECT.md` 入口页与 `09-Writing` 独立文稿；**不扫描**库内旧税法笔记、`paper/versions/` 快照，且不把项目内部草稿误报为全库孤立页或重名页。
   - 核查项：证据页超过 365 天未更新的 `freshness` 警告（只提示复核，不自动改）、frontmatter 完整性与语法、`sources[]` 路径可解析、断链、孤立页、`Meta/index.md` 覆盖、重名主干名、双地图是否漂移、可选 `[source: ... | as-of: ...]` 事实行生命周期标签语法/日期/来源存在性、可选 `<!-- current-picture:start/end -->` 行数（≤30）与列表格式、单页体积（>20 KB / >100 KB），以及 `--against <ref>` 历史事实行守恒（原有事实行只允许追加 `valid_to:` 或 `retracted:`，不得静默删改）。
2. **刷新两张地图**：运行 `python .claude/scripts/wiki_lint.py map --vault .`，同步更新 `Meta/folder-map.md`、`Meta/link-map.md` 以及 `CLAUDE.md`/`AGENTS.md` 中的 `ERC:MAP` 精简区块。
3. **项目与论文健康联动检查**（若库内存在活跃或近期结项项目）：
   - 运行 `python .claude/scripts/paper_tools.py report` 查看引文核验率、结果链接率、主张覆盖度与未答 `⟦问⟧` 数；
   - 检查已进入 S12 或结项的项目是否已把核心机制/综合结论回流至 `08-Research-Notes/`（`type: synthesis`）、`04-Theories/` 或 `05-Methods/`。
4. **语义级深度审计**（模型完成，每条必须附具体页面与段落位置）：
   - **页面间矛盾**：同一研究问题不同结论、同一指标/样本不同口径；
   - **过时与失效**：新摄入文献是否推翻旧笔记判断；中国税法条文是否已修订或废止；
   - **缺失概念页**：被多篇文献反复引用却尚未独立建页的核心机制（`04-Theories/`）或计量方法（`05-Methods/`）；
   - **缺失 `cite_key` / `locator`**：`03-Literature/` 中已核实但尚未补齐 `cite_key` 或三层锚点的文献卡；
   - **长期积压**：`Meta/review-queue.md` 中长期 `open` 的待决项。

## 3b. 周期复盘模式（证据锚定整理；研究者要求“复盘”时）
读最近 7 天的 `Meta/run-ledger.jsonl`、`Meta/log.md`、`Meta/review-queue.md` 与近期 `08-Research-Notes/`（`type: query` 问答笔记）。**原则：问答记录与日志只是线索，不是真相。**
1. **五类失效归因**：将检索或作答暴露的问题归入五类——`WRONG`（回答与原文/卡片矛盾）、`MISS`（误答“证据不足”而原文实有）、`DOCS-ONLY`（仅原始来源有而 Tier 1 文献卡未收录）、`UNPLACED`（实体/术语未入 `Meta/aliases.csv` 导致漏召回）、`CONFLICT`（两来源冲突未并列登记）；同时统计重复失败阶段与别名冲突。
2. **回原文逐条核实**：每条拟议修订必须先回 Tier 0 原文或 Tier 1 文献卡核对具体段落与锚点；无法核实者只记入 `Meta/review-queue.md`，绝不凭问答记录直接入库。
3. **非破坏性修订建议（仅出 diff，绝不自动写入）**：对已核实项输出 diff 建议——纠错或政策废止优先在原事实行追加 `retracted:` / `valid_to:` 并在新行补充正确事实（不删除原行），`UNPLACED` 提议补入 `Meta/aliases.csv`，`CONFLICT` 提议并列写明双方来源，以及对 Skill / `Meta/constraints.md` 的精简修改建议；**全部由研究者逐条批准后再执行**。

## 4. 产出与知识回流
- 输出结构化体检报告：**确定性错误 / 警告 / 项目与论文指标 / 语义问题 / 建议下一步**（含值得追问的新研究问题与待补来源）。
- 仅在研究者批准具体项后逐条修改；整理/体检结束后同步更新 `Meta/index.md`（文件系统与知识系统路由）并在 `Meta/log.md` 追加 `## [YYYY-MM-DD] lint | 范围`（附错误与警告计数）。

## 5. 硬性禁止
禁止未经批准自动改写、移动或删除任何页面；禁止把旧税法笔记纳入批量重构；无法确认是矛盾还是口径差异时记入 `Meta/review-queue.md`，严禁擅自裁决。
