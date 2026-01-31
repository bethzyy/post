#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成高质量今日头条文章 - 资深写手风格 + 配图"""

import os
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator
from pathlib import Path

# 读取草稿内容
with open('draft_v2.txt', 'r', encoding='utf-8') as f:
    draft_content = f.read()

print("="*80)
print("生成高质量今日头条文章")
print("="*80)
print(f"\n草稿字数: {len(draft_content)}字")
print("\n开始AI完善（资深写手风格）...\n")

# 创建生成器
generator = ToutiaoArticleGenerator()

# 完善草稿 - 使用资深写手风格
article = generator.improve_article_draft(draft_content, target_length=2000, style='professional')

print("\n"+"="*80)
print("文章完善成功!")
print("="*80)
print(f"标题: {article['title']}")
print(f"字数: {article['word_count']}")

# 生成配图
print("\n开始生成配图...")
print("风格: 艺术创作（符合深度文章调性）\n")

generated_images = generator.generate_article_images("未来图书馆", "artistic")

if generated_images:
    print(f"\n[成功] 成功生成 {len(generated_images)} 张配图")
else:
    print("\n[警告] 配图生成失败,但文章已成功生成")

# 保存文件
tool_dir = Path(__file__).parent
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_prefix = "文章草稿完善"

# Markdown文件
md_filename = f"{file_prefix}_未来图书馆_深度版_{timestamp}.md"
md_path = tool_dir / md_filename

# 生成Markdown内容（包含配图信息）
md_content = f"""# {article['title']}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {article['word_count']}字
**来源**: 基于用户草稿AI完善（资深写手风格）
**配图**: {len(generated_images) if generated_images else 0}张

---

{article['content']}

---

## 配图

"""

if generated_images:
    for i, img in enumerate(generated_images, 1):
        md_content += f"### 配图 {i}\n\n![配图{i}]({img})\n\n"

md_content += "\n---\n\n*本文由AI基于用户草稿完善生成，采用资深写手风格，注重思想深度和语言优美度*\n"

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\n[成功] Markdown文件已保存: {md_filename}")

# 生成HTML文件（包含配图）
html_filename = f"{file_prefix}_未来图书馆_深度版_{timestamp}.html"
html_path = tool_dir / html_filename

html_content = generator.create_article_html(
    article['title'],
    article['content'],
    "未来图书馆",
    images=generated_images  # 包含配图
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
if generated_images:
    print(f"[配图] 配图: {len(generated_images)}张")
print("="*80)
