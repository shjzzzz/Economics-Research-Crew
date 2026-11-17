---
name: paper-refine
description: "Refine a paper draft through independent review rounds: review, revise by presentation, re-review, accept the revision only if it improved, otherwise revert; at most 3 rounds, researcher decides at the end. Use for 精修、修改稿、返修、按审稿意见修改、润色并审阅、多轮修改."
argument-hint: "[project folder / draft path]"
---

# Paper Refine（评审—修改—接受或回退）

借鉴“以修改代替回复信”：审稿意见通过**改正文**来回应，而不是另写回复。区别于全自动方案：经济学里识别是否可信不能靠分数判断，所以接受规则看**问题数**，最终由研究者决定。

## 循环（最多 3 轮；每个版本都保留）
0. `paper_tools.py refine start paper/draft.md`：保存 `paper/versions/v0.md`。
1. **独立评审**：派出 `academic-reviewer`（一次一个，独立上下文），**只给产物路径**：稿件、主张—证据对照表、结果登记簿清单、分析计划；不给你的推理。要求结构化输出：**带编号的问题清单**（F1…、M1…、m1…，每条一句话并指向稿件位置），以及 5 个维度的 1–10 分：`ident`（识别可信度）、`contrib`（贡献与定位）、`inst`（制度与法源）、`consist`（证据一致性）、`write`（写作）。
2. 登记基线（条数 = 清单条数）：`paper_tools.py refine record --version v0 --fatal F --major M --minor m --scores ident=5,contrib=6,inst=6,consist=7,write=6`。
3. **修改**，写成 `paper/versions/v1.md`（再下一轮 v2、v3）：
   - 用改正文回应弱点；评审的问题要在正文里自然回答。
   - 保留“优点”所在的段落，除非必须改动。
   - 数字仍只用 `{{res:id}}`，引用仍只用引文表里的键；**不得新增分析与数据**。
   - 评审要求的新实验、新稳健性、新基线：**不要忽略，也不要自己做**，逐条追加到 `Meta/review-queue.md`（标“需要新分析，待研究者决定”）。
   - 每轮写 `paper/worklog-vN.md`：回应了哪些弱点、整合了哪些答案、做了哪些改动。
4. 对新版本再次评审。**必须按基线清单逐条复核**（已解决 / 部分 / 仍存在），再单独列出**新增**问题，不要重新数一遍；最好用 `SendMessage` 让同一个 reviewer 复评以保持口径。不同 reviewer 各自独立数条数不可比（冒烟测试中 Major 4→6 就是口径差异）。登记：`paper_tools.py refine record --version v1 --carried-fatal a --carried-major b --new-fatal c --new-major d --minor m --scores ...`（仍存在与部分解决的计入 carried）。脚本给出**接受 / 回退**：
   - 接受条件：Fatal 数不增加，且 Major 数下降，或 Major 持平而总分不低于上一采用版；任何维度下降 ≥2 分一律回退。
   - 回退时：当前采用版本不变，**回到该版本再改**，不要在被回退的版本上继续。
5. 停止：3 轮用完、Fatal 与 Major 都为 0，或连续回退。`paper_tools.py refine status` 查看轨迹。

## 收尾（C4 检查点）
- 向研究者汇报：版本轨迹、当前采用版本、剩余 Fatal/Major、进入 review-queue 的“需要新分析”清单。
- 研究者认可后，把采用版复制为 `paper/final.md`；`orchestrator.py artifact paper/reviews.json paper/final.md`，`verify`，等研究者表态再 `gate`。
- 终检（S12）前再运行 `cite check --strict`（所有被引文献须已核验或已由研究者确认）、`results check`、`questions`，并起草 `paper/ai-disclosure.md`：依据 `orchestrator.py log` 与 `Meta/run-ledger.jsonl` 列出 AI 参与的阶段与任务，交研究者审定后再用于投稿。
- 成稿后经研究者同意，把“主张—证据对照”整理为 `type: synthesis` 的 wiki 页，链回文献笔记与结果表来源。

## 禁止
为让分数上升而弱化或删除真实的识别局限；把评审的“新分析”要求悄悄当作已完成；修改已登记的结果数值；替研究者接受或拒绝审稿意见。
