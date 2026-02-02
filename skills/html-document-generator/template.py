#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML文档生成器模板
使用MCP服务器生成带标注的HTML文档
"""

import sqlite3
import os
from datetime import datetime

# ==================== 配置区域 ====================
CONFIG = {
    "output_dir": "output",           # 输出目录
    "db_name": "articles.db",         # 数据库名称
    "article_title": "文档标题",       # 文章标题
    "author": "AI Assistant",         # 作者
}

# ==================== MCP服务器类 ====================

class WikipediaMCP:
    """Wikipedia MCP - 知识源"""

    def __init__(self):
        self.name = "Wikipedia MCP"
        self.color = "#1976d2"
        self.css_class = "wikipedia"

    def query(self, term):
        """查询Wikipedia（示例实现）"""
        # 实际应用中应调用Wikipedia API
        examples = {
            "AI": {
                "title": "Artificial Intelligence",
                "summary": "人工智能是指由机器展现的智能",
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
            }
        }
        return examples.get(term, {})

class SQLiteMCP:
    """SQLite MCP - 数据管理"""

    def __init__(self, db_path=None):
        """初始化SQLite MCP

        Args:
            db_path: 数据库路径（可选）。如果只提供文件名，会在当前目录创建
        """
        import os

        self.name = "SQLite MCP"
        self.color = "#7b1fa2"
        self.css_class = "sqlite"

        # 如果没有指定路径或只指定了文件名，在当前目录创建
        if db_path is None:
            self.db_path = os.path.join(os.getcwd(), 'articles.db')
        elif not os.path.isabs(db_path):
            self.db_path = os.path.join(os.getcwd(), db_path)
        else:
            self.db_path = db_path

        self.conn = None
        self.cursor = None

    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """创建表结构"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS refs (
                id INTEGER PRIMARY KEY,
                article_id INTEGER,
                source_name TEXT,
                url TEXT
            )
        ''')
        self.conn.commit()

    def insert_article(self, title, content):
        """插入文章"""
        self.cursor.execute('''
            INSERT INTO articles (title, content, created_at)
            VALUES (?, ?, ?)
        ''', (title, content, datetime.now()))
        return self.cursor.lastrowid

    def insert_ref(self, article_id, source_name, url):
        """插入引用"""
        self.cursor.execute('''
            INSERT INTO refs (article_id, source_name, url)
            VALUES (?, ?, ?)
        ''', (article_id, source_name, url))
        self.conn.commit()

    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()

class FilesystemMCP:
    """Filesystem MCP - 文档生成"""

    def __init__(self):
        self.name = "Filesystem MCP"
        self.color = "#388e3c"
        self.css_class = "filesystem"

    def generate_html(self, title, sections, output_path=None):
        """生成HTML文档

        Args:
            title: 文章标题
            sections: 章节列表
            output_path: 输出路径（可选）。如果只提供文件名，会在当前目录的output子目录下创建
        """
        import os

        # 如果没有指定完整路径，在当前目录创建output子目录
        if output_path is None:
            output_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{title}.html"
            output_path = os.path.join(output_dir, filename)
        elif not os.path.isabs(output_path):
            # 如果是相对路径，在当前目录的output子目录下创建
            output_dir = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_path)

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {self.get_css()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p class="meta">生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="content">
            {self._generate_sections(sections)}
        </div>

        <div class="footer">
            <p>由MCP自动化系统生成</p>
        </div>
    </div>
</body>
</html>
"""

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return html

    def get_css(self):
        """获取CSS样式"""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.8;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }

        .content { padding: 40px; }

        h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }

        .mcp-section {
            margin: 30px 0;
            padding: 20px;
            border-radius: 8px;
            position: relative;
        }

        .mcp-section-wikipedia {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left: 5px solid #1976d2;
        }

        .mcp-section-sqlite {
            background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
            border-left: 5px solid #7b1fa2;
        }

        .mcp-section-filesystem {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            border-left: 5px solid #388e3c;
        }

        .mcp-label {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 600;
        }

        .mcp-wikipedia {
            background: #e3f2fd;
            color: #1976d2;
            border: 2px solid #1976d2;
        }

        .mcp-sqlite {
            background: #f3e5f5;
            color: #7b1fa2;
            border: 2px solid #7b1fa2;
        }

        .mcp-filesystem {
            background: #e8f5e9;
            color: #388e3c;
            border: 2px solid #388e3c;
        }

        .footer {
            background: #f5f5f5;
            padding: 30px;
            text-align: center;
        }
        """

    def _generate_sections(self, sections):
        """生成HTML章节"""
        html = ""
        for section in sections:
            mcp_class = section['mcp_type']
            label = section['label']
            content = section['content']

            html += f"""
            <div class="mcp-section mcp-section-{mcp_class}">
                <div class="mcp-label mcp-{mcp_class}">{label}</div>
                {content}
            </div>
            """
        return html

# ==================== 主函数 ====================

def main():
    """主函数"""

    # 1. 初始化MCP服务器
    wiki_mcp = WikipediaMCP()
    sqlite_mcp = SQLiteMCP(CONFIG['db_name'])
    fs_mcp = FilesystemMCP()

    # 2. 连接数据库
    sqlite_mcp.connect()
    sqlite_mcp.create_tables()

    # 3. 准备内容章节
    sections = []

    # Wikipedia MCP - 知识内容
    ai_info = wiki_mcp.query("AI")
    sections.append({
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': f"""
            <h2>什么是AI？</h2>
            <p>{ai_info.get('summary', '')}</p>
            <p>参考: <a href="{ai_info.get('url', '')}" target="_blank">{ai_info.get('title', '')}</a></p>
        """
    })

    # SQLite MCP - 数据统计
    sections.append({
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 数据管理',
        'content': """
            <h2>数据统计</h2>
            <p>本文使用SQLite MCP管理所有数据。</p>
        """
    })

    # Filesystem MCP - 内容生成
    sections.append({
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 内容生成',
        'content': """
            <h2>文档说明</h2>
            <p>本文档由Filesystem MCP生成，展示了MCP服务器的协作能力。</p>
        """
    })

    # 4. 生成HTML
    output_path = os.path.join(CONFIG['output_dir'], 'article.html')
    os.makedirs(CONFIG['output_dir'], exist_ok=True)

    html_content = fs_mcp.generate_html(
        CONFIG['article_title'],
        sections,
        output_path
    )

    # 5. 保存到数据库
    article_id = sqlite_mcp.insert_article(CONFIG['article_title'], html_content)

    # 6. 添加引用
    if ai_info.get('url'):
        sqlite_mcp.insert_ref(article_id, ai_info['title'], ai_info['url'])

    # 7. 清理
    sqlite_mcp.close()

    print(f"[OK] HTML文档已生成: {output_path}")
    print(f"[OK] 文章已保存到数据库，ID: {article_id}")

if __name__ == "__main__":
    main()
