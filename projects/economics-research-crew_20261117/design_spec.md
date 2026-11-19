<!-- ppt-master-schema: design-spec/v1 -->
# Economics Research Crew - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | Economics Research Crew |
| Canvas Format | PPT 16:9 (1280×720) |
| Page Count | 12 |
| Primary Language | zh-CN |
| Target Audience | 对 AI 辅助经济学研究工作流感兴趣的学者、研究生、研究团队成员或技术同行 |
| Communication Intent | 系统讲解 Economics Research Crew 的设计动机、核心架构与各关键模块概念，让听众理解它如何用规则、技能、子代理、编排器、Hook 与知识库约束 AI 开展严谨的经济学研究 |
| Desired Audience Outcome | 听众能清晰区分项目中的核心概念（Rules / Skills / Subagents / Orchestrator / Hooks / 可积累 Wiki / 人机协作写稿 / 多平台适配），并知道如何在自己的研究库中落地使用 |
| Core Message / Ask / Action | Economics Research Crew 不是计量软件，而是一套面向经济学与因果推断研究的 AI 协作规范与工程约束体系：让研究流程可追溯、可审查、可积累 |
| Delivery Context | 主要为有主讲人的现场技术/学术分享（约 15–20 分钟）；次要为会后可独立阅读的项目导览材料 |
| Artifact Afterlife | 作为项目介绍材料、团队内部培训参考与新成员上手指南 |
| Reading Mode | balanced |
| Content Strategy | 平衡重组：忠实于仓库 README、USAGE、ECONOMICS-RESEARCH 与 pipeline-stages 事实，按“定位总览 → 核心概念逐个拆解 → 落地上手”重排教学动线 |
| Design Style | 学术极简（Swiss Minimal + Editorial） |
| AI Image Acquisition Path | not applicable |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — confirmed in Stage 2 |
| Custom Animations | disabled — confirmed in Stage 2 |
| Narration Audio | disabled — confirmed in Stage 2 |
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
- **Mode Behavior**: 先用 pyramid 结论先行建立项目整体定位与四层架构认知，再以 instructional 循序拆解 8 个核心概念，每页聚焦“是什么、解决什么痛点、如何运作”。
- **Visual style**: custom
- **Visual Style References**: swiss-minimal, editorial
- **Visual Style Behavior**: 以 swiss-minimal 精确栅格、大留白与直角几何区块为主骨架，辅以 editorial 的细规则分隔线、序号徽标与证据对照层级；严格扁平无阴影。
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

- **Hierarchy direction**: 左上标题与核心断言先入眼，随后进入主结构图或对照卡片区，右下角保留页码与章节脉络。
- **Composition tendency**: 非对称分栏、三/四列结构卡、流程状态链与对比矩阵交替使用，避免连续两页同构。
- **Cross-page continuity**: 顶部统一细规则页眉与概念序号徽标（`01`–`08`），底部统一简洁页码与项目名。
- **Spacing posture**: 留白充足（25%–35%），卡片内部紧凑对齐。
- **Spacing anchors**: margin 64 px, block gap 24 px, column gutter 28 px, corner radius 4 px, body leading 1.45

## VI. Icon Usage Specification

- **Primary bundled library**: tabler-outline
- **Stroke Width**: 2

| Icon Path | Suitable Scenarios |
| --- | --- |
| `tabler-outline/shield-check` | 规则约束与安全校验 |
| `tabler-outline/terminal-2` | Skills 斜杠命令 |
| `tabler-outline/users` | 多 Subagent 分工 |
| `tabler-outline/git-branch` | 阶段编排与流水线 |
| `tabler-outline/lock` | 原始数据只读保护 |
| `tabler-outline/database` | 可积累 Wiki 知识库 |
| `tabler-outline/file-text` | 论文写作与引文 |
| `tabler-outline/devices` | 多平台适配（Claude / agy / Codex） |
| `tabler-outline/alert-triangle` | 痛点与风险警示 |
| `tabler-outline/search` | 文献检索与审计 |
| `tabler-outline/code` | 计量脚本与复现 |
| `tabler-outline/scale` | 因果识别与审稿评判 |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Image pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: 项目定位与总体架构

#### Slide 01 - 封面：Economics Research Crew
- **Audience move**: 初识项目名称 → 建立“经济学研究的 AI 工程化协作体系”第一印象
- **Relationships**: 主标题、副标题与三大核心标签（可追溯 · 可审查 · 可积累）构成总起关系
- **Composition**: 深海蓝主视觉色块与右侧极简四层结构线框呼应，突出主标题与演讲副题
- **Title**: Economics Research Crew
- **Core message**: 面向经济学与因果推断研究的 AI 协作规范与工程约束体系
- **Content**:
  - 副标题：把通用编程 AI 改造成遵守学术铁律的研究团队
  - 核心标签：Claude Code · Antigravity CLI (`agy`) · Codex CLI
  - 三大支柱：可追溯 · 可审查 · 可积累
- **Cover impact**: 用“不是计量软件，而是科研护栏”建立明确记忆点；深海蓝左置色域与极简几何框。

#### Slide 02 - 核心定位与痛点：为什么需要它
- **Audience move**: 以为只是几个 Prompt → 理解通用 AI 做科研的四大失控风险及本项目的对策
- **Relationships**: 左侧“通用 AI 裸跑的 4 大痛点”与右侧“Economics Research Crew 的 4 项硬约束”形成一一对比（contrast）
- **Title**: 它不是计量软件，而是 AI 科研的“工程护栏”
- **Core message**: 不自动跑回归、不替代研究者决策，专门约束 AI 如何组织、检查和记录研究
- **Content**:
  - 痛点 vs 对策：1) 编造文献/DOI/法条 → 证据铁律（未核实即标“待核实”）；2) 直接跑回归跳过识别 → 强制先审 Estimand 与识别假设；3) 误改原始数据/覆盖笔记 → 原始目录只读与备份机制；4) 对话结束知识清零 → 三层可积累 Wiki 与状态账本
  - 明确边界：不包含 Stata/R/Python 计量引擎，脚本与数据由研究者确认

#### Slide 03 - 总体架构：四层协同模型
- **Audience move**: 面对众多目录与文件感到零散 → 建立清晰的四层架构心智模型
- **Relationships**: 自底向上/自顶向下的四层依赖关系（parent / order）：规则层 → 技能与子代理层 → 编排与安全层 → 知识库与产出层
- **Title**: 总体架构：四层协同如何把研究管起来
- **Core message**: 通过“规则定底线、技能定流程、代理分职责、脚本守状态”实现全链路可控
- **Content**:
  - 第 1 层 Rules（规则层）：`CLAUDE.md` / `AGENTS.md` + `ECONOMICS-RESEARCH.md`，每次会话自动加载
  - 第 2 层 Skills & Subagents（能力层）：14 个标准化 Skill（`/命令`）+ 7 个职责隔离的 Subagent
  - 第 3 层 Orchestrator & Hooks（控制层）：`orchestrator.py`（S1–S12 状态机）+ 6 个技术拦截/校验 Hook
  - 第 4 层 Wiki & Outputs（沉淀层）：`Meta/`、`03-Literature/`、`06-Data/`、`paper/` 模板与账本

### Part 2: 八大关键概念逐层拆解

#### Slide 04 - 关键概念 ① Rules（项目规则）
- **Audience move**: 以为规则只是客套话 → 理解 Rules 是每次会话自动加载的“科研宪法”
- **Relationships**: 三大规则支柱（证据铁律 · 计量纪律 · 数据安全）并列支撑研究可信度（membership）
- **Title**: 01 | Rules：每次会话自动加载的“科研宪法”
- **Core message**: 把方法论要求写进 `CLAUDE.md` / `AGENTS.md`，让 AI 默认遵守而非每次口头提醒
- **Content**:
  - 载体：Claude Code 读 `CLAUDE.md` + `.claude/ECONOMICS-RESEARCH.md`；`agy`/Codex 读 `AGENTS.md`（`ERC:BEGIN…END` 区块，≤24 KB）
  - 证据铁律：不编造文献/DOI/法条/结果；中国税法须给出文号、发布与生效日期、废止状态
  - 计量纪律：区分相关与因果；先定 Estimand 与假设再谈回归；说明聚类层级与样本筛选
  - 数据安全：`06-Data/raw` 与 `03-Literature/_sources` 绝对只读；衍生数据仅写 `06-Data/processed`

#### Slide 05 - 关键概念 ② Skills（14 个标准化技能）
- **Audience move**: 混淆普通对话与 Skill → 理解 Skill 是“带门控与固定产出的标准化 SOP”
- **Relationships**: 按研究生命周期分组呈现 14 个 Skill 的触发与产出关系（membership）
- **Title**: 02 | Skills：用 `/命令` 触发标准化科研 SOP
- **Core message**: 14 个 Skill 各自封装了必须步骤、检查点与模板路径，防止 AI 跳步自由发挥
- **Content**:
  - 研究推进类（7 个）：`/research-question`、`/literature-review`、`/theory-modeling`、`/tax-policy-analysis`、`/causal-inference-audit`、`/econometric-analysis`、`/academic-review`
  - 知识库维护类（3 个）：`/ingest-source`、`/query-wiki`、`/wiki-lint`
  - 论文写作类（3 个）：`/paper-outline`、`/paper-draft`、`/paper-refine`
  - 总控编排类（1 个）：`/research-pipeline`（全流程串联）

#### Slide 06 - 关键概念 ③ Subagents（7 个专业子代理）
- **Audience move**: 疑惑“为什么不让一个 AI 全干” → 理解上下文隔离、工具权限分级与独立审稿的价值
- **Relationships**: 7 个 Subagent 按“研究执行”与“独立审查”划分，体现工具权限最小化原则（contrast / membership）
- **Title**: 03 | Subagents：职责隔离与工具权限分级
- **Core message**: 独立上下文防止长阅读污染主对话；只有 `econometrics-agent` 能执行 Bash，审稿人只读不改
- **Content**:
  - 5 个前置研究代理：`literature-agent`（读/搜/网）、`theory-agent`（读/写）、`tax-policy-agent`（读/搜/网）、`causal-inference-agent`（读/搜/网/写）、`paper-writer-agent`（成稿/精修）
  - 1 个执行代理：`econometrics-agent`（唯一拥有 Bash 权限，负责数据审计与计量代码）
  - 1 个对抗审稿代理：`academic-reviewer`（只读+联网，严禁写文件，只看产物交接单 `Templates/handoff.md`，杜绝“边审边改”）

#### Slide 07 - 关键概念 ④ Research Director（编排器）
- **Audience move**: 担心多阶段研究中断或 AI 越权 → 理解 `orchestrator.py` 如何用状态机与人工关卡管住全流程
- **Relationships**: S1→S12 线性阶段流（order），穿插 Researcher Gate（关卡）与重试上限约束
- **Title**: 04 | Research Director：S1–S12 状态机与关卡机制
- **Core message**: `/research-pipeline` 通过 `orchestrator.py` 维护 `STATE.json` 与 `run-ledger.jsonl`，关卡只由研究者拍板
- **Content**:
  - 两段 12 阶段：S1–S7 研究闭环（问题 → 文献 → 机制 → 设计 → 执行 → 独立审查 → 决定）；S8–S12 写作闭环（大纲 → 引文 → 成稿 → 精修 → 终检）
  - 核心机制：断点续跑（读 `STATE.json`）、单阶段最多重试 2 次、并发上限控制（默认 1，S3 最多 2，硬上限 3）
  - 铁律：AI 严禁自行执行 `gate --decision pass`，必须由研究者确认后通过

#### Slide 08 - 关键概念 ⑤ Hooks（技术安全网）
- **Audience move**: 担心“规则写了 AI 不听怎么办” → 理解 Hooks 在工具调用前后提供的确定性技术拦截
- **Relationships**: 6 个 Hook 按触发时机（PreToolUse / PostToolUse / 编排与提示）构成多层防护（membership）
- **Title**: 05 | Hooks：把“口头约束”变成确定性技术拦截
- **Core message**: 在 `-WithHooks` 启用后，通过 Python 脚本在工具调用层硬性保护原始数据、格式与阶段纪律
- **Content**:
  - 原始材料保护 `protect_raw.py`：拦截对 `06-Data/raw` 与 `03-Literature/_sources` 已有文件的 Write/Edit 与危险 Bash 操作
  - 格式与论文校验：`validate_frontmatter.py`（检查 `.md` 元数据闭合/Tab）与 `validate_paper.py`
  - 编排守卫与记录：`orchestrator_guard.py` & `orchestrator_record.py`（Claude Code 下硬拦截越级派出、超重试与直接改 `STATE.json`）
  - 路由提示 `routing_hint.py`：注入路由提醒；坦诚说明局限——是护栏而非沙箱，仍需配合 Git 备份

#### Slide 09 - 关键概念 ⑥ 可积累 Wiki（知识库）
- **Audience move**: 每次做研究都从零查文献 → 理解三层 Wiki 如何让知识越用越厚、冲突显性化
- **Relationships**: 三层沉淀链路（order）：原始来源（不可变）→ Wiki 页面（可积累）→ 规则层，配合两步摄入与体检
- **Title**: 06 | 可积累 Wiki：让知识库越用越厚的三层结构
- **Core message**: 借鉴 llm_wiki 思路，用“两步摄入 + 冲突入队 + 确定性体检”替代一次性检索
- **Content**:
  - 三层架构：`03-Literature/_sources/`（不可变原件）→ `03-Literature/`、`04-Theories/` 等 Wiki 页面 → `CLAUDE.md` 规则
  - 两步摄入 `/ingest-source`：先算 SHA256 去重并输出分析与拟改清单 → **研究者确认后**才写入页面、更新 `Meta/index.md` 与 `research-log.md`
  - 冲突不静默消解：不同来源的矛盾并列写入 `Meta/review-queue.md` 等待裁决
  - 确定性体检 `wiki_lint.py`：查断链、孤立页、溯源与 `index` 覆盖（自动跳过库内原有税法笔记）

#### Slide 10 - 关键概念 ⑦ 人机协作写稿（S8–S12）
- **Audience move**: 害怕 AI 写论文胡编乱造数字与文献 → 理解 `paper_tools.py` 如何用机械绑定锁死引文与实证数字
- **Relationships**: 大纲主张 → 引文表 & 结果账本 → 成稿标记 → 精修判定（order + link）
- **Title**: 07 | 人机协作写稿：引文与数字的机械可追溯
- **Core message**: 正文禁止手写文献和数字，所有引用与实证结果必须锚定到账本并经人工确认
- **Content**:
  - 引文锚定 `[@key]`：仅允许使用 `Meta/citation-map.json` 中的 key；`paper_tools.py cite` 支持 Crossref 仅发标题/DOI 核验（可 `--offline` 关闭）
  - 数字锚定 `{{res:id}}`：所有回归与描述性数字从 `Meta/results-ledger.json` 映射，杜绝篡改或幻觉
  - 不确定时显式发问 `⟦问：…⟧`：AI 遇到缺口不准脑补，用标记向研究者提问，研究者用 `⟦答：…⟧` 回复
  - 精修闭环 `refine record`：最多 3 轮，仅当未新增 Fatal 且减少了 Major 问题才接受修改

### Part 3: 多平台适配与快速上手

#### Slide 11 - 关键概念 ⑧ 多平台适配（Claude / agy / Codex）
- **Audience move**: 担心换了 CLI 工具就要重写两套配置 → 理解单一源生成机制与平台能力边界
- **Relationships**: 单一源 `payload/.claude/` 向三大平台编译分发，同时对比三平台的能力差异矩阵（contrast）
- **Title**: 08 | 多平台适配：单一源生成与平台能力边界
- **Core message**: `payload/.claude/` 是唯一维护源，安装器自动为 Claude Code、`agy` 与 Codex CLI 生成对应配置
- **Content**:
  - 单一源原则：修改规则或 Skill 只改 `payload/.claude/`，再用 `-Update` 或 `Sync-AgentsMd.ps1` 同步，不直接改目标库 `.agents/`
  - Claude Code（完整版）：`CLAUDE.md` + `.claude/`，支持全量 Hooks（含编排强拦截）
  - Antigravity CLI（`agy`，已冒烟测试）：`AGENTS.md` + `.agents/` + `.agents/hooks.json`（含原始材料保护与路由提示，无编排强拦截 Hook）
  - Codex CLI（已生成文件，未跑全测）：`AGENTS.md` + `.agents/`，无 Hook，靠规则文本约束

#### Slide 12 - 总结与上手路径：3 步落地到你的研究库
- **Audience move**: 听完概念想亲自试用 → 掌握安全、不覆盖原有文件的 3 步安装与体检流程
- **Relationships**: 预演安装 → 校验结构 → 首次只读体检（order），辅以核心记忆口诀
- **Title**: 总结与上手：3 步无损接入你的研究库
- **Core message**: 安装器绝不覆盖已有 `CLAUDE.md` / `settings.json`，改动前自动备份至 `_erc-backups/`
- **Content**:
  - 第 1 步 预演与安装：`.\Install-EconomicsResearchCrew.ps1 -VaultPath "<库路径>" -WhatIf` → 确认后去掉 `-WhatIf` 并按需加 `-WithHooks`
  - 第 2 步 结构校验：`.\Test-EconomicsResearchCrew.ps1 -VaultPath "<库路径>"` 与 `tests\run.ps1` 回归测试
  - 第 3 步 首次只读体检：启动 CLI 后先让其只读 `CLAUDE.md` / `AGENTS.md` 与 `Meta/vault-map.md`，报告已发现的 Agent 与 Skill
  - 一句话带走：用工程化护栏守住学术底线，把判断权留给研究者
- **Closing impact**: 给出 3 条可直接复制的 PowerShell 命令与核心总结句，干脆收束。

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: match each SVG filename under `notes/`
- **Content**: 为每页生成口播讲解词，解释概念“是什么、为什么这样设计、实际怎么用”，语气温和清晰，约 120–180 字/页，帮助主讲人流畅讲透每个关键概念
- **Total duration**: 15-20 minutes
- **Notes style**: conversational
- **Presentation purpose**: 系统讲解 Economics Research Crew 的设计动机、核心架构与各关键模块概念，让听众理解它如何用规则、技能、子代理、编排器、Hook 与知识库约束 AI 开展严谨的经济学研究
