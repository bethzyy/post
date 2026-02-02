# 如何使用 html-document-generator Skill

## 🎯 Skill概述

**Skill名称**: `html-document-generator`
**版本**: 1.0.0
**Python包位置**: `skills/html-document-generator/`
**Claude Skill位置**: `.claude/skills/html-document-generator.md`

这个Skill提供三个MCP服务器类，用于生成带MCP标注的HTML文档：
- `WikipediaMCP` - 知识来源（🔵 蓝色）
- `SQLiteMCP` - 数据管理（🟣 紫色）
- `FilesystemMCP` - 文档生成（🟢 绿色）

---

## 🔄 两种使用方式

### 方式对比

| 特性 | 方式1: Python包 | 方式2: Claude Code Skill |
|------|----------------|----------------------|
| **使用场景** | 在Python脚本中使用 | 在Claude Code对话中使用 |
| **实现方式** | Python包导入 | Claude识别Skill描述 |
| **配置文件** | `__init__.py` | `.claude/skills/html-document-generator.md` |
| **导入方式** | `from html_document_generator import ...` | Claude自动识别 |
| **灵活性** | 高（完全控制） | 中（通过对话） |
| **难度** | 需要写Python代码 | 直接对话即可 |

---

## 📖 方式1: 作为Python包使用

### 适用场景
- ✅ 你有自己的Python项目
- ✅ 需要完全控制代码逻辑
- ✅ 要集成到现有系统中
- ✅ 需要批量自动化处理

### 实现原理

**核心文件**: `skills/html-document-generator/__init__.py`

```python
# __init__.py 让目录成为Python包
from .template import WikipediaMCP, SQLiteMCP, FilesystemMCP

__all__ = ['WikipediaMCP', 'SQLiteMCP', 'FilesystemMCP']
```

### 使用步骤

#### 步骤1: 确保Skill在Python路径中

```python
import sys
from pathlib import Path

# 添加Skill目录到Python路径
skill_path = Path(__file__).parent / 'skills' / 'html-document-generator'
sys.path.insert(0, str(skill_path))
```

#### 步骤2: 导入并使用

**⭐ 新特性：自动使用当前目录**

从v1.0.0开始，Skill会自动在**当前工作目录**创建输出文件：

```python
#!/usr/bin/env python3
from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

# 初始化MCP服务器（不指定路径，自动使用当前目录）
sqlite_mcp = SQLiteMCP()  # 数据库在: {当前目录}/articles.db
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备内容
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>什么是Python？</h2>
            <p>Python是一种高级编程语言...</p>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 内容生成',
        'content': '''
            <h2>Python应用领域</h2>
            <ul>
                <li>Web开发（Django, Flask）</li>
                <li>数据科学（Pandas, NumPy）</li>
                <li>人工智能（TensorFlow, PyTorch）</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 数据统计',
        'content': '''
            <h2>文档信息</h2>
            <p>生成时间：2026-02-01</p>
            <p>MCP服务器：3个</p>
        '''
    }
]

# 生成HTML（不指定路径，自动在当前目录/output下生成）
fs_mcp = FilesystemMCP()
html_content = fs_mcp.generate_html(
    "Python编程入门",
    sections
    # output_path不指定，自动生成到: {当前目录}/output/Python编程入门.html
)

# 保存到数据库
article_id = sqlite_mcp.insert_article('Python编程入门', html_content)

sqlite_mcp.close()
print(f"✅ 完成！文章ID: {article_id}")
print(f"📄 HTML: {当前目录}/output/Python编程入门.html")
print(f"🗄️ 数据库: {当前目录}/articles.db")
```

**输出位置说明：**
- 📄 HTML文件：`{当前工作目录}/output/{标题}.html`
- 🗄️ 数据库文件：`{当前工作目录}/articles.db`

**如果你需要指定绝对路径：**
```python
# 仍然支持指定绝对路径
sqlite_mcp = SQLiteMCP(r'C:\path\to\custom.db')
fs_mcp.generate_html("标题", sections, r'C:\path\to\output.html')
```

#### 步骤3: 运行脚本

```bash
python your_script.py
```

### 优势
- ✅ 完全控制代码逻辑
- ✅ 可以集成到自动化流程
- ✅ 支持批量处理
- ✅ 易于调试和修改

### 劣势
- ❌ 需要手写Python代码
- ❌ 需要管理依赖关系
- ❌ 需要处理路径问题

---

## 🤖 方式2: 作为Claude Code Skill使用

### 适用场景
- ✅ 快速生成文档
- ✅ 不想写代码
- ✅ 通过对话交互
- ✅ 探索和测试

### 实现原理

**核心文件**: `.claude/skills/html-document-generator.md`

```markdown
---
name: html-document-generator
description: 使用MCP服务器生成带标注的HTML文档
---

## When to use
使用此技能生成技术文档、博客文章、测试报告...

## How to use
在Python脚本中使用：
from html_document_generator import FilesystemMCP...
```

Claude Code会读取这个文件，了解Skill的能力和使用方法。

### 使用方式

#### 方法1: 直接要求使用（推荐）

```
你: "使用html-document-generator Skill生成一篇关于量子计算的文章"

Claude:
1. 识别到Skill
2. 创建Python脚本
3. 使用 `from html_document_generator import ...`
4. 运行脚本生成HTML
5. 打开生成的文档
```

#### 方法2: 查看Skill文档

```
你: "查看html-document-generator的文档"

Claude:
1. 读取 `.claude/skills/html-document-generator.md`
2. 展示使用说明
3. 提供示例代码
```

#### 方法3: 批量生成

```
你: "用html-document-generator批量生成AI、区块链、物联网三篇文章"

Claude:
1. 创建批量处理脚本
2. 循环生成三篇文章
3. 保存到数据库
4. 生成统计报告
```

### 实际对话示例

#### 示例1: 生成技术文档

**你**:
```
使用html-document-generator生成一篇关于Rust语言的文章
```

**Claude会**:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# 添加Skill路径
skill_path = Path(__file__).parent / 'skills' / 'html-document-generator'
sys.path.insert(0, str(skill_path))

from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

# 初始化
sqlite_mcp = SQLiteMCP('rust_article.db')
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备内容
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP',
        'content': '''
            <h2>什么是Rust？</h2>
            <p>Rust是一种系统编程语言，注重安全、并发和性能...</p>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP',
        'content': '''
            <h2>Rust的特点</h2>
            <ul>
                <li>内存安全 - 编译时保证</li>
                <li>零成本抽象</li>
                <li>现代工具链</li>
            </ul>
        '''
    }
]

# 生成
fs = FilesystemMCP()
fs.generate_html("Rust语言教程", sections, "rust.html")

# 保存
with open('rust.html', 'r') as f:
    content = f.read()
article_id = sqlite_mcp.insert_article('Rust语言教程', content)

sqlite_mcp.close()
print(f"✅ 完成！ID: {article_id}")
```

#### 示例2: 生成测试报告

**你**:
```
用html-document-generator生成测试报告，包含：
- 测试统计（通过率、失败数）
- 失败用例详情
- 改进建议
```

**Claude会**:
创建包含上述sections的脚本，生成带MCP标注的测试报告。

### 优势
- ✅ 不需要写代码
- ✅ 通过对话即可使用
- ✅ Claude自动处理路径
- ✅ 快速迭代和修改

### 劣势
- ❌ 需要Claude Code环境
- ❌ 灵活性较低
- ❌ 依赖Claude的理解

---

## 🎯 如何选择使用方式

### 决策树

```
需要生成HTML文档
    │
    ├─ 你会写Python代码吗？
    │   ├─ 是 → 使用方式1（Python包）
    │   └─ 否 → 使用方式2（Claude Skill）
    │
    ├─ 需要批量自动化吗？
    │   ├─ 是 → 使用方式1（Python包）
    │   └─ 否 → 两种都可以
    │
    └─ 需要快速原型吗？
        ├─ 是 → 使用方式2（Claude Skill）
        └─ 否 → 使用方式1（Python包）
```

### 推荐场景

**使用方式1（Python包）适合**:
- 🔄 批量生成100+文档
- 🔄 集成到CI/CD流程
- 🔄 作为Web服务后端
- 🔄 需要自定义逻辑

**使用方式2（Claude Skill）适合**:
- 🚀 快速生成单篇文档
- 🚀 探索Skill的功能
- 🚀 不想写代码
- 🚀 交互式迭代

---

## 💡 混合使用（高级技巧）

### 场景：用Claude快速原型，然后转为Python包

**步骤1**: 用Claude Skill快速生成

```
你: "使用html-document-generator生成一篇关于Vue.js的文章"
```

**步骤2**: 查看生成的代码

```
你: "把刚才的代码保存到vue_article.py"
```

**步骤3**: 基于代码扩展

```python
# vue_article.py
from html_document_generator import FilesystemMCP

# 原有代码
sections = [...]

# 添加自定义逻辑
def add_custom_section(topic):
    return {
        'mcp_type': 'filesystem',
        'content': f'<h2>{topic}实战技巧</h2><p>高级内容...</p>'
    }

sections.append(add_custom_section('Vue.js'))

# 生成最终版本
fs = FilesystemMCP()
fs.generate_html("Vue.js完全指南", sections, "vue_complete.html")
```

---

## 📝 完整示例对比

### 同一个任务，两种实现

**任务**: 生成一篇关于"机器学习"的文章

#### 方式1: Python包（手动编写）

```python
# ml_article.py
from html_document_generator import FilesystemMCP, SQLiteMCP

sqlite_mcp = SQLiteMCP('ml.db')
sqlite_mcp.connect()
sqlite_mcp.create_tables()

sections = [
    {
        'mcp_type': 'wikipedia',
        'content': '<h2>机器学习定义</h2><p>...</p>'
    },
    {
        'mcp_type': 'filesystem',
        'content': '<h2>ML算法</h2><p>...</p>'
    }
]

fs = FilesystemMCP()
fs.generate_html("机器学习入门", sections, "ml.html")

with open('ml.html') as f:
    article_id = sqlite_mcp.insert_article('ML入门', f.read())
sqlite_mcp.close()
```

运行：
```bash
python ml_article.py
```

#### 方式2: Claude Skill（对话）

```
你: "使用html-document-generator生成一篇关于机器学习的文章，包含定义、算法和应用"

Claude:
[创建脚本]
[运行脚本]
[生成ml.html]
```

---

## 🔧 配置要求

### 方式1需要的文件

```
skills/html-document-generator/
├── __init__.py          ✅ 必需
├── template.py          ✅ 必需
└── ...
```

### 方式2需要的文件

```
.claude/
└── skills/
    └── html-document-generator.md  ✅ 必需（已创建）
```

**注意**: 两种方式可以共存，互相补充！

---

## 🎯 快速参考

### 方式1快速命令

```python
# 导入
from html_document_generator import FilesystemMCP

# 使用
sections = [{'mcp_type': 'filesystem', 'content': '<h2>标题</h2>'}]
fs = FilesystemMCP()
fs.generate_html("文章", sections, "output.html")
```

### 方式2快速命令

```
"使用html-document-generator生成关于XXX的文章"
```

---

## 📚 相关文档

- **SKILL.md** - 完整的Skill官方描述
- **EXAMPLES.md** - 5个详细示例
- **demo.py** - 完整演示程序
- **test_skill_usage.py** - 测试程序
- **.claude/skills/html-document-generator.md** - Claude Skill描述

---

## 🎉 总结

### 两种方式的本质区别

**方式1（Python包）**:
- 本质：**代码复用**
- 实现：`import` + 函数调用
- 控制：**完全由你控制**
- 适合：**项目集成、批量处理**

**方式2（Claude Skill）**:
- 本质：**AI能力扩展**
- 实现：对话 + 自动识别
- 控制：**由Claude控制**
- 适合：**快速原型、交互式使用**

### 推荐工作流

1. **探索阶段**: 使用方式2（Claude Skill）
2. **原型验证**: 使用方式2快速生成
3. **生产部署**: 转为方式1（Python包）
4. **维护迭代**: 两种方式结合使用

---

## ❓ 常见问题

**Q: 两种方式可以同时使用吗？**

A: 可以！而且推荐同时使用：
- 用Claude Skill快速探索
- 用Python包深度定制

**Q: 方式2需要配置吗？**

A: Skill描述文件 `.claude/skills/html-document-generator.md` 已经创建好了，可以直接使用。

**Q: 如何在方式1和方式2之间转换？**

A:
- 从方式2→方式1: 复制Claude生成的代码，保存为.py文件
- 从方式1→方式2: 告诉Claude"参考xxx.py的逻辑生成文章"

---

**立即开始**:
- **有代码需求**: 使用方式1
- **快速生成**: 使用方式2

**推荐**: 先用方式2体验，再用方式1深入！🚀
