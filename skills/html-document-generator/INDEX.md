# HTML文档生成器 Skill - 完整文档

## 📋 目录结构

```
skills/html-document-generator/
├── SKILL.md           # Skill主文档（详细说明）
├── README.md          # 快速入门指南
├── template.py        # Python模板代码
└── INDEX.md          # 本文件（总览）
```

## 🎯 Skill概述

**名称**: `html-document-generator`
**版本**: 1.0.0
**作者**: MCP Test System
**创建日期**: 2026-02-01

### 核心功能

此Skill展示了如何**协调三个MCP服务器**生成高质量的HTML文档：

```
Wikipedia MCP (知识源)
    ↓ 提供权威定义
SQLite MCP (数据层)
    ↓ 结构化存储
Filesystem MCP (输出层)
    ↓ HTML生成
完整文档 (带MCP标注)
```

## 🚀 快速开始

### 30秒上手

```python
# 1. 导入模板
from skills.html_document_generator.template import WikipediaMCP, SQLiteMCP, FilesystemMCP

# 2. 准备内容
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP',
        'content': '<h2>AI介绍</h2><p>人工智能是...</p>'
    }
]

# 3. 生成HTML
fs_mcp = FilesystemMCP()
fs_mcp.generate_html("我的文章", sections, "output.html")
```

### 5分钟完整示例

查看 `template.py` 获取完整实现。

## 📚 文档导航

### 📖 SKILL.md - 完整文档

**包含内容**:
- ✅ 何时使用此Skill
- ✅ 三个MCP服务器的详细说明
- ✅ MCP标注系统实现
- ✅ 分步实现指南
- ✅ 最佳实践和高级技巧
- ✅ 常见问题解答
- ✅ 示例和模板

**适合**: 需要深入了解实现细节的用户

### 📘 README.md - 使用指南

**包含内容**:
- ✅ 快速开始教程
- ✅ 核心功能介绍
- ✅ 使用方法和示例
- ✅ 自定义样式
- ✅ 数据库结构
- ✅ 常见问题

**适合**: 想要快速上手的用户

### 💻 template.py - 代码模板

**包含内容**:
- ✅ 三个MCP服务器的类实现
- ✅ HTML生成器
- ✅ CSS样式系统
- ✅ 完整的配置系统
- ✅ 可运行的示例代码

**适合**: 需要修改和扩展的用户

## 🎨 核心特性

### 1. MCP标注系统

| MCP服务器 | 颜色 | 用途 |
|-----------|------|------|
| Wikipedia | 🔵 蓝色 | 知识来源 |
| SQLite | 🟣 紫色 | 数据管理 |
| Filesystem | 🟢 绿色 | 内容生成 |

### 2. 响应式设计

- ✅ 桌面端优化
- ✅ 移动端适配
- ✅ 平板支持
- ✅ 渐变色主题

### 3. 数据完整性

- ✅ 数据库存储
- ✅ 引用关系管理
- ✅ 版本控制
- ✅ 时间戳记录

## 📊 应用场景

### 适合使用此Skill的情况

1. **需要生成技术文档**
   - API文档
   - 技术规范
   - 系统设计文档

2. **需要展示MCP能力**
   - AI Agent演示
   - 技术方案展示
   - 功能验证

3. **需要知识集成**
   - 研究报告
   - 学术论文
   - 知识库构建

4. **需要可追溯性**
   - 内容来源标注
   - 数据引用管理
   - 版本追踪

## 🔧 定制化

### 添加新颜色主题

```css
.mcp-section-custom {
    background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    border-left: 5px solid #d32f2f;
}
```

### 集成新的MCP服务器

```python
class CustomMCP:
    def __init__(self):
        self.name = "Custom MCP"
        self.color = "#ff5722"
        self.css_class = "custom"
```

## 📝 实际案例

### 案例1: 技术博客

```python
sections = [
    {'mcp_type': 'wikipedia', 'content': '技术定义'},
    {'mcp_type': 'filesystem', 'content': '实践经验'},
    {'mcp_type': 'sqlite', 'content': '数据统计'}
]
```

### 案例2: 测试报告

```python
sections = [
    {'mcp_type': 'sqlite', 'content': '测试结果'},
    {'mcp_type': 'filesystem', 'content': '分析结论'},
    {'mcp_type': 'wikipedia', 'content': '背景知识'}
]
```

## 🛠️ 工具和依赖

### 必需依赖

```bash
pip install sqlite3  # 数据库
```

### 可选依赖

```bash
pip install wikipedia  # Wikipedia API
pip install markdown  # Markdown支持
pip install weasyprint  # PDF生成
```

## 📈 性能优化

### 批量生成

```python
from concurrent.futures import ThreadPoolExecutor

def generate_article(title):
    # 生成逻辑
    pass

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(generate_article, title_list)
```

### 缓存策略

```python
import pickle
import os

def cache_wiki_data(term):
    cache_file = f"cache/{term}.pkl"
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    # 查询并缓存
    data = query_wikipedia(term)
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
    return data
```

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 联系方式

- 问题反馈: 通过GitHub Issues
- 功能建议: 通过Pull Requests

## 🎓 学习资源

### 相关教程

- [MCP协议官方文档](https://modelcontextprotocol.io/)
- [Python SQLite教程](https://docs.python.org/3/library/sqlite3.html)
- [HTML5完整指南](https://developer.mozilla.org/zh-CN/docs/Web/HTML)
- [CSS3参考手册](https://css-tricks.com/)

### 示例项目

- `mcp_test/AI_Trends_2026.html` - 完整示例
- `mcp_test/mcp_test_html.py` - 测试代码
- `mcp_test/MCP_Test_Report.html` - 测试报告

## 🔄 更新历史

### v1.0.0 (2026-02-01)

**新增功能**:
- ✨ 初始版本
- ✅ 支持三个MCP服务器
- ✅ MCP颜色标注系统
- ✅ 响应式HTML设计
- ✅ 完整文档和示例

**已知问题**:
- 无

**下一步计划**:
- 📋 添加Markdown支持
- 📋 集成更多MCP服务器
- 📋 提供更多主题模板

## 🎉 总结

这个Skill展示了如何：

1. ✅ **协调多个MCP服务器**完成复杂任务
2. ✅ **清晰标注内容来源**，提高可追溯性
3. ✅ **生成美观的HTML文档**，支持响应式设计
4. ✅ **管理结构化数据**，实现关系映射
5. ✅ **提供可复用的模板**，便于快速开发

**立即开始使用**: 查看 `README.md` 获取快速入门指南！

---

**Happy Coding! 🚀**
