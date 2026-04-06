# Toutiao Cnt Skill - PRD 文档

## 文档信息

| 属性 | 值 |
|------|-----|
| **名称** | article-gen |
| **版本** | v5.3.0 |
| **状态** | ✅ 已实现 |
| **入口文件** | main.py |
| **技术栈** | Python + ZhipuAI GLM + BeautifulSoup |
| **最后更新** | 2026-03-24 |

---

## 1. 产品概述

### 1.1 产品定位

Toutiao Cnt 是一个今日头条文章创作工具，支持从主题生成文章和智能内容整合。基于事实生成，杜绝 AI 编造。

### 1.2 核心价值

- **事实导向**: 严格基于事实材料生成，不编造
- **详细程度控制**: 支持 simple/medium/detailed 三种模式
- **内容整合**: 智能合并新内容到现有文章
- **格式规范**: 自动生成头条兼容的 HTML 格式

### 1.3 触发模式

```
"create article", "generate article", "write article about [topic]",
"生成一篇头条文章", "写一篇头条文章", "创作一篇头条文章",
"把 [内容] 写成头条文章", "把 [文件] 转换成头条文章"
```

---

## 2. 功能需求

### F1: 文章创作 (create)

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `topic` | string | 必需 | 文章主题 |
| `--detail` | choice | detailed | 详细程度: simple/medium/detailed |
| `--content` | string | - | 用户提供的专业内容 |
| `--strict` | flag | False | 严格模式：无事实材料则拒绝 |
| `--output-dir` | string | 当前目录 | 输出目录 |
| `--style` | string | - | 写作风格 |

### F2: 详细程度

| 模式 | 字数 | 章节数 | 适用场景 |
|------|------|--------|----------|
| `simple` | 300-600 | 2-3 | 快速阅读，核心要点 |
| `medium` | 500-2000 | 2-4 | 适中长度 |
| `detailed` | 1500-3500 | 4-6 | 深度分析（默认） |

### F3: 内容整合 (integrate)

| 参数 | 类型 | 描述 |
|------|------|------|
| `html_file` | string | 现有 HTML 文章路径 |
| `content` | string | 新内容（文本/Markdown/HTML） |
| `--position` | choice | after/before/end |
| `--merge` | flag | 智能合并，跳过重复章节 |

### F4: 事实导向机制

- **`--content` 参数**: 支持传入用户已有专业内容
- **`--strict` 参数**: 无事实材料则拒绝生成
- **自适应字数**: 根据事实材料量自动调整
- **信息来源标注**: 文章末尾自动添加"参考来源"

---

## 3. 技术架构

### 3.1 模块结构

```
.claude/skills/article-gen/
├── main.py                    # CLI 入口
├── scripts/
│   ├── article_creator.py     # 文章创作
│   └── integrate_content.py   # 内容整合
└── requirements.txt
```

### 3.2 HTML 模板

标准 CSS 模板包含：
- 响应式布局（max-width: 750px）
- 标题样式（H1-H4）
- Banner 样式（intro-box, warning-banner 等）
- 表格样式
- ASCII 图表样式（.diagram）

---

## 4. 使用示例

### 4.1 基础文章创作

```bash
python .claude/skills/article-gen/main.py create "元宵节风俗"
```

### 4.2 使用用户内容

```bash
python .claude/skills/article-gen/main.py create "Claude Code Agent 使用指南" \
    --content "post/article/他山之石/Claude-Code原生Agent完全指南-头条版.html"
```

### 4.3 详细程度控制

```bash
# 简洁版
python .claude/skills/article-gen/main.py create "Selenium vs Playwright" --detail simple

# 深度版（默认）
python .claude/skills/article-gen/main.py create "Selenium vs Playwright" --detail detailed
```

### 4.4 严格模式

```bash
# 无事实材料会失败
python .claude/skills/article-gen/main.py create "不存在的主题" --strict

# 有用户内容会成功
python .claude/skills/article-gen/main.py create "自定义主题" \
    --content "专业内容..." --strict
```

### 4.5 内容整合

```bash
python .claude/skills/article-gen/main.py integrate article.html content.md --merge
```

---

## 5. 输出文件

- **命名**: `Article_{title}_{timestamp}.html`
- **格式**: 头条兼容 HTML
- **位置**: 指定输出目录或当前目录

---

## 6. 依赖项

```
beautifulsoup4>=4.12.0
zhipuai>=0.1.0
requests
```

---

## 7. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.3.0 | 2026-03-XX | 添加 `--detail` 详细程度参数 |
| v5.2.0 | 2026-03-XX | 日期准确性增强 |
| v5.1.0 | 2026-03-XX | 明确"适当扩展"边界 |
| v5.0.0 | 2026-03-XX | 基于事实生成，杜绝编造 |
| v4.0.0 | 2026-03-08 | 迁移到 Anthropic 官方标准架构 |

---

## 8. 相关文件

- **SKILL.md**: `.claude/skills/article-gen/SKILL.md`
- **主入口**: `.claude/skills/article-gen/main.py`
- **创作模块**: `.claude/skills/article-gen/scripts/article_creator.py`
- **整合模块**: `.claude/skills/article-gen/scripts/integrate_content.py`
