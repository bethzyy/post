#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建最终的汪曾祺风格文章（包含内容和配图）"""

import os
import json
from pathlib import Path
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator

# 读取解析后的文章内容
with open('parsed_article.json', 'r', encoding='utf-8') as f:
    article_data = json.load(f)

title = article_data['title'] or '城市的第三空间：未来图书馆的沉思'
content = article_data['content']
word_count = article_data['word_count']

print(f"标题: {title}")
print(f"字数: {word_count}")
print(f"内容预览: {content[:200]}...")

# 获取之前生成的配图
tool_dir = Path(__file__).parent
image_files = []
for f in os.listdir(tool_dir):
    if f.startswith("文章配图") and f.endswith(".jpg"):
        # 只包含本次生成的图片（时间戳在15:47-15:15之间）
        if "20260130_154" in f or "20260130_1551" in f:
            image_files.append(str(tool_dir / f))

image_files.sort()

print(f"\n找到 {len(image_files)} 张配图")

# 创建生成器
generator = ToutiaoArticleGenerator()

# 生成文件时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 生成Markdown文件
md_filename = f"汪曾祺风格_未来图书馆_{timestamp}.md"
md_path = tool_dir / md_filename

md_content = f"""# {title}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {word_count}字
**风格**: 汪曾祺文风（淡雅、怀旧、有生活气息）
**配图**: {len(image_files)}张真实照片

---

## 原草稿片段

> 每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁...
> 我想象中的未来图书馆，绝不仅仅是数字化升级后的"智能书库"。它应该是一座城市的"第三空间"——不是家，不是办公室，而是属于心灵的栖息地。

---

{content}

---

## 配图展示

"""

for i, img_path in enumerate(image_files, 1):
    img_name = os.path.basename(img_path)
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

# 生成HTML文件
html_filename = f"汪曾祺风格_未来图书馆_{timestamp}.html"
html_path = tool_dir / html_filename

html_content = generator.create_article_html(
    title,
    content,
    "未来图书馆",
    images=image_files
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
print(f"[配图] {len(image_files)}张真实照片风格配图")
print(f"[字数] {word_count}字")
print("="*80)
