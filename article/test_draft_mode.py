#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试草稿完善功能 - 生成完整文章"""

import os
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator
from pathlib import Path

# 读取草稿内容
with open('draft.txt', 'r', encoding='utf-8') as f:
    draft_content = f.read()

print("="*80)
print("测试草稿完善功能")
print("="*80)
print(f"\n草稿内容 ({len(draft_content)}字)")
print(f"\n开始AI完善...\n")

# 创建生成器
generator = ToutiaoArticleGenerator()

# 完善草稿
article = generator.improve_article_draft(draft_content, target_length=2000)

print("\n"+"="*80)
print("完善成功!")
print("="*80)
print(f"标题: {article['title']}")
print(f"字数: {article['word_count']}")

# 保存文件
tool_dir = Path(__file__).parent
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_prefix = "文章草稿完善"

# Markdown文件
md_filename = f"{file_prefix}_未来图书馆_{timestamp}.md"
md_path = tool_dir / md_filename

# 生成Markdown内容
md_content = f"""# {article['title']}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {article['word_count']}字
**来源**: 基于用户草稿AI完善

---

{article['content']}

---

*本文由AI基于用户草稿完善生成*
"""

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\n[成功] Markdown文件已保存: {md_filename}")

# 生成HTML文件
html_filename = f"{file_prefix}_未来图书馆_{timestamp}.html"
html_path = tool_dir / html_filename

html_content = generator.create_article_html(
    article['title'],
    article['content'],
    "未来图书馆",
    images=None
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[成功] HTML文件已保存: {html_filename}")

# 自动打开HTML文件
try:
    import webbrowser
    webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
    print(f"[成功] 已在浏览器中打开文章预览")
except:
    print(f"[提示] 请手动打开HTML文件查看文章: {html_path}")

print("\n生成完成!")
print(f"[文件] 文章: {md_filename}")
print(f"[文件] HTML: {html_filename}")
print("="*80)
