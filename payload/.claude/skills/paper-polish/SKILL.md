---
name: paper-polish
description: "Language and voice pass for an economics draft: strip generic AI phrasing and over-claiming, keep claim wording within the evidence, match the author's voice and the target venue; never changes a number, citation key, {{res:id}} placeholder or marker, and is not for evading AI-use detection or disclosure. Use for 润色、去AI味、语言精修、文风校准、统一文风、消除套话、表达打磨."
argument-hint: "[draft path, optional: author sample / target venue]"
data_access_level: verified_only
task_type: open-ended
---

# Paper Polish（语言与文风精修）

只处理**表达**：把成稿读得更清楚、更像作者本人，同时保证内容分毫不变。内容是否站得住脚，由 `/paper-refine` 的独立评审负责，不在这里解决。

## 边界（先读）
- **不碰**：数字、`[@key]`、`{{res:id}}`、`<!-- claim: Cn -->`、`⟦问：…⟧`/`⟦答：…⟧`、变量名、公式、符号、法规文号与日期、表图编号、章节标题。
- **不加**：新事实、新数据、新文献、新的研究过程叙述（例如编一段“先试了 A，没解释通才改用 B”）、个人化的“口吻”或有意制造的粗糙。
- **不是**用来规避 AI 检测或免除披露的工具。**遇到“降低 AI 率 / 降 AIGC / 过检测”这类要求，拒绝**，并说明：本流程只改善表达；AI 参与（含润色）仍须按目标期刊要求披露，并写入 `paper/ai-disclosure.md`。
- 缺证据的句子**不改写成结论**，写 `⟦问：…⟧` 交研究者；措辞强度不得超过 `outline.md` 里该主张“允许的措辞强度”。

## 流程
1. **读入**：采用版稿件（`paper/draft.md` 或精修后的版本）、`Meta/style-guide.md`、`paper/outline.md` 的主张表；作者若提供代表作段落或目标期刊，先读样本，记下句长节奏、连接词习惯、限定语的位置、段首写法、固定术语，再动笔。没有样本时用 `Meta/style-guide.md`，仍未填写就用克制、精确、少形容词的中性学术文风，并用 `⟦问：…⟧` 询问偏好。
2. **扫描**（确定性，只提示不判定）：`python .claude/scripts/paper_tools.py polish scan paper/draft.md`。命中清单来自 `Meta/ai-tells.json`（研究者可增删）；命中不等于错，先判断是否真是套话或夸大。
3. **审计**（先不改）：列出每处命中的位置、类别和拟改法；另列每个实证主张的证据状态（有 `{{res:id}}`/`[@key]`/表图，还是没有）。
4. **改写**，写入 `paper/polished.md`（不覆盖原稿）：同一结构、同一内容，逐段对应。
5. **机械核对**：`python .claude/scripts/paper_tools.py polish check --before paper/draft.md --after paper/polished.md`。引文键、`{{res}}` 占位符、主张标注、问答标记和正文数字必须与润色前完全一致，否则退回修改；标题变化给警告。
6. **汇报**：润色稿 + 变更报告（按类别计数、动词降级清单、未解决的 `⟦问⟧`、`polish check` 的输出）。研究者认可后，再作为 `paper/final.md` 的候选，沿用 `/paper-refine` 收尾的 C4 流程。

## 改写层次（自上而下）
### 1. 去套话与夸大（对应 `Meta/ai-tells.json`）
- 时代背景开头（“近年来”“随着……的快速发展”）、意义空话（“具有重要的理论意义和现实意义”）、空洞强调（“值得注意的是”“综上所述”）、“不仅……而且……”式机械句式、模糊程度词（“较为”“在一定程度上”）：删去，或换成具体内容（量级、区间、口径）。
- 无来源断言（“大量研究表明”）：改成具体 `[@key]` 并说明该文献的结论与适用条件；没有对应文献就删，不编造。
- 新颖性堆砌（“首次”“填补空白”“创新性地”）：写出与哪些文献相比差在哪里。
- 文献堆砌（一处 ≥4 个引用）：只留最相关的 1–2 篇并说明相关在哪里。
- 超长句：一句一个意思，删去不承载信息的从句。
- 句子之间让逻辑连接，不靠“此外/同时/另外”开头；列举理由时轻重不一，不凑整齐的三段。
- 具体写出制度、数据库、政策与年份，不用“某些地区”“相关部门”这类占位说法。

### 2. 措辞强度与证据匹配
- “证明”“证实”“彻底”“毫无疑问”：实证结果写“表明”“提供证据”，除非是定理。
- “显著”：同时给出经济量级与统计精度，或用 `{{res:id}}` 链接；只写“显著”不算数。
- 因果动词必须与大纲里该主张的类型一致；大纲限定为相关或仅描述的主张，不得用“导致”“引起”等（`paper_tools.py claim check` 也会检查）。
- 模糊量级（“大幅提高”）：改成登记簿里的数值或区间，并注明比较对象；只能引用**已登记**的结果。

### 3. 保留项（不要“修正”）
- 与证据挂钩的限定语（“与……相关”“在……假设下，估计表明”“可能反映”）；识别局限的如实陈述。
- 学术常用的“本文/我们”、必要的被动语态、术语、变量名、公式与符号。
- 作者的固定术语译法（见 `Meta/style-guide.md` 术语表）。

### 4. 章节层检查（只提出问题，需改动结构时交研究者）
- **摘要**：先写发现，再写数据与识别策略，不评价他人文献；字数以目标期刊要求为准。
- **引言**：尽早进入问题与主要结果（含量级），文献写成“前人做了什么、还缺什么、本文补什么”的叙述，而不是逐篇罗列；路线图按本文具体内容写。引言前几页没有结果，应指出。
- **结论**：简短，换一种说法重述发现，不引入新结果，不堆砌笼统的局限，不写“留待未来研究”之类的空话而是给出具体的延伸做法。
- **标题**：能看出问题与方法或结果，不夸大。

## 语域与期刊
- 中文稿默认遵循 `Meta/style-guide.md`；英文稿注意主语与时态一致、少用名词堆叠、能用简单词就不用复杂词。
- 目标期刊的语域参考 `Templates/venues/`（均为未核实的骨架，以期刊官网为准）。
- 中文破折号、英文 em-dash 是否使用，由作者与期刊习惯决定；既不为“像人写的”而刻意添加，也不机械删除。

## 与其他环节的关系
- 在 `/paper-refine` 的评审—修改循环**结束之后**使用；内容改动（补分析、改识别论证）不属于本 Skill。
- 润色版本通过 `polish check` 后，才可替换送审或定稿版本；把 AI 参与润色的事实写入 `paper/ai-disclosure.md`。
- 终检（S12）仍会运行 `cite check --strict`、`results check`、`claim check` 与未答问题检查。

## 致谢
本 Skill 的结构借鉴了以下 MIT 许可项目的思路并按本项目的约束重写（未复制其文本）：
`AIScientists-Dev/academic-humanizer`（分层的 AI 套话目录、“保留学术惯例”、主张—证据匹配）；
`hanlulong/econ-writing-skill`（摘要/引言/结论的章节公式、删除套话与具体化的写法）；
`redbaronyyyyy-eng/humanizer-zh-academic`（中文学术 AI 套话的模式分类；其“降低 AIGC 检测率”的目标**不采用**）。
`franklee16/academic-research-skills` 是汇编库，仓库根目录未见许可证，仅作参考，未采用其内容。

## 禁止
为通过检测或显得“更像人”而改写；改动或“补全”数字、引文、占位符与标记；把缺证据的句子润色成有结论的句子；删除真实的识别局限；编造研究过程或来源。
