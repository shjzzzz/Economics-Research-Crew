<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 对 AI 辅助经济学研究工作流感兴趣的学者、研究生、研究团队成员或技术同行
- objective: 系统讲解 Economics Research Crew 的设计动机、核心架构与各关键模块概念，使听众清晰区分各组件并了解落地方式
- core_message: Economics Research Crew 不是计量软件，而是一套面向经济学与因果推断研究的 AI 协作规范与工程约束体系：让研究流程可追溯、可审查、可积累
- consumption_mode: balanced

## mode
- mode: custom
- mode_references: instructional, pyramid
- mode_behavior: 先用 pyramid 结论先行建立项目整体定位与四层架构认知，再以 instructional 循序拆解 8 个核心概念，每页聚焦“是什么、解决什么痛点、如何运作”。

## visual_style
- visual_style: custom
- visual_style_references: swiss-minimal, editorial
- visual_style_behavior: 以 swiss-minimal 精确栅格、大留白与直角几何区块为主骨架，辅以 editorial 的细规则分隔线、序号徽标与证据对照层级；严格扁平无阴影。

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
- inventory: tabler-outline/shield-check, tabler-outline/terminal-2, tabler-outline/users, tabler-outline/git-branch, tabler-outline/lock, tabler-outline/database, tabler-outline/file-text, tabler-outline/devices, tabler-outline/alert-triangle, tabler-outline/search, tabler-outline/code, tabler-outline/scale

## page_rhythm
- P01: anchor
- P02: dense
- P03: dense
- P04: dense
- P05: dense
- P06: dense
- P07: dense
- P08: dense
- P09: dense
- P10: dense
- P11: dense
- P12: breathing

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
