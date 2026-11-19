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
5. **识别真实缺口与竞争解释**：区分“没人写过”与“值得写且现有识别未解决”，并列出竞争性解释。
6. **三层定位锚点与引文登记**：每条重要主张记录页码/表号/公式/条款（`--locator`）与主张适用边界（`--claim-scope`）。
   - 已有 `03-Literature/*.md` 文献卡：优先运行 `python .claude/scripts/paper_tools.py cite from-note <卡片路径>` 桥接入库。
   - 新增引文：运行 `python .claude/scripts/paper_tools.py cite add --key <k> --title "…" --year Y [--doi D] --locator "…" --claim-scope "…"`；中文文献加 `--type chinese`，法规加 `--type legal --doc-no "…" --effective YYYY-MM-DD`，均须由研究者核对原文后执行 `cite confirm`。

## 4. 产出与知识回流
- 输出：检索记录、争论簇文献矩阵、精确研究缺口、未核实清单；写入项目目录或经研究者确认后按 `Templates/literature-note.md`（含 `cite_key` 与 `locator`）沉淀至 `03-Literature/`，更新 `Meta/index.md`、`Meta/research-log.md` 并刷新双地图。
- 下游交接：缺口与竞争机制交给 S3；`Meta/citation-map.json` 交给 S8/S10。

## 5. 硬性禁止
严禁编造作者/标题/年份/DOI；严禁把摘要当作全文实证细节（防 L3 错配）；严禁在没有定位锚点的情况下把文献写进强主张支撑。
