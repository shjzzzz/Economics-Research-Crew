# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Economics Research Crew（开发仓库）

这是**安装包源码**，不是研究库。`payload/` 由安装器装进用户的 Obsidian 库；`payload/CLAUDE.template.md` 是装给库的模板，不是本文件。

## 目录
- `payload/`：必装内容（18 个 Skill、7 个 Agent、Meta、Templates、hooks、scripts）。
- `payload-extras/`：可选扩展（`agents/` 与 `extras/` 说明；24 个第三方 Skill 已直接装在研究库 `.claude/skills`、`.agents/skills`，本地不再存放 `skills/`），**已 gitignore，不得提交**（上游多数无许可证），只有其 README 入库。
- `tools/`（跨平台安装 CLI、ARS 追踪）、`tests/`、`docs/`、`README.md`。

## 验证（改动后必跑，两个宿主都要过）
- `pwsh -NoProfile -File tests\run.ps1`
- `powershell -NoProfile -File tests\run.ps1`
- 支持按节调试：`pwsh -NoProfile -File tests\run.ps1 -Section 11,17,18`（省略 `-Section` 时全量运行 `[1]`…`[20]`）。
- 预期 475 项通过（本机安装 `claude` CLI 时为 476 项；本地放有 `payload-extras/skills` 时再加 3 项 extras 检查）。

## 规则
- 改 `payload/` 里 Skill / Agent / Meta / Hook 的数量或名称，须先更新单一清单 `tools/manifest.json`，再同步 README、docs/USAGE.md、`tests/run.ps1` 和 PPT 的数字。
- 新增第三方 Skill 前先确认许可证；仅 MIT 等允许再分发的可进 `payload/`，并附 LICENSE。
- 行尾：`*.sh`、`*.py` 用 LF；`.ps1` 保留 BOM。
- 不要提交 `_erc-backups/`、`tasks/`；push 前需经用户确认。

## 常用命令
- 安装到库（预演不写入）：`.\Install-EconomicsResearchCrew.ps1 -VaultPath <库> -WhatIf`；常用开关 `-ProjectName`（写入库 CLAUDE.md 标题，默认目录名；不带 `-VaultPath` 时交互询问）、`-Platform auto|claude|agy|codex|all`、`-WithHooks`、`-WithExtras`、`-Update`（差异写 `.new`，不覆盖）。
- 跨平台等价入口：`./install.sh --vault <库> ...` 或 `python tools/erc_cli.py install|test|sync|check-ars|check-upstreams`。
- 校验已安装的库：`.\Test-EconomicsResearchCrew.ps1 -VaultPath <库>`。
- 同步 AGENTS.md 的 ERC 区块：`.\Sync-AgentsMd.ps1 -VaultPath <库> [-Check]`。
- 上游更新检查（零 LLM 额度；无更新退出码 0，有更新 2，抓取失败 1）：`python tools/check_upstreams.py check [--repo ars|paper-orchestra|obsidian-second-brain|research-superpowers|aers]`；清单在 `payload/Meta/upstream-ars.json` 与 `tools/upstreams/*.json`；`.github/workflows/upstream-watch.yml` 每周一自动运行并开 issue。
- `tests/run.ps1` 支持按节号运行（`-Section 11,17,18`），自动拉起跨节前置依赖（如 `[14]` 自动带 `[10][12][13]`）；全量跑完 `[1]`…`[20]` 并打印每节耗时。
- `tests/evals/run_evals.py --chain --selftest`：S1–S12 网络连通性（清单、路由、关卡检查名、Skill 里引用的 CLI 子命令）与评分细则正反例；`--grade <目录>` 离线评已保存的回答，不调用模型。
- `tests/refmgr_selftest.py <库>/.claude/scripts/paper_tools.py <库>`：离线测 EndNote/Zotero 交换。
- `tests/routing_eval.py --vault <一次性库>`：**消耗 Claude Code 额度**，只在用户明确要求时运行；拒绝在已有 `settings.local.json` 的库上运行。

## 架构（需跨文件理解）
- **单一事实来源**：`payload/.claude/` 是内容正本，`tools/manifest.json` 是安装/校验清单正本（供 `Install-EconomicsResearchCrew.ps1`、`Test-EconomicsResearchCrew.ps1`、`tools/erc_cli.py` 共用）。`tools/build_platform.py` 从正本生成 agy / Codex 的 `.agents/`（脚本路径改写）与 `AGENTS.erc.md`，不要手改生成物。
- **三条安装路径**：`Install-EconomicsResearchCrew.ps1`（PS 5.1/7）与 `tools/erc_cli.py`（Python）实现同一套逻辑，行为必须一致；`install.sh` 只是 `erc_cli.py` 的封装。改安装行为须两处同改。
- **hooks 合并**：`payload/.claude/settings.hooks.json` 是片段，经 `tools/merge_hooks.py` 幂等并入用户 `settings.json`（按脚本文件名判重，从不重复，不动其他键）；hook 命令在 Windows 优先 `py -3`（无 py 启动器时回退 `python`；避开 Microsoft Store 的 `python` 占位程序，它在 PATH 靠前时会让 hook 静默失败），macOS/Linux 自适应 `python3`。
- **路由与流水线**：`payload/.claude/routing-triggers.json`（触发词→Skill/Agent）、`pipeline-stages.json`（阶段定义，供 `orchestrator.py` 使用）；改触发词后用 `tests/routing_cases.json` 对应的用例核对。
- **库的内容模型**：`Meta/` 为控制面（规范、日志、索引），四层知识流与只读层（Tier 0 由 hook 拦写）见 `README.md`「核心架构」；`payload/CLAUDE.template.md` 才是装进用户库的 CLAUDE.md。
- **许可边界**：`Imbad0202/academic-research-skills`（CC-BY-NC-4.0）只借设计模式、原生重写，禁止拷入其代码或提示词；映射见 `Meta/upstream-ars.json`。`paper-orchestra`（Apache-2.0）、`obsidian-second-brain`（MIT）、`research-superpowers`（MIT）与 `Auto-Empirical-Research-Skills`（CC-BY-SA-4.0，拷贝即须同许可发布，故严禁拷文字）同样只借设计模式，不拷代码，清单在 `tools/upstreams/`；上游自动更新只检测并出简报，采纳须经研究者审阅。
## 多代理分工
- 主会话（Opus 5.5，high）负责规划、决策、整合；子代理（Sonnet，medium）见 `.claude/agents/`：`code-analyst`（只读分析）、`code-implementer`（改代码并测试）、`docs-researcher`（查官方文档）。通用规则与顾问触发时机见用户级 `~/.claude/CLAUDE.md`。
- 改安装器、hooks 或 `payload/.claude/scripts/` 这类代码时，委派前先说明数量；`code-implementer` 完成后，主会话自己复核 `git diff` 并重跑上面两条测试，不直接采信报告。
