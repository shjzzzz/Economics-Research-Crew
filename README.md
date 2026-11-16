# Economics Research Crew

面向税收经济学、公共经济学、计量经济学与因果推断的研究环境扩展，支持 Claude Code、Antigravity CLI（`agy`）与 Codex CLI。

## 设计
- 6 个研究 Subagents、11 个 Skills（含 `/research-pipeline` 研究总协调与质量闭环，以及 `/ingest-source`、`/query-wiki`、`/wiki-lint` 知识库维护流程）、研究规范、模板。
- 路由规则与角色映射见 [docs/USAGE.md](docs/USAGE.md) 第 4 节。
- 借鉴 llm_wiki 的“可积累 wiki”思路（purpose / index / log / 两步摄入 / lint）与 My-Brain-Is-Full-Crew 的 hooks 强制执行、安装器回归测试。
- 不覆盖已有 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`；不安装 MCP、不启用上游 Hooks。
- 不自动运行任何回归；脚本、数据、环境由研究者确认。
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
/research-question /literature-review /theory-modeling /tax-policy-analysis /causal-inference-audit /econometric-analysis /academic-review /ingest-source /query-wiki /wiki-lint /research-pipeline

## 规范摘要
原始数据只读；不删除文件；不虚构文献/法条/结果；区分相关与因果；结果必须关联脚本、数据版本与样本；法规核验时效。

## 验证流程
1. `Test-EconomicsResearchCrew.ps1`：文件存在、frontmatter 合法（name/description）、agent 名与文件名一致、根 CLAUDE.md 含 import。
2. 在 Claude Code 中运行 `/agents` 应列出 6 个 Agent；`/skills` 应列出 11 个 Skill。
3. 回归测试：`powershell -NoProfile -File tests\run.ps1` 与 `pwsh -NoProfile -File tests\run.ps1`（需要 Python；全部在临时目录进行，不碰你的库）。
   路由测试（消耗 Claude 额度）：`python tests/routing_eval.py --vault <装好本扩展的临时库>`。
4. 冒烟测试：`/causal-inference-audit` 给一个 DID 设想，检查是否先问 estimand 而不是直接跑回归。
