---
name: query-wiki
description: "Answer a research question from the accumulated wiki (and project decisions) with traceable citations, separating wiki-sourced facts from inference, and offer to file synthesis notes back into the wiki. Use for 知识库里有什么、库里有哪些证据、根据知识库回答、查一下我们已有的文献."
argument-hint: "[question]"
data_access_level: redacted
task_type: open-ended
---

# Query Wiki（沿图谱检索与证据综合）

## 1. 目标与边界
基于已积累的 Tier 1 知识库与项目决策记录回答研究问题，严格区分“库内一手依据”与“AI 推断”。**不用常识补齐库里不存在的事实，绝不冒充库内结论。**

## 2. 前置读取与检索顺序
1. 先读 `Meta/purpose.md`、`Meta/decisions.md`、`Meta/index.md` 与 `Meta/link-map.md`（优先锁定枢纽页与 `MOC/`）。
2. **全文召回（跨文献问答必做）**：运行 `python .claude/scripts/kb_search.py search --vault . '<关键词>' --expand-links 1`（本地 BM25，无模型、无网络；关键词用空格分隔，中文词至少 2 个字，可用 `--mode all` 要求全部命中、`--type literature --year 2015-2022` 过滤；索引随检索自动增量更新）。中英文关键词各试一次；同义词记入 `Meta/aliases.csv`（`canonical,alias`）。**命中只是线索，不是结论**：必须打开命中页原文核对，引用时带 `cite_key`、命中的标题路径/行号与文献卡 `locator`。旧税法笔记用 `--scope legacy`。零命中如实答“库内证据不足”，不得用常识补齐。
3. 从相关枢纽页和条目进入正文，再沿 `[[双链]]`（`Meta/link-map.md` 邻接表）向外展开 1–2 跳；若涉及在研项目进展，补充读取 `01-Research-Projects/<项目>/PROJECT.md`。
4. 必要时按目录检索库内既有旧税法笔记，**严禁**在 `.claude`、`.agents`、`_vendor`、`_erc-*`、`06-Data`、`07-Code` 中查找税法笔记。

## 3. 核心回答结构
1. **核心结论**：先给直接、克制的结论（不足以定论则直说“库内证据不足”）。
2. **库内依据（Fact）**：每条主张标明 `[[页面]]` 与其 `sources` 中的原始来源及定位锚点（页码/表/节/文号）；若用于论文写作准备，顺带列出各文献卡的 `cite_key`。
3. **综合推断（Inference）**：显式单独标注基于上述依据做出的归纳或演绎，说明适用条件，不与原文事实混写。
4. **未核实项与来源冲突**：引用 `verification: unverified` 页面或存在 `Meta/review-queue.md` 未决矛盾时必须标出；法规结论须注明发文机关、文号、生效/废止状态，并提醒本地资料不自动等于现行有效法。
5. **知识库盲区与下一步**：明确列出“库中没有覆盖的部分”，建议对应 `/literature-review` 或 `/ingest-source`。

## 4. 产出与知识回流
- 回答结束后询问研究者是否回存为笔记：
  - 一般问答 → `08-Research-Notes/`（`type: query`）；
  - 面向 `/paper-outline` 的跨文献证据综合 → `08-Research-Notes/`（`type: synthesis`，附 `[[双链]]` 与文献簇归纳）。
- **经研究者同意才写入**；写入后更新 `Meta/index.md`、在 `Meta/log.md` 追加 `## [YYYY-MM-DD] query | 问题`（或 `synthesis`），并运行 `python .claude/scripts/wiki_lint.py map --vault .`。

## 4b. 检索自测模式（研究者要求“测一下检索”时）
从库内随机抽 5–10 页，各出一个只能由该页回答的问题，另出 2–3 个库内确无答案的问题；按本 Skill 流程作答，统计是否找到正确页（并记录目标页在 `kb_search.py search` 结果中的名次：Top-5 / Top-10 / 未召回）、无答案题是否如实答“库内证据不足”。把漏检原因（页面缺双链、未入 `Meta/index.md`、标题不含关键词、`keywords` 未同时写中英文、`Meta/aliases.csv` 缺同义条目）列为建议，**只报告，不改页面**。

## 5. 硬性禁止
禁止用模型常识填补库内缺口并包装为“库内已有证据”；禁止在未核对多页的情况下宣称“文献一致认为”；禁止把 `kb_search.py` 的命中片段当结论引用；禁止未经同意擅自新建笔记。
