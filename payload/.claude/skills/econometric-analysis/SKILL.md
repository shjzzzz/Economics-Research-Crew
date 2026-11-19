---
name: econometric-analysis
description: "Plan, implement, inspect, reproduce or audit an econometric analysis in Stata, R or Python with sample waterfall accounting and results-ledger registration. Use for 数据清洗、变量构造、描述统计、回归分析、基准回归、异质性分析、复现论文、代码审计、稳健性检验执行."
argument-hint: "[dataset, model or task]"
data_access_level: raw
task_type: open-ended
---

# Econometric Analysis（S5：可复现计量执行、代码审计与结果入簿）

## 1. 目标与边界
严格按冻结的分析计划在 Stata / R / Python 中执行数据审计、变量构造、模型估计、复现或代码审计，输出**完整样本瀑布、经济量级与可机读结果表**，并登记入 `Meta/results-ledger.json`。**绝不修改 `06-Data/raw`，绝不事后挑设定追显著性。**

## 2. 前置读取
- 读取 `06-Data/metadata/` 数据卡（若缺失先按 `Templates/dataset-card.md` 建卡）、项目 `analysis-plan.md`（若尚未冻结且涉及因果估计，提醒先走 `/causal-inference-audit`）。
- 核对 `07-Code/{stata,python,R}/` 既有脚本与环境版本。

## 3. 核心流程与委派规则
- **委派授权**：长脚本执行、大数据集清洗或系统代码审计可派出 `econometrics-agent`（按 `Templates/handoff.md` 交接，一次一个；仅该 Agent 具备 Bash 执行权限）。
### 3.1 标准实证执行模式
1. **原始数据审计（只读）**：核查观测粒度、唯一主键、重复行、缺失模式、时间/地区覆盖与异常值；严禁原地修改 `06-Data/raw/`。
2. **确认执行清单**：动代码前向研究者复核 $Y$、$D$、控制变量、固定效应、样本筛选、权重、聚类层级与输入/输出路径。
3. **模块化可复现实现**：在 `07-Code/<lang>/<project>/` 按步骤组织脚本（`01_clean` → `02_build` → `03_main` → `04_robustness` → `05_mechanisms`），衍生数据仅写入 `06-Data/processed/`；运行任何写文件脚本前先说明输入与输出。
4. **样本瀑布与诊断核验**：逐行记录原始 $N$ → 去重 → 合并（检查合并前后行数变化防多对多爆炸）→ 筛选 → 最终估计样本 $N$；核查系数符号与量纲、标准误、收敛状态与软件/包版本。
5. **计算经济量级并导出机读表**：同步计算因变量处理前均值/标准差、系数占均值/标准差比例或隐含弹性；将关键回归表导出为清晰 CSV。
6. **强制结果入簿（打通 S5 → S8/S10）**：使用 `python .claude/scripts/paper_tools.py results import <CSV> --prefix <项目.表号> --source <CSV路径> --script <脚本路径>` 或 `results register` 登记全部待引用核心数值、标准误与样本量。
7. **记录分析日志与偏离**：按 `Templates/analysis-log.md` 写入日志；任何偏离冻结分析计划的调整（含缩尾、控制变量或样本变更）必须逐条记录原因，明确区分“预设主分析”与“探索性补充”。

### 3.2 论文复现与代码审计模式
用于复现既有论文或审计已有实证代码：
1. 登记复现目标（论文、表/图号、原文报告估计值、标准误、$N$、软件）。
2. 定位数据与代码，明确缺失或受限部分，绝不静默替换数据。
3. 先原封不动运行原始代码并记录环境与包版本。
4. 逐格比对复现值与原文报告值（系数、SE、$N$），分级标注：`exact` / `within rounding` / `different`。
5. 差异归因（数据版本、样本筛选、聚类方式、包版本、编码 bug），先定位根因再修改。
6. 代码审计必查项：合并行数前后对比、重复键、样本过滤、变量定义是否与正文一致、聚类层级、硬编码数字。
7. 输出复现对照表与差异清单；**忠实复现完成后再做稳健性拓展**。

## 4. 产出与知识回流
- 产出：模块化代码（`07-Code/`）、衍生数据（`06-Data/processed/`）、数据卡（`06-Data/metadata/`）、分析日志（`analysis-log.md`）、机读结果 CSV 及更新后的 `Meta/results-ledger.json`。
- 下游交接：仅把产物路径（不含作者辩护推理）交给 S6 `/academic-review`。

## 5. 硬性禁止
严禁写入/覆盖 `06-Data/raw`；严禁未告知输入输出即运行写文件脚本；严禁静默删样本、未记录缩尾或以追逐显著性为目的更改设定；不得把“代码跑通”等同于“因果识别成立”。
