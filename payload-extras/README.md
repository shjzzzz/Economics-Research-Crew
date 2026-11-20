# payload-extras（可选扩展）

`Install-EconomicsResearchCrew.ps1 -WithExtras` 会把本目录的 `skills/`、`agents/` 装进研究库（只新增，不覆盖，不配置任何 MCP）。

原精选的 6 个学术绘图与制表 Skill（`publication-chart-skill`、`econ-visualization`、`scientific-visualization`、`copyplot`、`thu-digitizer`、`tikz`）已转入必装目录 `payload/.claude/skills/`，默认随核心框架一起安装。

本目录保留用于用户本机自用的额外第三方扩展（不随公开仓库分发）；这些文件未经本项目安全审计，使用规则见研究库 `Meta/extras/INDEX.md`。
