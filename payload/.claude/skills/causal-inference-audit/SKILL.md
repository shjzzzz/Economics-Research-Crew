---
name: causal-inference-audit
description: "Audit a causal design: identification assumptions, threats, inference and robustness."
argument-hint: "[design, model or proposal]"
---

# Causal Inference Audit
1. Define estimand, treatment, outcome, unit, timing, population.
2. State identifying assumptions.
3. Map confounders, selection, anticipation, spillovers, measurement error, concurrent policies.
4. Design-specific checks:
   - DID: parallel trends, timing, anticipation, heterogeneity, comparison group.
   - IV: relevance, exclusion, independence, monotonicity, LATE.
   - RDD: continuity, manipulation, bandwidth, functional form.
   - Synthetic control: donor pool, pre-fit, placebo inference, spillovers.
5. Distinguish diagnostics from proofs.
6. Recommend falsification, sensitivity, robustness checks.
7. State the strongest defensible causal wording.
