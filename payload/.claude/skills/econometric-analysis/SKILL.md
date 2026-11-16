---
name: econometric-analysis
description: "Plan, implement, inspect or reproduce an econometric analysis in Stata, R or Python."
argument-hint: "[dataset, model or task]"
---

# Econometric Analysis Workflow
1. Inspect project files, data dictionary, raw-data provenance.
2. Audit grain, keys, duplicates, missingness, coverage, attrition.
3. Confirm outcome, treatment, controls, FE, sample, weights, inference level.
4. Write an analysis plan (Templates/analysis-plan.md) before execution.
5. Implement code; preserve raw inputs.
6. Run scripts only after confirming inputs/outputs.
7. Check sample counts, coefficient scale, SEs, convergence.
8. Produce tables, figures, logs, environment info (Templates/analysis-log.md).
9. Record deviations from the plan and reasons.

Never alter raw data or change specifications to chase significance.
