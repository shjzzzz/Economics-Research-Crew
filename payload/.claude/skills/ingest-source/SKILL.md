---
name: ingest-source
description: "Ingest one source (paper, report, legal document, data note) into the research wiki in two steps: analyze first, write only after the researcher approves; cross-link concept pages and prepare cite_key for paper writing. Use for 摄入文献、入库、把这篇论文加入知识库、处理 _sources 里的文件."
argument-hint: "[path to a file under 03-Literature/_sources/]"
data_access_level: raw
task_type: open-ended
---

# Ingest Source（两步摄入：原始来源 → 复利知识库）

## 1. 目标与边界
一次只处理一个原始来源，严格分两步执行：**先分析并停下等研究者确认，确认后再写入**。不仅生成孤立文献卡，更推动跨文献概念页（`04-Theories/`、`05-Methods/`、`MOC/`）复利生长，并预置 `cite_key` 桥接论文引文表。

## 2. 前置检查
1. 读取 `Meta/purpose.md`（未填则提醒并按“方向未定”处理）、`Meta/index.md`、`Meta/link-map.md`、`Meta/source-registry.md`。
2. 核实来源位于 `03-Literature/_sources/`（若在别处，请研究者自行移入；**不得移动、改名或修改原始文件**）。
3. 计算哈希去重：`python .claude/scripts/wiki_lint.py hash <文件> --vault .`。若返回 `ALREADY REGISTERED`，停止并告知，除非研究者明确要求重新摄入。

## 3. 核心两步流程
### 第一步：分析（不写任何文件，输出后必须停止等待确认）
1. **全文通读**：读不到全文（仅摘要、扫描不清、受限）须如实说明，不得用摘要推断细节。
2. **结构化抽取**：
   - 学术文献：研究问题、理论与机制、数据与样本、变量、识别策略、核心定量结果（含量级）、稳健性、局限；每条关键主张附三层定位锚点（页码/表/图/公式），拟定规范英文 `cite_key`（如 `chetty2009salience`）与 `claim_scope`。
   - 法规文件：发文机关、文号、发布日期、生效日期、废止/修订状态、过渡条款、适用范围。
3. **跨库比对与知识复利评估**：
   - 查 `Meta/index.md` 与 `Meta/link-map.md`：找出可关联的已有文献卡、机制页（`04-Theories/`）和方法页（`05-Methods/`）。
   - 列出**矛盾与张力**：两侧主张各自附原始来源与位置，绝不擅自裁决。
4. **拟改动清单**：新建哪张文献卡、建议在哪些已有概念/机制/方法页追加双链或对照段落（每条一句话）。
5. **未核实项与待研究者判断项**。

**输出以上分析后立即停下，等待研究者确认或调整范围。**

### 第二步：写入（仅在确认后执行）
1. 按 `Templates/literature-note.md` 写入 `03-Literature/`，frontmatter 必填：`type: literature`、`cite_key`、`title`、`locator`、`claim_scope`、`sources`（指向 `_sources` 文件）、`sha256`、`updated`、`verification`（`verified | unverified`）。
2. 更新已确认触及的 `04-Theories/`、`05-Methods/` 或 `MOC/` 页面：只追加相关段落与 `[[双链]]`，不整页重写；文末“更新记录”注明日期与来源。
3. 矛盾处理：在相关页面并列写出两侧主张与来源，同时记入 `Meta/review-queue.md`（状态 `open`）。
4. 更新 `Meta/index.md`（每页一行，附 `cite_key`）、在 `Meta/source-registry.md` 登记 SHA256 与访问日期、在 `Meta/log.md` 追加 `## [YYYY-MM-DD] ingest | 标题`。
5. 若研究者同意同时进入论文引文表，运行 `python .claude/scripts/paper_tools.py cite from-note <文献卡路径>`（中文/法规条目提醒人工 `cite confirm`）。
6. 运行 `python .claude/scripts/wiki_lint.py map --vault .` 刷新双地图，再运行 `python .claude/scripts/wiki_lint.py lint --vault .`；有错误必须修完再收尾。

## 4. 产出与知识回流
- 新增/更新的 Tier 1 知识页、更新后的 `index`/`source-registry`/`log`、刷新后的两张地图与 lint 报告。

## 5. 硬性禁止
禁止跳过确认直接写文件；禁止修改或移动 `03-Literature/_sources/`；禁止编造 DOI/页码/法条；禁止擅自裁决来源矛盾；禁止把受限/含个人信息来源外发外部服务。
