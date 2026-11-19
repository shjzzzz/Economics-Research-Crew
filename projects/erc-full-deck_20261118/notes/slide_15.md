为了让长周期研究不断档、不越权，Research Director 编排器通过 `orchestrator.py` 维护 `STATE.json` 和 `run-ledger.jsonl`。整个流程分成 S1–S7 研究闭环和 S8–S12 写作闭环。它不仅支持断点续跑和单阶段最多 2 次的重试熔断，还规定 AI 严禁自己过关，必须由研究者确认关卡。
