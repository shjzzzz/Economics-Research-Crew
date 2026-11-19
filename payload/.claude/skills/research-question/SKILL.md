---
name: research-question
description: "Define and refine an economics research question, estimand, contribution and feasible design with Socratic non-generation guardrails. Use for 选题、确定研究问题、收敛题目、定题、可检验的研究问题、estimand、研究可行性."
argument-hint: "[research topic or initial question]"
data_access_level: verified_only
task_type: open-ended
---

# Research Question（S1：选题收敛与 Estimand 定义）

## 1. 目标与边界
把宽泛的研究主题收敛为**可检验、可识别、有明确经济重要性**的研究问题与 estimand。本 Skill 只界定问题、理想实验与可行准实验；**不替代文献检索、不设计完整计量代码、不编造新颖性宣称**。

## 2. 前置读取
- 读取 `Meta/purpose.md`（未填写则提醒研究者，不代设研究方向）与 `Meta/decisions.md`。
- 若已有初步文献或笔记，先查 `Meta/index.md` 确认库内相关背景。

## 3. 核心流程与苏格拉底防越位护栏
### 3.0 意图识别（必须先做）
- **探索型**（研究者仍在发散/犹豫/追问“值不值得做”）：仅做概念澄清、边界区分、归纳研究者已表达的方向并提出尖锐反问，**不代拟、代排或代选研究问题与假说**，也不得过早收口。
- **目标型**（研究者已选定方向并要求收敛评估，或明确要求 AI 提出候选）：先显式输出 `[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]`，再给出至多 3 个候选并标注为 AI 建议。
- **对话健康自检**：警惕连续顺从、回避识别/数据硬伤或用“有意思/有意义”替代真实缺口。

### 3.1 六步经济学收敛法
1. **剥离层级**：区分研究主题（Topic）→ 现实/理论张力（Problem）→ 具体问题（Question）→ 目标估计量（Estimand：ATT / ATE / LATE / 弹性）。
2. **六要素锁定**：观测单位（Unit）、目标总体（Population）、结果变量 $Y$、处理/冲击 $D$、时间窗口、制度情境。
3. **理想实验 vs 可行准实验**：先写“如果有无限预算，理想随机实验是什么”，再对照现实中可能的外生冲击/门槛/政策变化，标出二者差距（内部与外部有效性权衡）。
4. **经济重要性与文献定位检验**：回答“So what?”——哪怕系数显著，该效应在财政/福利/行为上是否重要？它试图介入哪支具体文献争论？
5. **可行性四维评估**：理论/政策重要性、文献缺口（未检索前仅标“待核实”）、数据可得性、识别可行性。
6. **最小推进证据与收敛建议**：给出推进到 S2/S4 所需的最小证据；目标型模式下推荐 1 个主问题并单列未解决的硬风险。

## 4. 产出与知识回流
- 仅在研究者批准定题后，用 `Templates/research-project.md` 写入 `01-Research-Projects/<项目名>/PROJECT.md`（S1 产物），更新 `Meta/index.md` 与 `Meta/research-log.md`。
- 下游交接：把锁定后的 6 要素与待查文献缺口交给 S2 `/literature-review`。

## 5. 硬性禁止
未经有记录的文献检索不得宣称“首次/填补空白”；探索阶段不得替研究者拍板研究问题；不得在未获确认前写入项目文件。
