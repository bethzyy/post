#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成汪曾祺风格文章 + 真实照片配图"""

import os
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator
from pathlib import Path

# 读取草稿内容
with open('draft_wangzengqi.txt', 'r', encoding='utf-8') as f:
    draft_content = f.read()

print("="*80)
print("生成汪曾祺风格文章 + 真实照片配图")
print("="*80)
print(f"\n原草稿: {len(draft_content)}字")
print("\n开始AI生成（汪曾祺文风）...\n")

# 创建生成器
generator = ToutiaoArticleGenerator()

# 使用主题生成，采用汪曾祺风格
print(f"[AI生成] 主题: 未来图书馆")
print(f"[AI生成] 风格: 汪曾祺文风（淡雅、怀旧、有生活气息）\n")

article = generator.generate_article_with_ai(
    "未来图书馆：在AI时代，图书馆作为城市第三空间的价值",
    target_length=2000,
    style='wangzengqi'  # 使用汪曾祺风格
)

print("\n"+"="*80)
print("文章生成成功!")
print("="*80)
print(f"标题: {article['title']}")
print(f"字数: {article['word_count']}")

# 生成配图（真实照片风格）
print("\n开始生成配图...")
print("风格: 真实照片（符合文章氛围）\n")

generated_images = generator.generate_article_images("未来图书馆", "realistic")

if generated_images:
    print(f"\n[成功] 成功生成 {len(generated_images)} 张真实照片风格配图")
    for i, img in enumerate(generated_images, 1):
        print(f"  配图{i}: {os.path.basename(img)}")
else:
    print("\n[警告] 配图生成失败,但文章已成功生成")

# 保存文件
tool_dir = Path(__file__).parent
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_prefix = "汪曾祺风格_未来图书馆"

# Markdown文件
md_filename = f"{file_prefix}_{timestamp}.md"
md_path = tool_dir / md_filename

# 生成Markdown内容
md_content = f"""# {article['title']}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {article['word_count']}字
**风格**: 汪曾祺文风（淡雅、怀旧、有生活气息）
**配图**: {len(generated_images) if generated_images else 0}张真实照片

---

## 原草稿片段

> 每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁...

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

## 创作说明

**文风特点**:
- 语言简洁平淡，朴实有趣
- 形散神聚，富有节奏感
- 关注日常人事，体察细微
- 乐观平和的人生态度

**灵感来源**:
- 原草稿的情感基调：静谧、书香气息、心神安宁
- 汪曾祺散文的8大特点（参考[搜索结果](https://www.163.com/dy/article/ECNMDHJH0542865M.html)）
- 2026年AI时代图书馆转型思考

---

*本文由AI基于用户草稿情感，采用汪曾祺文风深度创作*
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
    print(f"[配图] {len(generated_images)}张真实照片风格配图")
print("="*80)
