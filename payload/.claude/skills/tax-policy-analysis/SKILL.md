---
name: tax-policy-analysis
description: "Analyze tax law, administration, compliance, incidence, legal conflict resolution and policy-shock identification elements from authoritative sources. Use for 税法适用、税目判定、税收政策分析、税收征管、税收遵从、税负归宿、财税制度、政策评估."
argument-hint: "[policy, rule or institutional question]"
data_access_level: redacted
task_type: open-ended
---

# Tax Policy Analysis（S3：税法制度、冲突适用与政策冲击抽取）

## 1. 目标与边界
基于权威法源剖析税制设计、税收征管、遵从行为与税负归宿，并将复杂的中国财税制度转化为**可供 S4 因果识别使用的精确政策冲击要素**。**不编造法条文号，不将库内旧税法笔记自动视为现行有效法。**

## 2. 前置读取
- 读取 `Meta/purpose.md`、`Meta/source-registry.md`（优先官方源：国家法律法规数据库、国家税务总局）。
- 可按文件夹检索库内既有旧税法笔记作为线索（排除 `.claude`、`.agents`、`_vendor`、`_erc-*`、`06-Data`、`07-Code`），但必须核验现行时效。

## 3. 核心流程与委派规则
- **委派授权**：复杂法源查证、税法冲突适用与归宿分析可派出 `tax-policy-agent`（按 `Templates/handoff.md` 交接，一次一个；严格执行其“基本原则 + 6 项适用原则 + 6 步冲突处理顺序”）。
1. **锁定制度与法律关系**：税种/政策工具、纳税主体、扣缴义务人、分析税期、管辖层级与核心问题。
2. **权威法源核验与效力层级**：区分法律、行政法规、部门规章、规范性文件、司法解释与学理评论；逐条记录**发文机关、文号、发布日期、生效日期、修订/废止状态、过渡条款与适用范围**；多份文件冲突时严格按“法律优位 → 特别法优于普通法 → 新法优于旧法（先读过渡条款与不溯及既往）”排序，无法确认的标 `待定/unverified`。
3. **五层剥离**：明确区分法律形式、实质经济关系、法定纳税义务、税款代扣/汇算环节与最终经济归宿（Economic Incidence），严禁仅凭平台合同标签（如“个体户/承揽”）反推法律定性。
4. **行为渠道映射**：梳理申报、避税、逃税、劳动力供给、投资、组织形式切换（如个人/个体户/小微企业转换）与税负转嫁渠道，对照 `Meta/mechanism-library.md`。
5. **效率、公平与征管评估**：评估无谓损失、分配效应、征管成本、纳税人遵从成本与执行约束（如第三方信息可见度、地方征管弹性）。
6. **政策冲击识别要素抽取（直通 S4 `/causal-inference-audit`）**：
   - 精确区分**政策宣布/发文日**与**正式生效日**（用于判断预期效应 Anticipation）；
   - 列出**法定门槛/税率级距/优惠资格条件**（用于判断 RDD / Bunching 聚束设计）；
   - 列出**分批试点地区/行业时间表**（用于判断交错 DID 及处理组边界）；
   - 排查**同一时间窗口内的同期财税或监管改革**（用于识别混淆冲击）。

## 4. 产出与知识回流
- 输出：法源与效力表（含证据等级：直接 / 部分 / 解释性）、机制与归宿分析、政策冲击识别要素表、需官方确认清单。
- 涉及论文引用时，以 `python .claude/scripts/paper_tools.py cite add --type legal --doc-no "…" --effective YYYY-MM-DD` 登记，交研究者人工 `cite confirm`；制度分析笔记可沉淀至 `08-Research-Notes/` 或项目目录。

## 5. 硬性禁止
严禁编造法条文号或生效日期；严禁跳过过渡条款直接追溯适用新法；严禁仅依据合同名称判定所得项目或劳动关系；不得将未核实的本地旧笔记当现行有效法规引用。
