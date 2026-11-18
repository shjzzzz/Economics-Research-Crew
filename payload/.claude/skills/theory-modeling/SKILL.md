---
name: theory-modeling
description: "Build or audit a formal economic model, mechanism, comparative statics and testable hypotheses. Use for 理论模型、建模、机制分析、均衡推导、比较静态、博弈模型、委托代理、研究假说."
argument-hint: "[mechanism or research question]"
data_access_level: verified_only
task_type: open-ended
---

# Theory Modeling Workflow
## 0. 苏格拉底机制护栏
- 研究者处于探索态（尚未确定核心机制）时，只追问主体、约束、信息结构与制度边界，不替研究者拍板核心机制假设；若明确要求 AI 拟定机制候选，先输出 `[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]` 并标注为 AI 建议。

## 1. 建模步骤
1. Define question and mechanism.
2. Specify agents, decisions, information, timing, constraints, institutions.
3. Write objectives and constraints; derive choices and equilibrium step by step.
4. Check feasibility, signs, units, boundary cases; comparative statics.
5. Give intuition; derive testable implications.
6. List strong or institutionally implausible assumptions.

No proposition without a derivation.
