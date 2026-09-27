# gewenxing-vacuum-gravity

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22994259.svg)](https://doi.org/10.5281/zenodo.22994259)



Agent 技能，由葛文星（Ge Wenxing）的原创论文《关于原子核内中子、质子振动性与引力常数的关联性猜测》（真空 0 压层引力假说 / 波源理论）经 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 生成。


本技能忠实提取论文的理论结构、核心公式与可证伪预测，供 Agent Skills 兼容的主机加载使用。内容为**对论文的提炼与结构整理，非论文原文**。


## 安装


在任意 Agent Skills 兼容主机上安装：


```bash
npx skills add https://github.com/DULI756/gewenxing-vacuum-gravity --skill gewenxing-vacuum-gravity
```


## 文件清单


```
SKILL.md          — 核心框架 + 章节/主题索引（公式已由作者补齐，LaTeX 完整录入）
chapters/         — 7 个章节摘要（ch01–ch07）
glossary.md       — 关键术语定义
patterns.md       — 推导与技术模式
cheatsheet.md     — 决策速查表
```


## 使用


- 问 `gewenxing-vacuum-gravity` → 加载核心框架
- 问 `gewenxing-vacuum-gravity 关于 <主题>` → 定位并解释相关章节
- 问 `gewenxing-vacuum-gravity 的 ch03` → 深入某一章节


## 说明


- 本技能是对作者原创论文的提炼，**不构成对理论真伪的判定或认可**。
- 论文中的公式已由作者本人逐条补充并以 LaTeX 形式完整录入。
- 源文档为作者自有论文，作者已授权公开发布本仓库。

