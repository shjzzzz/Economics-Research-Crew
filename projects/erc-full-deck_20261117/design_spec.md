<!-- ppt-master-schema: design-spec/v1 -->
# Claude Code 基础概念与 Economics Research Crew 实战 - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | Claude Code 基础概念与 Economics Research Crew 实战 |
| Canvas Format | PPT 16:9 (1280×720) |
| Page Count | 18 |
| Primary Language | zh-CN |
| Target Audience | 对 AI 辅助科研与 Claude Code 工程实践感兴趣的学者、研究生、研究团队与技术同行 |
| Communication Intent | 先基于 claude-howto 系统讲清 Claude Code 的 8 大基础概念（CLAUDE.md、Slash Commands、Skills、Subagents、MCP、Hooks、Git Worktree、Plugins），再展示 Economics Research Crew 如何将它们组装成严谨的经济学研究护栏 |
| Desired Audience Outcome | 听众能先建立完整的 Claude Code 概念底座，再看懂 Economics Research Crew 每一层设计的来龙去脉与落地方法 |
| Core Message / Ask / Action | 理解底层原语（Memory/Skills/MCP/Hooks/Subagents/Worktree/Plugins），才能真正用好面向经济学研究的工程化协作体系 |
| Delivery Context | 20–25 分钟现场分享与会后导览材料 |
| Artifact Afterlife | 团队培训与新成员入门参考 |
| Reading Mode | balanced |
| Content Strategy | 平衡重组：Part 1 严格依据 claude-howto 仓库，Part 2 严格依据 Economics Research Crew 仓库 |
| Design Style | 学术极简（Swiss Minimal + Editorial） |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — user-facing live presentation |
| Custom Animations | disabled |
| Narration Audio | disabled |
| Created Date | 2026-11-17 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 64 px left/right, 56 px top, 48 px bottom |
| Content Area | 1152 × 616 (x: 64..1216, y: 56..672) |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Mode References**: instructional, pyramid
- **Mode Behavior**: 双部结构：Part 1 以 instructional 逐一讲透 8 个 Claude Code 基础概念；Part 2 以 pyramid + instructional 展示这些概念如何在 Economics Research Crew 中落地为科研护栏。
- **Visual style**: custom
- **Visual Style References**: swiss-minimal, editorial
- **Visual Style Behavior**: 以 swiss-minimal 精确栅格、大留白与直角几何区块为主骨架，辅以 editorial 的细规则分隔线、序号徽标与对比层级；严格扁平无阴影。
- **Theme**: 冷静、严谨、结构化的学术工程美学
- **Tone**: 清晰、克制、重证据与可追溯性

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #FFFFFF | 内容页主画布底色 |
| Secondary background | #F4F6F8 | 卡片、代码/命令区、对照面板底色 |
| Primary | #1A3A6B | 封面/主标题/结构框/核心层级主色 |
| Accent | #E8A317 | 关键数字、门控节点、警示高亮 |
| Secondary accent | #4A7BB5 | 次级模块标识、流程连线、图标辅色 |
| Body text | #1D2430 | 正文与列表主文字 |
| Secondary text | #5A6577 | 页脚、副标题、注解与标签文字 |
| Divider | #DCE2EA | 细分隔线与表格/卡片边框 |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | 锐利无衬线粗体 | Microsoft YaHei | Arial | sans-serif |
| Body | 中性易读无衬线 | Microsoft YaHei | Arial | sans-serif |

- **Title stack**: 'Microsoft YaHei', Arial, sans-serif
- **Body stack**: 'Microsoft YaHei', Arial, sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 24 |
| Title | 40 |
| Section title | 36 |
| Subtitle | 22 |
| Card title | 19 |
| Annotation | 16 |
| Code | 13 |

## V. Layout Principles

### Deck-wide Direction

- **Hierarchy direction**: 左上标题与章节定位先入眼，随后进入主结构图或对照卡片区，右下角保留页码。
- **Composition tendency**: 非对称分栏、层级栈、生命周期流与对比矩阵交替使用。
- **Cross-page continuity**: 顶部统一 Part 1 / Part 2 色标与细规则页眉，底部统一页码。
- **Spacing posture**: 留白充足，卡片内部紧凑对齐。
- **Spacing anchors**: margin 64 px, block gap 24 px, column gutter 28 px, corner radius 4 px, body leading 1.45

## VI. Icon Usage Specification

- **Primary bundled library**: tabler-outline
- **Stroke Width**: 2

| Icon Path | Suitable Scenarios |
| --- | --- |
| `tabler-outline/shield-check` | 规则与安全校验 |
| `tabler-outline/terminal-2` | Slash Commands & Skills |
| `tabler-outline/users` | Subagents |
| `tabler-outline/git-branch` | Git Worktree & Pipeline |
| `tabler-outline/lock` | 权限与原始数据保护 |
| `tabler-outline/database` | Memory & Wiki |
| `tabler-outline/file-text` | 论文写作 |
| `tabler-outline/devices` | 多平台适配 |
| `tabler-outline/alert-triangle` | 痛点与风险 |
| `tabler-outline/search` | 文献检索 |
| `tabler-outline/code` | 计量脚本 |
| `tabler-outline/scale` | 识别与审稿 |
| `tabler-outline/plug` | MCP 协议连接 |
| `tabler-outline/package` | Plugins 插件打包 |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: Claude Code 核心基础概念（基于 claude-howto）

#### Slide 01 - 封面
- **Audience move**: 初识分享主题 → 建立“先基础概念、后科研实战”的两段式预期
- **Relationships**: 主标题、副标题与双部结构标签（Part 1 + Part 2）构成总起关系
- **Title**: 从 Claude Code 核心概念到经济学研究实战
- **Core message**: 先看懂 AI 编程底座的 8 个核心原语，再看懂 Economics Research Crew 如何用它们管住科研全流程
- **Content**: Part 1 基础概念（claude-howto）+ Part 2 科研体系（Economics Research Crew）

#### Slide 02 - 全场导览：为什么先讲基础概念
- **Audience move**: 疑惑为何分两部分 → 理解 Part 1 的 8 个概念与 Part 2 模块的一一映射关系
- **Relationships**: 左侧 Part 1（8 大底座）与右侧 Part 2（科研护栏）形成映射连接（link）
- **Title**: 全场导览：两部分如何串联起来
- **Core message**: Economics Research Crew 不是凭空造轮子，而是把 Claude Code 原生机制组合成科研规范
- **Content**: 左侧 Part 1 8 大基础概念清单；右侧 Part 2 对应落地模块映射

#### Slide 03 - Part 1 总览：Claude Code 扩展生态与加载顺序
- **Audience move**: 面对众多名词感到混淆 → 用一张加载时间线和对比表分清 8 个概念的触发与作用域
- **Relationships**: 会话启动加载链（order）+ 能力对比矩阵（contrast）
- **Title**: Part 1 总览：会话启动顺序与核心能力定位
- **Core message**: 静态记忆自动加载、斜杠命令手动触发、Skills 模型自选、MCP 连外部实时数据、Hooks 事件驱动拦截
- **Content**: 启动加载时间线 + 6 维对比矩阵

#### Slide 04 - 基础概念 ① CLAUDE.md（Memory 记忆体系）
- **Audience move**: 以为 CLAUDE.md 只是普通说明文档 → 理解 7 层拼接记忆层级与 Auto Memory 机制
- **Relationships**: 7 层记忆按优先级从高到低拼接（order）
- **Title**: 基础 ① | CLAUDE.md：跨会话的 7 层记忆体系
- **Core message**: 7 层记忆文件拼接加载而非互相覆盖，越靠近本地与当前项目越后读入
- **Content**: 7 层层级表（Managed Policy → `./CLAUDE.md` → `.claude/rules/` → `~/.claude/CLAUDE.md` → `~/.claude/rules/` → `./CLAUDE.local.md` → Auto Memory）

#### Slide 05 - 基础概念 ② Slash Commands（斜杠命令）
- **Audience move**: 区分内置命令与自定义命令 → 理解 `.claude/commands/*.md` 如何把高频 Prompt 变成 `/命令`
- **Relationships**: 用户输入 `/cmd` → 检索 `.claude/commands/` → 加载 Markdown 与参数 → 执行（order）
- **Title**: 基础 ② | Slash Commands：手动触发的 Prompt 快捷方式
- **Core message**: 把团队高频工作流写成 Markdown 文件，支持 `@文件` 引用、Bash `$(...)` 注入与传参
- **Content**: 执行生命周期 + 作用域（项目级 `.claude/commands/` vs 个人级 `~/.claude/commands/`）+ 核心能力

#### Slide 06 - 基础概念 ③ Skills（智能体技能）
- **Audience move**: 分不清 Skill 与 Slash Command → 理解 Skill 是“模型按需自动加载的能力文件夹”
- **Relationships**: Skill 文件夹结构（parent）+ 与 Slash Command 对比（contrast）
- **Title**: 基础 ③ | Skills：模型按需自动调用的能力包
- **Core message**: 文件夹封装 `SKILL.md`（YAML 元数据 + 指令）与脚本/模板，由模型根据任务语义自动匹配触发
- **Content**: 目录结构 + 4 种来源（Pre-built / Personal / Project / Plugin）+ 与 Slash Commands 的 3 点差异

#### Slide 07 - 基础概念 ④ Subagents（专业子代理）
- **Audience move**: 疑惑为什么需要子代理 → 理解独立上下文窗口、定制提示词与嵌套委派
- **Relationships**: Main Agent 向专门 Subagent 委派并汇总结果（parent / order）
- **Title**: 基础 ④ | Subagents：上下文隔离与专才分工
- **Core message**: 每个 Subagent 拥有独立上下文窗口与工具权限，避免长任务污染主对话（v2.1.219 默认支持 3 层嵌套）
- **Content**: 协调者-专才架构图 + 核心优势（上下文隔离、工具权限裁剪、独立系统提示词、可嵌套）

#### Slide 08 - 基础概念 ⑤ MCP（Model Context Protocol）
- **Audience move**: 混淆 Memory 与 MCP → 理解 MCP 是连接外部工具与实时数据的标准化协议
- **Relationships**: Claude ↔ MCP Server ↔ 外部服务（Filesystem / GitHub / Slack / DB）双向请求响应（link）
- **Title**: 基础 ⑤ | MCP：连接外部工具与实时数据的标准协议
- **Core message**: Memory 管静态上下文，MCP 管实时外部读写（文件系统、GitHub、数据库、Slack 等）
- **Content**: MCP 架构流 + 常见 MCP Server 与实时权限对比

#### Slide 09 - 基础概念 ⑥ Hooks（事件驱动钩子）
- **Audience move**: 以为只能靠提示词求 AI 听话 → 理解配置在 `settings.json` 的确定性事件拦截机制
- **Relationships**: 33 种生命周期事件按时机分布（order）+ 5 种 Hook 实现载体（membership）
- **Title**: 基础 ⑥ | Hooks：事件驱动的确定性自动化与拦截
- **Core message**: 在工具调用前后、会话启停等 33 个事件节点自动触发脚本或校验，无需 AI “自觉遵守”
- **Content**: 核心事件（`PreToolUse`、`PostToolUse`、`UserPromptSubmit`、`SubagentStart/Stop`、`Stop`）+ 5 种载体 + `settings.json` 示例

#### Slide 10 - 基础概念 ⑦⑧ Git Worktree & Plugins
- **Audience move**: 了解单会话扩展后 → 掌握多分支并行隔离（Worktree）与生态打包分发（Plugins）
- **Relationships**: 左侧 Git Worktree 与右侧 Plugins 并列对比（membership）
- **Title**: 基础 ⑦⑧ | Git Worktree（并行隔离）与 Plugins（打包分发）
- **Core message**: Worktree 让多任务在不同分支目录并行不打架；Plugin 把 Commands/Subagents/MCP/Hooks 一键打包共享
- **Content**: 左：Worktree（`claude --worktree` / `.claude/worktrees/` / `bgIsolation` / `EnterWorktree`）；右：Plugins（`.claude-plugin/plugin.json` / 四类分发范围）

### Part 2: Economics Research Crew 科研实战

#### Slide 11 - Part 2 核心定位：它不是计量软件，而是科研护栏
- **Audience move**: 从通用概念切入科研场景 → 理解通用 AI 做科研的 4 大失控风险及本项目对策
- **Relationships**: 4 大痛点与 4 项工程对策一一对比（contrast）
- **Title**: Part 2 实战 | 不是计量软件，而是 AI 科研的“工程护栏”
- **Core message**: 不自动跑回归、不替代研究者决策，专门约束 AI 如何组织、检查和记录研究
- **Content**: 4 大痛点 vs 4 项对策 + 明确边界声明

#### Slide 12 - 总体架构：Part 1 概念在科研中的四层组装
- **Audience move**: 看到四层架构 → 瞬间对应上 Part 1 学过的 Rules / Skills / Subagents / Hooks
- **Relationships**: L1 规则层 → L2 能力层 → L3 控制层 → L4 沉淀层（order）
- **Title**: 总体架构：四层协同如何把研究管起来
- **Core message**: 把 Part 1 的基础原语组合成“规则定底线、技能定流程、代理分职责、脚本守状态”的科研系统
- **Content**: 四层架构图与核心文件位置

#### Slide 13 - 科研 Rules & 14 个 Skills 实战
- **Audience move**: 看懂规则与技能如何针对经济学研究做深度定制
- **Relationships**: 左边 3 条科研 Rules 支柱，右边 14 个 Skills 分组（membership）
- **Title**: 科研落地 ① | Rules（证据/计量/数据）与 14 个 Skills
- **Core message**: 用 `CLAUDE.md`/`AGENTS.md` 立下证据与因果铁律，用 14 个 `/命令` 固化研究、Wiki 与写作 SOP
- **Content**: 3 条底线 + 14 个 Skills 分类清单

#### Slide 14 - 科研 Subagents：7 个专业代理与权限隔离
- **Audience move**: 理解科研场景下为什么必须把“写代码”和“审稿”拆开
- **Relationships**: 5 个研究代理 → 1 个唯一有 Bash 的 `econometrics-agent` → 1 个只读 `academic-reviewer`（order）
- **Title**: 科研落地 ② | 7 个 Subagents：权限最小化与独立审稿
- **Core message**: 只有 `econometrics-agent` 能执行 Bash；`academic-reviewer` 只读且靠 `handoff.md` 隔离，杜绝“边审边改”
- **Content**: 三栏角色权限图 + 质量闭环

#### Slide 15 - Research Director：S1–S12 状态机与关卡机制
- **Audience move**: 理解 `/research-pipeline` 如何把长周期研究拆成可控阶段
- **Relationships**: S1–S7 研究闭环与 S8–S12 写作闭环（order）+ 三大核心机制
- **Title**: 科研落地 ③ | Research Director：S1–S12 状态机与关卡
- **Core message**: `orchestrator.py` 维护 `STATE.json` 与 `run-ledger.jsonl`，支持断点续跑、2 次重试熔断与研究者拍板关卡
- **Content**: S1–S12 两段流程图 + 3 大机制卡

#### Slide 16 - 科研 Hooks 安全网与工程边界
- **Audience move**: 理解 Part 1 的 Hooks 如何落地为科研数据保护与编排拦截
- **Relationships**: 事前 `PreToolUse` → 编排守卫 → 事后 `PostToolUse`（order）
- **Title**: 科研落地 ④ | 6 个 Hooks：原始数据保护与编排守卫
- **Core message**: `protect_raw.py` 锁死 `raw` 与 `_sources`，`orchestrator_guard.py` 拦越级派出；坦诚说明“护栏非沙箱”
- **Content**: 三阶段 Hook 清单 + 工程边界声明

#### Slide 17 - 可积累 Wiki 与人机协作写稿（S8–S12）
- **Audience move**: 理解研究知识如何跨项目复利积累，论文草稿如何杜绝数字与文献幻觉
- **Relationships**: 左半区三层 Wiki 两步摄入，右半区 `paper_tools.py` 三大锚定标记（membership）
- **Title**: 科研落地 ⑤ | 可积累 Wiki 与论文机械可追溯机制
- **Core message**: `/ingest-source` 两步摄入 + `review-queue.md` 冲突入队；正文用 `[@key]`、`{{res:id}}` 与 `⟦问：…⟧` 锁死账本
- **Content**: 左 Wiki 三层与体检 + 右写稿三大机械标记

#### Slide 18 - 多平台适配与 3 步无损上手
- **Audience move**: 知道如何把这套体系安装到 Claude Code / `agy` / Codex 并安全试跑
- **Relationships**: 上部 `payload/.claude/` 单一源与三平台对比，下部 3 步上手命令（order）
- **Title**: 总结与上手 | 多平台适配与 3 步无损接入
- **Core message**: `payload/.claude/` 单一源生成 Claude Code / `agy` / Codex 配置；`-WhatIf` 预演、校验、首次只读体检即可安全落地
- **Content**: 三平台能力对比 + 3 步 PowerShell 上手命令

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: match each SVG filename under `notes/`
- **Content**: 为每页生成 120–180 字口播讲解词，流畅衔接 Part 1 基础概念与 Part 2 科研实战
- **Total duration**: 20-25 minutes
- **Notes style**: conversational
- **Presentation purpose**: 系统讲解 Claude Code 基础概念与 Economics Research Crew 科研实战落地
