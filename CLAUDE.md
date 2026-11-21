# Economics Research Crew（开发仓库）

这是**安装包源码**，不是研究库。`payload/` 由安装器装进用户的 Obsidian 库；`payload/CLAUDE.template.md` 是装给库的模板，不是本文件。

## 目录
- `payload/`：必装内容（17 个 Skill、7 个 Agent、Meta、Templates、hooks、scripts）。
- `payload-extras/`：可选扩展（50 个第三方 Skill），**已 gitignore，不得提交**（上游多数无许可证），只有其 README 入库。
- `tools/`（跨平台安装 CLI、ARS 追踪）、`tests/`、`docs/`、`README.md`。

## 验证（改动后必跑，两个宿主都要过）
- `pwsh -NoProfile -File tests\run.ps1`
- `powershell -NoProfile -File tests\run.ps1`
- 预期 246 项通过；本机放置 extras 时为 249 项。

## 规则
- 改 `payload/` 里 Skill / Agent 的数量或名称，须同步 README、docs/USAGE.md、两个 checker（`Test-EconomicsResearchCrew.ps1`、`tools/erc_cli.py`）、`tests/run.ps1` 和 PPT 的数字。
- 新增第三方 Skill 前先确认许可证；仅 MIT 等允许再分发的可进 `payload/`，并附 LICENSE。
- 行尾：`*.sh`、`*.py` 用 LF；`.ps1` 保留 BOM。
- 不要提交 `_erc-backups/`、`tasks/`；push 前需经用户确认。

## 多代理分工
- 主会话（Opus 5.5，high）负责规划、决策、整合；子代理（Sonnet，medium）见 `.claude/agents/`：`code-analyst`（只读分析）、`code-implementer`（改代码并测试）、`docs-researcher`（查官方文档）。通用规则与顾问触发时机见用户级 `~/.claude/CLAUDE.md`。
- 改安装器、hooks 或 `payload/.claude/scripts/` 这类代码时，委派前先说明数量；`code-implementer` 完成后，主会话自己复核 `git diff` 并重跑上面两条测试，不直接采信报告。
