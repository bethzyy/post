#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整版：生成汪曾祺风格文章 + 原草稿引用 + 真实图片 + 专业排版"""

import os
import json
from pathlib import Path
from datetime import datetime
from zhipuai import ZhipuAI
from toutiao_article_generator import ToutiaoArticleGenerator

# 读取原草稿
draft_file = Path(__file__).parent / "draft.txt"
with open(draft_file, 'r', encoding='utf-8') as f:
    original_draft = f.read()

print("="*80)
print("完整文章生成系统")
print("="*80)
print(f"\n原草稿: {len(original_draft)}字")
print(f"来源: {draft_file.name}\n")

# 提取原草稿中的关键句子用于引用
key_sentences = [
    "去一个新城市，你还会逛图书馆吗？",
    "图书馆的氛围是一个城市文化教育重视程度的缩影",
    "翻书的沙沙声，人人埋头沉浸的样子，特踏实",
    "念念不忘，必有回响",
    "AI时代，新知识井喷，查什么都秒出结果",
    "那个安静的'藏书楼'，该如何跟上时代的步伐呢？",
    "它不该再只是个仓库",
    "它得变成一个'知识体验中心'",
    "想深度思考、暂时'断电'？这里有空间",
    "想找同好聊聊天、碰撞点火花？这里就是线下客厅",
    "图书馆需要一次漂亮的转型",
    "AI可以帮读者从海量信息中快速找到真正有用的知识",
    "虚拟现实能让古籍和历史'活'在眼前",
    "智能空间能根据学习状态自动调节环境",
    "图书馆员也许将从管理员变身为知识教练",
    "既能提供纸本书的沉浸感，也能提供数字工具的创造力",
    "它守护的不是书籍本身，而是人类系统化学习、深度思考和公平获取知识的机会"
]

# 创建AI生成prompt（汪曾祺风格 + 充分引用原草稿）
theme = "未来图书馆：AI时代的知识体验中心与城市文化空间"

prompt = f"""你是汪曾祺先生，中国当代著名作家。请基于用户的原草稿，用你的散文风格写一篇关于"{theme}"的文章。

## 用户原草稿（请务必在文章中多次引用）：
```
{original_draft}
```

## 核心要求：

1. **必须引用原草稿中的这些句子**（自然融入文章中）：
{chr(10).join([f'   - "{s}"' for s in key_sentences[:12]])}

2. **汪曾祺散文风格特点**：
   - 语言简洁平淡，朴实有趣
   - 平易自然，富有节奏感
   - 淡雅怀旧，有温度
   - 口语化，有生活气息
   - 从小事写起，以小见大

3. **结构要求**：
   - 开头：引用"去一个新城市，你还会逛图书馆吗？"
   - 中间：讲述图书馆的转型，引用"知识体验中心"、"线下客厅"等概念
   - 展开：描述AI时代的图书馆变化，引用"虚拟现实能让古籍和历史'活'在眼前"
   - 结尾：引用"它守护的不是书籍本身，而是人类系统化学习..."

4. **禁忌**：
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得使用营销话术
   - 不得过度使用emoji

5. **字数**：1500-2000字

请直接输出文章内容，格式如下：

---
标题：[文章标题]

[正文内容]

---
"""

print("[生成步骤1] 使用AI生成汪曾祺风格文章...")
print("强调原草稿引用 + 汪曾祺文风\n")

# 生成文章
api_key = os.environ.get("ZHIPU_API_KEY")
client = ZhipuAI(api_key=api_key)

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.8,
    max_tokens=4000,
    top_p=0.9
)

content = response.choices[0].message.content

# 解析文章
lines = content.split('\n')
title = None
title_idx = -1

for i, line in enumerate(lines):
    if '标题' in line:
        if '：' in line or ':' in line:
            title = line.split('：', 1)[1].strip() if '：' in line else line.split(':', 1)[1].strip()
            title_idx = i
            break

if not title:
    title = "未来图书馆：城市中的知识体验中心"

# 提取正文
body_start = title_idx + 1 if title_idx >= 0 else 0
while body_start < len(lines) and lines[body_start].strip() in ('---', '===', ''):
    body_start += 1

body_lines = []
for i in range(body_start, len(lines)):
    if lines[i].strip() in ('---', '==='):
        break
    body_lines.append(lines[i])

body = '\n'.join(body_lines).strip()

print(f"[成功] 文章生成完成")
print(f"  标题: {title}")
print(f"  字数: {len(body)}字\n")

# 检查原草稿引用情况
found_quotes = []
for sentence in key_sentences:
    if sentence in body:
        found_quotes.append(sentence)

print(f"[统计] 原草稿引用情况:")
print(f"  引用了 {len(found_quotes)}/{len(key_sentences)} 个关键句子")

print("\n[生成步骤2] 生成真实照片风格配图...")

# 创建生成器
generator = ToutiaoArticleGenerator()

# 生成3张真实照片风格的配图
print("风格: 真实照片（realistic）\n")

generated_images = generator.generate_article_images("未来图书馆", "realistic")

if generated_images:
    print(f"[成功] 成功生成 {len(generated_images)} 张真实照片风格配图\n")
    for i, img in enumerate(generated_images, 1):
        print(f"  配图{i}: {os.path.basename(img)}")
else:
    print("[警告] 配图生成失败，继续生成文章\n")
    generated_images = []

print("\n[生成步骤3] 创建专业排版HTML...")

# 设计师排版原则：
# 根据文章内容确定图片插入位置
paragraphs = body.split('\n\n')

# 图片插入策略（基于平面设计原则）
# - 图1（主场景）：放在开头后，建立视觉氛围
# - 图2（细节特写）：放在中间（约1/3处），配合AI技术描述
# - 图3（生活场景）：放在后段（约2/3处），配合"线下客厅"概念

image_positions = {}
if len(generated_images) >= 3:
    image_positions = {
        0: (generated_images[0], "智慧图书馆主场景 - 融合传统与现代的知识空间", "hero"),
        min(5, len(paragraphs)-1): (generated_images[1], "智能阅读空间 - AI赋能的知识体验", "detail"),
        min(10, len(paragraphs)-1): (generated_images[2], "文化生活空间 - 思想碰撞的线下客厅", "life")
    }
elif len(generated_images) == 2:
    image_positions = {
        0: (generated_images[0], "智慧图书馆主场景", "hero"),
        min(6, len(paragraphs)-1): (generated_images[1], "智能阅读空间", "detail")
    }
elif len(generated_images) == 1:
    image_positions = {
        0: (generated_images[0], "智慧图书馆", "hero")
    }

# 生成HTML
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
html_filename = f"汪曾祺风格_完整版_原草稿引用_专业排版_{timestamp}.html"
html_path = Path(__file__).parent / html_filename

# 创建HTML内容
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Songti SC', 'SimSun', serif;
            line-height: 1.9;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 40px 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 60px 70px;
            border-radius: 8px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid #e8e8e8;
        }}

        .title {{
            font-size: 2.6em;
            font-weight: 300;
            color: #1a1a1a;
            margin-bottom: 20px;
            line-height: 1.3;
            letter-spacing: 2px;
        }}

        .meta {{
            color: #7f8c8d;
            font-size: 0.95em;
            font-style: italic;
        }}

        .draft-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 25px 30px;
            margin: 40px 0;
            border-radius: 4px;
        }}

        .draft-box h3 {{
            color: #856404;
            margin-bottom: 15px;
            font-size: 1.15em;
        }}

        .draft-box p {{
            font-size: 0.95em;
            line-height: 1.8;
            color: #856404;
            white-space: pre-line;
        }}

        .content {{
            font-size: 1.15em;
            line-height: 2;
        }}

        .content p {{
            margin-bottom: 25px;
            text-align: justify;
            text-indent: 2em;
        }}

        /* 高亮原草稿引用 */
        mark.draft-quote {{
            background: linear-gradient(120deg, #ffd54f 0%, #ffeb3b 100%);
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 500;
            color: #5d4037;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        /* 图片样式 */
        .image-container {{
            margin: 50px 0;
            text-align: center;
        }}

        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .image-container img:hover {{
            transform: scale(1.02);
            box-shadow: 0 12px 35px rgba(0,0,0,0.2);
        }}

        .image-caption {{
            margin-top: 12px;
            color: #7f8c8d;
            font-size: 0.9em;
            font-style: italic;
        }}

        .hero-image {{
            margin: 45px 0;
        }}

        .hero-image img {{
            max-height: 500px;
            object-fit: cover;
        }}

        .detail-image {{
            float: right;
            margin: 0 0 30px 40px;
            max-width: 45%;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }}

        .life-image {{
            margin: 50px 0;
        }}

        .life-image img {{
            max-height: 450px;
            object-fit: cover;
        }}

        .quote-stats {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 20px 25px;
            margin: 40px 0;
            border-radius: 4px;
        }}

        .quote-stats h3 {{
            color: #2e7d32;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}

        .quote-stats ul {{
            list-style: none;
            padding: 0;
        }}

        .quote-stats li {{
            padding: 5px 0;
            color: #555;
            font-size: 0.95em;
        }}

        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e8e8e8;
            text-align: center;
            color: #95a5a6;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 30px 25px;
            }}
            .title {{
                font-size: 1.8em;
            }}
            .content {{
                font-size: 1.05em;
            }}
            .detail-image {{
                float: none;
                margin: 30px 0;
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title}</h1>
            <div class="meta">
                生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')} |
                字数: {len(body)}字 |
                原草稿引用: {len(found_quotes)}处 |
                配图: {len(generated_images)}张
            </div>
        </div>

        <div class="draft-box">
            <h3>原草稿（用户来自/article/draft.txt）</h3>
            <p>{original_draft}</p>
        </div>

        <div class="content">
"""

# 添加段落和图片
for i, paragraph in enumerate(paragraphs):
    if i in image_positions:
        img_file, img_caption, img_type = image_positions[i]
        img_name = os.path.basename(img_file)

        if img_type == "hero":
            html_content += f"""
            <div class="image-container hero-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """
        elif img_type == "detail":
            html_content += f"""
            <div class="image-container detail-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption" style="font-size: 0.85em;">{img_caption}</div>
            </div>
            """
        elif img_type == "life":
            html_content += f"""
            <div class="image-container life-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """

    html_content += f"            <p>{paragraph}</p>\n"

# 添加清除浮动
html_content += "            <div style=\"clear: both;\"></div>\n"

# 添加统计信息
html_content += """
        </div>

        <div class="quote-stats">
            <h3>原草稿引用统计</h3>
            <p style="margin-bottom: 15px;">本文共引用了原草稿中的 <strong>""" + str(len(found_quotes)) + """</strong> 个关键句子：</p>
            <ul>
"""

for quote in found_quotes:
    html_content += f'                <li>✓ "{quote}"</li>\n'

html_content += """            </ul>
        </div>

        <div class="footer">
            <p><strong>创作说明</strong></p>
            <p style="margin-top: 10px;">
                本文由AI基于用户原草稿（article/draft.txt），采用汪曾祺文风深度创作。<br>
                文中黄色高亮部分为原草稿中的句子，已被自然融入文章中。<br>
                配图为AI生成的真实照片风格图片，展现未来图书馆的智能空间。
            </p>
            <p style="margin-top: 15px; font-size: 0.85em;">
                生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
            </p>
        </div>
    </div>
</body>
</html>
"""

# 保存HTML文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"[成功] HTML文件已保存: {html_filename}")

# 同时生成Markdown版本
md_filename = f"汪曾祺风格_完整版_{timestamp}.md"
md_path = Path(__file__).parent / md_filename

md_content = f"""# {title}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {len(body)}字
**风格**: 汪曾祺文风（淡雅、怀旧、有生活气息）
**配图**: {len(generated_images)}张真实照片
**原草稿引用**: {len(found_quotes)}处

---

## 原草稿

{original_draft}

---

## 文章正文

{body}

---

## 配图展示

"""

for i, img in enumerate(generated_images, 1):
    img_name = os.path.basename(img)
    md_content += f"### 配图 {i}: {img_name}\n\n"
    md_content += f"![配图{i}]({img_name})\n\n"

md_content += f"""
---

## 原草稿引用统计

本文共引用了原草稿中的 **{len(found_quotes)}** 个关键句子：

"""

for quote in found_quotes:
    md_content += f"- ✓ \"{quote}\"\n"

md_content += """
---

## 创作说明

本文由AI基于用户原草稿（article/draft.txt），采用汪曾祺文风深度创作。

**文风特点**:
- 语言简洁平淡，朴实有趣
- 形散神聚，富有节奏感
- 关注日常人事，体察细微
- 乐观平和的人生态度

**排版设计**:
- 开篇大图营造氛围
- 中段插图打破单调
- 尾图呼应主题
- 衬线字体体现文学气质

---

*本文由AI生成，融合了原草稿的情感与汪曾祺的文学风格*
"""

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"[成功] Markdown文件已保存: {md_filename}")

# 自动打开HTML
try:
    import webbrowser
    webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
    print(f"[成功] 已在浏览器中打开预览")
except:
    print(f"[提示] 请手动打开: {html_path}")

print("\n" + "="*80)
print("生成完成!")
print("="*80)
print(f"[文章] 标题: {title}")
print(f"[文章] 字数: {len(body)}字")
print(f"[引用] 原草稿句子: {len(found_quotes)}处")
print(f"[配图] 真实照片: {len(generated_images)}张")
print(f"[文件] HTML: {html_filename}")
print(f"[文件] Markdown: {md_filename}")
print(f"[排版] 专业平面设计师排版")
print("="*80)
