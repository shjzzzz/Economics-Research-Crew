# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Economics Research Crew（开发仓库）

这是**安装包源码**，不是研究库。`payload/` 由安装器装进用户的 Obsidian 库；`payload/CLAUDE.template.md` 是装给库的模板，不是本文件。

## 目录
- `payload/`：必装内容（17 个 Skill、7 个 Agent、Meta、Templates、hooks、scripts）。
- `payload-extras/`：可选扩展（50 个第三方 Skill），**已 gitignore，不得提交**（上游多数无许可证），只有其 README 入库。
- `tools/`（跨平台安装 CLI、ARS 追踪）、`tests/`、`docs/`、`README.md`。

## 验证（改动后必跑，两个宿主都要过）
- `pwsh -NoProfile -File tests\run.ps1`
- `powershell -NoProfile -File tests\run.ps1`
- 预期 344 项通过（本机安装 `claude` CLI 时为 345 项，同时放置 extras 时为 348 项）。

## 规则
- 改 `payload/` 里 Skill / Agent 的数量或名称，须同步 README、docs/USAGE.md、两个 checker（`Test-EconomicsResearchCrew.ps1`、`tools/erc_cli.py`）、`tests/run.ps1` 和 PPT 的数字。
- 新增第三方 Skill 前先确认许可证；仅 MIT 等允许再分发的可进 `payload/`，并附 LICENSE。
- 行尾：`*.sh`、`*.py` 用 LF；`.ps1` 保留 BOM。
- 不要提交 `_erc-backups/`、`tasks/`；push 前需经用户确认。

## 常用命令
- 安装到库（预演不写入）：`.\Install-EconomicsResearchCrew.ps1 -VaultPath <库> -WhatIf`；常用开关 `-Platform auto|claude|agy|codex|all`、`-WithHooks`、`-WithExtras`、`-Update`（差异写 `.new`，不覆盖）。
- 跨平台等价入口：`./install.sh --vault <库> ...` 或 `python tools/erc_cli.py install|test|sync|check-ars`。
- 校验已安装的库：`.\Test-EconomicsResearchCrew.ps1 -VaultPath <库>`。
- 同步 AGENTS.md 的 ERC 区块：`.\Sync-AgentsMd.ps1 -VaultPath <库> [-Check]`。
- 上游 ARS 更新检查（零 LLM 额度；无更新退出码 0，有更新 2）：`python tools/check_ars_updates.py check`。
- `tests/run.ps1` 没有单测选择器，按编号分节（`[1]`…`[17]`）；要单独调试某节，直接读该节并手动运行对应安装/检查命令。
- `tests/refmgr_selftest.py <库>/.claude/scripts/paper_tools.py <库>`：离线测 EndNote/Zotero 交换。
- `tests/routing_eval.py --vault <一次性库>`：**消耗 Claude Code 额度**，只在用户明确要求时运行；拒绝在已有 `settings.local.json` 的库上运行。

## 架构（需跨文件理解）
- **单一事实来源**：`payload/.claude/` 是唯一正本。`tools/build_platform.py` 从它生成 agy / Codex 的 `.agents/`（脚本路径改写）与 `AGENTS.erc.md`，因此不要手改生成物，改正本后重新生成。
- **三条安装路径**：`Install-EconomicsResearchCrew.ps1`（PS 5.1/7）与 `tools/erc_cli.py`（Python）实现同一套逻辑，行为必须一致；`install.sh` 只是 `erc_cli.py` 的封装。改安装行为须两处同改。
- **hooks 合并**：`payload/.claude/settings.hooks.json` 是片段，经 `tools/merge_hooks.py` 幂等并入用户 `settings.json`（按脚本文件名判重，从不重复，不动其他键）；hook 命令在 Windows 用 `python`，macOS/Linux 自适应 `python3`。
- **路由与流水线**：`payload/.claude/routing-triggers.json`（触发词→Skill/Agent）、`pipeline-stages.json`（阶段定义，供 `orchestrator.py` 使用）；改触发词后用 `tests/routing_cases.json` 对应的用例核对。
- **库的内容模型**：`Meta/` 为控制面（规范、日志、索引），四层知识流与只读层（Tier 0 由 hook 拦写）见 `README.md`「核心架构」；`payload/CLAUDE.template.md` 才是装进用户库的 CLAUDE.md。
- **许可边界**：`Imbad0202/academic-research-skills`（CC-BY-NC-4.0）只借设计模式、原生重写，禁止拷入其代码或提示词；映射见 `Meta/upstream-ars.json`。
## 多代理分工
- 主会话（Opus 5.5，high）负责规划、决策、整合；子代理（Sonnet，medium）见 `.claude/agents/`：`code-analyst`（只读分析）、`code-implementer`（改代码并测试）、`docs-researcher`（查官方文档）。通用规则与顾问触发时机见用户级 `~/.claude/CLAUDE.md`。
- 改安装器、hooks 或 `payload/.claude/scripts/` 这类代码时，委派前先说明数量；`code-implementer` 完成后，主会话自己复核 `git diff` 并重跑上面两条测试，不直接采信报告。
