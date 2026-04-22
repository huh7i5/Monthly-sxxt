# 📝 研究生月报生成器 (Monthly Report Generator)

一个 Claude Agent Skill，用于自动生成研究生月度工作月报。

## 功能

- 🎯 **输入实验结果，自动生成月报** — 只需提供本月的实验数据、代码进展等原始素材
- 📊 **固定格式输出** — 按学校/课题组标准格式：封面、进度表、摘要、主进展、下月计划、导师意见、文献阅读
- 🔢 **量化优先** — 自动将定性描述转化为定量数据（F1 分数、误差率等）
- 🧠 **智能推断** — 基于本月进展自动推断下月计划和上月回顾
- 📄 **多格式输出** — 支持 Markdown 和 DOCX (via pandoc)

## 月报结构

生成的月报包含以下固定结构（参照真实月报模板）：

```
封面：姓名——工作月报 / 研究方向 / 年月

┌─────────────────────────────────────────┐
│ 工作进度一览表（上月 vs 本月对比）        │
├─────────────────────────────────────────┤
│ 1. 摘要                                 │
│ 2. 本月主进展                            │
│    2.1 方向一                            │
│      2.1.1 子课题A                       │
│      2.1.2 子课题B                       │
│    2.2 方向二                            │
│      2.2.1 子课题C                       │
│ 3. 下月工作计划                           │
│ 4. 导师意见（留空）                       │
│ 5. 文献阅读情况                           │
│    5.1 文献阅读目录                       │
│    5.2 重点文献笔记                       │
└─────────────────────────────────────────┘
```

## 快速开始

### 在 Claude.ai 中使用

1. 将 `monthly-report-generator` 文件夹压缩为 ZIP
2. 上传到 [Claude > Customize > Skills](https://claude.ai/customize/skills)
3. 在对话中直接说："帮我写本月月报"，然后粘贴实验结果

### 在 Claude Code 中使用

```bash
cp -r monthly-report-generator /path/to/project/.claude/skills/
```

### 示例对话

**你：**
> 帮我生成 4 月月报，本月做的事：
> 1. Module 2 验证了 Gu (2021) 论文，L1 LCOM = 3498，误差 0.00%
> 2. 实现了 Tool Registry，支持 3 种方法论自动切换
> 3. 读了 Zimmermann (2020) TEA Harmonization 指南

**Claude：** *(自动生成完整 5 章节月报)*

## 自定义模板

### 修改章节结构
编辑 `templates/report_template.md` — 调整月报的章节和占位符

### 修改写作风格
编辑 `templates/style_guide.md` — 调整语气、措辞和格式规范

### 生成 DOCX
```bash
python scripts/generate_report.py -i report.md --docx
```

## 文件结构

```
monthly-report-generator/
├── SKILL.md                     # Skill 主文件（元数据 + 完整生成指令）
├── README.md                    # 本文件
├── templates/
│   ├── report_template.md       # 月报结构模板（可自定义）
│   └── style_guide.md           # 写作风格指南
└── scripts/
    └── generate_report.py       # Markdown → DOCX 转换辅助脚本
```

## 许可

Apache 2.0
