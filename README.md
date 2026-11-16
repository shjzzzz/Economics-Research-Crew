# Economics Research Crew

面向税收经济学、公共经济学、计量经济学与因果推断的 Claude Code 研究环境扩展。

## 设计
- 6 个研究 Subagents、7 个 Skills、研究规范、模板。
- 不覆盖已有 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json`；不安装 MCP、不启用上游 Hooks。
- 不自动运行任何回归；脚本、数据、环境由研究者确认。
- 上游框架（My-Brain-Is-Full-Crew）为**可选**：加 `-WithUpstream` 才会克隆并在隔离目录构建。

## 安装
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -WhatIf   # 先预演
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki"           # 仅安装本扩展
.\Install-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki" -WithUpstream -RepoUrl "<上游仓库地址>"
.\Test-EconomicsResearchCrew.ps1 -VaultPath "D:\TaxWiki"
```
脚本只新增文件，已存在的文件一律跳过并列出；改动前备份 `CLAUDE.md`、`.mcp.json`、`.claude/settings.json` 到 `_erc-backups/<时间戳>/`。

## 首次对话
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```

## 用法
/research-question /literature-review /theory-modeling /tax-policy-analysis /causal-inference-audit /econometric-analysis /academic-review

## 规范摘要
原始数据只读；不删除文件；不虚构文献/法条/结果；区分相关与因果；结果必须关联脚本、数据版本与样本；法规核验时效。

## 验证流程
1. `Test-EconomicsResearchCrew.ps1`：文件存在、frontmatter 合法（name/description）、agent 名与文件名一致、根 CLAUDE.md 含 import。
2. 在 Claude Code 中运行 `/agents` 应列出 6 个 Agent；`/skills` 应列出 7 个 Skill。
3. 冒烟测试：`/causal-inference-audit` 给一个 DID 设想，检查是否先问 estimand 而不是直接跑回归。
