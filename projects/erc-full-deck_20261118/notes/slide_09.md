第六个基础概念是 Hooks。前面讲的 CLAUDE.md 是“写给 AI 看的软约束”，而 Hooks 则是“由程序强制执行的硬拦截”。Claude Code 支持 33 种生命周期事件，配置在 settings.json 里，支持本地脚本等 5 种载体。最常用的是工具执行前的 PreToolUse 和执行后的 PostToolUse——比如在修改文件前拦住受保护路径，或在写入后自动格式化。
