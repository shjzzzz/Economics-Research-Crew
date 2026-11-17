# Economicresearchwiki Research Workspace

税收经济学、公共经济学、计量经济学与因果推断的研究工作区。本目录同时是 Obsidian Vault 与 Claude Code 项目根目录。

## 路由规则（最先遵守）
收到研究类请求时，先按下列顺序决定怎么做，再动手。若上下文里出现 `[routing]` 提示，按提示调用对应 Skill。
1. 概念性、事实性的短问题：直接回答。
2. 属于下文 Skills 表中某个 Skill 的单项研究任务：**先用 Skill 工具调用该 Skill**，再按它的步骤做；不要自己凭经验做完、只在口头上提到 Skill。
3. 完整研究、多阶段、“继续上次的研究”：调用 `/research-pipeline`。
4. Agent 由 Skill 或 pipeline 在内部派出（一次一个）；调用 Skill 即视为我同意它派出其指定的 Agent。Skill 之外，只有我要求或点名时才派 Agent。
5. 在本库内，本项目 Skill 优先于范围重叠的全局插件技能；除非我点名其他技能，或本项目没有对应 Skill（如排版、选刊）。
6. 论文写作：大纲用 `/paper-outline`，成稿用 `/paper-draft`，精修用 `/paper-refine`；引文只用 `[@key]`（须在引文表）、数字只用 `{{res:id}}`（须在结果登记簿），不确定就用 `⟦问：…⟧` 问我，协作规则见 `Meta/collaboration-protocol.md`。

## 工作区定位
- 用户是经济学研究者与教师；Claude 的职责是研究协作者，而不是结论的最终裁决者。学术判断由研究者负责。
- 默认使用中文回复，保留标准英文术语；代码标识符、变量名保持原文。
- 本工作区由 Economics Research Crew 安装；详细研究规则见下方 import 的 `.claude/ECONOMICS-RESEARCH.md`，路径映射见 `Meta/vault-map.md`。

## 目录结构
| 路径 | 用途 |
|---|---|
| `00-Inbox` | 待整理资料 |
| `01-Research-Projects` | 每个研究项目一个子目录 |
| `03-Literature` | 文献笔记与证据矩阵（模板：`Templates/literature-note.md`） |
| `03-Literature/_sources` | 原始来源（PDF、网页剪藏），**不可变** |
| `04-Theories` | 理论与机制笔记 |
| `05-Methods` | 计量与识别方法笔记 |
| `06-Data/raw` | 原始数据，**只读** |
| `06-Data/processed` | 衍生数据 |
| `06-Data/metadata` | 数据字典与来源说明（模板：`Templates/dataset-card.md`） |
| `07-Code/{python,R,stata}` | 分析脚本 |
| `08-Research-Notes` | 研究笔记 |
| `09-Writing` | 论文与报告 |
| `10-Archive` | 已完成项目 |
| `Meta/` | `purpose`（方向）、`index`（目录）、`research-log`、`review-queue`、`source-registry`、研究规范 |
| `MOC/` | 主题索引 |

此外，库内原有的税法资料保持原位，不移动、不重命名、不批量改写；它们是本地资料，不等于现行有效法规。

## 硬性规则
1. `06-Data/raw` 与 `03-Literature/_sources` 不得修改或覆盖；衍生数据只写入 `06-Data/processed`。
2. 不删除文件；清理、移动、重命名需先征得明确同意。
3. 不虚构文献、作者、DOI、法条、数据或回归结果；无法核实的内容标注“未核实”。
4. 区分相关、预测与因果；先说明 estimand 与识别假设，再解释系数。
5. 每个实证结果须可追溯到脚本、数据版本、样本与模型设定；运行会写文件的脚本前，先说明输入与输出。
6. 税法结论须注明发文机关、文号、发布日期、生效日期、废止/修订状态与适用范围。
7. 含个人信息或受限数据的内容不得发送到外部服务。
8. 先读 `Meta/vault-map.md` 再假定路径；不要在 `.claude`、`_vendor`、`_erc-*`、`06-Data`、`07-Code` 中检索税法笔记。

## Skills（用 `/名称` 触发）
| 命令 | 用途 | 主要产出 |
|---|---|---|
| `/research-question` | 把主题收敛为可检验的研究问题与 estimand | ≤3 个候选问题、可行性评估、推荐一个 |
| `/literature-review` | 有来源的文献检索与综述 | 检索记录、文献矩阵、研究缺口、未核实清单 |
| `/theory-modeling` | 构建或审查理论模型与机制 | 设定、假设、逐步推导、比较静态、可检验推论 |
| `/tax-policy-analysis` | 税制、征管、遵从、归宿与中国税法制度 | 法源与有效性、机制、效率与分配、待官方确认项 |
| `/causal-inference-audit` | 审查 DID/IV/RDD 等识别策略 | estimand、假设、威胁、检验、可用的因果措辞 |
| `/econometric-analysis` | 数据审计、实现与复现计量分析 | 分析计划、代码、样本核算、日志 |
| `/academic-review` | 对稿件或设计做对抗式审稿 | Fatal / Major / Minor 分级意见 |
| `/ingest-source` | 摄入一个来源：先分析、确认后再写入 wiki | 文献笔记、index/日志/登记更新、矛盾进 review-queue |
| `/query-wiki` | 基于已积累的 wiki 回答问题 | 带引用的回答，可回存为笔记 |
| `/wiki-lint` | 知识库体检：断链、孤立页、溯源、矛盾、过时 | 错误/警告报告与下一步建议 |
| `/paper-outline` | 把冻结的研究产物变成论文架构：主张清单、章节计划、文献布局 | `paper/outline.md`（主张—证据—措辞强度） |
| `/paper-draft` | 依据大纲分节写作；只用引文表与结果登记簿 | `paper/draft.md`、主张—证据对照表 |
| `/paper-refine` | 评审—修改—接受/回退，最多 3 轮 | `paper/versions/`、`reviews.json`、`final.md` |
| `/research-pipeline` | 完整推进一个研究：分阶段、设关卡、Reviewer 质量闭环 | 阶段计划、项目状态 `PROJECT.md`、每阶段产出与决定记录 |

## Agents（由 Skill 或 pipeline 派出，也可点名调用）
| Agent | 职责 | 工具 |
|---|---|---|
| `literature-agent` | 检索、抽取、比较、综合文献 | Read, Grep, Glob, WebSearch, WebFetch |
| `theory-agent` | 模型设定与推导、比较静态 | Read, Grep, Glob, Write, Edit |
| `tax-policy-agent` | 税法、征管、遵从与归宿分析 | Read, Grep, Glob, WebSearch, WebFetch |
| `econometrics-agent` | 数据审计、估计实现与输出核对 | Read, Grep, Glob, Bash, Write, Edit |
| `causal-inference-agent` | 识别假设、威胁与稳健性设计 | Read, Grep, Glob, WebSearch, WebFetch, Write |
| `academic-reviewer` | 独立审查，不改稿 | Read, Grep, Glob, WebSearch, WebFetch |
| `paper-writer-agent` | 在隔离上下文中写作或修改论文的一部分 | Read, Write, Edit, Grep, Glob |

同时运行多个 Agent 前先说明数量；超过 3 个须经我同意。质量闭环：研究 Agent 提方案 → `econometrics-agent` 执行 → `academic-reviewer` 质疑 → Director 与我决定是否接受；有致命问题不得接受。

## 知识库维护（wiki 约定）
- 每次会话先读 `Meta/purpose.md`；内容为空或未填时提醒我填写，不要替我编造研究方向。
- 新增页面的 frontmatter：`type`（literature|theory|method|synthesis|query|research-project|dataset|analysis-plan|analysis-log）、`sources`（指向 `03-Literature/_sources` 或 DOI/URL）、`updated`、`verification`（verified|unverified）。
- 摄入一个来源会触及多个页面：先分析、我确认后再写；每次写入后更新 `Meta/index.md`，并在 `Meta/research-log.md` 追加 `## [日期] 类型 | 标题`。
- 来源之间的矛盾并列写出并记入 `Meta/review-queue.md`，不要擅自裁决。
- 有价值的回答经我同意后回存为笔记。定期运行 `/wiki-lint`。

## 汇报格式
重要改动或结论按：改了什么 / 为什么 / 如何验证 三段说明；无法验证的部分明确写出。

@.claude/ECONOMICS-RESEARCH.md
