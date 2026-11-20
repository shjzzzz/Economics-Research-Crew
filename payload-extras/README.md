# payload-extras（可选扩展）

`Install-EconomicsResearchCrew.ps1 -WithExtras` 会把本目录的 `skills/`、`agents/` 装进研究库（只新增，不覆盖，不配置任何 MCP）。

两个 MIT 许可的绘图 Skill（`scientific-visualization`、`thu-digitizer`）已转入必装目录 `payload/.claude/skills/`；`publication-chart-skill`、`econ-visualization`、`copyplot`、`tikz` 因上游未附许可证，仍留在本目录，仅供本机自用。

本目录保留用于用户本机自用的额外第三方扩展（不随公开仓库分发）；这些文件未经本项目安全审计，使用规则见研究库 `Meta/extras/INDEX.md`。
