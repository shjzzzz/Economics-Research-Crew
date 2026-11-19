# payload-extras（可选扩展）

`Install-EconomicsResearchCrew.ps1 -WithExtras` 会把本目录的 `skills/`、`agents/` 装进研究库（只新增，不覆盖，不配置任何 MCP）。

公开仓库里只包含**上游带宽松许可证（MIT）**的扩展，保留其 LICENSE 与版权声明：

| 目录 | 上游 | 许可证 |
|---|---|---|
| `skills/neishengxing-main` | 汇编库 `franklee16/academic-research-skills` 的 `data-analysis/neishengxing-main`（作者 Yichao Li） | MIT |
| `skills/thu-digitizer-main` | 同一汇编库的 `visualization/thu-digitizer-main`（作者 Rimagination） | MIT |

其余第三方 Skill（数据获取、Stata/R/Python 分析、CNKI 等）上游未附许可证或使用非商用许可，不在公开仓库中发布；作者本人在本机和研究库中自用。
这些文件未经本项目安全审计；使用规则（核心 Skill 优先、不改 raw、不外发受限数据、文献先进引文表）见研究库 `Meta/extras/INDEX.md`。
