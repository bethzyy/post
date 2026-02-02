---
name: html-document-generator
description: 使用MCP服务器生成带标注的HTML文档，支持Wikipedia知识源、SQLite数据管理和Filesystem文件操作
metadata:
  tags: html, mcp, document-generation, wikipedia, sqlite, filesystem
  version: 1.0.0
  author: MCP Test System
  created: 2026-02-01
---

## When to use

使用此技能 whenever you need to:

1. 生成**带MCP标注的HTML文档**
2. 集成**多个MCP服务器**完成文档生成任务
3. 展示**AI Agent的能力扩展**
4. 创建**可追溯的内容来源**的文档
5. 生成**美观的响应式HTML文章**

典型应用场景：
- 📝 技术博客文章
- 📚 知识库文档
- 📊 测试报告
- 🎓 学术论文草稿
- 📖 在线教程

## How to use

### 核心概念

此技能展示了如何**协调三个MCP服务器**生成高质量HTML文档：

```
Wikipedia MCP (知识源)
    ↓ 提供权威定义
SQLite MCP (数据层)
    ↓ 结构化存储
Filesystem MCP (输出层)
    ↓ HTML生成
完整文档 (带MCP标注)
```

### MCP服务器角色

#### 1️⃣ Wikipedia MCP - 知识源
**职责**: 提供权威的背景知识和术语定义

**典型用途**:
- 查询技术术语的准确定义
- 获取历史事件和人物信息
- 查找科学概念的解释
- 提供可引用的权威来源

**数据结构**:
```python
wiki_data = {
    "title": "术语名称",
    "summary": "简要描述",
    "url": "Wikipedia链接"
}
```

#### 2️⃣ SQLite MCP - 数据管理
**职责**: 结构化数据存储和关系映射

**典型用途**:
- 存储文章元数据
- 管理引用文献
- 维护内容版本
- 实现关系映射

**数据库模式**:
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE refs (
    id INTEGER PRIMARY KEY,
    article_id INTEGER,
    source_name TEXT,
    url TEXT,
    FOREIGN KEY (article_id) REFERENCES articles(id)
);
```

#### 3️⃣ Filesystem MCP - 文档生成
**职责**: 生成HTML文档，处理样式和布局

**典型用途**:
- 创建HTML文件
- 应用CSS样式
- 实现响应式布局
- 添加MCP标注

### MCP标注系统

**颜色编码方案**:

| MCP服务器 | 颜色 | CSS类名 | 用途 |
|-----------|------|---------|------|
| Wikipedia | 🔵 蓝色 | `.mcp-wikipedia` | 知识来源 |
| SQLite | 🟣 紫色 | `.mcp-sqlite` | 数据管理 |
| Filesystem | 🟢 绿色 | `.mcp-filesystem` | 内容生成 |

**HTML实现**:
```html
<div class="mcp-section mcp-section-wikipedia">
    <div class="mcp-label mcp-wikipedia">Wikipedia MCP - 知识来源</div>
    <h2>章节标题</h2>
    <p>内容...</p>
</div>
```

**CSS样式**:
```css
.mcp-section-wikipedia {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    border-left: 5px solid #1976d2;
}

.mcp-wikipedia {
    background: #e3f2fd;
    color: #1976d2;
    border: 2px solid #1976d2;
}
```

### 实现步骤

#### Step 1: 创建数据库结构
```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT,
        created_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS refs (
        id INTEGER PRIMARY KEY,
        article_id INTEGER,
        source_name TEXT,
        url TEXT
    )
''')
```

#### Step 2: 查询Wikipedia知识
```python
# 模拟Wikipedia查询结果
wiki_data = [
    {
        "title": "Artificial Intelligence",
        "summary": "人工智能是指由机器展现的智能",
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
    }
    # ... 更多条目
]
```

#### Step 3: 生成HTML内容
```python
html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        /* CSS样式 */
    </style>
</head>
<body>
    <div class="container">
        <!-- 内容区域 -->
    </div>
</body>
</html>
"""
```

#### Step 4: 添加MCP标注
```python
# Wikipedia MCP负责的内容
wikipedia_section = f"""
<div class="mcp-section mcp-section-wikipedia">
    <div class="mcp-label mcp-wikipedia">Wikipedia MCP</div>
    <h2>{wiki_data['title']}</h2>
    <p>{wiki_data['summary']}</p>
</div>
"""

# SQLite MCP负责的内容
sqlite_section = """
<div class="mcp-section mcp-section-sqlite">
    <div class="mcp-label mcp-sqlite">SQLite MCP</div>
    <h2>数据统计</h2>
    <p>文章数量: {count}</p>
</div>
"""
```

#### Step 5: 写入文件
```python
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
```

### 最佳实践

#### 1. 内容分工
- **Wikipedia MCP**: 提供事实性、定义性的内容
- **SQLite MCP**: 管理结构化数据、元信息
- **Filesystem MCP**: 负责文档结构、样式设计

#### 2. 标注原则
- 每个主要章节都应标注MCP来源
- 使用统一的颜色编码系统
- 标签位置一致（建议右上角）
- 边框宽度统一（建议5px）

#### 3. 样式设计
- 使用渐变色提升视觉效果
- 保持足够的内边距和外边距
- 采用圆角设计（建议8-16px）
- 添加阴影增强层次感

#### 4. 响应式设计
```css
@media (max-width: 768px) {
    .container {
        padding: 20px;
    }

    h1 {
        font-size: 1.8em;
    }
}
```

#### 5. 数据完整性
- 始终验证文件写入成功
- 检查数据库操作是否提交
- 添加错误处理机制
- 记录生成时间戳

### 常见问题

**Q: 如何添加新的MCP服务器？**

A: 在CSS中添加新的颜色类，然后在HTML中使用相应的标注：

```css
.mcp-section-newserver {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-left: 5px solid #f57c00;
}

.mcp-newserver {
    background: #fff3e0;
    color: #f57c00;
    border: 2px solid #f57c00;
}
```

**Q: 如何自定义颜色方案？**

A: 修改CSS中的渐变色和边框颜色：

```css
/* 示例：改为红色主题 */
.mcp-section-wikipedia {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    border-left: 5px solid #d32f2f;
}
```

**Q: 如何生成Markdown而不是HTML？**

A: 使用类似的标注系统，但使用Markdown语法：

```markdown
## 🔵 Wikipedia MCP - 知识来源

### 人工智能

人工智能是指由机器展现的智能...

## 🟣 SQLite MCP - 数据管理

数据统计：文章1篇，引用4条...
```

**Q: 如何处理大量Wikipedia查询？**

A: 使用批量查询并缓存结果：

```python
import json

# 缓存Wikipedia数据
def cache_wiki_data(queries, cache_file='wiki_cache.json'):
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 执行查询
    results = query_wikipedia_batch(queries)

    # 保存缓存
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results
```

### 高级技巧

#### 1. 动态内容生成
```python
def generate_mcp_section(mcp_type, title, content):
    """生成带MCP标注的HTML段落"""
    return f"""
    <div class="mcp-section mcp-section-{mcp_type}">
        <div class="mcp-label mcp-{mcp_type}">{get_mcp_name(mcp_type)}</div>
        <h2>{title}</h2>
        {content}
    </div>
    """
```

#### 2. 模板继承
```python
base_template = """
<!DOCTYPE html>
<html>
<head>
    <style>{css}</style>
</head>
<body>
    {header}
    {content}
    {footer}
</body>
</html>
"""
```

#### 3. 数据验证
```python
def validate_html_content(html_content):
    """验证HTML内容完整性"""
    required_tags = ['<!DOCTYPE html>', '<html', '<body>', '</html>', '</body>']
    return all(tag in html_content for tag in required_tags)
```

### 示例输出

查看完整示例：
- 文章示例: `mcp_test/AI_Trends_2026.html`
- 测试报告: `mcp_test/MCP_Test_Report.html`
- 生成代码: `mcp_test/mcp_test_html.py`

### 相关技能

- `article-writer` - 基础文章写作技能
- `data-visualizer` - 数据可视化技能
- `citation-manager` - 文献管理技能

### 更新日志

**v1.0.0** (2026-02-01)
- ✨ 初始版本
- ✅ 支持三个MCP服务器
- ✅ 实现颜色标注系统
- ✅ 响应式HTML设计
- ✅ 完整文档和示例
- ⭐ **新特性**：自动使用当前工作目录生成文件
  - 📄 HTML自动生成到：`{当前目录}/output/`
  - 🗄️ 数据库自动创建在：`{当前目录}/articles.db`
  - 仍然支持指定绝对路径

---

**需要帮助？** 查看示例代码或参考测试用例。
