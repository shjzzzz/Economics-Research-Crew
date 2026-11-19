# erc-full-deck_20261118_20261118_173722

- Source: `erc-full-deck_20261118_20261118_173722.pptx`
- Total slides: 18

## Slide 1

本场分享双主线

CLAUDE-HOWTO × ECONOMICS RESEARCH CREW

从 Claude Code 核心概念

Part 1：Claude Code 8 大原语

- CLAUDE.md（7 层记忆） • Slash Commands

到经济学研究实战

- Skills（自动能力包） • Subagents（隔离）

- MCP（外部实时协议） • Hooks（事件拦截）

- Git Worktree（并行） • Plugins（打包）

先理解 CLAUDE.md / Skills / MCP / Hooks / Worktree 等底座原语，

再拆解它们如何组装成“可追溯、可审查、可积累”的科研护栏。

Part 2：科研工程护栏实战

- 科研 Rules（证据铁律与计量纪律）

PART 01 · 基础底座

PART 02 · 科研实战

- 14 Skills + 7 Subagents（含只读审稿）

8 大核心概念（claude-howto）

Economics Research Crew 架构

- S1–S12 状态机 + 6 个安全 Hooks

- 可积累 Wiki + 论文账本机械追溯

适用平台：Claude Code · Antigravity CLI (agy) · Codex CLI

### Speaker Notes

大家好！今天这次分享分为两部分：第一部分我们基于 claude-howto 教程仓库，把 Claude Code 最核心的 8 个基础概念一次讲透——包括 CLAUDE.md、Slash Commands、Skills、Subagents、MCP、Hooks、Git Worktree 和 Plugins；第二部分我们再来看 Economics Research Crew 这个项目，是如何把这些通用能力组装成一套严谨的经济学研究护栏的。

## Slide 2

[luongnv89/claude-howto: A visual, example-driven guide to Claude Code — from basic concepts to advanced agents, with copy-paste templates that bring immediate value.](https://github.com/luongnv89/claude-howto)

全场导览 · 双部映射关系

为什么先讲基础概念？从“原语”到“科研系统”

Part 1：Claude Code 基础原语（claude-howto）

Part 2：Economics Research Crew 落地

CLAUDE.md (Memory)

科研 Rules (CLAUDE.md / AGENTS.md)

7 层拼接记忆，跨会话自动加载项目规范

固化证据铁律、因果识别纪律与数据只读底线

Slash Commands & Skills

14 个标准化科研 / Wiki / 写作 Skills

手动 /命令 快捷方式 + 模型自匹配能力文件夹

把选题、文献、识别审计、成稿封装成防跳步 SOP

Subagents

7 个专业代理 + 独立对抗审稿

独立上下文窗口 + 定制提示词 + 工具权限隔离

仅 econometrics-agent 有 Bash；reviewer 只读不改

Hooks

6 个安全与编排 Hooks (-WithHooks)

33 种生命周期事件驱动的确定性脚本拦截

保护 raw/\_sources 只读、拦越级派出、校验草稿

MCP · Git Worktree · Plugins

克制外部依赖 + 多平台安装器

实时外部工具连接 · 并行分支隔离 · 扩展包分发

默认不装 MCP 防数据外泄；单一源分发三平台

看懂 Part 1 的 8 个底座能力，就能看透 Part 2 科研体系的每一处工程取舍。

Claude Code 基础概念 × Economics Research Crew

02 / 18

### Speaker Notes

为什么讲科研项目前要先花时间讲 Claude Code 的基础概念？因为 Economics Research Crew 并不是凭空造轮子，而是把 Claude Code 的原生原语进行了精准组合与取舍：用 CLAUDE.md 定科研底线，用 Skills 固化研究 SOP，用 Subagents 做权限隔离与独立审稿，用 Hooks 保护原始数据，同时克制地选择不默认安装 MCP 以防受限数据外泄。看懂左边的底座，右边的设计意图就一目了然。

## Slide 3

PART 01 · CLAUDE CODE 基础概念总览

一张图分清：会话加载顺序与 8 大核心能力

会话启动加载顺序（Interaction Timeline）

1. Session Start

2. 发现 Skills

3. 注册 Commands

4. 连接 MCP

5. 交互与 Hooks 护航

加载 Memory (CLAUDE.md)

扫描 SKILL.md 元数据

注册 .claude/commands/

挂载外部工具与数据源

工具前后自动触发校验

核心概念定位对比矩阵（claude-howto）

概念

触发方式

持久性 / 状态

作用域

典型用途

CLAUDE.md (Memory)

启动自动加载

跨会话持久化

组织 / 项目 / 个人

规范、架构与长期偏好

Slash Commands

用户手动 (/cmd)

仅当前会话

单个快捷指令

高频重复 Prompt 模板

Skills

模型自动匹配调用

文件系统能力包

可复用专业工作流

带脚本与模板的复杂 SOP

Subagents

自动/显式委派

独立上下文窗口

专项子任务

并行分析、审查与隔离执行

MCP Protocol

工具调用时查询

实时外部连接

外部 API / 数据库

GitHub、SQL、Slack 等实时读写

Hooks

33 种事件自动触发

确定性脚本执行

工具 / 会话生命周期

安全拦截、格式校验、日志

Git Worktree

-w 启动 / 后台会话

独立分支工作目录

单仓库多分支并行

多任务并行开发互不冲突

Plugins

单命令安装/加载

可分发扩展包

官方 / 社区 / 团队

打包分发 Cmd+Agent+MCP+Hook

Part 1 · Claude Code 基础概念（claude-howto）

03 / 18

### Speaker Notes

在进入具体概念前，先看一张全局图。启动一次 Claude Code 会话时，系统按固定顺序加载能力：先读入 CLAUDE.md 记忆，再扫描可用的 Skills，注册 Slash Commands，连接 MCP 外部服务器，最后在交互过程中由 Hooks 在工具调用前后保驾护航。下面这张矩阵帮大家先对 8 个概念的触发方式、持久性和典型用途建立直觉。

## Slide 4

PART 01 · 基础概念 (01 / 08)

基础 ① | CLAUDE.md：跨会话的 7 层记忆体系

Claude Code 7 层记忆加载顺序（拼接而非覆盖）

Tier 1 · Managed Policy（最高优先级）

核心加载机制

企业管理员下发 | 全组织共享 | 合规与安全策略

- 拼接而非覆盖 (Concatenated)：

Tier 2 · Project Memory (./CLAUDE.md)

所有命中的 CLAUDE.md 按顺序拼接进上下文，

项目根目录 | Git 团队共享 | 团队规范、架构与构建命令

越具体/本地的文件越晚读入。

- Auto Memory 自动学习：

Tier 3 · Project Rules (.claude/rules/\*.md)

项目内模块化规则 | Git 团队共享 | 按主题拆分的项目约定

后台自动沉淀编码风格、纠偏规则与沟通偏好。

Tier 4 · User Memory (\~/.claude/CLAUDE.md)

用户主目录 | 个人跨项目生效 | 个人编码习惯与语言偏好

它解决了什么问题？

Tier 5 · User Rules (\~/.claude/rules/\*.md)

1. 告别每次开新会话重复粘贴背景

用户级模块化规则 | 个人私有 | 可复用的个人规则切片

2. 团队通过 Git 共享统一规范

Tier 6 · Local Memory (./CLAUDE.local.md)

3. 个人偏好与团队规范分层解耦

本地机器私有（不入 Git） | 本机路径、端口或临时覆盖配置

→ 对应 Part 2：科研 Rules 的核心载体

Tier 7 · Auto Memory（自动记忆）

按仓库自动捕获 | 无需手写 | 记录用户纠正与常用工具偏好

Part 1 · Claude Code 基础概念（claude-howto）

04 / 18

### Speaker Notes

第一个基础概念是 CLAUDE.md，也就是 Claude Code 的记忆体系。claude-howto 把它拆解为 7 个层级：从企业管理员的 Managed Policy，到项目根目录的 CLAUDE.md 和模块化 rules，再到用户主目录的个人记忆、本地私有的 CLAUDE.local.md，以及自动学习的 Auto Memory。要注意的是，这 7 层是“拼接”而不是“覆盖”进上下文的，越靠近当前项目和本机的文件越晚读入。

## Slide 5

PART 01 · 基础概念 (02 / 08)

基础 ② | Slash Commands：手动触发的 Prompt 快捷方式

执行流程：把常用工作流存成 Markdown，用 /命令 一键调用

用户输入 /optimize

检索 .claude/commands/

展开 Prompt + 注入上下文

Claude 执行并输出

匹配 optimize.md 文件

展开 @文件 与 \$(git ...) 输出

仅在当前会话上下文生效

可附带参数，如 --verbose

组织方式与两类命令

Markdown 命令文件支持的 5 项能力

- 项目级命令：.claude/commands/

1. 文件引用

@path/to/file.js

随 Git 仓库提交，团队共享标准工作流（如 /pr、/commit）

- 个人级命令：\~/.claude/commands/

2. Bash 动态注入

\$(git log --oneline -5)

个人跨项目私有快捷方式，不进入团队仓库

3. 脚本执行

bash scripts/deploy.sh

- 子目录命名空间与内置命令

支持子目录分类（如 docs/）；Claude Code 另内置 60+ 命令

4. 命令行参数

/pr --verbose

如 /help · /clear · /compact · /mcp · /agents · /skills

要点：Slash Command 必须由人显式输入 /名称 才会触发

5. 调用 MCP Prompt

/mcp__github__list_prs

Part 1 · Claude Code 基础概念（claude-howto）

05 / 18

### Speaker Notes

第二个基础概念是 Slash Commands，也就是斜杠命令。它本质上是存放在 \`.claude/commands/\` 目录下的 Markdown 文件。当你输入 \`/optimize\` 时，Claude Code 会找到对应的 \`optimize.md\`，把里面的 Prompt 展开到当前会话。它非常强大，支持 \`@文件路径\` 引用、Bash 命令动态注入 \`\$(git ...)\` 和传参。记住一个核心特点：Slash Command 是由人手动输入 \`/名称\` 来触发的。

## Slide 6

PART 01 · 基础概念 (03 / 08)

基础 ③ | Skills：模型按需自动调用的能力包

Skill 的本质：能力文件夹 (Folder Package)

高频混淆点：Skills vs. Slash Commands

1. 触发机制不同（最核心差异）

.claude/skills/\<skill-name>/

- Slash Command：用户显式输入 /cmd 才执行。

├── SKILL.md

YAML 元数据 (name/description) + 指令

- Skill：启动时只加载 YAML 摘要，模型根据用户

├── scripts/

可执行的 Python / Shell 辅助脚本

需求语义自动匹配并按需读入完整 SKILL.md。

├── templates/

标准输出模板与参考样例

└── references/

按需读取的补充文档（省上下文）

2. 载体复杂度不同

- Slash Command：单个 Markdown 提示词文件。

- Skill：完整目录，可打包脚本、模板与参考手册，

4 种来源与作用域：

实现“渐进式披露 (Progressive Disclosure)”。

- Pre-built 内置：全局可用（如 pptx / xlsx / docx / pdf）

- Personal 个人：\~/.claude/skills/（个人自动化）

3. 何时用哪个？

- Project 项目：.claude/skills/（Git 共享团队标准）

- 简单单步快捷操作 → Slash Command

- Plugin 插件：随插件安装自动注册

- 带多步检查点、脚本和模板的专业工作流 → Skill

注：也支持用户直接输入 /skill-name 显式触发

（Part 2 的 14 个科研流程全部采用 Skill 封装）

Part 1 · Claude Code 基础概念（claude-howto）

06 / 18

### Speaker Notes

第三个基础概念是 Skills。很多同学分不清 Skill 和 Slash Command。其实核心差异有两点：第一，触发方式不同，Skill 启动时只加载 YAML 元数据摘要，模型会根据你的意图“自动匹配并按需加载”；第二，载体不同，Slash Command 只是一个 Markdown 文件，而 Skill 是一个完整的文件夹，里面可以打包 SKILL.md、辅助脚本、模板和参考手册。所以复杂的多步骤科研 SOP，在 Part 2 里全都是用 Skill 封装的。

## Slide 7

PART 01 · 基础概念 (04 / 08)

基础 ④ | Subagents：上下文隔离与专才分工

主从委派架构（Main Agent → Subagents）

Subagents 的 4 个核心工程价值

1. 上下文窗口隔离（最重要）

User（提出复杂任务）

读几十篇文献或大量代码的过程留在子代理内部，

只把精炼结论返还主代理，防止主会话上下文爆炸。

Main Agent（协调者）

2. 工具权限最小化裁剪

拆解任务 · 委派子代理 · 汇总最终结果

可在 .claude/agents/\*.md 中指定 tools 列表，

例如让审稿人只有 Read/Grep 权限，无法改文件。

3. 独立视角的客观性

Code Reviewer

Test Engineer

Docs Writer

不继承主会话的历史推理偏见，适合做对抗式

独立上下文窗口

独立上下文窗口

独立上下文窗口

代码审查或学术论文审稿。

只读权限 + 审查

写测试 + 跑命令

定制文档提示词

仅返回结论摘要

不污染主会话

支持并行执行

4. 生命周期可被 Hook 观测

配合 SubagentStart / SubagentStop 事件记录账本

支持嵌套委派（v2.1.219 默认深度 3 层）：

→ 对应 Part 2：7 个科研 Subagent 与质量闭环

Subagent 还可派生下级 Subagent；可通过 CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH 调节。

Part 1 · Claude Code 基础概念（claude-howto）

07 / 18

### Speaker Notes

第四个基础概念是 Subagents，也就是专业子代理。在 claude-howto 里，主代理负责拆解任务，再把专项子任务委派给带有独立上下文窗口和定制提示词的子代理，比如代码审查员或测试工程师。子代理最大的工程价值在于“上下文隔离”和“工具权限裁剪”：长篇阅读留在子代理里，不污染主对话；而且从 v2.1.219 开始，子代理默认支持最多 3 层嵌套调用。

## Slide 8

PART 01 · 基础概念 (05 / 08)

基础 ⑤ | MCP：连接外部工具与实时数据的协议

MCP (Model Context Protocol) 标准化连接架构

常见外部服务生态（claude-howto）

Claude Code

MCP Server（适配层）

JSON-RPC

- Filesystem：本地文件读写（OS 权限）

MCP Client（发起工具调用）

将外部 API / DB 暴露为标准工具

- GitHub：查 PR / Issue / 推送代码（OAuth）

- 统一认证（OAuth / Token / 密钥）

- /mcp 管理连接状态

- Database：PostgreSQL / MySQL 实时查询

- 支持按需延迟加载工具

- 配置在 .mcp.json（可共享）

实时返回结果

- Slack / Google Docs：团队消息与云端文档

Memory (CLAUDE.md) vs. MCP

工程启示：为什么 Part 2 默认不装 MCP？

- Memory：静态、跨会话的“背景知识与规则”

Economics Research Crew 在 README 中明确声明：

如代码规范、目录约定、研究伦理要求。

“不覆盖已有 .mcp.json，也不默认安装任何 MCP”

- MCP：动态、实时的“外部动作与最新状态”

原因：经济学研究常涉及受限微观数据或未公开手稿，

如查询线上数据库最新记录、创建 GitHub Issue、读取实时文档。

减少默认外部连接面可以降低敏感数据外发风险，

仅在 paper_tools 核验文献时只发送标题/DOI（且可离线）。

两者互补：用 Memory 约束行为，用 MCP 获取实时信息。

Part 1 · Claude Code 基础概念（claude-howto）

08 / 18

### Speaker Notes

第五个基础概念是 MCP（Model Context Protocol）。它相当于 AI 连接外部世界的 USB-C 标准接口，让 Claude Code 可以通过 MCP Server 实时读写本地文件系统、GitHub、数据库或 Slack。这里要和 CLAUDE.md 区分开：Memory 存的是静态规则，MCP 连的是实时数据。也正因为 MCP 会连外部服务，Part 2 的科研项目出于数据保密考虑，默认不自动安装任何 MCP。

## Slide 9

PART 01 · 基础概念 (06 / 08)

基础 ⑥ | Hooks：事件驱动的确定性自动化与拦截

核心定位（claude-howto）：配置在 \~/.claude/settings.json 或 .claude/settings.json，无需 AI “自觉遵守”

支持 33 种生命周期事件 · 5 种实现载体：command（本地脚本） · http · mcp_tool · prompt · agent

1. 会话与输入阶段

2. 工具调用前后（最常用）

3. 子代理、分支与响应结束

SessionStart / SessionEnd

PreToolUse

SubagentStart / SubagentStop

环境初始化、会话结束清理与日志

工具执行前拦截（如 Edit/Write/Bash），

子代理派生时注入上下文，结束时验产物

用于安全检查、路径保护与审批门控

InstructionsLoaded

WorktreeCreate / Remove

PermissionRequest / Denied

CLAUDE.md 或规则加载时校验增强

自定义 Git Worktree 创建与资源清理

自动审批流或策略拒绝日志

UserPromptSubmit

Stop / TaskCompleted

PostToolUse / Failure

用户提交提问时做输入校验或注入提示

回答完成或任务完结时触发收尾检查

工具成功后自动格式化（如 prettier）、

PreCompact / PostCompact

PreModelSwitch / ConfigChange

检查 YAML frontmatter 或发送告警

上下文压缩前后保存关键状态

模型切换门控与配置变更传播

settings.json 典型用法（matcher 精确匹配工具名）：

"PreToolUse": \[{"matcher": "Edit|Write", "hooks": \[{"type": "command", "command": "python protect_raw.py"}\]}\]

Part 1 · Claude Code 基础概念（claude-howto）

09 / 18

### Speaker Notes

第六个基础概念是 Hooks。前面讲的 CLAUDE.md 是“写给 AI 看的软约束”，而 Hooks 则是“由程序强制执行的硬拦截”。Claude Code 支持 33 种生命周期事件，配置在 settings.json 里，支持本地脚本等 5 种载体。最常用的是工具执行前的 PreToolUse 和执行后的 PostToolUse——比如在修改文件前拦住受保护路径，或在写入后自动格式化。

## Slide 10

PART 01 · 基础概念 (07 & 08 / 08)

基础 ⑦⑧ | Git Worktree（并行隔离）与 Plugins

⑦ Git Worktree：多分支并行隔离

⑧ Plugins：最高层级的生态打包机制

解决什么痛点？

什么是 Plugin？

多个 AI 会话同时改同一个仓库目录会互相覆盖；

把前面学过的所有扩展能力打包成一个可共享的安装包，

Worktree 让每个会话拥有独立分支工作区，无需 stash。

一条命令即可在任意项目加载完整工作流。

claude --worktree \<name> (或 claude -w)

清单文件：.claude-plugin/plugin.json

创建路径：\<repo>/.claude/worktrees/\<name>

一次打包：Slash Commands + Skills + Subagents +

若会话结束无改动，worktree 会自动清理

MCP Servers + Hooks（本地测试：claude --plugin-dir）

关键机制（claude-howto 09-advanced-features）：

4 类分发范围（claude-howto 07-plugins）：

- 后台隔离 worktree.bgIsolation：默认给后台任务

- Official（官方）：Anthropic 提供，如 PR Review

分配独立 worktree（设 "none" 则直接改当前目录）

- Community（社区）：开源 DevOps / Data Science

- 稀疏检出 worktree.sparsePaths：加速大仓库克隆

- Organization（组织）：公司内部规范与工具包

- 会话内工具：EnterWorktree / ExitWorktree

- Personal（个人）：开发者自用工作流合集

- 生命周期 Hook：WorktreeCreate / WorktreeRemove

→ 适用于：同时跑多组稳健性检验或并行代码分支

Part 1 小结：8 个原语齐备 → 下面进入 Part 2 科研实战！

Part 1 · Claude Code 基础概念（claude-howto）

10 / 18

### Speaker Notes

最后两个基础概念是 Git Worktree 和 Plugins。当你希望多个后台任务或 AI 会话同时改代码而不互相冲突时，用 \`claude --worktree\` 就能在 \`.claude/worktrees/\` 下开辟隔离分支目录，结束后没改动还会自动清理。而 Plugins 则是最高层级的打包机制，通过 \`.claude-plugin/plugin.json\` 把 Commands、Skills、Subagents、MCP 和 Hooks 一键打包分发。至此，Part 1 的 8 个基础原语就全部讲完了，接下来我们进入 Part 2，看 Economics Research Crew 如何把它们组装成科研护栏。

## Slide 11

PART 02 · ECONOMICS RESEARCH CREW 科研实战

Part 2 | 不是计量软件，而是 AI 科研的“工程护栏”

通用 AI 直接做科研的 4 大失控风险

Economics Research Crew 的工程对策

1. 幻觉与编造证据

证据铁律 + 账本机械绑定

凭空捏造论文 DOI、税法条文号、回归系数或样本量

查不到一律标“待核实”；引文 \[@key\] 与数字 {{res:id}} 锁死账本

2. 跳过识别直接跑回归

强制阶段门控 (S1–S7) + 独立审稿

把相关当因果，未定义 Estimand 与假设就输出回归脚本

先过识别审计 (/causal-inference-audit)，再执行与对抗审查

3. 误改原始数据与笔记

Hook 技术拦截 + 安装不覆盖

在清洗或整理时覆盖 raw 数据、删除或批量改写原有笔记

protect_raw.py 锁死 raw 与 \_sources；工具权限按代理最小化

4. 会话结束知识清零

可积累 Wiki + STATE.json 断点续跑

每次新开对话都要重喂文献与研究进度，难以长期积累

三层知识库持续沉淀，研究状态与交接产物落盘可续接

重要边界：

本项目不含 Stata/R/Python 计量引擎，不自动跑回归；脚本、数据、环境与研究判断权永远由研究者确认。

Part 2 · Economics Research Crew 科研实战

11 / 18

### Speaker Notes

现在进入 Part 2：Economics Research Crew 科研实战。先明确项目定位：它不是计量软件，也不自动跑回归，而是针对通用 AI 做科研的四大失控风险——编造文献、跳过识别直接跑回归、误改原始数据、会话结束知识清零——构建的一套工程护栏。接下来我们看它是如何把 Part 1 学过的原语落到每一层里的。

## Slide 12

PART 02 · 总体架构

四层协同：Part 1 基础原语如何组装成科研系统

核心职责：定义路由优先级、证据铁律、计量纪律与数据只读底线

L1 规则层 (Rules)

核心文件：CLAUDE.md + .claude/ECONOMICS-RESEARCH.md（Claude Code） | AGENTS.md（agy / Codex）

基于 Part 1 的 Memory 机制

解决：不用每次对话重复叮嘱“别编文献、先定 estimand”

核心职责：14 个 Skill 固化研究/写作/Wiki SOP；7 个 Subagent 分工执行与独立审稿

L2 能力层 (Skills/Agents)

核心目录：.claude/skills/\*/SKILL.md · .claude/agents/\*.md（含只读 academic-reviewer）

基于 Part 1 的 Skills + Subagents

解决：防跳步、防长上下文污染、杜绝“自己写自己审”

核心职责：orchestrator.py 管进度与人工关卡；6 个 Python Hook 拦越权与护数据

L3 控制层 (Director/Hooks)

核心文件：scripts/orchestrator.py · pipeline-stages.json · hooks/\*.py

基于 Part 1 的 Hooks 生命周期拦截

解决：研究中断可续跑、AI 无法越级推进或私自放行关卡

核心职责：Wiki 两步摄入与体检；paper_tools.py 锁死引文表与实证数字账本

L4 沉淀层 (Wiki & Paper)

核心目录：Meta/（index、log、citation-map、results-ledger） · 03-Literature/ · 06-Data/

可积累的知识库与可追溯论文产出

解决：知识跨项目复利积累，成稿每个数字与引文都可机械溯源

Part 2 · Economics Research Crew 科研实战

12 / 18

### Speaker Notes

从架构上看，Economics Research Crew 正好把 Part 1 的概念组装成四层：第一层 Rules 依托 CLAUDE.md 和 AGENTS.md 记忆机制；第二层把 14 个科研流程和 7 个专业角色落到 Skills 和 Subagents；第三层用 Research Director 和 6 个 Hooks 管住状态流转与技术拦截；第四层用三层 Wiki 和 paper_tools 实现知识复利与论文机械溯源。

## Slide 13

PART 02 · 科研落地 ①

科研落地 ① | Rules（铁律）与 14 个 Skills（SOP）

Rules：CLAUDE.md / AGENTS.md 科研宪法

14 个 Skills：在本库内优先于全局技能

研究推进（7 个）

1. 证据铁律

/research-question

苏格拉底防越位 + Estimand 收敛

- 严禁编造论文、DOI、法条、数据或结果；查不到标“待核实”

/literature-review

带来源文献矩阵与研究缺口

- 中国税法须写明发文机关、文号、生效日期与废止状态

/theory-modeling

探索态护栏与均衡推演

- 严格区分：来源事实 vs. 模型解释 vs. 研究者假说

/tax-policy-analysis

税制法源、征管遵从与归宿

/causal-inference-audit

DID/IV/RDD 识别审计与措辞边界

2. 计量纪律

/econometric-analysis

数据审计、回归与论文复现

/academic-review

Fatal / Major / Minor 分级挑刺

- 区分相关、预测与因果；先定 Estimand 再跑回归

- DID/IV/RDD 各自核查假设与安慰剂检验

Wiki 维护（3 个） & 论文写作（3 个）

- 明确聚类层级与样本处理；禁止静默删样本或改设定

/ingest-source · /query-wiki · /wiki-lint

两步摄入 / 溯源问答 / 体检

/paper-outline · /paper-draft · /paper-refine

大纲 / 文风成稿 / 3轮+R&R

3. 数据与笔记安全

- 06-Data/raw 与 03-Literature/\_sources 绝对只读

/research-pipeline

总控编排 Skill（1 个）

- 衍生数据仅写 processed；不删除或批量改写既有笔记

串联 S1–S12 全流程，每阶段停在研究者关卡，含独立审稿闭环。

- data_access_level 分级数据隔离

Part 2 · Economics Research Crew 科研实战

13 / 18

### Speaker Notes

具体来看 Part 1 的 Memory 和 Skills 在科研里是怎么落地的：左侧是写进 CLAUDE.md 和 AGENTS.md 的三条科研铁律——不编造文献和税法文号、先定 Estimand 再跑回归、原始数据目录绝对只读；右侧则是 14 个标准化的科研 Skills，覆盖从选题到审稿、Wiki 维护以及论文写作全流程，而且在本库内优先级高于全局插件技能。

## Slide 14

PART 02 · 科研落地 ②

科研落地 ② | 7 个 Subagents：权限最小化与审稿

研究与写作代理（5 个 · 上下文隔离）

唯一可执行代理（1 个）

对抗式独立审稿（1 个）

econometrics-agent

academic-reviewer

literature-agent

文献检索、抽取与比较 | 权限：读 / 搜 / 联网

唯一拥有 Bash 权限

只读 + 联网 · 严禁写文件

theory-agent

核心职责：

为什么这样设计？

理论模型推导与机制 | 权限：读 / 写 / 编辑

- 独立上下文 + 框架锁定检测

- 数据审计与样本核算

- 计量回归代码实现与日志

- 交接只给产物路径 (handoff.md)

tax-policy-agent

- 让步门槛 ≥4/5，禁连续让步

- 已有论文复现与代码审计

税法、征管与归宿分析 | 权限：读 / 搜 / 联网

causal-inference-agent

权限最小化设计：

分级输出标准：

识别策略与稳健性设计 | 权限：读 / 搜 / 网 / 写

其他 6 个 Agent 均无 Shell

- Fatal：致命漏洞（一票否决）

执行权，降低误操作风险。

- Major：重要缺陷（必须回应）

paper-writer-agent

- Minor：次要建议

论文成稿与精修（S10–S11） | verified_only

质量闭环：

研究代理提方案 → econometrics-agent 执行 → academic-reviewer 质疑 → Director 与研究者决策（Fatal 阻断通过）

Part 2 · Economics Research Crew 科研实战

14 / 18

### Speaker Notes

结合 Part 1 讲过的 Subagents 上下文隔离和工具裁剪原理，Economics Research Crew 配置了 7 个分工明确的子代理：5 个研究与写作代理各自深耕，只有 econometrics-agent 拥有 Bash 执行权限，而 academic-reviewer 则是只读加联网、严禁写文件，并且只看交接单里的产物路径，真正实现“审写分离”和对抗式挑刺。

## Slide 15

PART 02 · 科研落地 ③

科研落地 ③ | Research Director：S1–S12 状态机

第一段：研究与实证闭环（S1–S7）

每阶段结束均需通过研究者关卡 (Gate) 方可推进

S1 问题

S2 文献

S3 机制 (并行≤2)

S4 设计

S5 执行

S6 独立审查

S7 决定

定题与 Estimand

缺口与矩阵

理论与税法法源

识别与计划冻结

代码与分析日志

Fatal + 7类失效闸门

接受 / 退回 / 停止

/research-question

literature-agent

theory / tax-policy

causal-inference

econometrics-agent

academic-reviewer

Director + 研究者

第二段：论文写作与人机协作闭环（S8–S12）

对应研究者检查点 C1–C5，机械校验引文与数字

S8 论文大纲 (C1)

S9 引文 (C2)

S10 成稿 (C3)

S11 精修 (C4)

S12 终检 (C5)

Crossref + 锚点核验

\[@key\]+{{res:id}}+claim check

3轮精修 / R&R 矩阵

主张清单与证据强度

引文/锚点/7类闸门

/paper-outline

paper_tools cite

/paper-draft

/paper-refine

paper_tools report

1. 持久化状态与断点续跑

2. 重试熔断与并发上限

3. 关卡只由研究者决定

状态存放在 STATE.json，派出历史记入

每个 Agent 在单阶段最多重试 2 次，

AI 严禁自行运行 gate --decision pass。

Meta/run-ledger.jsonl。中断后只需运行

耗尽即停下向研究者汇报（防止死循环）。

脚本强制要求 --note，并在 Claude Code

并发默认 1（S3 最多 2，硬上限 3）。

下通过 Hook 弹出权限确认提示，

orchestrator.py next

即可接续当前阶段，不重做已过关卡。

产物与日志校验通过后才允许过关。

确保每个关键节点由人拍板。

Part 2 · Economics Research Crew 科研实战

15 / 18

### Speaker Notes

为了让长周期研究不断档、不越权，Research Director 编排器通过 \`orchestrator.py\` 维护 \`STATE.json\` 和 \`run-ledger.jsonl\`。整个流程分成 S1–S7 研究闭环和 S8–S12 写作闭环。它不仅支持断点续跑和单阶段最多 2 次的重试熔断，还规定 AI 严禁自己过关，必须由研究者确认关卡。

## Slide 16

PART 02 · 科研落地 ④

科研落地 ④ | 6 个 Hooks：原始数据保护与守卫

1. 提示与事前拦截 (Pre)

2. 编排守卫 (Claude Code)

3. 事后校验 (PostToolUse)

routing_hint.py

orchestrator_guard.py

validate_frontmatter.py

每轮首次调用前注入路由提示，提醒

- 阻止派出后续阶段的 Agent（防跳步）

写入 .md 笔记后自动检查 YAML

优先匹配项目 Skill（Claude / agy）。

frontmatter 是否闭合、有无非法 Tab，

- 阻止单阶段重试耗尽（>2 次）后继续派出

发现问题即时反馈给 AI 修复。

- 阻止超出阶段并发上限

- 阻止直接编辑 STATE.json / run-ledger

protect_raw.py (PreToolUse)

- 精确拦截 Write / Edit 修改

注：agy / Codex 无此拦截层，靠规则遵守

validate_paper.py

06-Data/raw 与 03-Literature/\_sources

中已存在的文件（允许新建导入）。

针对论文草稿写入的自动校验，

orchestrator_record.py

- 启发式拦截危险 Bash 命令

检查 \[@key\]、{{res:id}} 与未答

自动记录 Subagent 派出与完成事件，

（rm / mv / 重定向等涉及受保护路径）。

问题标记，防止手写未登记引用。

写入 Meta/run-ledger.jsonl 账本。

agy 下放行时返回 ask，沿用审批流程

坦诚的工程边界（Limitation）：

安装时加 -WithHooks 才启用；Bash 拦截仅为关键字启发式检查，输入异常时 fail-open。

Hooks 是在规则文本之外增加的技术护栏，而非操作系统级沙箱——Git 版本控制与定期备份依然不可或缺。

Part 2 · Economics Research Crew 科研实战

16 / 18

### Speaker Notes

再看 Part 1 讲过的 Hooks 在科研里的实战用法：安装时加上 \`-WithHooks\` 后，6 个 Python 脚本会在事前、编排和事后三个环节介入——比如 \`protect_raw.py\` 锁死原始数据和文献目录，\`orchestrator_guard.py\` 拦住越级派出，\`validate_frontmatter.py\` 和 \`validate_paper.py\` 事后自动查格式与标记。当然，Hook 只是护栏不是沙箱，Git 备份依然必须配合使用。

## Slide 17

PART 02 · 科研落地 ⑤

科研落地 ⑤ | 可积累 Wiki 与论文机械可追溯

可积累 Wiki（借鉴 llm_wiki）

人机协作写稿（S8–S12 · paper_tools.py）

三层沉淀架构

\[@key\] 引文机械绑定

1. 原始来源 (03-Literature/\_sources/)：不可变 + SHA256 去重

仅限 Meta/citation-map.json 已登记文献；Crossref 核验仅发

2. Wiki 页面 (03-Literature / 04-Theories / 08-Notes)：页码溯源

标题/DOI；--locator 三层锚点 + claim check 防 L3 错配

3. 方向与规则 (Meta/purpose.md + CLAUDE.md)

{{res:id}} 实证数字机械绑定

两步摄入 (/ingest-source)

正文回归系数、样本量等数字一律写成占位符，

先只读分析（抽取要点 + 发现矛盾 + 拟改清单），

从 Meta/results-ledger.json 映射，杜绝 AI 篡改或幻觉

等研究者确认后才写入页面、更新 index 与 research-log

⟦问：…⟧ / ⟦答：…⟧ 显式提问替代脑补

冲突入队 (Meta/review-queue.md)

遇到证据缺口时在稿内显式发问；终检前未答问题数必须清零

来源结论冲突时不静默覆盖，并列记录并排队等待研究者裁决

文风校准/去AI味 + 3轮精修 + R&R 返修追溯矩阵

确定性体检 (wiki_lint.py / /wiki-lint)

人机分工底线 (collaboration-protocol.md)：

查断链、孤立页与溯源；自动跳过原有税法笔记

AI 永不决定识别策略、不拔高因果措辞强度、不决定投稿期刊。

Part 2 · Economics Research Crew 科研实战

17 / 18

### Speaker Notes

最后看知识沉淀与论文写作。左侧是三层 Wiki 知识库：原始来源不可变、Wiki 页面人机共建、方向与规则在最顶层；通过 \`/ingest-source\` 两步摄入、冲突进 \`review-queue.md\`、\`wiki_lint.py\` 体检，让知识越用越厚。右侧是 S8–S12 写稿防幻觉机制：所有引用写 \`\[@key\]\`，所有数字写 \`{{res:id}}\`，缺证据必须用 \`⟦问：…⟧\` 发问，绝不脑补。

## Slide 18

PART 02 · 多平台适配与快速上手

总结与上手 | 单一源多平台分发 & 3 步无损接入

平台（唯一维护源：payload/.claude/）

规则 / Skills / Agents

Hooks (-WithHooks)

验证状态

Claude Code（完整版）

CLAUDE.md + .claude/{skills,agents}

全量 Hook（含编排强拦截）

已完整测试

Antigravity CLI (agy)

AGENTS.md(≤24KB) + .agents/

raw 保护(ask) + 路由；无编排拦截

agy 1.5.9 冒烟

Codex CLI

AGENTS.md + .agents/

无 Hook，靠规则文本约束

仅生成·未实测

STEP 01 · 预演与安装

STEP 02 · 结构与回归校验

STEP 03 · 首次只读体检

.\\Install-EconomicsResearchCrew.ps1

.\\Test-EconomicsResearchCrew.ps1

进入研究库启动 claude 或 agy，先执行：

-VaultPath "D:\\YourVault"

-VaultPath "D:\\YourVault"

“读取规则与 Meta/vault-map.md，只检查

-WithHooks -WhatIf

pwsh -NoProfile -File tests\\run.ps1

配置与目录，报告 Agent 与 Skills。”

不覆盖已有配置，改前备份至 \_erc-backups/

校验 frontmatter、脚本与 hooks.json

填好 Meta/purpose.md 后即可用

-Platform auto|claude|agy|codex|all

回归测试全在临时目录执行，不碰真实库

/causal-inference-audit 做首次冒烟

用 Claude Code 原语筑起工程护栏，把学术判断权稳稳留给研究者

Claude Code 基础概念 × Economics Research Crew

18 / 18

### Speaker Notes

最后一页讲多平台适配与上手路径。整个项目以 \`payload/.claude/\` 作为唯一维护源，通过安装器自动适配 Claude Code、agy 和 Codex CLI，同时清晰标明各平台的 Hook 能力边界。大家如果想接入自己的研究库，只需要三步：用 \`-WhatIf\` 预演安装、运行 \`Test-EconomicsResearchCrew.ps1\` 校验、启动 CLI 做一次只读体检。谢谢大家！
