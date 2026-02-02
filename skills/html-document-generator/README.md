# HTML文档生成器 Skill

使用MCP服务器生成带标注的HTML文档的完整解决方案。

## 🚀 快速开始

### 1. 基础使用（自动使用当前目录）

```python
from html_document_generator import FilesystemMCP, SQLiteMCP

# 初始化（不指定路径，自动使用当前目录）
sqlite_mcp = SQLiteMCP()  # 数据库: {当前目录}/articles.db
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备内容
sections = [{
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP',
    'content': '<h2>我的文章</h2><p>内容...</p>'
}]

# 生成HTML（自动在当前目录/output下生成）
fs_mcp = FilesystemMCP()
fs_mcp.generate_html("文章标题", sections)
# 输出: {当前目录}/output/文章标题.html
```

### 2. 自定义路径（可选）

```python
# 如果需要指定绝对路径
sqlite_mcp = SQLiteMCP(r'C:\custom\path\database.db')
fs_mcp.generate_html("标题", sections, r'C:\custom\path\output.html')
```

**⭐ 新特性（v1.0.0）：**
- 默认情况下，所有文件自动生成在**当前工作目录**
- 📄 HTML：`{当前目录}/output/`
- 🗄️ 数据库：`{当前目录}/articles.db`
- 仍然支持指定绝对路径

## 📚 核心功能

### ✨ 特色功能

1. **MCP标注系统** - 清晰标注每个MCP服务器的贡献
2. **颜色编码** - 蓝/紫/绿三色区分不同MCP来源
3. **响应式设计** - 支持桌面和移动设备
4. **数据管理** - SQLite存储文章和引用关系
5. **知识集成** - Wikipedia提供权威背景知识

### 🎯 适用场景

- 📝 **技术文档** - API文档、技术指南
- 📚 **知识库** - 产品文档、帮助中心
- 📊 **测试报告** - 测试结果、分析报告
- 🎓 **学术论文** - 研究报告、学位论文
- 📖 **在线教程** - 课程材料、学习指南

## 🔧 使用方法

### Step 1: 准备内容

定义你的章节和MCP来源：

```python
sections = [
    {
        'mcp_type': 'wikipedia',  # 知识来源
        'label': 'Wikipedia MCP - 知识来源',
        'content': '<h2>章节标题</h2><p>内容...</p>'
    },
    {
        'mcp_type': 'sqlite',  # 数据统计
        'label': 'SQLite MCP - 数据管理',
        'content': '<h2>数据统计</h2><p>数据...</p>'
    },
    {
        'mcp_type': 'filesystem',  # 文档生成
        'label': 'Filesystem MCP - 内容生成',
        'content': '<h2>文档说明</h2><p>说明...</p>'
    }
]
```

### Step 2: 调用生成器

```python
from skills.html_document_generator.template import FilesystemMCP

fs_mcp = FilesystemMCP()
html_content = fs_mcp.generate_html(
    title="我的文章",
    sections=sections,
    output_path="output.html"
)
```

### Step 3: 查看结果

在浏览器中打开生成的HTML文件，你会看到：
- 🔵 蓝色区域 - Wikipedia MCP提供的内容
- 🟣 紫色区域 - SQLite MCP管理的数据
- 🟢 绿色区域 - Filesystem MCP生成的文档

## 🎨 自定义样式

### 修改颜色主题

```python
def get_css(self):
    return """
    .mcp-section-wikipedia {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #d32f2f;  /* 改为红色 */
    }
    """
```

### 添加新的MCP服务器

```python
.mcp-section-newmcp {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    border-left: 5px solid #f57c00;
}

.mcp-newmcp {
    background: #fff3e0;
    color: #f57c00;
    border: 2px solid #f57c00;
}
```

## 📊 数据库结构

### articles表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| title | TEXT | 文章标题 |
| content | TEXT | HTML内容 |
| created_at | TIMESTAMP | 创建时间 |

### refs表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| article_id | INTEGER | 关联文章ID |
| source_name | TEXT | 来源名称 |
| url | TEXT | 链接地址 |

## 🔄 工作流程

```
1. Wikipedia MCP → 查询知识
       ↓
2. SQLite MCP → 存储数据
       ↓
3. Filesystem MCP → 生成HTML
       ↓
4. 完整文档 → 带MCP标注
```

## 📝 示例代码

完整示例请参考：
- `mcp_test/mcp_test_html.py` - 完整实现
- `mcp_test/AI_Trends_2026.html` - 输出示例
- `template.py` - 简化模板

## 🛠️ 高级用法

### 1. 批量生成文档

```python
titles = ["文档1", "文档2", "文档3"]

for title in titles:
    sections = prepare_sections(title)
    fs_mcp.generate_html(title, sections, f"{title}.html")
```

### 2. 集成Wikipedia API

```python
import wikipedia

def query_wikipedia(term):
    try:
        page = wikipedia.page(term)
        return {
            "title": page.title,
            "summary": page.summary[:500],
            "url": page.url
        }
    except:
        return {}
```

### 3. 添加互动元素

```python
content = """
<div class="mcp-section mcp-section-wikipedia">
    <button onclick="toggleDetails()">显示详情</button>
    <div id="details" style="display:none">
        <p>详细内容...</p>
    </div>
</div>

<script>
function toggleDetails() {
    document.getElementById('details').style.display = 'block';
}
</script>
"""
```

## ❓ 常见问题

**Q: 如何支持Markdown格式？**

A: 使用markdown库转换：

```python
import markdown

md_content = "# 标题\n\n内容"
html_content = markdown.markdown(md_content)
```

**Q: 如何添加图片？**

A: 在内容中插入img标签：

```python
content = f"""
<img src="{image_path}" alt="图片说明" style="max-width:100%;">
"""
```

**Q: 如何生成PDF？**

A: 使用wkhtmltopdf或weasyprint：

```python
import weasyprint

weasyprint.HTML('output.html').write_pdf('output.pdf')
```

## 📚 相关资源

- [Wikipedia API文档](https://en.wikipedia.org/api/rest_v1/)
- [SQLite文档](https://docs.python.org/3/library/sqlite3.html)
- [HTML5教程](https://www.w3schools.com/html/)
- [CSS3指南](https://css-tricks.com/)

## 🤝 贡献

欢迎提交改进建议和bug报告！

## 📄 许可证

MIT License

---

**需要帮助？** 查看 `SKILL.md` 获取完整文档。
