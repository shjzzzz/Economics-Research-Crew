<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 对 AI 辅助科研与 Claude Code 工程实践感兴趣的学者、研究生、研究团队与技术同行
- objective: 先系统讲清 Claude Code 的 8 大基础概念，再展示 Economics Research Crew 如何将它们组合成严谨的经济学研究护栏
- core_message: 理解底层原语（CLAUDE.md/Skills/MCP/Hooks/Subagents/Worktree/Plugins），才能真正用好面向经济学研究的工程化协作体系
- consumption_mode: balanced

## mode
- mode: custom
- mode_references: instructional, pyramid
- mode_behavior: 双部结构：Part 1 以 instructional 逐一讲透 8 个 Claude Code 基础概念；Part 2 以 pyramid + instructional 展示这些概念如何在 Economics Research Crew 中落地为科研护栏。

## visual_style
- visual_style: custom
- visual_style_references: swiss-minimal, editorial
- visual_style_behavior: 以 swiss-minimal 精确栅格、大留白与直角几何区块为主骨架，辅以 editorial 的细规则分隔线、序号徽标与对比层级；严格扁平无阴影。

## colors
- background: #FFFFFF
- secondary_bg: #F4F6F8
- primary: #1A3A6B
- accent: #E8A317
- secondary_accent: #4A7BB5
- body_text: #1D2430
- secondary_text: #5A6577
- divider: #DCE2EA

## typography
- font_family: 'Microsoft YaHei', Arial, sans-serif
- title_family: 'Microsoft YaHei', Arial, sans-serif
- body_family: 'Microsoft YaHei', Arial, sans-serif
- body: 24
- title: 40
- section_title: 36
- subtitle: 22
- card_title: 19
- annotation: 16
- code: 13

## icons
- library: tabler-outline
- stroke_width: 2
- inventory: tabler-outline/shield-check, tabler-outline/terminal-2, tabler-outline/users, tabler-outline/git-branch, tabler-outline/lock, tabler-outline/database, tabler-outline/file-text, tabler-outline/devices, tabler-outline/alert-triangle, tabler-outline/search, tabler-outline/code, tabler-outline/scale, tabler-outline/plug, tabler-outline/package

## page_rhythm
- P01: anchor
- P02: breathing
- P03: dense
- P04: dense
- P05: dense
- P06: dense
- P07: dense
- P08: dense
- P09: dense
- P10: dense
- P11: dense
- P12: dense
- P13: dense
- P14: dense
- P15: dense
- P16: dense
- P17: dense
- P18: breathing

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
