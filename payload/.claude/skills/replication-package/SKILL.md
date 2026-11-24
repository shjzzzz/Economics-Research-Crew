---
name: replication-package
description: "Assemble and audit the replication package of an economics paper before submission (S12): README with data availability, computational requirements, run instructions and a table/figure-to-script map; one master script; every registered result reproducible from the package; honest statements for confidential data; double-blind clean-up of hidden characters and Office author metadata. Use for 复现包、复现材料、replication package、数据与代码可得性声明、投稿前打包、双盲清理."
argument-hint: "[project folder, optional: target journal policy]"
data_access_level: verified_only
task_type: open-ended
---

# Replication Package（S12：复现包组装与审计）

## 1. 目标与边界
把 S5 的代码、S5 的两本账（`Meta/results-ledger.json`、`Meta/spec-ledger.json`）与终稿连成一个**他人拿到即可重现全部表图**的复现包，放在 `01-Research-Projects/<项目>/replication/`。本 Skill 只组装与审计，**不改分析、不改稿件数字**；发现结果无法重现时退回 S5。
- **不运行来路不明的代码**：审计外来复现包时只读，不执行其中脚本、不安装其依赖。
- **保密数据**（如税务微观数据）不得放入复现包；改为在 README 写明获取途径、申请机构、审批周期与费用，并给出可公开的模拟数据或代码路径。不得假装数据可公开。

## 2. 前置读取
- 项目 `analysis-log.md`、`07-Code/<lang>/<项目>/`、`06-Data/metadata/` 数据卡、`paper/final.md`。
- `python .claude/scripts/paper_tools.py spec summary` 与 `paper_tools.py report` 的输出。
- 目标期刊若有专门的数据与代码政策，以研究者提供的政策文本为准；未提供则按本节清单执行，并用 `⟦问：…⟧` 询问是否有期刊专门要求。

## 3. 核心流程
1. **建目录**：`replication/` 下按 `code/`、`data/`（只放可公开数据）、`output/` 组织；从 `07-Code/` 复制（不移动）终版脚本。
2. **主脚本**：写一个一键运行的 `main.do` / `run_all.R` / `main.py` / `Makefile`，按 `01_clean` → … → 出表顺序调用全部脚本；路径一律相对复现包根目录。
3. **README**：按 `Templates/replication-readme.md` 填写四个必备节——数据可得性、计算环境（软件与包版本、硬件、预计运行时长）、运行说明、表图对照（每张表/图 → 生成它的脚本与输出文件）。
4. **账本对账**：终稿引用的每个 `{{res:id}}` 都应能追到复现包内的脚本；`spec summary` 中“已报告”的规格须出现在表图对照中，非预设规格在 README 中注明为探索性。
5. **机械审计**：运行 `python .claude/scripts/paper_tools.py package check 01-Research-Projects/<项目>/replication`。错误（缺 README、缺必备节、缺主脚本）必须清零；警告逐条处理或在 README 中说明理由。
6. **双盲清理（仅在研究者确认要匿名投稿时）**：`package check … --fix` 删除零宽/双向控制等隐藏字符并清空 docx/pptx/xlsx 的作者元数据；README 与代码注释中的作者姓名、单位、致谢另行人工检查。
7. **关卡**：S12 的 `package_ready` 检查即上述错误清零；通过后把复现包路径登记为 S12 产物（`orchestrator.py artifact`）。

## 4. 产出与知识回流
- `replication/`（README、主脚本、代码、可公开数据、输出）+ `package check` 原样输出。
- 复现包中可复用的数据获取经验写回对应数据卡（`06-Data/metadata/`），供下一个项目检索。

## 5. 硬性禁止与致谢
- 禁止把保密或受许可限制的数据放入复现包；禁止为通过检查而删改结果或伪造运行时长；禁止执行外来复现包中的代码；禁止在研究者未确认匿名投稿时清除作者信息。
- 致谢（思路借鉴、原生重写、未复制文本）：`brycewang-stanford/Auto-Empirical-Research-Skills`（CC BY-SA 4.0）中复现包审计与“README 四节”的设计。
