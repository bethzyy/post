# 使用示例

本文展示如何使用 `html-document-generator` Skill 生成HTML文档。

## 示例1: 基础用法

### 目标
生成一篇关于"Python编程"的简单HTML文档

### 代码

```python
#!/usr/bin/env python3
import sqlite3
from datetime import datetime
from skills.html_document_generator.template import WikipediaMCP, SQLiteMCP, FilesystemMCP

# 初始化MCP服务器
wiki_mcp = WikipediaMCP()
sqlite_mcp = SQLiteMCP('python_article.db')
fs_mcp = FilesystemMCP()

# 连接数据库
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备章节
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>什么是Python？</h2>
            <p>Python是一种高级编程语言，由Guido van Rossum于1991年创建。</p>
            <p><strong>特点</strong>：</p>
            <ul>
                <li>简洁易读的语法</li>
                <li>强大的标准库</li>
                <li>跨平台支持</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 内容生成',
        'content': '''
            <h2>Python应用领域</h2>
            <p>Python广泛应用于：</p>
            <ul>
                <li>Web开发（Django, Flask）</li>
                <li>数据科学（Pandas, NumPy）</li>
                <li>人工智能（TensorFlow, PyTorch）</li>
                <li>自动化脚本</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 数据统计',
        'content': f'''
            <h2>文档信息</h2>
            <p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>字数：约500字</p>
            <p>MCP服务器：3个</p>
        '''
    }
]

# 生成HTML
html_content = fs_mcp.generate_html(
    title='Python编程入门',
    sections=sections,
    output_path='python_article.html'
)

# 保存到数据库
article_id = sqlite_mcp.insert_article('Python编程入门', html_content)
sqlite_mcp.insert_ref(article_id, 'Python', 'https://en.wikipedia.org/wiki/Python')

sqlite_mcp.close()

print(f"[OK] 文章已生成: python_article.html")
print(f"[OK] 数据库ID: {article_id}")
```

### 输出

生成的 `python_article.html` 包含：
- 🔵 蓝色区域：Python的定义（来自Wikipedia）
- 🟢 绿色区域：应用领域说明（Filesystem生成）
- 🟣 紫色区域：文档统计信息（SQLite管理）

---

## 示例2: 集成真实Wikipedia API

### 目标
从Wikipedia查询真实数据并生成文档

### 代码

```python
#!/usr/bin/env python3
import wikipedia
from skills.html-document-generator.template import FilesystemMCP

def get_wiki_content(term):
    """从Wikipedia获取内容"""
    try:
        page = wikipedia.page(term)
        return {
            'title': page.title,
            'summary': page.summary[:500],
            'url': page.url
        }
    except wikipedia.exceptions.PageError:
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        # 选择第一个选项
        page = wikipedia.page(e.options[0])
        return {
            'title': page.title,
            'summary': page.summary[:500],
            'url': page.url
        }

# 查询多个主题
topics = ['Artificial intelligence', 'Machine learning', 'Deep learning']
sections = []

for topic in topics:
    wiki_data = get_wiki_content(topic)
    if wiki_data:
        sections.append({
            'mcp_type': 'wikipedia',
            'label': f'Wikipedia MCP - {topic}',
            'content': f'''
                <h2>{wiki_data['title']}</h2>
                <p>{wiki_data['summary']}</p>
                <p>📖 <a href="{wiki_data['url']}" target="_blank">阅读完整文章</a></p>
            '''
        })

# 添加总结章节
sections.append({
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP - 总结',
    'content': '''
        <h2>总结</h2>
        <p>本文介绍了AI、ML和Deep Learning的基本概念。</p>
        <p>所有内容均来自Wikipedia百科全书。</p>
    '''
})

# 生成HTML
fs_mcp = FilesystemMCP()
fs_mcp.generate_html(
    title='AI技术概览',
    sections=sections,
    output_path='ai_overview.html'
)

print("[OK] 文档已生成: ai_overview.html")
```

---

## 示例3: 批量生成文档

### 目标
批量生成多个技术文档

### 代码

```python
#!/usr/bin/env python3
from skills.html_document_generator.template import FilesystemMCP
import sqlite3

# 文档配置
documents = [
    {
        'title': 'JavaScript入门',
        'wikipedia_term': 'JavaScript',
        'sections': ['简介', '应用', '框架']
    },
    {
        'title': 'Rust语言指南',
        'wikipedia_term': 'Rust',
        'sections': ['特性', '应用', '生态']
    },
    {
        'title': 'Go语言实战',
        'wikipedia_term': 'Go',
        'sections': ['历史', '特点', '应用']
    }
]

def generate_document(doc_config):
    """生成单个文档"""

    # 查询Wikipedia
    wiki_data = get_wiki_content(doc_config['wikipedia_term'])

    # 构建章节
    sections = []

    # Wikipedia章节
    if wiki_data:
        sections.append({
            'mcp_type': 'wikipedia',
            'label': 'Wikipedia MCP - 知识来源',
            'content': f'''
                <h2>{doc_config['title']}</h2>
                <p>{wiki_data['summary']}</p>
            '''
        })

    # 内容章节
    for section_title in doc_config['sections']:
        sections.append({
            'mcp_type': 'filesystem',
            'label': 'Filesystem MCP - 内容生成',
            'content': f'<h3>{section_title}</h3><p>相关内容...</p>'
        })

    # 生成HTML
    fs_mcp = FilesystemMCP()
    filename = f"{doc_config['title']}.html"
    fs_mcp.generate_html(doc_config['title'], sections, filename)

    return filename

# 批量生成
for doc in documents:
    filename = generate_document(doc)
    print(f"[OK] 生成文档: {filename}")
```

---

## 示例4: 自定义样式主题

### 目标
使用自定义颜色主题生成文档

### 代码

```python
#!/usr/bin/env python3
from skills.html_document_generator.template import FilesystemMCP

class CustomFilesystemMCP(FilesystemMCP):
    """自定义样式的Filesystem MCP"""

    def get_css(self):
        """返回自定义CSS"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
        }

        /* 自定义Wikipedia样式 - 改为橙色 */
        .mcp-section-wikipedia {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            border-left: 5px solid #f57c00;
        }

        .mcp-wikipedia {
            background: #fff3e0;
            color: #f57c00;
            border: 2px solid #f57c00;
        }

        /* 自定义SQLite样式 - 改为红色 */
        .mcp-section-sqlite {
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            border-left: 5px solid #d32f2f;
        }

        .mcp-sqlite {
            background: #ffebee;
            color: #d32f2f;
            border: 2px solid #d32f2f;
        }

        /* 自定义Filesystem样式 - 保持绿色 */
        .mcp-section-filesystem {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-left: 5px solid #388e3c;
        }

        .mcp-filesystem {
            background: #e8f5e9;
            color: #388e3c;
            border: 2px solid #388e3c;
        }
        """

# 使用自定义MCP
custom_fs = CustomFilesystemMCP()

sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP',
        'content': '<h2>自定义主题示例</h2><p>Wikipedia现在是橙色</p>'
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP',
        'content': '<h2>数据库信息</h2><p>SQLite现在是红色</p>'
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP',
        'content': '<h2>文档说明</h2><p>Filesystem保持绿色</p>'
    }
]

custom_fs.generate_html(
    title='自定义主题文档',
    sections=sections,
    output_path='custom_theme.html'
)

print("[OK] 自定义主题文档已生成")
```

---

## 示例5: 生成测试报告

### 目标
生成软件测试报告

### 代码

```python
#!/usr/bin/env python3
from skills.html_document_generator.template import SQLiteMCP, FilesystemMCP
from datetime import datetime

# 测试数据
test_results = {
    'total': 100,
    'passed': 95,
    'failed': 5,
    'skipped': 0,
    'duration': '5m 32s'
}

# 初始化MCP
sqlite_mcp = SQLiteMCP('test_report.db')
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备章节
sections = [
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 测试统计',
        'content': f'''
            <h2>测试概览</h2>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="background: #667eea; color: white;">
                    <th style="padding: 10px; text-align: left;">指标</th>
                    <th style="padding: 10px; text-align: left;">数值</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">总测试数</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{test_results['total']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">通过</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; color: green;">{test_results['passed']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">失败</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; color: red;">{test_results['failed']}</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">耗时</td>
                    <td style="padding: 10px;">{test_results['duration']}</td>
                </tr>
            </table>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 失败用例',
        'content': '''
            <h2>失败用例详情</h2>
            <div style="background: #ffebee; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3 style="color: #d32f2f;">Test Case #45</h3>
                <p><strong>错误</strong>: AssertionError</p>
                <p><strong>原因</strong>: 期望值与实际值不匹配</p>
            </div>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 结论',
        'content': f'''
            <h2>测试结论</h2>
            <p>测试通过率: <strong>{test_results['passed']/test_results['total']*100:.1f}%</strong></p>
            <p>建议: 修复5个失败用例后重新测试</p>
            <p style="margin-top: 20px; color: #666;">
                报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
        '''
    }
]

# 生成报告
fs_mcp = FilesystemMCP()
html_content = fs_mcp.generate_html(
    title=f'测试报告 - {datetime.now().strftime("%Y-%m-%d")}',
    sections=sections,
    output_path='test_report.html'
)

# 保存到数据库
article_id = sqlite_mcp.insert_article(f'测试报告_{datetime.now()}', html_content)

sqlite_mcp.close()

print(f"[OK] 测试报告已生成: test_report.html")
print(f"[OK] 数据库ID: {article_id}")
```

---

## 总结

以上示例展示了 `html-document-generator` Skill 的多种用途：

1. ✅ **基础文档生成** - 快速创建HTML文档
2. ✅ **Wikipedia集成** - 获取真实知识数据
3. ✅ **批量处理** - 高效生成多个文档
4. ✅ **自定义样式** - 灵活的主题定制
5. ✅ **测试报告** - 专业的报告生成

**立即开始**: 选择一个示例，修改代码，生成你自己的文档！
