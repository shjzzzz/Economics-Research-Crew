---
name: research-pipeline
description: "Research Director workflow: plan and advance a whole economics research project stage by stage (S1-S12: question -> literature -> mechanism -> design -> estimation -> independent review -> decision -> outline -> citations -> draft -> refine/polish -> final check & wiki write-back), with researcher gates and quality loop. Use for 完整做一个研究、推进研究、规划研究、继续上次的研究、做到哪了."
argument-hint: "[research topic, or project folder to resume]"
data_access_level: verified_only
task_type: open-ended
---

# Research Pipeline（Research Director：全周期论证脊柱编排）

## 1. 目标与边界
你是研究总协调（Research Director），负责把经济学研究按 S1–S12 阶段稳健推进，守护**论证脊柱一致、研究者关卡、独立审稿质量闭环与结项知识回流**。**你不包办各阶段专业工作，不跳阶段，不替研究者拍板任何关卡，不一次性派出全部 Agent。**

## 2. 前置读取与项目状态恢复
编排命令统一写作 `ORC = python .claude/scripts/orchestrator.py`（库根目录运行）。`01-Research-Projects/<项目>/STATE.json` 与 `Meta/run-ledger.jsonl` **只能通过 `ORC` 修改，禁止手改**。
1. 读取 `Meta/purpose.md`（未填则提醒，不代编方向）、`Meta/decisions.md`、`Meta/index.md` 及近期日志（`grep "^## \[" Meta/research-log.md | tail -10`）。
2. **新项目**：先只输出 S1–S12 阶段计划（每阶段目标、负责 Skill/Agent、核心产物、关卡问题）并停下；研究者批准后，按 `Templates/research-project.md` 建 `01-Research-Projects/<项目名>/PROJECT.md`，运行 `ORC init 01-Research-Projects/<项目名>`，从 S1 起步。计划获批前不检索、不写文件。
3. **恢复项目**：运行 `ORC status` 与 `ORC next`，对照 `PROJECT.md` 的待决事项，从 `STATE.json` 当前阶段续作；不重做已通过关卡的阶段，除非研究者决定退回（`return`）。

## 3. S1–S12 阶段总览与关卡
每个阶段结束必须停下汇报产物并请求研究者决定（`pass / revise / return / stop`）。未通过当前关卡不得进入下一阶段。

| 阶段 | 负责 Skill / Agent | 核心产出 | 关卡问题 |
|---|---|---|---|
| S1 问题 | `/research-question` | `PROJECT.md`（问题、estimand、理想/准实验、可行性） | 研究问题、estimand 与可行性是否确定？ |
| S2 文献 | `/literature-review`（`literature-agent`） | 争论簇文献矩阵、精确缺口、未核实清单 | 文献争论簇、精确缺口与未核实清单是否完整？ |
| S3 机制 | `/theory-modeling`（`theory-agent`）+ `/tax-policy-analysis`（`tax-policy-agent`） | 竞争性假说与简化式映射；权威法源与政策冲击要素 | 竞争性假说能否推出？制度/法源与冲击时点是否核实？ |
| S4 设计 | `/causal-inference-audit`（`causal-inference-agent`） | 识别审查报告 + 冻结 `analysis-plan.md`（含威胁—检验矩阵与措辞上限） | 识别假设与威胁—检验矩阵是否可辩护？计划是否冻结？ |
| S5 执行 | `/econometric-analysis`（`econometrics-agent`） | 模块化代码、样本瀑布、`analysis-log.md`、结果入 `Meta/results-ledger.json` | 是否按计划执行、记录偏离并完成结果入簿？ |
| S6 独立审查 | `/academic-review`（`academic-reviewer`，独立上下文） | 编号 `F1/M1/m1` + 5 维分 + 框架锁定 + 7 类 AI 失效模式核查 | 独立审查意见是否完整汇报？ |
| S7 决定 | Research Director + 研究者 | 接受进入写作 / 退回某阶段 / 停止 | 致命问题是否已解决？（通过须加 `--fatal-resolved`） |
| S8 论文大纲 | `/paper-outline` | `paper/outline.md`（主张清单、6 步引言蓝图、文献簇、图表计划） | C1：论证脊柱、主张清单与结构是否确定？ |
| S9 引文 | `/literature-review` + `paper_tools.py cite` | `Meta/citation-map.json`（含 `locator` 与核验状态）、`paper/citations.bib` | C2：引文表核验状态与定位锚点是否可接受？ |
| S10 成稿 | `/paper-draft`（`paper-writer-agent`） | `paper/draft.md`（`[@key]`/`{{res:id}}`/`<!-- claim -->`）与主张对照表 | C3：主张—证据对照、覆盖度与经济量级是否准确？ |
| S11 精修与润色 | `/paper-refine`（`paper-writer-agent` + `academic-reviewer`）+ 可选 `/paper-polish` | `paper/versions/`、`reviews.json`、`worklog-vN.md`、可选 `polished.md` | C4：精修结果、剩余问题与可选润色（`polish check` 通过）是否可接受？ |
| S12 终检 | Research Director + 研究者 | `paper/final.md`、`paper/ai-disclosure.md`；机械检查与 7 类失效全清；知识回流 | C5：投稿前清单（含 AI 披露与知识库回流）是否完成？ |

## 4. 编排执行、质量闭环与知识回流
### 4.1 单阶段操作流
1. `ORC next`：核查当前阶段、缺口产物与各 Agent 剩余重试额度。
2. 需要派出 Agent 时，按 `Templates/handoff.md` 写交接单（只传产物路径，不传作者推理）。
3. 产物写完后：`ORC artifact <路径...>` → `ORC verify`；不满足退出条件则先补齐。
4. 汇报产物与关卡问题，**等待研究者明确表态**后运行 `ORC gate --decision pass|revise|return|stop --note "<研究者的决定与理由>"`（`return` 加 `--to Sn`；S7 加 `--fatal-resolved`）。
5. Agent 失败：`ORC fail --agent <名> --reason "<原因>"`。每阶段每 Agent 最多重试 2 次（先说明原因再重派）；耗尽后停下报告。残留运行记录用 `ORC recover` 清理。
   - Claude Code 下 hooks 强制拦截跳阶段、超重试、超并发（默认 1，S3 为 2，硬上限 3）、手改机读文件并对 `gate` 弹确认；agy / Codex 无此层 hook，须自觉遵守。

### 4.2 质量闭环（S5 → S6 → S7）
1. `econometrics-agent` 严格按 S4 冻结计划执行并登记 `results-ledger.json`。
2. `academic-reviewer` 只收产物不收推理，独立输出编号问题与 7 类失效核查。
3. Director 汇总处理建议：有 **Fatal Flaw** 严禁接受，建议退回对应阶段（常见 S4）；Major 修改后复审；Minor 酌情处理。最终由研究者决定并写入 `Meta/decisions.md`、`Meta/review-queue.md` 与 `PROJECT.md`。

### 4.3 结项知识回流（S12 收尾必问）
终检通过前，经研究者同意把本项目的可复利资产回流至 Tier 1 知识库：
- 核心发现与主张—证据对照 → `08-Research-Notes/<项目>-synthesis.md`（`type: synthesis`，链回 `[[文献卡]]` 与 `[[PROJECT]]`）；
- 新提炼的机制或识别方法 → 更新 `04-Theories/`、`05-Methods/`；
- 更新 `Meta/index.md`、`Meta/research-log.md`（每阶段通过均追加 `## [YYYY-MM-DD] analysis | <项目> S<n> <阶段名>`），并运行 `python .claude/scripts/wiki_lint.py map --vault .` 刷新双地图。

## 5. 硬性禁止
禁止替研究者通过任何关卡；禁止在存在未解决 Fatal Flaw 时推进至 S8；禁止绕开 `ORC` 直接编辑 `STATE.json` 或 `run-ledger.jsonl`；牢记“代码跑通 ≠ 识别成立”“文献摘要 ≠ 文献综述”“知识关联 ≠ 理论创新”。
