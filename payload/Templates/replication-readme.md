---
type: template
---
# 复现包 README · <论文题目>

> 本文件随复现包提供。四个带 * 的节为必备项，`paper_tools.py package check` 会逐一核对。

## 数据可得性 *（Data availability）
| 数据 | 来源 / 机构 | 能否公开 | 获取方式（申请途径、周期、费用） | 复现包内位置 |
|---|---|---|---|---|
| | | 是 / 否（保密） | | `data/…` 或“不含，见左栏” |

保密数据说明：<为何不能公开；替代方案，如模拟数据或可公开的子样本>

## 计算环境 *（Computational requirements）
- 软件与版本：<Stata 18 / R 4.4 / Python 3.12>；用到的包及版本：<reghdfe 6.12 …>
- 硬件：<CPU / 内存>；预计完整运行时长：<…>

## 运行说明 *（Instructions）
1. 把复现包根目录设为工作目录。
2. 运行 `main.do`（或 `run_all.R` / `main.py` / `make`）；它按顺序调用 `code/` 下全部脚本，输出写入 `output/`。
3. 无需修改任何路径。

## 表图对照 *（Tables and figures）
| 表 / 图 | 生成脚本 | 输出文件 | 备注（预设 / 探索性） |
|---|---|---|---|
| 表 1 | `code/03_main.do` | `output/table1.csv` | 预设 |

## 引用与许可
<数据与代码的引用方式、许可证>
