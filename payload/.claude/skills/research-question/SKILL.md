---
name: research-question
description: "Define and refine an economics research question, estimand, contribution and feasible design. Use for 选题、确定研究问题、收敛题目、可检验的研究问题、estimand、研究可行性."
argument-hint: "[research topic or initial question]"
data_access_level: verified_only
task_type: open-ended
---

# Research Question Development
## 0. 意图识别与苏格拉底非生成护栏
- 先判断研究者意图：**探索型**（仍在发散/犹豫/追问“值不值得做”）vs **目标型**（已选定方向，要求结构化收敛与评估）。
- 探索型阶段只做概念澄清、边界区分、归纳研究者已表达的方向并反问，**不代拟、代排或代选研究问题与假说**，也不得在未收敛时强行收口。
- 仅当研究者明确要求 AI 提出候选问题时，先显式输出 `[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]`，再给出至多 3 个候选并标注为 AI 建议。
- 对话健康自检：警惕连续顺从、回避识别/数据冲突或过早收敛。

## 1. 收敛步骤
1. Restate topic; distinguish topic, problem, question, estimand.
2. Identify unit, population, outcome, treatment/exposure, time, institutional setting.
3. Generate at most three candidate questions (only after explicit exit or in goal-directed mode).
4. Assess importance, literature gap, data feasibility, identification feasibility, contribution.
5. State the minimum evidence needed to proceed.
6. Recommend one question with reasons and unresolved risks.

No novelty claim without a documented literature search. Save a brief only after the user approves the question.
