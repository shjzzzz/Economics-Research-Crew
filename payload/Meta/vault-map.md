---
inbox: 00-Inbox
projects: 01-Research-Projects
areas: 02-Areas
resources: .
literature: 03-Literature
literature_raw: 03-Literature/_sources
theories: 04-Theories
methods: 05-Methods
data_raw: 06-Data/raw
data_processed: 06-Data/processed
data_metadata: 06-Data/metadata
code: 07-Code
notes: 08-Research-Notes
writing: 09-Writing
archive: 10-Archive
templates: Templates
meta: Meta
moc: MOC
---

# Vault Map（四层知识架构与 Meta 控制面）

## 四层知识流
1. **Tier 0 原始只读层（Immutable Sources）**
   - `00-Inbox/`：`/ingest-source` 默认待摄入原始来源入口（如 `00-Inbox/文献/`；摄入时不原地修改、移动或删除原始文件）。
   - `03-Literature/_sources/`：已归档原始文献 PDF / 剪藏（只读，可新增、不得覆盖或修改）。
   - `06-Data/raw/`：原始数据（只读，禁止任何原地清洗或覆盖）。
   - 库根目录既有笔记（文献库/知识库，`resources: .`）：保持原位、不移动/重命名/批量改写，仅作本地参考资料，不自动视为已核实结论。
2. **Tier 1 跨项目复利知识层（Compounding Wiki Graph）**
   - `02-Areas/`：长期职责与主题领域页（如税收政策、财政分权等持续关注方向；跨项目复用，可链接文献、理论与项目）。
   - `03-Literature/`：结构化文献卡（含 `cite_key` 与三层证据定位，可桥接 `Meta/citation-map.json`）。
   - `04-Theories/`：理论模型、机制与竞争假说页。
   - `05-Methods/`：识别策略、现代估计量与诊断方法页。
   - `08-Research-Notes/`：跨文献综合页（`type: synthesis`）、问答回存（`type: query`）与结项回流摘要。
   - `MOC/`：主题枢纽索引页（Map of Content）。
3. **Tier 2 项目执行与手稿层（Project Workspace，按项目隔离）**
   - `01-Research-Projects/<project>/`：
     - `PROJECT.md`：项目入口页（进 `Meta/index.md` 与双链图）。
     - `STATE.json`：阶段机读状态（仅由 `orchestrator.py` 维护）。
     - `analysis-plan.md`、`analysis-log.md`：预设分析计划与执行日志。
     - `paper/`：该项目全部论文产物（`outline.md`、`draft.md`、`versions/`、`worklog-vN.md`、`reviews.json`、`polished.md`、`final.md`、`rebuttal-matrix.md`、`ai-disclosure.md`）。项目内部手稿与版本快照不进入全库双链图，避免多项目并行时的重名与孤立页噪音。
   - `06-Data/processed/` + `06-Data/metadata/`：衍生数据与数据卡（建议按 `<project>/` 分目录）。
   - `07-Code/{python,R,stata}/`：模块化脚本（建议按 `<project>/01_clean..05_mechanisms` 组织）。
4. **Tier 3 独立交付与归档层（Outputs & Archive）**
   - `09-Writing/`：**仅放非完整研究项目的独立文稿**（政策简报、书评、教学讲义、审稿报告、投稿导出包），不与 `01-Research-Projects/<project>/paper/` 重叠。
   - `10-Archive/`：已结项项目归档。

## Meta 控制面（三类文件）
- **静态规范（研究者可编辑）**：`purpose.md`、`research-standards.md`、`collaboration-protocol.md`、`style-guide.md`、`mechanism-library.md`、`ai-tells.json`、`vault-map.md`。
- **协作账本（人机共同维护）**：`index.md`、`source-registry.md`、`log.md`、`review-queue.md`、`decisions.md`、`constraints.md`（研究者纠正）、`aliases.csv`（术语别名）。
- **脚本独占机读文件（禁止手改）**：`citation-map.json`、`results-ledger.json`（`paper_tools.py`）；`run-ledger.jsonl`（`orchestrator.py`）；`folder-map.md`、`link-map.md`（`wiki_lint.py map`，精简版嵌入 `CLAUDE.md`/`AGENTS.md` 的 `ERC:MAP` 区块）。

## 检索边界
- 检索库根目录既有笔记时排除 `.claude`、`.agents`、`_vendor`、`_erc-staging`、`_erc-backups`、`06-Data`、`07-Code`。
- 若本文件安装前已存在，安装器不会覆盖，请手动比对更新。
