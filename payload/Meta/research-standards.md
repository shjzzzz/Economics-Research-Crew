# Research Standards

## Evidence hierarchy (practical preference, not truth ranking)
Primary legal/statistical sources -> peer-reviewed -> working papers -> policy reports -> commentary.

## Literature record
Full citation, DOI/URL, status, question, mechanism, data/sample, variables, identification, findings, limitations, relevance, page/table refs.

## Empirical record
Project ID, data source/version, sample, variables, specification, software/package versions, script path and Git commit, output, diagnostics.

## Causal language
Use "associated with" unless a defensible design is established; state estimand and assumptions before "effect/impact/caused".

## Tax-law record
Issuing authority, document number, promulgation date, effective date, amendment/repeal status, tax period, scope, official URL.

## 7-Mode AI Research Failure Gate (S6 & S12)
Before passing S6 (Independent Review) or S12 (Final Check), explicitly check and clear:
1. **Implementation bugs** (silent sample drop, merge explosion, wrong clustering/FE).
2. **Hallucinated results** (any number not in `Meta/results-ledger.json`).
3. **Shortcut reliance** (post-hoc spec search, unreported winsorizing/subsampling).
4. **Bug-as-insight reframing** (treating coding/data anomalies as economic mechanisms).
5. **Methodology fabrication** (claiming DID/IV/RDD assumptions hold without diagnostics).
6. **Frame-lock** (polishing inside a flawed identification/model instead of questioning the frame).
7. **Citation hallucinations & L3 mismatch** (unverified keys or `[@key]` lacking locator/claim alignment).
