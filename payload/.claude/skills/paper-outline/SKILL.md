---
name: paper-outline
description: "Turn frozen research outputs (design, analysis plan, registered results) into a structured economics paper outline with an Argument Spine: claim list, 6-move introduction blueprint, competing-mechanism plan, threat-to-test robustness mapping, literature clusters and table storytelling plan. Use for 论文大纲、论文框架、论文结构、写作大纲、主张清单、贡献定位、引言怎么布局."
argument-hint: "[project folder, target journal template]"
data_access_level: verified_only
task_type: open-ended
---

# Paper Outline（S8：经济学论文论证脊柱与架构设计）

## 1. 目标与边界
把已经冻结的 S1–S7 研究产物变成**可机械核查的论文架构**。大纲不写正文，只锁定五件事：核心主张与证据边界、6 步引言蓝图、竞争机制与识别威胁的章节映射、文献宏观/微观布局、待研究者裁决项（`⟦问：…⟧`）。**不写正文、不在此登记引文、不新增实证分析。**

## 2. 前置读取（不满足就停下说明）
- 检查项目已有 `PROJECT.md`、冻结的 `analysis-plan.md`（含威胁—检验矩阵与因果措辞上限）、`analysis-log.md`，以及已登记的 `Meta/results-ledger.json`（运行 `python .claude/scripts/paper_tools.py report` 核查）。若结果登记簿为空，只写到“数据与实证策略”，暂停并提示先在 S5 登记结果。
- 读取 `Meta/purpose.md`、`Meta/decisions.md`、`Meta/style-guide.md`、`Meta/mechanism-library.md`，以及研究者指定的期刊骨架 `Templates/venues/*.md`（篇幅与格式要求一律以研究者核对期刊官网为准）。

## 3. 核心架构设计流程
1. **主张清单（Claim List）——全稿机械校验基线**：
   - 每条一行：`C编号 | 主张 | 类型（描述/因果/机制/政策含义）| estimand | 证据（结果登记簿 id）| 允许的措辞强度 | 局限与边界`。
   - 因果主张措辞强度不得高于 `analysis-plan.md` 与 `/causal-inference-audit` 冻结上限；识别未获确认的标“仅相关性/关联”；机制检验无法排除竞争解释的标“与……一致/推测”。
   - **无 `res:id` 支撑的主张标“无证据”**，禁止直接入稿，改写成 `⟦问：…⟧` 交研究者决定（补分析 / 降级 / 删除）。
2. **经济学 6 步引言蓝图（顶刊标准）**：
   - 逐一列出引言 6 个构件的要点：① 问题与现实/理论张力（去“近年来”套话）→ ② 本文数据与准实验识别 → ③ 核心定量发现（锚定 `{{res:…}}` 与经济量级）→ ④ 机制与异质性 → ⑤ 对 2–3 支文献的边际贡献（写清前人局限与本文增量）→ ⑥ 紧扣实质内容的结构安排。
3. **章节与论证脊柱映射**（按期刊模板调整结构，子节成对不留孤立子节）：
   - **制度背景**：只写服务于“政策外生性、处理/对照边界、预期窗口、同期改革排查”的制度事实与法源，不堆砌百科式介绍。
   - **理论与竞争性机制**：对照 `Meta/mechanism-library.md`，列出主机制与竞争机制的**排他性可检验推论**及对应检验表。
   - **数据与实证策略**：样本瀑布、核心变量口径、估计方程、聚类层级与现代估计量。
   - **基准结果**：每条要点必须指向具体 `{{res:id}}` 并注明经济量级口径（占均值/标准差比例或弹性），禁止写“描述基准结果”式空话。
   - **稳健性与机制**：把 S4 冻结的**识别威胁—检验—证伪矩阵**一一映射到本节，杜绝无目的堆表；异质性分组须紧扣理论预测。
   - **结论**：简短重述核心发现、明确外部有效性边界（ATT/LATE 适用范围、一般均衡局限）与有证据支撑的政策含义。
4. **文献双层布局（避免引言与文献综述重复引用）**：
   - **引言（宏观，约 10–20 篇）**：政策重要性、核心缺口（严格限定在本文数据与设计可支持范围）与奠基/综述文献。
   - **相关文献（微观，2–4 个争论簇）**：每簇写清 ① 簇名 ② 检索任务 ③ **局限假设**（方法在何处失效）④ 针对局限的检索式 ⑤ **与本文的桥接**。
   - **引文提示 `citation_hints`**：每个数据集、关键估计量、指标、法源、核心机制均给提示，格式 `作者（确切标题）` 或 `待检索：<描述>`（法规写文号与生效日），**严禁猜作者或标题**；交 S9 `/literature-review` 与 `paper_tools.py cite add/from-note` 登记。
5. **图表叙事计划**：一表一问——每张表/图注明编号、它在论证链中回答的**唯一核心问题**、对应主张、来源 `res:id` 与注释要点。

## 4. 产出与停点（C1 检查点）
- 写引言八段或理论模型一节的结构时参照 `Templates/intro-model-blueprint.md`（只给结构，不提供内容）。
- 按 `Templates/paper-outline.md` 写入 `01-Research-Projects/<项目>/paper/outline.md`。
- 在流程中运行 `python .claude/scripts/orchestrator.py artifact <路径>` 与 `verify`；向研究者汇报主张清单、无证据主张与未决 `⟦问⟧`。**C1 检查点：必须等研究者表态后再推进至 S9/S10。**

## 5. 硬性禁止
禁止在本 Skill 写正文段落；禁止凭记忆登记引文或猜作者标题；禁止把无 `res:id` 支撑的猜想包装为大纲核心主张；禁止新增分析。
