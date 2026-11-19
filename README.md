# Economics Research Crew

面向税收经济学、公共经济学、计量经济学与因果推断的研究环境扩展，支持 Claude Code、Antigravity CLI（`agy`）与 Codex CLI。

## 设计
- **7 个研究 Subagents、15 个核心 Skills**（统一高信号中文+英文术语五段式规范，覆盖 S1–S12 研究与论文写作全周期以及 `/ingest-source`、`/query-wiki`、`/wiki-lint` 可复利知识库流程）、研究规范与模板。
- **经济学论文论证脊柱（Argument Spine）**：将 `S1 问题与 Estimand → S2 争论簇文献矩阵 → S3 竞争性机制与政策冲击要素 → S4 威胁—检验—证伪矩阵与因果措辞上限 → S5 模块化脚本、样本瀑布与结果入簿 → S6–S7 独立对抗审查（F1/M1/m1 + 5 维分 + 7 类失效闸门）→ S8 6 步引言蓝图与主张清单 → S9 三层锚点引文表（支持 cite from-note 从文献卡桥接）→ S10–S12 受限成稿、清单精修、可选润色、AI 披露与知识回流` 贯通为闭环。
- **四层知识架构与双地图**：区分 Tier 0 原始只读层、Tier 1 跨项目复利 Wiki、Tier 2 项目执行与手稿（仅 `PROJECT.md` 进索引与双链图，`paper/` 与版本快照不污染全库图谱）、Tier 3 独立文稿与归档（`09-Writing/` 仅放非项目独立文稿）及 Meta 三分控制面；两张自动生成地图（`Meta/folder-map.md`、`Meta/link-map.md`）及其精简版写在 `CLAUDE.md` / `AGENTS.md` 的 `ERC:MAP` 标记之间，由 `wiki_lint.py map` 生成；旧税法笔记只做目录级汇总。
- 路由规则与角色映射见 [docs/USAGE.md](docs/USAGE.md) 第 4 节。
- 语言精修借鉴（思路，已按本项目约束重写，未复制文本）：`AIScientists-Dev/academic-humanizer`（MIT）、`hanlulong/econ-writing-skill`（MIT）、`humanizer-zh-academic`（MIT，仅采用中文套话的模式分类，**不采用**其“降低 AIGC 检测率”目标）；`franklee16/academic-research-skills` 为汇编库，根目录无许可证，仅作参考。本项目不用于规避 AI 检测，AI 参与仍须按期刊要求披露。
- 借鉴 `llm_wiki` 的“可积累 wiki”思路（purpose / index / log / 两步摄入 / lint）、`My-Brain-Is-Full-Crew` 的 hooks 强制执行与安装器回归测试，以及 `Imbad0202/academic-research-skills` 的设计理念（苏格拉底防越位、魔鬼代言人让步门槛与框架锁定检测、L3 引文锚点与主张对齐审计、`data_access_level` 数据隔离、7 类 AI 失效模式闸门、文风校准与 R&R 返修追溯矩阵；仅借设计模式并在本项目原生重写，不含其代码）。
- 不覆盖已有 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`；不安装 MCP、不启用上游 Hooks。
- 不自动运行任何回归；脚本、数据、环境由研究者确认。
- 扩展 Skills 为**可选**：加 `-WithExtras` 安装 `payload-extras/` 中的第三方 Skill（未经本项目审计）。公开仓库只含上游为 MIT 许可的两个（`neishengxing-main`、`thu-digitizer-main`，来自 `franklee16/academic-research-skills` 汇编库，保留其 LICENSE），其余无许可证或非商用许可的不随仓库发布，见 `payload-extras/README.md`；安装器不配置任何 MCP。
- 上游框架（My-Brain-Is-Full-Crew）为**可选**：加 `-WithUpstream` 才会克隆并在隔离目录构建。

## 安装
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki" -WhatIf   # 先预演
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki"           # 仅安装本扩展（默认 -Platform auto）
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki" -Platform all       # 指定平台：auto | claude | agy | codex | all
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki" -WithHooks            # 可选：安装 hooks（合并 settings.json）
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki" -Update               # 升级：差异文件生成 .new，不覆盖
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki" -WithUpstream -RepoUrl "<上游仓库地址>"
.\Test-EconomicsResearchCrew.ps1 -VaultPath "D:\Economicresearchwiki"
```
脚本只新增文件，已存在的文件一律跳过并列出；改动前备份 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`、`AGENTS.md`、`.agents/hooks.json` 到 `_erc-backups/<时间戳>/`。

### 编排层（Research Director）
`/research-pipeline` 通过 `.claude/scripts/orchestrator.py` 维护项目状态 `01-Research-Projects/<项目>/STATE.json` 和派出日志 `Meta/run-ledger.jsonl`（只通过脚本修改）：`init / status / next / artifact / verify / gate / fail / recover / enforce / log`。阶段定义在 `.claude/pipeline-stages.json`，交接模板在 `Templates/handoff.md`。
- **关卡只由研究者决定：** 脚本需要 `--note`；`gate` 命令经 hook 触发权限提示，研究者确认后才执行。
- **Claude Code 下的强制（`-WithHooks`）：** 不能派出后续阶段的 Agent、重试（每个 Agent 每阶段最多 2 次）用尽后不能再派、同时运行数不得超过阶段上限（默认 1，S3 为 2，硬上限 3）；直接编辑 `STATE.json` / 账本会被拦。`orchestrator.py enforce off` 可关闭拦截，`recover` 清理残留记录。
- agy / Codex 没有这层 hook，命令照常可用，规则靠遵守。

### 论文写作与人机协作（S8–S12）
借鉴 PaperOrchestra 的思路（只借想法，不含其代码）：写作输入受限，引文与数字机械地可追溯。
- 流程：大纲 `/paper-outline` → 引文 → 成稿 `/paper-draft` → 精修 `/paper-refine`（最多 3 轮，改进才接受）→ 语言精修 `/paper-polish`（数字、引文、占位符机械核对不变）→ 终检；每步有研究者检查点 C1–C5，规则见 `Meta/collaboration-protocol.md`。
- `paper_tools.py`：引文表（Crossref 联网核验，**只发送被引文献的标题/DOI，不发送研究内容**；中文文献与法规文件标为人工核验，法规须写文号与生效日期；`--offline` 或 `ERC_OFFLINE=1` 可关闭）、结果登记簿（正文数字写成 `{{res:id}}`）、精修判定、`report` 指标。
- 稿内标记：引用 `[@key]`、数字 `{{res:id}}`、AI 提问 `⟦问：…⟧`、研究者回答 `⟦答：…⟧`。
- 期刊模板 `Templates/venues/` 只给通用章节骨架，篇幅与格式要求须由研究者对照官网核对；`Meta/mechanism-library.md` 的参考文献全部标“待核实”。
- 源稿为 Markdown，可用 pandoc 导出 docx / LaTeX（`paper_tools.py cite bib` 生成 BibTeX）。

### 多平台（自适应）
`-Platform auto`（默认）检测本机已安装的 `claude`、`agy`、`codex`，只为检测到的平台生成文件；都没检测到时安装 Claude Code 版。`payload/.claude/` 是唯一源，其他平台的文件在安装时生成（需要 python）。

| 平台 | 规则 | Skills | Agents | Hooks（`-WithHooks`） | 状态 |
|---|---|---|---|---|---|
| Claude Code | `CLAUDE.md` + `.claude/ECONOMICS-RESEARCH.md` | `.claude/skills/` | `.claude/agents/` | `.claude/settings.json` | 已测试 |
| Antigravity（agy） | 根 `AGENTS.md` 中带标记的区块（自包含，≤24 KB） | `.agents/skills/` | `.agents/agents/`（subagent） | `.agents/hooks.json` 的 `economics-research-crew` 键：原始材料保护 + 路由提示 | 已在 agy 1.5.9 冒烟测试 |
| Codex CLI | 同上 `AGENTS.md` | `.agents/skills/` | `.agents/agents/` 作为角色说明读取 | 无（原始材料保护仅靠规则文本） | 仅生成文件，**未运行测试** |

`.\Sync-AgentsMd.ps1` 以库里当前的 `CLAUDE.md` 为准重新生成 `AGENTS.md` 区块，保持两者一致。

已存在的 `AGENTS.md` 只追加区块、不覆盖；`-Update` 时若区块过期，生成 `AGENTS.md.new` 供比对。

详细用法见 [docs/USAGE.md](docs/USAGE.md)。

## 首次对话
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```

## 用法
/research-question /literature-review /theory-modeling /tax-policy-analysis /causal-inference-audit /econometric-analysis /academic-review /ingest-source /query-wiki /wiki-lint /paper-outline /paper-draft /paper-refine /paper-polish /research-pipeline

## 规范摘要
原始数据只读；不删除文件；不虚构文献/法条/结果；区分相关与因果；结果必须关联脚本、数据版本与样本；法规核验时效。

## 验证流程
1. `Test-EconomicsResearchCrew.ps1`：文件存在、frontmatter 合法（name/description）、agent 名与文件名一致、根 CLAUDE.md 含 import。
2. 在 Claude Code 中运行 `/agents` 应列出 7 个 Agent；`/skills` 应列出 15 个 Skill。
3. 回归测试：`powershell -NoProfile -File tests\run.ps1` 与 `pwsh -NoProfile -File tests\run.ps1`（需要 Python；全部在临时目录进行，不碰你的库）。
   路由测试（消耗 Claude 额度）：`python tests/routing_eval.py --vault <装好本扩展的临时库>`。
4. 冒烟测试：`/causal-inference-audit` 给一个 DID 设想，检查是否先问 estimand 而不是直接跑回归。
