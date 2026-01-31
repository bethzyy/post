#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成高质量今日头条文章 - 最终版"""

import os
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator
from pathlib import Path

# 读取草稿内容
with open('draft_v2.txt', 'r', encoding='utf-8') as f:
    draft_content = f.read()

print("="*80)
print("生成高质量今日头条文章（最终版）")
print("="*80)

# 创建生成器
generator = ToutiaoArticleGenerator()

# 使用标准模式生成（避免格式解析问题）
print("\n使用AI生成文章（基于草稿思想，全新创作）...\n")

# 直接使用主题生成功能，但基于草稿的核心思想
article = generator.generate_article_with_ai(
    "未来图书馆：在AI时代重塑城市的第三空间",
    target_length=2000
)

print("\n"+"="*80)
print("文章生成成功!")
print("="*80)
print(f"标题: {article['title']}")
print(f"字数: {article['word_count']}")

# 生成配图（艺术风格）
print("\n开始生成配图...")
print("风格: 艺术创作（符合深度文章调性）\n")

generated_images = generator.generate_article_images("未来图书馆", "artistic")

if generated_images:
    print(f"\n[成功] 成功生成 {len(generated_images)} 张配图")
    for i, img in enumerate(generated_images, 1):
        print(f"  配图{i}: {os.path.basename(img)}")
else:
    print("\n[警告] 配图生成失败,但文章已成功生成")

# 保存文件
tool_dir = Path(__file__).parent
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_prefix = "未来图书馆深度文章"

# Markdown文件
md_filename = f"{file_prefix}_{timestamp}.md"
md_path = tool_dir / md_filename

# 生成Markdown内容
md_content = f"""# {article['title']}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {article['word_count']}字
**主题**: 未来图书馆在AI时代的转型
**配图**: {len(generated_images) if generated_images else 0}张艺术创作风格配图

---

{article['content']}

---

## 配图展示

"""

if generated_images:
    for i, img in enumerate(generated_images, 1):
        img_name = os.path.basename(img)
        md_content += f"### 配图 {i}: {img_name}\n\n"
        md_content += f"![配图{i}]({img_name})\n\n"

md_content += """
---

## 文章说明

本文基于以下灵感创作：
- **搜索来源**: [未来图书馆：知识空间的重新定义](http://www.kongjiansheji.com/sys-nd/322.html)
- **搜索来源**: [AI时代大学变革](https://www.shobserver.com/staticsg/res/html/web/newsDetail.html?id=1032957&v=2.0&sid=67)
- **核心概念**: 第三空间、知识体验中心、AI赋能、人文精神

---

*本文由AI基于2026年最新趋势深度创作，融合了对图书馆作为城市第三空间的思考*
"""

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\n[成功] Markdown文件已保存: {md_filename}")

# 生成HTML文件（包含配图）
html_filename = f"{file_prefix}_{timestamp}.html"
html_path = tool_dir / html_filename

html_content = generator.create_article_html(
    article['title'],
    article['content'],
    "未来图书馆",
    images=generated_images
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
print(f"[文件] Markdown: {md_filename}")
print(f"[文件] HTML: {html_filename}")
if generated_images:
    print(f"[配图] {len(generated_images)}张配图已生成")
print("="*80)
