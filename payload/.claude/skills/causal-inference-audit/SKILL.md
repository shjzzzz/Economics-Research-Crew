---
name: causal-inference-audit
description: "Audit a causal design: estimand, identification assumptions, threats, inference and robustness. Use for 识别策略、因果识别、DID、双重差分、事件研究、IV、工具变量、RDD、断点回归、平行趋势、内生性、稳健性设计."
argument-hint: "[design, model or proposal]"
---

# Causal Inference Audit
1. Define estimand, treatment, outcome, unit, timing, population.
2. State identifying assumptions, and answer explicitly:
   - Is the policy shock exogenous to the outcome (who chose treatment, and why)?
   - How are treatment and control groups defined, and is the comparison credible?
   - Are there concurrent policies or shocks over the same window?
   - Is there anticipation (announcement before implementation)?
   - Is there sample selection or attrition caused by treatment?
   - At what level is treatment assigned, and are standard errors clustered there?
3. Map confounders, selection, anticipation, spillovers, measurement error, concurrent policies.
4. Design-specific checks:
   - DID: parallel trends, timing, anticipation, heterogeneity, comparison group.
   - IV: relevance, exclusion, independence, monotonicity, LATE.
   - RDD: continuity, manipulation, bandwidth, functional form.
   - Synthetic control: donor pool, pre-fit, placebo inference, spillovers.
5. Distinguish diagnostics from proofs.
6. Recommend falsification, sensitivity, robustness checks.
7. Interpret the estimand: what does the coefficient (e.g. beta on Treat x Post) mean economically, in which units, for which population, and is its magnitude plausible?
8. State the strongest defensible causal wording.

Do not run regressions here; this Skill audits the design. Hand execution to `/econometric-analysis` only after the design is approved.
