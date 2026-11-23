---
name: theory-modeling
description: "Build or audit a formal economic model, competing mechanisms, comparative statics, reduced-form mapping and testable hypotheses. Use for 理论模型、建模、机制分析、均衡推导、比较静态、博弈模型、委托代理、研究假说."
argument-hint: "[mechanism or research question]"
data_access_level: verified_only
task_type: open-ended
---

# Theory Modeling（S3：形式化建模、竞争机制与简化式映射）

## 1. 目标与边界
把经济直觉与行为/制度机制转化为严谨的形式化模型，推导出**可区分竞争性机制的排他性可检验假说**，并明确理论比较静态如何映射到实证回归系数。**不写装饰性数学方程，不允许无推导的命题。**

## 2. 前置读取（规划前 Pre-RAG）
- 读取 `Meta/purpose.md`、`Meta/constraints.md`（研究者纠正，必须遵守）、`Meta/link-map.md`（枢纽页）、`Meta/mechanism-library.md`（公共经济学 × 行为经济学机制起点，注意参考文献均标“待核实”，不得直接引用）与 `04-Theories/` 既有笔记。
- 若属于项目 S3：读取 `01-Research-Projects/<项目>/PROJECT.md` 及 S2 文献缺口、S3 制度/税法事实。

## 3. 核心流程与苏格拉底防越位护栏
- **探索态护栏**：当研究者尚未确定核心机制时，只追问行为主体、目标函数、信息结构、约束条件与制度摩擦，不替研究者拍板核心假说；若明确要求 AI 拟定机制候选，先显式输出 `[SOCRATIC-NON-GENERATION-EXIT: explicit_user_request]` 并标注为 AI 建议。
- **写作结构**：模型一节的段落顺序与"偏离环节"清单见 `Templates/intro-model-blueprint.md`。
- **委派授权**：复杂优化与逐步推导可派出 `theory-agent`（按 `Templates/handoff.md` 交接，一次一个）。
1. **界定环境与要素**：参与人（纳税人/企业/平台/税务机关等）、决策变量、时序（Timing）、信息结构（对称/不对称/有限注意）、预算与制度约束。
2. **引入行为或制度摩擦**：若使用 `Meta/mechanism-library.md` 中的行为机制（如凸显性、损失厌恶、现时偏向、第三方信息、遵从成本），须明确其数学表征与标准理性基准模型的差异。
3. **逐步推导最优解与均衡**：写出目标函数、一阶/二阶条件、角点解与边界条件；检查符号、量纲与定义域；对不确定的代数步骤显式标出，不跳步。
4. **比较静态与经济学直觉**：推导核心外生政策参数 $\tau$ 变动对关键决策变量的偏导（如 $\partial y^* / \partial \tau$），拆解替代效应、收入效应、威慑/可见度效应等渠道，并用清晰经济语言解释直觉。
5. **竞争性机制与排他性推论**：至少对照 1 个竞争机制，明确列出**二者在数据中会产生何种相反或可区分的观测后果**（异质性方向、中介变量反应或聚束形态），避免只能讲“与某机制一致”的不可证伪故事。
6. **简化式映射（Theory → Empirical Bridge）**：说明理论比较静态如何对应到 S4/S5 的待估系数 $\beta$，哪些不可观测结构参数会进入残差项，以及何种强假设或制度不现实假设会改变结论符号。

## 4. 产出与知识回流
- 输出：模型设定、假设表、逐步推导、比较静态、竞争机制排他推论表、简化式映射与强假设清单。
- 跨项目可复用的机制模型写入 `04-Theories/`（frontmatter 含 `type: theory`、`sources`、`updated`、`verification`），更新 `Meta/index.md` 与 `Meta/log.md`；项目专属假说同步写入 `PROJECT.md`。

## 5. 硬性禁止
禁止无推导直接宣布 Proposition；禁止装饰性方程（实证完全用不到的符号堆砌）；禁止凭记忆为机制库补写未核实引文。
