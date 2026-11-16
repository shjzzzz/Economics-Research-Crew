---
name: econometric-analysis
description: "Plan, implement, inspect, reproduce or audit an econometric analysis in Stata, R or Python. Use for 数据清洗、变量构造、描述统计、回归分析、基准回归、异质性分析、复现论文、代码审计、稳健性检验执行."
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

## Replication & code-audit mode
Use when asked to reproduce a paper's results or audit existing analysis code.
1. Record the target: paper, table/figure, reported estimates, sample size, software.
2. Locate data and code; note what is missing or restricted. Do not substitute data silently.
3. Run the original code unchanged first; log environment and versions.
4. Compare reproduced numbers with the reported ones cell by cell (estimate, SE, N); classify each as exact / within rounding / different.
5. For differences, trace the cause (data vintage, sample filter, clustering, package version, coding error) before changing anything.
6. Code audit: check merges (row counts before/after), duplicates, filters, variable construction vs paper definitions, clustering level, hard-coded numbers.
7. Report a replication table and a list of discrepancies with their likely causes; robustness extensions come after faithful replication.

Delegation: long execution or large code reading may be dispatched to `econometrics-agent` (invoking this Skill authorizes that, one agent at a time).

Never alter raw data or change specifications to chase significance.
