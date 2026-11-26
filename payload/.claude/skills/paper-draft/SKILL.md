---
name: paper-draft
description: "Draft an economics paper section by section from an approved outline using strictly constrained inputs (registered citations and registered results only), following top-journal section protocols; unsupported claims become researcher questions. Use for 起草论文、写初稿、成稿、分节写作、撰写全文、把大纲写成论文."
argument-hint: "[project folder, sections to draft]"
data_access_level: verified_only
task_type: open-ended
---

# Paper Draft（S10：受限输入的经济学分节成稿）

## 1. 目标与边界
仅依据 **C1 已批准的大纲**分节起草正文。通过**严格限定输入源**从机械层面杜绝幻觉：
| 唯一允许的输入 | 约束规则 |
|---|---|
| `paper/outline.md`（C1 已通过） | 结构、主张清单（含措辞强度上限）、各节要点 |
| `Meta/citation-map.json`（`paper_tools.py cite list`） | **唯一允许引用的文献**，写作 `[@key]` |
| `Meta/results-ledger.json` | **唯一允许出现的实证数字**，写作 `{{res:id}}` 或 `{{res:id:3}}` |
| `Meta/style-guide.md`、`Templates/venues/*.md` | 文风锚定、术语表、期刊骨架 |

## 2. 前置读取
- 运行 `python .claude/scripts/orchestrator.py status` 确认 S8/S9 关卡已通过；运行 `python .claude/scripts/paper_tools.py cite list` 查看可用键（非 `verified`/`confirmed` 状态可暂引但终检会被挡，须提醒研究者核验）。
- 读取 `Meta/style-guide.md` 完成**文风校准**（目标期刊语域、作者代表作样本锚定、固定中英术语表与因果措辞分级）。

## 3. 核心流程、分节写作规程与委派
- **委派授权**：长节起草可派出隔离上下文的 `paper-writer-agent`（一次一个，按 `Templates/handoff.md` 交接，只给上表 4 类文件路径）。
1. **逐节写作**（一次一节，写入 `01-Research-Projects/<项目>/paper/draft.md`）：
   - **摘要**：先亮核心定量发现与经济量级，再交代数据、识别策略与机制；不评价他人文献。
   - **引言**：严格按大纲 6 步蓝图推进，前 2–3 页内亮出主结果 `{{res:…}}` 与经济量级；文献写成“前人做过什么—局限在哪—本文补什么”的对话，拒绝逐篇罗列。
   - **制度背景**：紧扣政策外生性、时间节点（发文日 vs 生效日）与处理/对照边界；所有法条用已登记的 `[@key]`。
   - **理论与假说**：写清核心机制与竞争机制的排他推论，不堆砌与实证脱节的符号；按“环境→假设→命题→一句话直觉→编号预测”的顺序，见 `Meta/style-guide.md` §IV.10A。
   - **数据与实证策略**：写清样本瀑布、变量口径、estimand、基准方程、识别假设与聚类层级；主方程逐项定义符号并指定首选设定，见 `Meta/style-guide.md` §IV.10B。
   - **实证结果**：每个结果段落开头加 `<!-- claim: Cn -->`，且**同时报告统计精度与经济量级**（系数、标准误/显著性、占均值/标准差比例或弹性），措辞严禁超过大纲该主张允许的上限；段落按“发现→量级→精度→边界”写，零结果用置信区间界定，见 `Meta/style-guide.md` §IV.10C。
   - **稳健性与机制**：按威胁—检验映射逐一回应 S4 识别威胁；机制分析明确是否排除竞争解释，否则最高写“与……机制一致”。
   - **结论**：简短换言重述发现、诚实界定外部有效性边界，不引入新结果、不写空洞展望。
2. **硬性占位纪律**：
   - 数字只写 `{{res:id}}`（保留小数写 `{{res:id:3}}`），严禁心算或手写登记簿外的数字。
   - 引用只写 `[@key]`（且 `citation-map.json` 应带 `locator` 防 L3 错配）；缺失文献写 `⟦问：需要引用…，请先登记⟧`。
   - 证据不足写 `⟦问：…⟧`，绝不用“显然/众所周知”绕过，绝不擅自补分析。
3. **成稿机械审计与质检**（每节或全稿完成后依次运行）：
   - `python .claude/scripts/paper_tools.py cite check paper/draft.md`
   - `python .claude/scripts/paper_tools.py results check paper/draft.md`
   - `python .claude/scripts/paper_tools.py claim check paper/draft.md`（核对 `locator` 锚点、`<!-- claim: Cn -->` 覆盖度、大纲主张匹配与因果动词越界）
   - `python .claude/scripts/paper_tools.py questions paper/draft.md`
   - 对照 `Meta/style-guide.md` 去 AI 味负面清单清理机械套话。
4. **生成主张—证据对照表**（C3 检查点用）：主张编号 → 正文节/段 → 结果 id → 实际措辞强度 → 是否符合大纲上限 → 覆盖状态。

## 4. 产出与停点（C3 检查点）
- 运行 `python .claude/scripts/orchestrator.py artifact paper/draft.md` 与 `verify`。
- 向研究者汇报主张—证据对照表、主张覆盖度、未核验引文与未回答 `⟦问⟧`。**C3 检查点：等研究者表态并在稿内写 `⟦答：…⟧` 后再修改或推进。**

## 5. 硬性禁止
禁止把相关写成因果；禁止引用不在 `citation-map.json` 的文献；禁止手写不在 `results-ledger.json` 的核心数字；禁止无来源断言（“大量研究表明”）；禁止替研究者做 A3 决策。
