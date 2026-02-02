#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改后的skill - 在当前目录生成output
"""

import sys
from pathlib import Path

# 添加Skill路径
skill_path = Path(__file__).parent / 'skills' / 'html-document-generator'
sys.path.insert(0, str(skill_path))

from template import FilesystemMCP, SQLiteMCP, WikipediaMCP
import os

print("="*60)
print("测试在当前目录生成文件")
print("="*60)
print(f"当前工作目录: {os.getcwd()}")
print()

# 初始化MCP（不传参数，使用默认当前目录）
sqlite_mcp = SQLiteMCP()
print(f"数据库位置: {sqlite_mcp.db_path}")

sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备简单的测试内容
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>测试文章</h2>
            <p>这是一个测试，验证文件是否在当前目录生成。</p>
            <p><strong>当前目录</strong>: {os.getcwd()}</p>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 内容生成',
        'content': '''
            <h2>测试内容</h2>
            <p>这个文件应该生成在当前工作目录的 <code>output</code> 子目录中。</p>
            <p>数据库也应该在当前工作目录中。</p>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 数据管理',
        'content': '''
            <h2>测试结果</h2>
            <p>✅ HTML文件位置: <code>output/测试文章.html</code></p>
            <p>✅ 数据库位置: <code>articles.db</code></p>
        '''
    }
]

# 生成HTML（不传output_path参数）
print("\n生成HTML文档...")
fs_mcp = FilesystemMCP()
html_content = fs_mcp.generate_html(
    title='测试文章',
    sections=sections
    # 不传output_path，使用默认
)

print(f"HTML文件大小: {len(html_content)} 字符")

# 保存到数据库
print("\n保存到数据库...")
article_id = sqlite_mcp.insert_article('测试文章', html_content)
print(f"文章ID: {article_id}")

sqlite_mcp.close()

print("\n" + "="*60)
print("测试完成！")
print("="*60)
print(f"检查当前目录: {os.getcwd()}")
print(f"  - output/测试文章.html")
print(f"  - articles.db")
print("="*60)

# 列出实际生成的文件
print("\n实际生成的文件:")
if os.path.exists('output'):
    for f in os.listdir('output'):
        print(f"  - output/{f}")
else:
    print("  [output目录不存在]")

if os.path.exists('articles.db'):
    print(f"  - articles.db ({os.path.getsize('articles.db')} bytes)")
else:
    print("  [articles.db不存在]")
