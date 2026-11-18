---
name: paper-outline
description: "Turn frozen research outputs (design, analysis plan, registered results) into a structured economics paper outline: claim list with evidence, section plan, literature positioning plan, table/figure plan. Use for 论文大纲、论文框架、论文结构、写作大纲、主张清单、贡献定位、引言怎么布局."
argument-hint: "[project folder, target journal template]"
data_access_level: verified_only
task_type: open-ended
---

# Paper Outline（论文架构：先有大纲，再写正文）

目标：把已经冻结的研究产物变成**可检查的论文架构**。大纲不写正文，只回答：我主张什么、证据在哪、各节写什么、文献怎么布局、哪些地方还要研究者决定。

## 0. 前提（不满足就停下说明）
- 有 `PROJECT.md`、冻结的分析计划、分析日志，且**结果已登记**：`python .claude/scripts/paper_tools.py results ...`。结果登记簿 `Meta/results-ledger.json` 为空时，不写结果与讨论章节，只写到“数据与实证策略”，并提示先登记结果。
- 读 `Meta/purpose.md`、`Meta/style-guide.md`、`Meta/mechanism-library.md`，以及目标期刊的 `Templates/venues/*.md`（若研究者指定了期刊）。期刊的篇幅与格式要求以研究者核对官网后的为准，不凭记忆。

## 1. 主张清单（Claim list）——大纲的核心
每条主张一行：`C编号 | 主张 | 类型（描述 / 因果 / 机制 / 政策含义）| estimand | 证据：结果登记簿 id | 允许的措辞强度 | 局限`。
- 类型为“因果”的主张，措辞强度必须以 `/causal-inference-audit` 的结论为上限；识别未通过的写成“相关/关联”。
- **没有登记结果支撑的主张，标“无证据”，不得进入正文当作结论**；写成 `⟦问：…⟧` 交研究者决定（补分析、降级为推测，或删除）。
- 机制类主张对照 `Meta/mechanism-library.md`：每个机制要有可检验含义；找不到就如实写“仅为解释性推测”。

## 2. 结构（按期刊模板调整）
引言（含贡献定位）→ 制度背景 → 理论框架与假说（行为机制）→ 数据与样本 → 实证策略 → 结果 → 稳健性、异质性与机制检验 → 结论与政策含义。每节写：本节要回答的问题、对应主张编号、要点（**指向具体来源**，如“用 `{{res:tbl2.DID.coef}}` 报告基准估计，并说明单位”，而不是“描述结果”）。子节要成对出现，不留孤立子节。

## 3. 文献布局（引言与相关文献分工，避免引用重复）
- **引言（宏观）**：政策重要性与问题缺口的证据、综述与奠基文献，约 10–20 篇；缺口陈述必须限定在本文数据与设计能支持的范围内。
- **相关文献（微观，2–4 个簇）**：每簇写 ① 簇名 ② 该簇最新进展的检索任务 ③ **局限假设**（该簇方法可能在哪里失效）④ 针对该局限的检索式 ⑤ **与本文的桥接**（本文如何处理该局限）。
- **引文提示 `citation_hints`**：每个数据集、关键估计量（如 DID 的现代估计量）、指标、制度文件、核心机制概念都要有提示。格式 `作者（确切标题）`；不确定作者时写 `待检索：<描述>`，**禁止猜作者或标题**。法规写文号与生效日期。
- 这些提示是 `/literature-review` 与 `paper_tools.py cite add` 的输入；大纲阶段**不登记引文**。

## 4. 图表计划
每个表/图一行：编号、目的、来源结果 id、需要的样本说明与注释。

## 5. 输出与停点
- 用 `Templates/paper-outline.md` 写到 `01-Research-Projects/<项目>/paper/outline.md`。
- 在流程中：`orchestrator.py artifact <路径>`，`verify`，然后向研究者汇报：主张清单（逐条含证据与措辞强度）、无证据主张、未决 `⟦问⟧`。**C1 检查点：等研究者表态后才推进。**
- 不要在本 Skill 里写正文、不要登记引文、不要新增分析。
