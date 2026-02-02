# 如何使用 html-document-generator Skill

## 📖 正确的复用方式

### 安装Skill

将 `html-document-generator` 目录复制到你的项目中，或者添加到Python路径：

```bash
# 方式1: 复制到项目目录
cp -r skills/html-document-generator /path/to/your/project/

# 方式2: 添加到PYTHONPATH
export PYTHONPATH="/path/to/skills:$PYTHONPATH"
```

---

## 🚀 使用方式

### 方式1: 作为包导入（推荐）

```python
#!/usr/bin/env python3
# my_article.py

# 直接导入Skill
from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

# 使用Skill生成文档
sqlite_mcp = SQLiteMCP('my_article.db')
sqlite_mcp.connect()
sqlite_mcp.create_tables()

sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>什么是AI？</h2>
            <p>人工智能是计算机科学的一个分支...</p>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 内容生成',
        'content': '''
            <h2>应用场景</h2>
            <p>AI应用于医疗、金融、教育等领域...</p>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 数据统计',
        'content': '''
            <h2>数据统计</h2>
            <p>本文包含3个章节，使用了3个MCP服务器...</p>
        '''
    }
]

# 生成HTML
fs_mcp = FilesystemMCP()
fs_mcp.generate_html(
    title='AI技术深度解析',
    sections=sections,
    output_path='ai_article.html'
)

# 保存到数据库
with open('ai_article.html', 'r', encoding='utf-8') as f:
    content = f.read()
article_id = sqlite_mcp.insert_article('AI技术深度解析', content)

# 添加引用
sqlite_mcp.insert_ref(article_id, 'Artificial Intelligence',
    'https://en.wikipedia.org/wiki/Artificial_intelligence')

sqlite_mcp.close()

print(f"✅ 文章已生成！ID: {article_id}")
```

---

### 方式2: 相对导入

```python
#!/usr/bin/env python3
# 如果Skill在项目子目录中

import sys
from pathlib import Path

# 添加Skill路径
skill_path = Path(__file__).parent / 'skills' / 'html-document-generator'
sys.path.insert(0, str(skill_path))

# 导入并使用
from html_document_generator import FilesystemMCP

sections = [{
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP',
    'content': '<h2>我的文章</h2><p>内容...</p>'
}]

fs_mcp = FilesystemMCP()
fs_mcp.generate_html("标题", sections, "output.html")
```

---

### 方式3: 使用setup.py安装（开发模式）

**步骤1**: 创建 `setup.py`

```python
# skills/setup.py
from setuptools import setup, find_packages

setup(
    name="html-document-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'sqlite3',  # 通常Python自带
    ],
)
```

**步骤2**: 安装到开发环境

```bash
cd skills
pip install -e .
```

**步骤3**: 在任何地方使用

```python
# 现在可以在任何Python脚本中使用
from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

# 使用代码...
```

---

## 📝 实际应用场景

### 场景1: 技术博客生成器

```python
from html_document_generator import FilesystemMCP, WikipediaMCP

def generate_tech_blog(topic):
    """生成技术博客"""

    wiki = WikipediaMCP()
    wiki_data = wiki.query(topic)  # 查询Wikipedia

    sections = [
        {
            'mcp_type': 'wikipedia',
            'label': 'Wikipedia MCP',
            'content': f'''
                <h2>{topic} 简介</h2>
                <p>{wiki_data['summary']}</p>
                <p>参考: <a href="{wiki_data['url']}">Wikipedia</a></p>
            '''
        },
        {
            'mcp_type': 'filesystem',
            'label': 'Filesystem MCP',
            'content': f'''
                <h2>{topic} 实战</h2>
                <p>在实际项目中，{topic}广泛应用于...</p>
            '''
        }
    ]

    fs = FilesystemMCP()
    fs.generate_html(f"{topic}技术博客", sections, f"{topic}.html")

# 生成多个博客
topics = ['Python', 'JavaScript', 'Rust']
for topic in topics:
    generate_tech_blog(topic)
```

---

### 场景2: 测试报告生成器

```python
from html_document_generator import FilesystemMCP, SQLiteMCP

def generate_test_report(test_results):
    """生成测试报告"""

    sqlite = SQLiteMCP('test_reports.db')
    sqlite.connect()
    sqlite.create_tables()

    sections = [
        {
            'mcp_type': 'sqlite',
            'label': 'SQLite MCP - 测试统计',
            'content': f'''
                <h2>测试概览</h2>
                <ul>
                    <li>总测试数: {test_results['total']}</li>
                    <li>通过: {test_results['passed']}</li>
                    <li>失败: {test_results['failed']}</li>
                </ul>
            '''
        },
        {
            'mcp_type': 'filesystem',
            'label': 'Filesystem MCP - 失败详情',
            'content': '<h2>失败用例</h2><p>详情...</p>'
        }
    ]

    fs = FilesystemMCP()
    report_path = f"report_{test_results['date']}.html"
    fs.generate_html("测试报告", sections, report_path)

    # 保存到数据库
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    article_id = sqlite.insert_article(f"测试报告_{test_results['date']}", content)

    sqlite.close()
    return article_id

# 使用
results = {'total': 100, 'passed': 95, 'failed': 5, 'date': '2026-02-01'}
report_id = generate_test_report(results)
```

---

### 场景3: 知识库文档生成

```python
from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

class KnowledgeBaseGenerator:
    """知识库文档生成器"""

    def __init__(self, db_path='knowledge_base.db'):
        self.sqlite = SQLiteMCP(db_path)
        self.wiki = WikipediaMCP()
        self.fs = FilesystemMCP()

        self.sqlite.connect()
        self.sqlite.create_tables()

    def generate_article(self, topic):
        """生成知识库文章"""

        # 查询Wikipedia
        wiki_data = self.wiki.query(topic)

        # 构建章节
        sections = [
            {
                'mcp_type': 'wikipedia',
                'label': 'Wikipedia MCP',
                'content': f'''
                    <h2>{topic} 定义</h2>
                    <p>{wiki_data['summary']}</p>
                '''
            },
            {
                'mcp_type': 'filesystem',
                'label': 'Filesystem MCP',
                'content': f'''
                    <h2>{topic} 应用</h2>
                    <p>在项目中，{topic}可以用于...</p>
                '''
            },
            {
                'mcp_type': 'filesystem',
                'label': 'Filesystem MCP',
                'content': f'''
                    <h2>最佳实践</h2>
                    <ul>
                        <li>实践1</li>
                        <li>实践2</li>
                    </ul>
                '''
            }
        ]

        # 生成HTML
        filename = f"kb_{topic}.html"
        self.fs.generate_html(f"{topic}知识库", sections, filename)

        # 保存到数据库
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        article_id = self.sqlite.insert_article(f"{topic}知识库", content)
        self.sqlite.insert_ref(article_id, wiki_data['title'], wiki_data['url'])

        return article_id

    def close(self):
        self.sqlite.close()

# 使用
generator = KnowledgeBaseGenerator()
article_id = generator.generate_article('Machine Learning')
generator.close()
```

---

## 🎨 高级用法

### 自定义MCP服务器

```python
from html_document_generator import FilesystemMCP

class CustomMCP(FilesystemMCP):
    """自定义MCP服务器"""

    def get_css(self):
        """自定义CSS样式"""
        base_css = super().get_css()

        custom_css = """
        .mcp-section-custom {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            border-left: 5px solid #f57c00;
        }

        .mcp-custom {
            background: #fff3e0;
            color: #f57c00;
            border: 2px solid #f57c00;
        }
        """

        return base_css + custom_css

# 使用自定义MCP
custom_mcp = CustomMCP()
sections = [{
    'mcp_type': 'custom',
    'label': 'Custom MCP',
    'content': '<h2>自定义内容</h2><p>使用自定义样式...</p>'
}]

custom_mcp.generate_html("自定义文章", sections, "custom.html")
```

---

## 📊 批量生成

```python
from html_document_generator import FilesystemMCP, SQLiteMCP
from concurrent.futures import ThreadPoolExecutor

def generate_single_article(topic):
    """生成单篇文章"""
    sections = [{
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP',
        'content': f'<h2>{topic}</h2><p>关于{topic}的内容...</p>'
    }]

    fs = FilesystemMCP()
    fs.generate_html(topic, sections, f"{topic}.html")
    return f"{topic}.html"

# 批量生成
topics = ['AI', '区块链', '物联网', '量子计算', '5G']

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(generate_single_article, topics)

print(f"生成了 {len(list(results))} 篇文章")
```

---

## 🔧 配置管理

### 使用配置文件

```python
# config.yaml
html_document_generator:
  output_dir: "output"
  db_name: "articles.db"
  default_author: "AI Assistant"

# app.py
import yaml
from html_document_generator import FilesystemMCP, SQLiteMCP

# 加载配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 使用配置
sqlite_mcp = SQLiteMCP(config['html_document_generator']['db_name'])
fs_mcp = FilesystemMCP()

sections = [{'mcp_type': 'filesystem', 'content': '<h2>文章</h2>'}]
fs_mcp.generate_html("标题", sections,
    os.path.join(config['html_document_generator']['output_dir'], 'article.html'))
```

---

## 🎯 最佳实践

### 1. 项目结构

```
my_project/
├── main.py                 # 主程序
├── skills/                 # Skill目录
│   └── html-document-generator/
│       ├── __init__.py
│       ├── template.py
│       └── ...
├── output/                 # 输出目录
└── config.yaml            # 配置文件
```

### 2. 错误处理

```python
from html_document_generator import FilesystemMCP
import logging

try:
    fs = FilesystemMCP()
    fs.generate_html("标题", sections, "output.html")
    logging.info("文档生成成功")
except Exception as e:
    logging.error(f"文档生成失败: {e}")
```

### 3. 单元测试

```python
import unittest
from html_document_generator import FilesystemMCP

class TestHTMLGenerator(unittest.TestCase):
    def test_generate_html(self):
        fs = FilesystemMCP()
        sections = [{
            'mcp_type': 'filesystem',
            'content': '<h2>测试</h2>'
        }]

        fs.generate_html("测试", sections, "test.html")

        # 验证文件存在
        self.assertTrue(os.path.exists('test.html'))

if __name__ == '__main__':
    unittest.main()
```

---

## ❓ 常见问题

**Q: 如何更新Skill？**

A:
```bash
cd skills/html-document-generator
git pull  # 如果使用git
# 或者手动替换文件
```

**Q: 如何在不同项目中使用？**

A:
```bash
# 方式1: 复制Skill目录
cp -r skills/html-document-generator /path/to/other/project/

# 方式2: 使用符号链接
ln -s /path/to/skills/html-document-generator /path/to/project/skills/

# 方式3: 安装为包
pip install -e /path/to/skills
```

---

## 🎉 总结

### 正确的复用方式

```python
# 1. 导入Skill
from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP

# 2. 使用Skill
sections = [{'mcp_type': 'filesystem', 'content': '<h2>标题</h2>'}]
fs = FilesystemMCP()
fs.generate_html("文章", sections, "output.html")
```

### 关键点

- ✅ 使用 `from html_document_generator import ...`
- ✅ 通过 `__init__.py` 导出类
- ✅ 可以作为Python包使用
- ✅ 支持安装和复用

---

**现在明白了吗？`html-document-generator` 是一个Python包名，通过 `from html_document_generator import ...` 来使用！** 🚀
