---
name: causal-inference-audit
description: "Audit an economics causal identification strategy (DID, IV, RDD, Bunching, Synthetic Control): estimand, assumptions, threats, modern diagnostics, threat-to-test matrix and permissible causal wording. Use for 识别策略、因果识别、DID、双重差分、事件研究、IV、工具变量、RDD、断点回归、聚束、平行趋势、内生性、稳健性设计."
argument-hint: "[design, model or proposal]"
data_access_level: redacted
task_type: open-ended
---

# Causal Inference Audit（S4：识别审查、威胁—检验矩阵与措辞上限）

## 1. 目标与边界
在跑回归之前审查研究设计的因果可信度，产出**可冻结的分析计划核心**（威胁—检验—证伪矩阵 + 允许的因果措辞上限）。**本 Skill 只审查设计，绝不在此直接跑回归**；识别获研究者确认后才交给 S5 `/econometric-analysis`。

## 2. 前置读取
- 读取 `Meta/research-standards.md`、`05-Methods/` 既有方法笔记。
- 若处于项目 S4：读取 `PROJECT.md`、S3 理论假说与制度/政策冲击要素表（发文日/生效日/门槛/试点表/同期改革）。

## 3. 核心流程与委派规则
- **委派授权**：复杂识别诊断与替代设计比对可派出 `causal-inference-agent`（按 `Templates/handoff.md` 交接，一次一个）。
1. **锁定目标 Estimand**：明确处理变量 $D$、结果变量 $Y$、观测单位、时间点、目标人群与估计量（ATT / ATE / LATE / 局部弹性）。
2. **六项必答识别核查**（逐条给出制度/数据依据，不得敷衍）：
   - **冲击外生性**：政策为何在此时/此地/此类主体发生？谁选择了处理？
   - **分组可比性**：处理组与对照组如何界定？是否存在结构性不可比或污染对照（contaminated controls）？
   - **同期政策/冲击**：同一窗口内是否存在其他财税、监管或宏观冲击？
   - **预期效应（Anticipation）**：政策发文日早于生效日时，主体是否提前调整？
   - **样本选择与流失**：处理本身是否导致企业进入/退出、登记类型切换或申报口径变化？
   - **推断与聚类层级**：处理在哪一层级分配，标准误是否在该层级聚类？聚类数是否过少（需野靴法 Wild Cluster Bootstrap）？
3. **分方法现代应用微观计量诊断**：
   - **DID / 交错 DID**：平行趋势（强调“事前系数不显著 ≠ 平行趋势成立”）、事前检验力与敏感性（Rambachan-Roth / HonestDiD）、交错处理异质性与负权重（Goodman-Bacon 分解、Callaway-Sant'Anna、Sun-Abraham、stacked DID）、溢出与 SUTVA、坏控制排查。
   - **IV**：相关性与弱工具检验（有效 F 统计量 Olea-Pflueger、弱工具稳健 Anderson-Rubin 置信区间）、排他性约束（含零一阶段/简化式安慰剂检验）、单调性与 LATE 依从者画像；份额移动（Shift-Share / Bartik）区分外生份额（GPSS）与外生冲击（BHJ）。
   - **RDD / 税收聚束（Bunching）**：配置变量连续性与操纵密度检验（McCrary / CJM）、甜甜圈断点（Donut-hole）、局部多项式带宽与核函数敏感性、税率拐点/缺口（Kink/Notch）的优化摩擦与反事实分布假设。
   - **合成控制（SCM / SDID）**：备选池排除受污染单位、事前拟合质量、空间/时间安慰剂推断、权重稀疏性。
4. **严格区分“诊断”与“证明”**：将每条核心假设标为“可检验 / 部分可检验 / 不可检验”，分离内部有效性与外部有效性。
5. **构建威胁—检验—证伪矩阵**：把每一条具体识别威胁映射到对应诊断/稳健性/安慰剂检验，并事前写明**什么结果会证伪主结论**（直接写入 `Templates/analysis-plan.md` 与后续 S8 论文第 7 节）。
6. **系数经济含义与因果措辞上限**：明确核心系数 $\beta$ 的单位、适用人群、经济量级合理区间，并给出本设计**最高可辩护的因果措辞上限**（因果 / 条件因果 / 仅相关）。

## 4. 产出与知识回流
- 输出：识别审查报告 + 基于 `Templates/analysis-plan.md` 的预设分析计划（经研究者确认后冻结，作为 S4 产物与 S8 措辞上限依据）。
- 通用方法论经验可沉淀至 `05-Methods/`（`type: method`），更新 `Meta/index.md` 与 `Meta/research-log.md`。

## 5. 硬性禁止
禁止在本 Skill 中跑回归或改数据；禁止把固定效应或事前系数不显著当成因果证明；禁止由 AI 单方面拍板识别策略或放宽因果措辞上限（A3 事项）。
