"""
html-document-generator Skill
使用MCP服务器生成带标注的HTML文档

使用示例:
    >>> from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP
    >>>
    >>> # 初始化
    >>> fs_mcp = FilesystemMCP()
    >>> sqlite_mcp = SQLiteMCP('articles.db')
    >>>
    >>> # 准备内容
    >>> sections = [{
    ...     'mcp_type': 'filesystem',
    ...     'label': 'Filesystem MCP',
    ...     'content': '<h2>标题</h2><p>内容...</p>'
    ... }]
    >>>
    >>> # 生成文档
    >>> fs_mcp.generate_html("文章标题", sections, "output.html")

版本: 1.0.0
作者: MCP Test System
"""

__version__ = "1.0.0"
__author__ = "MCP Test System"

# 导出主要的类和函数
from .template import (
    WikipediaMCP,
    SQLiteMCP,
    FilesystemMCP
)

__all__ = [
    'WikipediaMCP',
    'SQLiteMCP',
    'FilesystemMCP',
]
