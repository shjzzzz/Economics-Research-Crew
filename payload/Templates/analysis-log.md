---
type: analysis-log
project_id: ""
date: YYYY-MM-DD
updated: YYYY-MM-DD
software: ""
script: ""
git_commit: ""
---

# 实证分析日志（Analysis Log）

## 1. 输入数据与版本
- 原始数据路径（`06-Data/raw/...`，只读）与校验和：
- 衍生数据路径（`06-Data/processed/...`）：
- 软件与核心包版本（Stata / R / Python）：

## 2. 样本瀑布核算（Sample Waterfall）
| 步骤 | 筛选/合并操作 | 样本量 $N$ | 变化量 $\Delta N$ | 说明 |
|---|---|---|---|---|
| 0 | 原始读入 | | — | |
| 1 | 去重 / 主键核验 | | | |
| 2 | 合并与筛选 | | | |
| 最终 | 基准回归估计样本 | | | |

## 3. 执行命令与模型设定
- 运行命令：
- 基准设定、控制变量、固定效应、聚类层级：

## 4. 输出文件与结果登记簿（`Meta/results-ledger.json`）
- 导出结果表/CSV 路径：
- 已登记 `paper_tools.py results import/register` 前缀与关键 ID：
- 核心估计量与经济量级摘要（系数、标准误、$N$、占因变量均值/标准差比例）：

## 5. 诊断与稳健性结果
- 识别诊断（事件研究/预趋势与 HonestDiD、一阶段有效 F、密度检验、Bacon 分解等）：
- 异常与未通过项（如实记录，不得隐瞒）：

## 6. 对预设分析计划的偏离
- 无偏离 / 偏离明细及理由：

## 7. 复现步骤
1.
