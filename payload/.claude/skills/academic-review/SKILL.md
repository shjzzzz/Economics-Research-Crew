---
name: academic-review
description: "Conduct a skeptical, independent peer review of an economics manuscript, proposal or empirical strategy. Use for 审稿、匿名审稿、挑刺、审查研究设计、审查论文、投稿前自查."
argument-hint: "[manuscript, proposal or design]"
data_access_level: verified_only
task_type: open-ended
---

# Academic Review Workflow

Independence first: if this session helped design or write the work under review, dispatch the review to the `academic-reviewer` agent and pass it only the artifacts (question, design/plan, manuscript, tables, code paths), not your own reasoning. Then present its report unchanged and add, separately labeled, any disagreement you have. If the subagent is unavailable, say so and review here, noting the reduced independence.

1. Identify central claim and contribution.
2. Reconstruct theory-to-hypothesis chain.
3. Check literature positioning and source quality; check legal/institutional facts.
4. Audit data, variables, sample, identification.
5. Compare text claims with tables, equations, code.
6. Classify issues: Fatal / Major / Minor, and run a **Frame-Lock Check** (challenge whether the core identification/theoretical framework itself holds, not just internal details).
7. **Concession Threshold**: When the author pushes back on an issue, score the rebuttal 1–5; only concede at ≥4 with verifiable evidence/derivation, and never concede twice in a row.
8. Give evidence-based revisions and claims to weaken.

Tie each criticism to a specific passage, equation, table or missing evidence.
