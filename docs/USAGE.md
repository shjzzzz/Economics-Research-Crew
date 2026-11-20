# 使用说明

本说明面向已把 Economics Research Crew 安装到研究库（下称 Vault，例如 `D:\Economicresearchwiki`）的使用者。安装与升级命令见 [README](../README.md)。

## 1. 它是什么
一组面向税收经济学、公共经济学、计量经济学与因果推断的 AI 研究协作框架：
- **7 个专业 Subagent**（`.claude/agents/` / `.agents/agents/`）：各有职责、工具权限与 `data_access_level` 隔离。
- **21 个必装 Skill**（`.claude/skills/` / `.agents/skills/`）：含 15 个 S1–S12 研究写作与知识库核心 Skill + 6 个学术绘图与制表 Skill（`publication-chart-skill`、`econ-visualization`、`scientific-visualization`、`copyplot`、`thu-digitizer`、`tikz`），用 `/名称` 触发。
- **单源项目规则**（`CLAUDE.md` + `.claude/ECONOMICS-RESEARCH.md`，同步生成多平台 `AGENTS.md`）：定义路由、四层知识架构与论证脊柱。
- **规范与模板**（`Meta/`、`Templates/`）：研究方向（`purpose`）、目录（`index`）、决定记录（`decisions`）、机制库、风格指南、AI 套话库，以及大纲/分析计划/日志/数据卡/文献卡/R&R 返修矩阵模板。
- **确定性脚本与 6 个 Hooks**（`.claude/scripts/`、`.claude/hooks/`）：`orchestrator.py`（状态机与关卡）、`paper_tools.py`（引文/结果/主张/精修/润色校验）、`wiki_lint.py`（体检与双地图）；可选的原始材料只读保护、编排守卫、草稿与 frontmatter 校验、意图路由提示。

它不包含计量软件，也不会擅自运行回归；它确保每项研究遵循“识别先行、数字与引文机械可追溯、研究者把关”的纪律。

## 2. 开始一次会话
```powershell
Set-Location D:\Economicresearchwiki
claude
```
首次使用先做只读检查：
```text
请读取 CLAUDE.md、.claude/ECONOMICS-RESEARCH.md、Meta/vault-map.md、Meta/research-standards.md。
只检查配置与目录，不修改知识库。报告已发现的 Agent、Skills、路径与潜在冲突。
```
再用 `/agents` 确认 **7 个 Agent**，`/skills` 确认 **21 个 Skill**。

## 3. 21 个必装 Skill 速查
| 命令 | 阶段 / 何时用 | 核心产出 |
|---|---|---|
| `/research-question <主题>` | S1：主题收敛为可检验研究问题与 estimand（苏格拉底防越位） | ≤3 候选（仅获明确指令后）、理想 vs 准实验对比、可行性评估、`PROJECT.md` |
| `/literature-review <范围>` | S2/S9：争论簇文献梳理与三层定位锚点引文登记 | 检索记录、2–4 簇文献矩阵、精确缺口、未核实清单、`citation-map.json` |
| `/theory-modeling <机制>` | S3：形式化建模与竞争性机制推导 | 假设表、逐步推导、比较静态、竞争机制排他推论、简化式映射 |
| `/tax-policy-analysis <政策>` | S3：中国税法适用、冲突处理、征管归宿与政策冲击抽取 | 法源与效力表（含证据等级）、归宿渠道、政策冲击识别要素表 |
| `/causal-inference-audit <设计>` | S4：DID/IV/RDD/聚束/SCM 识别审查（不跑回归） | 六项必答核查、现代诊断清单、威胁—检验—证伪矩阵、冻结 `analysis-plan.md` 与因果措辞上限 |
| `/econometric-analysis <任务>` | S5：数据审计、计量实现、论文复现与代码审计 | 模块化脚本、样本瀑布、`analysis-log.md`、机读 CSV 并入簿 `results-ledger.json` |
| `/academic-review <稿件/设计>` | S6/S11：独立对抗审稿（只审不改） | 编号清单 `F1/M1/m1` + 5 维评分 + 框架锁定检测 + 7 类 AI 失效核查 |
| `/paper-outline <项目>` | S8：把冻结研究产物转为可校验论文架构 | `paper/outline.md`（主张清单、6 步引言蓝图、文献布局、图表叙事计划） |
| `/paper-draft <项目>` | S10：严格受限输入的分节成稿 | `paper/draft.md`（只用 `[@key]`、`{{res:id}}`、`<!-- claim -->`）与主张对照表 |
| `/paper-refine <项目>` | S11：清单复核多轮精修（≤3 轮）与外部期刊 R&R 返修 | `paper/versions/`、`reviews.json`、`worklog-vN.md`、`rebuttal-matrix.md` |
| `/paper-polish <稿件>` | S11b：内容定稿后的语言与文风精修（不用于过 AI 检测） | `paper/polished.md`、变更报告、`polish check` 不变性核对结果 |
| `/research-pipeline <主题/项目>` | S1–S12 全流程编排、恢复进度、关卡与结项知识回流 | 阶段计划、`STATE.json`、质量闭环与 `08-Research-Notes/` 综合页回流 |
| `/ingest-source <文件>` | 两步摄入 `03-Literature/_sources/` 来源到 wiki | 先分析停下等确认；确认后写文献卡（含 `cite_key`）、关联概念页、刷新双地图 |
| `/query-wiki <问题>` | 沿 `index` + `link-map` 枢纽页检索库内证据 | 区分事实与推断的带引用回答，可回存 `query` / `synthesis` 笔记 |
| `/wiki-lint` | 知识库确定性体检、论文指标联动与语义审计 | 断链/孤立页/重名/矛盾/过时/知识回流报告，批准后再修 |
| `/publication-chart-skill` | 出版级科研图表与三线表/LaTeX 表一体工作流（`pubfig`/`pubtab`） | 论文级图表 + 配套出版表格 |
| `/econ-visualization` | 经济学论文出版级 R / `ggplot2` 图表 | 经济学期刊规范图表脚本与图件 |
| `/scientific-visualization` | 期刊投稿级 Python 多子图、误差棒与显著性标注 | 顶刊格式 PDF/SVG/TIFF 图件 |
| `/copyplot` | 逆向分析并复现论文图表（Python/Matplotlib + 示例数据） | 可复现绘图脚本 + Excel 示例数据 |
| `/thu-digitizer` | 从图表图片/PDF 校准坐标轴并本地提取可复核数值数据 | 校准提取 CSV/JSON + 残差校验报告 |
| `/tikz` | 审计并数学修复 `.tex` 中 TikZ 图形标签/箭头碰撞 | 无碰撞 TikZ 代码与编译验证 |

## 4. 路由与角色映射
收到请求时按序路由：
1. 概念性/事实性短问题 → 直接回答。
2. 单项研究任务 → 先激活对应项目 Skill（含中文意图触发词与 `routing_hint.py` 提示）。
3. 完整研究、多阶段、“继续上次的研究” → `/research-pipeline`。
4. Agent 由 Skill 或 pipeline 在内部按需派出（一次一个）；调用 Skill 即视为授权派出其指定 Agent。
5. 本库内项目 Skill 优先于范围重叠的全局插件技能；研究者显式点名其他技能时以研究者为准。

### 8 角色 + Director 映射
| 角色 | 承担者 | 工具与权限特点 |
|---|---|---|
| Research Director | `/research-pipeline` | 阶段状态机、关卡把控、质量闭环、知识回流 |
| 01 文献研究 | `/literature-review`、`literature-agent`、`/ingest-source` | 读、搜、联网（`redacted`） |
| 02 理论建模 | `/theory-modeling`、`theory-agent` | 读、写、编辑（`verified_only`） |
| 03 数据工程 & 04 计量 & 06 复现 | `/econometric-analysis`、`econometrics-agent`；识别由 `/causal-inference-audit`、`causal-inference-agent` 负责 | 仅 `econometrics-agent` 具备 Bash 执行权限（`raw`） |
| 05 税收研究 | `/tax-policy-analysis`、`tax-policy-agent` | 读、搜、联网（`redacted`），内置中国税法冲突处理协议 |
| 07 学术写作 | `/paper-outline`、`/paper-draft`、`/paper-refine`、`/paper-polish`、`paper-writer-agent` | 读、写、编辑（`verified_only`），严格受限于大纲/引文表/结果登记簿 |
| 08 学术审稿 | `/academic-review`、`academic-reviewer`（独立上下文） | 只读、联网（`verified_only`），绝不改稿 |

质量闭环：研究 Agent 提方案 → `econometrics-agent` 执行并入簿 → `academic-reviewer` 独立质疑（只收产物不收推理）→ Director 与研究者决策；存在 Fatal Flaw 不得接受。

## 5. 四层知识架构与论证脊柱（推荐工作流）
目录按**四层知识流 + Meta 控制面**分工（详见 `Meta/vault-map.md`）：
- **Tier 0 原始只读层**：`03-Literature/_sources/`、`06-Data/raw/`、库内既有旧税法笔记（不移动、不改写，不进双链图）。
- **Tier 1 跨项目复利层**：`03-Literature/`（含 `cite_key` 与 `locator`）、`04-Theories/`、`05-Methods/`、`08-Research-Notes/`（`synthesis`/`query`）、`MOC/`。
- **Tier 2 项目执行与手稿层**：`01-Research-Projects/<项目>/`（`PROJECT.md` 为唯一进索引/双链图的项目入口；`STATE.json`、`analysis-plan.md`、`analysis-log.md` 与 `paper/` 子目录为项目工作产物，不污染全库双链图与多项目重名检查）、`06-Data/{processed,metadata}`、`07-Code/{stata,python,R}/<项目>/`。
- **Tier 3 独立交付与归档层**：`09-Writing/`（仅放非完整研究项目的政策简报、书评、讲义与投稿导出包）、`10-Archive/`。

全周期论证脊柱（S1–S12）：
1. **S1 定题**：`/research-question` 锁定问题、estimand、理想 vs 准实验 → `PROJECT.md`。
2. **S2 文献**：`/literature-review` 建 2–4 个争论簇矩阵与精确缺口 → `03-Literature/`。
3. **S3 机制与制度**：`/theory-modeling` 推竞争性假说与简化式映射；`/tax-policy-analysis` 核验法源并抽取政策冲击要素。
4. **S4 识别与冻结计划**：`/causal-inference-audit` 产出威胁—检验—证伪矩阵与因果措辞上限 → 冻结 `analysis-plan.md`（切勿跳过）。
5. **S5 实证执行与入簿**：`/econometric-analysis` 按计划跑脚本、记样本瀑布与经济量级 → `analysis-log.md` 并 `paper_tools.py results import` 入簿。
6. **S6–S7 独立审查与裁决**：`/academic-review` 输出 `F1/M1/m1` + 5 维分 + 7 类失效核查 → 研究者决定接受/退回/停止。
7. **S8–S12 论文写作与知识回流**：`/paper-outline`（C1）→ `paper_tools.py cite from-note/add`（C2）→ `/paper-draft`（C3）→ `/paper-refine`（C4）→ 可选 `/paper-polish` → S12 终检、`paper/ai-disclosure.md`（C5）并将综合结论回流至 `08-Research-Notes/` 刷新双地图。

## 6. 知识库维护（可积累的 Wiki）
- **先填 `Meta/purpose.md`**：研究方向、核心问题、范围边界；研究者关键决定记入 `Meta/decisions.md`。
- **两步摄入（`/ingest-source`）**：原始文件放 `03-Literature/_sources/`，先算 SHA256 去重并输出分析（含拟定 `cite_key` 与拟关联概念页），**等你确认后**才写卡、更新 `Meta/index.md`/`source-registry.md`/`research-log.md` 并刷新双地图；可一键用 `paper_tools.py cite from-note` 桥接入论文引文表。
- **图谱检索（`/query-wiki`）**：先读 `Meta/index.md` 与 `Meta/link-map.md` 枢纽页，沿 `[[双链]]` 展开，回答区分“事实”与“推断”。
- **体检与双地图（`/wiki-lint`）**：`python .claude/scripts/wiki_lint.py lint --vault .` 与 `map --vault .` 生成 `Meta/folder-map.md`、`Meta/link-map.md` 并刷新 `CLAUDE.md`/`AGENTS.md` 中的 `ERC:MAP` 区块；自动排除旧税法笔记、`paper/versions/` 与项目过程稿的孤立/重名噪音。

## 7. Hooks（可选，`-WithHooks` 启用）
合并进 `.claude/settings.json`（合并前备份、幂等、非法 JSON 拒绝改动；需要 PATH 中有 `python`）：

| Hook | 事件 | 作用 |
|---|---|---|
| `protect_raw.py` | PreToolUse（Write/Edit/Bash/PowerShell） | 阻止覆盖/修改 `06-Data/raw` 与 `03-Literature/_sources` 中已存在文件（允许 Write 新建导入） |
| `orchestrator_guard.py` | PreToolUse（Agent/Task/Bash/PowerShell/Write/Edit） | 阻止跳阶段派 Agent、超重试/超并发、直接编辑机读账本；对 `gate` 与 `cite confirm` 强制弹权限确认 |
| `validate_frontmatter.py` | PostToolUse（Write/Edit） | 检查写入 `.md` 的 YAML frontmatter 是否闭合、有无 Tab（反馈修正，不撤回） |
| `validate_paper.py` | PostToolUse（Write/Edit） | 写入 `01-Research-Projects/*/paper/*.md` 后立即告警未知 `[@key]` 与未知 `{{res:id}}` |
| `routing_hint.py` | UserPromptSubmit（agy 为 PreInvocation） | 按 `routing-triggers.json` 注入匹配 Skill 的确定性路由提示（不阻断） |
| `orchestrator_record.py` | SubagentStart / SubagentStop | 将 Agent 派出起止追加记录至 `Meta/run-ledger.jsonl`（不存消息正文） |

**局限**：对 Bash/PowerShell 仅做关键字启发式拦截，无法覆盖所有 shell 写法；异常输入 fail-open。Hooks 是安全增强层而非沙箱，Git 与备份仍不可替代。

## 8. 编排层：状态、关卡、重试与恢复
- 常用命令（库根目录）：
  - `python .claude/scripts/orchestrator.py status`（项目进度）
  - `python .claude/scripts/orchestrator.py next`（当前阶段缺口与重试额度）
  - `python .claude/scripts/orchestrator.py verify`（检查退出条件与机械检查项）
  - `python .claude/scripts/orchestrator.py log -n 20`（最近派出与关卡记录）
- **关卡由研究者决定**：`gate --decision pass|revise|return|stop --note "…"` 会触发权限确认；Agent 失败每阶段最多重试 2 次（`revise` 清零）；残留运行记录用 `recover` 清理，临时关闭拦截用 `enforce off`。

## 9. 论文写作工具链（`paper_tools.py`）
1. **大纲（S8）**：`/paper-outline` 生成含主张清单与 6 步引言蓝图的 `paper/outline.md`。
2. **结果入簿（S5/S8）**：`paper_tools.py results import <csv> --prefix <proj.t2>` 或 `results register`；若为保密税务微数据/官方年鉴手工摘录而无法提供库内源文件，用 `--no-source-reason "…"` 做“诚实空值”披露（与 `--source` 互斥）。
3. **引文管理（S9）**：
   - 从知识库文献卡直接桥接：`paper_tools.py cite from-note 03-Literature/<卡片>.md`；
   - 手动新增：`paper_tools.py cite add --key k --title "…" --year Y --locator "p.12, Table 2" --claim-scope "…" [--doi D | --type chinese | --type legal --doc-no … --effective …]`；
   - 人工确认：`paper_tools.py cite confirm --key k --note "…"`（触发权限提示）；导出 BibTeX：`cite bib -o paper/citations.bib`。
4. **成稿与主张审计（S10）**：`cite check`、`results check`、`claim check`（核对 `locator` 锚点、大纲主张覆盖度与因果动词越界）、`questions`、`report`。
5. **精修、审稿复核与润色（S11/S11b）**：`refine start` → `academic-reviewer` 基线评审 → `paper_tools.py review verify --review <报告> --manuscript <稿件>`（NFC 核对审稿原文引述 + Crossref 核验审稿推荐文献存在性）→ `refine record`（复评强制 `--carried-*`/`--new-*`）→ 内容定稿后可选 `/paper-polish`（`polish scan` 扫描 `Meta/ai-tells.json`，`polish check --before 原稿 --after 润色稿` 证明数字/引文/标记全不变）。

## 10. 多平台与跨系统支持（Windows 11 / macOS；Claude Code / Antigravity `agy` / Codex CLI）
- **跨系统安装**：Windows 11 使用 `Install-EconomicsResearchCrew.ps1`（或 `python tools/erc_cli.py`）；macOS / Linux 使用 `./install.sh --vault ~/Economicresearchwiki [--platform all] [--with-hooks]`（自动将 hooks 里的命令适配为 `python3`，Windows 11 保持 `python`）。
- **多 CLI 自适应**：`-Platform auto` / `--platform auto` 自动检测本机 CLI，也可用 `claude` / `agy` / `codex` / `all` 指定；`payload/.claude/` 是唯一源。
- **ARS 上游自适应追踪**：运行 `python tools/check_ars_updates.py check`（或 macOS `./install.sh check-ars`）按 `Meta/upstream-ars.json` 能力映射表检测 `Imbad0202/academic-research-skills` 新版本并输出原生适配简报（零 LLM 额度、不拷贝 CC-BY-NC 代码）；适配后用 `mark-audited --tag <tag> --sha <sha>` 推进基线。
- agy 与 Codex 共用根目录 `AGENTS.md`（自包含 `ERC:BEGIN…ERC:END` 区块，压控在 ≤24,000 字节上限内）、`.agents/skills/`、`.agents/agents/`、`.agents/scripts/`。安装器在纯 agy/Codex 环境下也会自动调用 `.agents/scripts/wiki_lint.py map` 生成双地图。
- 修改库内 `CLAUDE.md` 或 `.claude/ECONOMICS-RESEARCH.md` 后，运行 `.\Sync-AgentsMd.ps1 -VaultPath <库>` 同步 `AGENTS.md` 区块（`-Check` 只查不写）。
- agy 在 `-WithHooks` 下安装 `protect_raw.py`（放行时返回 `ask`，不自动批准）与 `routing_hint.py`；Codex 无 hook，原始材料只读靠规则约束。

## 11. 自定义、扩展与常见问题
- **自定义**：修改 `.claude/agents/*.md`、`.claude/skills/<name>/SKILL.md`、`Meta/style-guide.md`、`Meta/ai-tells.json` 后运行 `Test-EconomicsResearchCrew.ps1` 检查结构。升级用 `-Update` 生成 `.new` 副本，绝不覆盖你的本地改动。
- **`-WithExtras`**：可选安装 `payload-extras/` 中的本地自用第三方 Skill（只新增、不装 MCP、未经审计；原 6 个精选绘图/制表 Skill 已转入必装），使用规则见 `payload-extras/README.md`；与必装 21 个 Skill 重叠时必装 Skill 优先。
- **`-WithUpstream`**：需同时指定 `-RepoUrl`，在隔离目录构建，不自动导入会冲突的上游 dispatcher。
- **验证回归**：运行 `pwsh -NoProfile -File tests\run.ps1` 与 `powershell -NoProfile -File tests\run.ps1`（全在临时目录运行，不触碰真实知识库）。
- **卸载**：不提供自动卸载，按 README 文件清单手动删除；安装前备份保留在 `_erc-backups/<时间戳>/`。
