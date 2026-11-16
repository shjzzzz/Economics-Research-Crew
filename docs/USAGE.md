# 使用说明

本说明面向已把本扩展安装到研究库（下称 Vault，例如 `D:\TaxWiki`）的使用者。安装步骤见 [README](../README.md)。

## 1. 它是什么
一组放进 Claude Code 项目的配置：
- **6 个 Subagent**（`.claude/agents/`）：各有职责与证据标准的专业角色。
- **7 个 Skill**（`.claude/skills/`）：固定流程，用 `/名称` 触发。
- **项目规则**（`CLAUDE.md` + `.claude/ECONOMICS-RESEARCH.md`）：每次会话自动加载。
- **规范与模板**（`Meta/`、`Templates/`）：研究标准、来源登记、研究日志、文献/数据/分析模板。

它不包含计量软件，也不会自动跑回归；它约束 Claude 如何组织、检查和记录研究工作。

## 2. 开始一次会话
```powershell
Set-Location D:\TaxWiki
claude
```
首次使用先做只读检查：
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```
再用 `/agents` 确认 6 个 Agent，`/skills` 确认 7 个 Skill。

## 3. Skill 速查
| 命令 | 何时用 | 产出 |
|---|---|---|
| `/research-question <主题>` | 题目还是一个主题，没有可检验的问题 | ≤3 个候选问题、可行性评估、推荐一个 |
| `/literature-review <范围>` | 需要有来源的文献梳理 | 检索记录、文献矩阵、研究缺口、未核实清单 |
| `/theory-modeling <机制>` | 需要把机制写成模型 | 设定、假设、逐步推导、比较静态、可检验推论 |
| `/tax-policy-analysis <政策>` | 税制、征管、遵从、归宿问题 | 法源与有效性、机制、效率与分配、待官方确认项 |
| `/causal-inference-audit <设计>` | 设计 DID/IV/RDD 前后审查识别 | estimand、假设、威胁、检验、可用的因果措辞 |
| `/econometric-analysis <任务>` | 数据审计、实现与复现回归 | 分析计划、代码、样本核算、日志 |
| `/academic-review <稿件/设计>` | 投稿或汇报前挑刺 | Fatal / Major / Minor 分级意见 |

例：
```text
/causal-inference-audit 研究金税四期上线对企业税收遵从的影响，处理组为首批试点地区企业，双向固定效应 DID
```

## 4. 调用 Agent
Claude 会按 `.claude/ECONOMICS-RESEARCH.md` 的分派规则，在任务确实专业化、可并行或需要独立审查时委派。也可以直接点名：
```text
请用 academic-reviewer 审查 01-Research-Projects/XXX/draft.md，只列致命问题和重要问题。
```
| Agent | 职责 | 工具权限 |
|---|---|---|
| literature-agent | 检索、抽取、比较文献 | 读、搜、联网 |
| theory-agent | 模型推导与机制 | 读、写、编辑 |
| tax-policy-agent | 税法、征管、归宿 | 读、搜、联网 |
| econometrics-agent | 数据审计、估计、复现 | 读、写、编辑、Bash |
| causal-inference-agent | 识别与稳健性设计 | 读、搜、联网、写 |
| academic-reviewer | 对抗式审稿 | 只读、联网 |

只有 econometrics-agent 能执行 Bash；reviewer 不能写文件，避免“边审边改”。

## 5. 推荐工作流
1. `/research-question` 定题 → 把确认后的问题写入 `01-Research-Projects/<项目>/`（用 `Templates/research-project.md`）。
2. `/literature-review` → 文献笔记放 `03-Literature/`（`Templates/literature-note.md`）。
3. `/theory-modeling`、`/tax-policy-analysis` → 机制与制度背景放 `04-Theories/`、`08-Research-Notes/`。
4. 数据入 `06-Data/raw`（只读），在 `06-Data/metadata` 建数据卡（`Templates/dataset-card.md`）。
5. `/causal-inference-audit` 先审设计，再用 `Templates/analysis-plan.md` 写分析计划。
6. `/econometric-analysis` 执行；日志用 `Templates/analysis-log.md`，代码放 `07-Code/`。
7. `/academic-review` 独立审查；按意见修改后再定稿。
8. 每次重要工作在 `Meta/research-log.md` 记一行；新来源登记到 `Meta/source-registry.md`。

不要跳过第 5 步：能跑出回归不等于识别成立。

## 6. 它会遵守的规则
- `06-Data/raw` 只读；衍生数据只写 `06-Data/processed`。
- 不删除、不移动、不重命名现有 TaxWiki 笔记，除非你明确同意。
- 不编造文献、DOI、法条、数据或结果；查不到就标“未核实”。
- 区分相关与因果，先说 estimand 与假设。
- 税法结论要给文号、日期、生效与废止状态。
- 涉及个人或受限数据，不外发。

这些是写在指令里的约束，不是技术隔离：模型可能出错，权限提示与 Git 才是实际保险。重要结论请自行核对原始来源。

## 7. 自定义
- **改角色**：编辑 `.claude/agents/*.md`（`description` 决定何时被自动调用，`tools` 决定权限）。
- **加 Skill**：新建 `.claude/skills/<name>/SKILL.md`，frontmatter 需有 `name`（与目录同名）和 `description`。
- **改规则**：编辑 `CLAUDE.md` 或 `.claude/ECONOMICS-RESEARCH.md`。
- **改路径映射**：编辑 `Meta/vault-map.md`。
- 重装不会覆盖已改过的文件（已存在即跳过）；想拿回默认版本，先把旧文件改名再安装。

改完后运行 `Test-EconomicsResearchCrew.ps1` 检查结构。

## 8. 常见问题
- **`/agents` 看不到 Agent**：确认在 Vault 根目录启动 `claude`，且 `.claude/agents/` 下有文件；改动后重启会话。
- **安装脚本提示“跳过(已存在)”**：正常，说明保护了你已有的文件。
- **中文乱码**：用 UTF-8 打开；`.ps1` 已带 BOM，Windows PowerShell 5.1 与 pwsh 7 均可运行。
- **`-WithUpstream`**：需同时给 `-RepoUrl`；上游构建参数未经本项目验证，运行前请先读其 `launchme.sh`。
- **卸载**：本项目不提供自动卸载。按 `README` 列出的文件手动删除；安装前的 `CLAUDE.md` 等备份在 `_erc-backups/<时间戳>/`。
