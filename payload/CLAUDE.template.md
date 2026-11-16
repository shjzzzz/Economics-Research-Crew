# TaxWiki Research Workspace

税收经济学、公共经济学、计量经济学与因果推断的研究工作区。本目录同时是 Obsidian Vault 与 Claude Code 项目根目录。

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
| `04-Theories` | 理论与机制笔记 |
| `05-Methods` | 计量与识别方法笔记 |
| `06-Data/raw` | 原始数据，**只读** |
| `06-Data/processed` | 衍生数据 |
| `06-Data/metadata` | 数据字典与来源说明（模板：`Templates/dataset-card.md`） |
| `07-Code/{python,R,stata}` | 分析脚本 |
| `08-Research-Notes` | 研究笔记 |
| `09-Writing` | 论文与报告 |
| `10-Archive` | 已完成项目 |
| `Meta/` | 研究规范、来源登记、研究日志 |
| `MOC/` | 主题索引 |

此外，根目录下原有的 TaxWiki 税法资料保持原位，不移动、不重命名、不批量改写；它们是本地资料，不等于现行有效法规。

## 硬性规则
1. `06-Data/raw` 不得修改或覆盖；衍生数据只写入 `06-Data/processed`。
2. 不删除文件；清理、移动、重命名需先征得明确同意。
3. 不虚构文献、作者、DOI、法条、数据或回归结果；无法核实的内容标注“未核实”。
4. 区分相关、预测与因果；先说明 estimand 与识别假设，再解释系数。
5. 每个实证结果须可追溯到脚本、数据版本、样本与模型设定；运行会写文件的脚本前，先说明输入与输出。
6. 税法结论须注明发文机关、文号、发布日期、生效日期、废止/修订状态与适用范围。
7. 含个人信息或受限数据的内容不得发送到外部服务。
8. 先读 `Meta/vault-map.md` 再假定路径；不要在 `.claude`、`_vendor`、`_erc-*`、`06-Data`、`07-Code` 中检索税法笔记。

## 常用命令
`/research-question` `/literature-review` `/theory-modeling` `/tax-policy-analysis` `/causal-inference-audit` `/econometric-analysis` `/academic-review`

## 汇报格式
重要改动或结论按：改了什么 / 为什么 / 如何验证 三段说明；无法验证的部分明确写出。

@.claude/ECONOMICS-RESEARCH.md
