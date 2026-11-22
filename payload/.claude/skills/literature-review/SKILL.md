---
name: literature-review
description: "Conduct a source-grounded economics literature review, debate-structured matrix, gap identification and citation registration with three-layer locator anchors. Use for 文献综述、梳理文献、国内外研究现状、研究缺口、文献矩阵、找文献."
argument-hint: "[topic, question or scope]"
data_access_level: redacted
task_type: open-ended
---

# Literature Review（S2 / S9：证据驱动文献梳理与引文锚点登记）

## 1. 目标与边界
产出**按争论/机制/识别演进组织**的文献矩阵与精确缺口，而非逐篇罗列摘要；在 S9 阶段协同 `paper_tools.py cite` 完成带三层定位锚点（`locator`）的引文表建设。**绝不编造文献，绝不用摘要替代全文证据。**

## 2. 前置读取
- 先读本地知识库：`Meta/purpose.md`、`Meta/index.md`、`Meta/link-map.md`（沿枢纽页与 `03-Literature/` 检索已有文献卡），再决定外部检索范围。
- 若处于论文 S9 阶段，先读 `paper/outline.md` 的第 4 节 `citation_hints` 与 `Meta/citation-map.json`（`python .claude/scripts/paper_tools.py cite list`）。

## 3. 核心流程与委派规则
- **委派授权**：长篇文献检索、逐篇抽取与矩阵比对可派出 `literature-agent`（按 `Templates/handoff.md` 交接，一次一个）。
1. **界定检索协议**：明确主题、时间跨度、语种、纳入/排除标准，记录检索日期、数据库与检索词。
2. **多源检索与分级筛选**：优先一手官方源、国内外顶刊与权威工作论文（NBER/CEPR/IZA/SSRN），明确区分已发表、工作论文、政策报告与预印本。
3. **逐篇方法论抽取**（禁止只看摘要下结论）：研究问题、理论机制、数据与样本、变量定义、识别策略与估计量、核心定量结果（含量级）、稳健性与局限；读不到全文时显式标注“仅摘要/未获全文”。
4. **按争论簇构建矩阵**（直接服务 S8 `/paper-outline`）：
   - 划分为 2–4 个微观文献簇（按机制、识别演进、制度背景或争议分组）。
   - 每簇明确：① 代表文献与共识/分歧；② 该簇的**局限假设**（在何种数据/制度下失效）；③ **与本文的桥接**（本文如何修补该局限）。
5. **识别真实缺口与竞争解释**：区分“没人写过”与“值得写且现有识别未解决”，并列出竞争性解释。缺口须按 §3a 的“研究缺口分类表”逐类登记，不得只写一句笼统的“现有研究不足”。
6. **三层定位锚点与引文登记**：每条重要主张记录页码/表号/公式/条款（`--locator`）与主张适用边界（`--claim-scope`）。
   - 已有 `03-Literature/*.md` 文献卡：优先运行 `python .claude/scripts/paper_tools.py cite from-note <卡片路径>` 桥接入库。
   - 已在 **Zotero / EndNote** 中管理的文献：先导出 RIS / BibTeX / CSL-JSON（本机 Zotero 也可用 `cite zotero` 直接拉取），先 `paper_tools.py cite import <文件> --dry-run` 预览，再正式导入（`--attach [--pdf-dir DIR]` 复制 PDF 到 `03-Literature/_sources/`）。条目一律 `unverified`（中文为 `manual`），自动建文献笔记并登记 `Meta/index.md`；**参考文献软件只是进出口，引文表才是写稿依据**，须对照原文核实或由研究者 `cite confirm` 后才能引用。Zotero 还可 `cite zotero --query 词 --list` 先搜、`--item KEY` 拉单条、`--notes` 带入其笔记；`cite open KEY` 打开 PDF；`cite zotero-note KEY --user ID` 预览后加 `--yes` 把文献笔记作为新子笔记写回 Zotero（需研究者同意）。定稿后用 `cite ris|csl|bib -o` 导回 EndNote / Zotero / Word。
   - 新增引文：运行 `python .claude/scripts/paper_tools.py cite add --key <k> --title "…" --year Y [--doi D] --locator "…" --claim-scope "…"`；中文文献加 `--type chinese`，法规加 `--type legal --doc-no "…" --effective YYYY-MM-DD`，均须由研究者核对原文后执行 `cite confirm`。

## 3a. 研究缺口分类表（据 Kumar 2020, *Journey through research gaps* 的缺口图谱）
研究缺口 = **已知（过往知识，来自文献综述）** 与 **未知（研究所需的预期知识）** 之间、由**过往发现的弱点**暴露出的差距。

**表 A：缺口分类表**（八类各占一行；无证据的类别写“未发现”，不要硬凑）

| 缺口类型 | 判定问题 | 已知（过往知识 + 引文 + locator） | 未知 / 所需知识 | 过往发现的弱点 | 张力类型（见表 B，无则填“—”） | 现有识别是否已解决 | 本文如何填补（交 S3） | 证据状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Population 人群/样本 | 哪些人群、地区、企业、时期没被覆盖？ | | | | | | | |
| Concepts 概念 | 核心概念定义不一、测度不同或缺失？ | | | | | | | |
| Perspectives 视角 | 缺哪类主体或学科视角（如只看企业不看政府）？ | | | | | | | |
| Theory 理论 | 机制、模型或竞争解释缺失？ | | | | | | | |
| Analysis 分析 | 分析层次、指标、异质性、动态效应缺失？ | | | | | | | |
| Implication 启示 | 结论的政策或实践含义是否未被检验？ | | | | | | | |
| Methods 方法 | 数据来源、估计技术、样本构造有局限？ | | | | | | | |
| Methodology 方法论 | 研究设计或识别逻辑有根本局限（如无外生变异）？ | | | | | | | |

> Methods 偏“具体做法”（数据、估计量、样本构造），Methodology 偏“设计与识别逻辑”（因果推断范式、外生性来源）。这是本 Skill 的操作性区分，写表时在“判定问题”里保持一致。

**表 B：张力表**（已知与未知交界处的 inconsistencies / controversies / conflicts / contradictions）

| 张力类型 | 一侧主张（来源 + locator） | 另一侧主张（来源 + locator） | 可能原因（数据、制度、识别、定义） | 对应表 A 的哪一行缺口 |
| --- | --- | --- | --- | --- |
| Inconsistency 不一致 / Controversy 争议 / Conflict 冲突 / Contradiction 矛盾（择一） | | | | |

**表 C：缺口到框架的收口**：概念框架（现有文献共用的框架）→ 新理论框架（本文拟提出或修正的框架），一句话说明由表 A 哪几行缺口推出。

规则：
- “已知”列必须来自已登记的文献与三层定位锚点；读不到全文的条目标“仅摘要”，不得据此判定缺口。
- 张力表两侧各附出处，**不替研究者裁决**；已核实的张力同步记入 `Meta/review-queue.md`（状态 `open`）。
- “现有识别是否已解决”填 是 / 部分 / 否，并写依据；填“否”的才有资格成为主缺口。
- 表 A 与 §3 步骤 4 的文献簇可互相对应，但不替代文献矩阵。

## 4. 产出与知识回流
- 输出：检索记录、争论簇文献矩阵、研究缺口分类表（表 A/B/C，§3a）、未核实清单；写入项目目录或经研究者确认后按 `Templates/literature-note.md`（含 `cite_key` 与 `locator`）沉淀至 `03-Literature/`，更新 `Meta/index.md`、`Meta/log.md` 并刷新双地图。
- 下游交接：缺口与竞争机制交给 S3；`Meta/citation-map.json` 交给 S8/S10。

## 5. 硬性禁止
严禁编造作者/标题/年份/DOI；严禁把摘要当作全文实证细节（防 L3 错配）；严禁在没有定位锚点的情况下把文献写进强主张支撑。
