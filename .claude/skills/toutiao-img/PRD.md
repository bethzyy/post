# Toutiao Img Skill - PRD 文档

## 文档信息

| 属性 | 值 |
|------|-----|
| **名称** | toutiao-img |
| **版本** | v3.0.0 |
| **状态** | ✅ 已实现 |
| **入口文件** | main.py |
| **技术栈** | Python + Selenium + GLM-4-flash + image-gen skill |
| **最后更新** | 2026-03-24 |

---

## 1. 产品概述

### 1.1 产品定位

Toutiao Img 是一个头条文章配图生成工具，自动分析文章内容并生成上下文相关的配图，同时支持表格转图像功能。

### 1.2 核心价值

- **上下文感知**: 分析文章内容生成相关图像提示词
- **表格转图像**: 自动将 HTML 表格转为图片（解决头条表格显示问题）
- **智能重用**: 检测已有图片，避免重复生成
- **语义命名**: 按位置命名（insertion_point_1.jpg）

### 1.3 触发模式

```
"add images to article", "generate article illustrations",
"create 配图", "add article pictures"
```

---

## 2. 功能需求

### F1: 配图生成

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `html_file_path` | string | 必需 | 文章 HTML 文件路径 |
| `style` | string | realistic | 图像风格 |
| `count` | int | 3 | 生成图片数量 |

### F2: 上下文感知提示词

**两阶段 AI 分析**:
1. **内容分析**: 使用 GLM-4-flash 分析文章
   - 提取主题、关键概念
   - 识别视觉机会
2. **提示词生成**: 生成具体英文提示词

### F3: 表格转图像

| 配置 | 值 |
|------|-----|
| 宽度 | 600px（固定） |
| 字体 | 24px |
| 内边距 | 8px |
| 表头背景 | #0e639c（蓝色） |

### F4: 图片重用机制

- **3+ 图片存在**: 全部重用，跳过 AI 生成
- **1-2 图片存在**: 重用已有，仅生成缺失
- **0 图片存在**: 全部生成

---

## 3. 技术架构

### 3.1 模块结构

```
.claude/skills/toutiao-img/
├── main.py                    # CLI 入口
├── scripts/
│   ├── article_illustrator.py # 配图逻辑
│   └── table_converter.py     # 表格转图像
└── requirements.txt
```

### 3.2 工作流程

```
1. 分析文章内容（GLM-4-flash）
2. 生成上下文感知提示词
3. 检查已有图片（智能重用）
4. 调用 image-gen skill 生成图片
5. 插入图片到 HTML
6. 转换表格为图像
7. 输出带图片的 HTML
```

### 3.3 依赖

- **必需**: `image-gen` skill (v2.0.0+)
- **环境**: `ZHIPU_API_KEY`
- **可选**: Chrome/Selenium（表格转换）

---

## 4. 使用示例

### 4.1 基础使用

```bash
python .claude/skills/toutiao-img/main.py article.html
```

### 4.2 指定风格和数量

```bash
python .claude/skills/toutiao-img/main.py article.html artistic 5
```

### 4.3 实际案例

```bash
python .claude/skills/toutiao-img/main.py \
  "post/article/他山之石/Claude-Code原生Agent完全指南-头条版.html" \
  realistic 3
```

---

## 5. 输出文件

| 文件 | 路径 | 描述 |
|------|------|------|
| HTML | `{original_name}-images.html` | 带图片的文章 |
| 图片 | `images/<document_name>/` | 生成的图片 |
| 命名 | `insertion_point_N.jpg` | 按位置命名 |

---

## 6. 性能指标

| 指标 | 值 |
|------|-----|
| 处理时间 | ~45 秒（3 张图片） |
| 图片大小 | 150-220 KB |
| 测试文章 | 13,260 字符 |

---

## 7. 依赖项

```
selenium
beautifulsoup4
zhipuai
pillow
```

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.0.0 | 2026-03-08 | 迁移到 Anthropic 官方标准架构 |
| v2.1.5 | 2026-03-04 | 语义化图片命名 |
| v2.1.4 | 2026-03-04 | 图片重用优化 |
| v2.1.3 | 2026-03-04 | 优化表格样式 |
| v2.1.0 | 2026-03-04 | 表格转图像 + 上下文感知提示词 |

---

## 9. 相关文件

- **SKILL.md**: `.claude/skills/toutiao-img/SKILL.md`
- **主入口**: `.claude/skills/toutiao-img/main.py`
- **配图模块**: `.claude/skills/toutiao-img/scripts/article_illustrator.py`
- **表格转换**: `.claude/skills/toutiao-img/scripts/table_converter.py`
