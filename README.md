# Economics Research Crew

面向税收经济学、公共经济学、计量经济学与因果推断的 Claude Code 研究环境扩展。

## 设计
- 6 个研究 Subagents、10 个 Skills（含 `/ingest-source`、`/query-wiki`、`/wiki-lint` 知识库维护流程）、研究规范、模板。
- 借鉴 llm_wiki 的“可积累 wiki”思路（purpose / index / log / 两步摄入 / lint）与 My-Brain-Is-Full-Crew 的 hooks 强制执行、安装器回归测试。
- 不覆盖已有 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`；不安装 MCP、不启用上游 Hooks。
- 不自动运行任何回归；脚本、数据、环境由研究者确认。
- 上游框架（My-Brain-Is-Full-Crew）为**可选**：加 `-WithUpstream` 才会克隆并在隔离目录构建。

## 安装
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -WhatIf   # 先预演
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki"           # 仅安装本扩展
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -WithHooks            # 可选：安装 hooks（合并 settings.json）
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -Update               # 升级：差异文件生成 .new，不覆盖
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -WithUpstream -RepoUrl "<上游仓库地址>"
.\Test-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki"
```
脚本只新增文件，已存在的文件一律跳过并列出；改动前备份 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json` 到 `_erc-backups/<时间戳>/`。

详细用法见 [docs/USAGE.md](docs/USAGE.md)。

## 首次对话
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```

## 用法
/research-question /literature-review /theory-modeling /tax-policy-analysis /causal-inference-audit /econometric-analysis /academic-review /ingest-source /query-wiki /wiki-lint

## 规范摘要
原始数据只读；不删除文件；不虚构文献/法条/结果；区分相关与因果；结果必须关联脚本、数据版本与样本；法规核验时效。

## 验证流程
1. `Test-EconomicsResearchCrew.ps1`：文件存在、frontmatter 合法（name/description）、agent 名与文件名一致、根 CLAUDE.md 含 import。
2. 在 Claude Code 中运行 `/agents` 应列出 6 个 Agent；`/skills` 应列出 10 个 Skill。
3. 回归测试：`powershell -NoProfile -File testsun.ps1` 与 `pwsh -NoProfile -File testsun.ps1`（需要 Python；全部在临时目录进行，不碰你的库）。
4. 冒烟测试：`/causal-inference-audit` 给一个 DID 设想，检查是否先问 estimand 而不是直接跑回归。
