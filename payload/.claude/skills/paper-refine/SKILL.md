---
name: paper-refine
description: "Refine a paper draft through independent review rounds (F1/M1/m1 checklist + 5 scores, accept only on measurable improvement, else revert, max 3 rounds) and manage external journal R&R via a traceability matrix. Use for 精修、修改稿、返修、R&R、按审稿意见修改、润色并审阅、多轮修改."
argument-hint: "[project folder / draft path]"
data_access_level: verified_only
task_type: open-ended
---

# Paper Refine（S11：清单复核精修闭环与期刊 R&R 返修）

## 1. 目标与边界
面向**内容与论证质量**的迭代精修：以“改稿回应弱点”为核心，通过独立审稿的编号问题清单与 5 维评分做**严格接受/回退控制**（最多 3 轮，所有版本留档），并支持外部期刊 R&R 返修追溯。纯语言表达打磨在内容定稿后交给 `/paper-polish`。

## 2. 前置读取
- 确认 `paper/draft.md`（C3 已通过）、`paper/outline.md`、`Meta/style-guide.md`、`Meta/results-ledger.json`、`Meta/citation-map.json`。
- 若为外部期刊 R&R 返修，同时读入审稿意见全文与 `Templates/rebuttal-matrix.md`。

## 3. 核心流程与委派规则
### 3.1 内部对抗精修循环（最多 3 轮，版本全保留）
0. **快照基线**：`python .claude/scripts/paper_tools.py refine start paper/draft.md` 生成 `paper/versions/v0.md` 与 `paper/reviews.json`。
1. **基线独立评审**：派出 `academic-reviewer`（独立上下文，一次一个，按 `Templates/handoff.md` **只给产物路径**：稿件、主张—证据对照表、结果登记簿、分析计划；不传作者推理）。要求按 `/academic-review` 契约输出：带编号清单（`F1…`、`M1…`、`m1…`，每条指向具体位置）+ 5 维 1–10 分（`ident, contrib, inst, consist, write`）+ 框架锁定检测 + 7 类 AI 失效核查。
2. **登记基线**：`python .claude/scripts/paper_tools.py refine record --version v0 --fatal F --major M --minor m --scores ident=5,contrib=6,inst=6,consist=7,write=6`。
3. **针对性改稿**（写成 `paper/versions/v1.md`…`v3.md`，长篇修改可派 `paper-writer-agent`）：
   - 通过修改正文直接化解弱点，保留评审认可的“优点”段落；遵守 `Meta/style-guide.md` 避免引入 AI 套话。
   - 严守受限输入：数字仍只用 `{{res:id}}`，引用只用 `[@key]`，**不得擅自补分析或改数据**。
   - 评审要求的**新实验/新稳健性/新基线**：绝不忽略，也不自行跑回归，逐条写入 `Meta/review-queue.md`（标“需要新分析，待研究者决定”）。
   - 每轮写 `paper/worklog-vN.md`：逐条记录回应了哪些编号问题、具体修改位置与未处理原因。
4. **按基线清单复评与机械判优**：
   - 再次评审须**对照基线编号清单逐条复核**（`已解决 / 部分解决 / 仍存在`，后两者计入 `carried`）并单列新增问题（计入 `new`），**尽量复用同一 `academic-reviewer` 实例**以保持口径可比。
   - 登记复评：`python .claude/scripts/paper_tools.py refine record --version vN --carried-fatal a --carried-major b --new-fatal c --new-major d --minor m --scores ident=...,contrib=...,inst=...,consist=...,write=...`。
   - 脚本机械判定接受/回退：仅当 `Fatal ≤ 上版` 且（`Major < 上版` 或 `Major == 上版 且同维度总分 ≥ 上版`），且**维度完全一致、任一维度未降 ≥2 分**时接受；否则回退。**回退时必须回到当前采用版本重新修改，不得在被回退版本上继续改。**
5. **停止条件**：用满 3 轮、Fatal 与 Major 均归零、或连续回退。运行 `python .claude/scripts/paper_tools.py refine status` 查看轨迹。

### 3.2 外部期刊返修模式（R&R / Revision Coach）
收到外部审稿意见时，按 `Templates/rebuttal-matrix.md` 建立 `paper/rebuttal-matrix.md`：
- 将每条意见拆解并分类：**① 直接改稿/澄清边界**（正文修订 + 绑定 `[@key]`/`{{res:id}}`）、**② 需新增实证/稳健性**（转入 `Meta/review-queue.md`，等研究者补充并入簿 `results-ledger.json` 后再写）、**③ 有理有据的反驳**（必须附带可核验证据或推导，遵守让步门槛与礼貌克制语气）。
- 每条回复绑定正文节/段、证据锚点与复核状态，确保“改稿处—回复信—证据”三方完全一致。

## 4. 收尾与停点（C4 → 可选 `/paper-polish` → S12）
1. 向研究者汇报：精修版本轨迹、当前采用版、剩余 Fatal/Major 及转入 `Meta/review-queue.md` 的“需新分析”清单。
2. **内容定稿后，可选调用 `/paper-polish`** 做纯语言精修：必须通过 `polish check`（引文、`{{res}}`、主张标注、问答标记、数字全不变）并经研究者认可。
3. 研究者确认采用版后，复制为 `paper/final.md`；运行 `orchestrator.py artifact paper/reviews.json paper/final.md` 与 `verify`，等研究者表态再 `gate`。
4. **S12 终检准备**：运行 `cite check --strict`、`results check`、`claim check --strict`、`questions`，清零 7 类 AI 失效模式，依据 `orchestrator.py log` 与 `Meta/run-ledger.jsonl` 起草 `paper/ai-disclosure.md` 交研究者审定；结项后经研究者同意将“主张—证据对照”回流为 `08-Research-Notes/` 的 `type: synthesis` 页并刷新双地图。

## 5. 硬性禁止
禁止为拉高评分而弱化或删除真实的识别局限；禁止把“需新分析”悄悄当作已完成；禁止修改已登记结果数值；禁止替研究者接受或拒绝审稿意见（A3）。
