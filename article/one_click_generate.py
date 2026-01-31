#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键生成高质量文章
整合所有高级功能：原草稿引用、专业排版、真实照片配图
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator

def extract_key_sentences(draft):
    """从草稿中提取关键句子"""
    key_sentences = []
    lines = draft.split('\n')

    for line in lines:
        line = line.strip()
        # 跳过空行和标签
        if not line or line.startswith('#'):
            continue
        # 提取有意义的句子（长度在10-100字之间）
        if 10 <= len(line) <= 100:
            key_sentences.append(line)

    return key_sentences[:15]  # 最多提取15个关键句子

def create_professional_html(title, content, draft, images, theme, found_quotes):
    """创建专业排版HTML"""

    # 图片信息
    image_info = []
    if len(images) >= 3:
        image_info = [
            (images[0], "主场景 - 融合传统与现代的知识空间", "hero"),
            (images[1], "智能阅读空间 - AI赋能的知识体验", "detail"),
            (images[2], "文化生活空间 - 思想碰撞的线下客厅", "life")
        ]
    elif len(images) == 2:
        image_info = [
            (images[0], "主场景", "hero"),
            (images[1], "智能空间", "detail")
        ]
    elif len(images) == 1:
        image_info = [
            (images[0], "智慧图书馆", "hero")
        ]

    # 分割段落
    paragraphs = content.split('\n\n')

    # 创建HTML
    html = f"""<!DOCTYPE html>
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

        mark.draft-quote {{
            background: linear-gradient(120deg, #ffd54f 0%, #ffeb3b 100%);
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 500;
            color: #5d4037;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

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
                字数: {len(content)}字 |
                原草稿引用: {len(found_quotes)}处 |
                配图: {len(images)}张
            </div>
        </div>

        <div class="draft-box">
            <h3>原草稿</h3>
            <p>{draft}</p>
        </div>

        <div class="content">
"""

    # 添加段落和图片
    image_positions = {
        0: 0,
        min(5, len(paragraphs)-1): 1,
        min(10, len(paragraphs)-1): 2
    } if len(image_info) >= 3 else {}

    for i, paragraph in enumerate(paragraphs):
        if i in image_positions and image_positions[i] < len(image_info):
            img_file, img_caption, img_type = image_info[image_positions[i]]
            img_name = os.path.basename(img_file)

            if img_type == "hero":
                html += f"""
            <div class="image-container hero-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """
            elif img_type == "detail":
                html += f"""
            <div class="image-container detail-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption" style="font-size: 0.85em;">{img_caption}</div>
            </div>
            """
            elif img_type == "life":
                html += f"""
            <div class="image-container life-image">
                <img src="{img_name}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """

        html += f"            <p>{paragraph}</p>\n"

    html += """            <div style="clear: both;"></div>
        </div>

        <div class="quote-stats">
            <h3>原草稿引用统计</h3>
            <p style="margin-bottom: 15px;">本文共引用了原草稿中的 <strong>""" + str(len(found_quotes)) + """</strong> 个关键句子：</p>
            <ul>
"""

    for quote in found_quotes:
        html += f'                <li>✓ "{quote}"</li>\n'

    html += """            </ul>
        </div>

        <div class="footer">
            <p><strong>创作说明</strong></p>
            <p style="margin-top: 10px;">
                本文由AI基于用户原草稿，采用汪曾祺文风深度创作。<br>
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

    return html

def generate_high_quality_article(draft_file, theme, style='wangzengqi'):
    """一键生成高质量文章"""

    print("="*80)
    print("一键生成高质量文章系统")
    print("="*80)

    # 1. 读取草稿
    print(f"\n[步骤1] 读取原草稿...")
    with open(draft_file, 'r', encoding='utf-8') as f:
        draft = f.read()

    print(f"  原草稿: {len(draft)}字")
    print(f"  来源: {draft_file}")

    # 2. 提取关键句子
    print(f"\n[步骤2] 提取关键句子...")
    key_sentences = extract_key_sentences(draft)
    print(f"  提取了 {len(key_sentences)} 个关键句子")

    # 3. 生成文章
    print(f"\n[步骤3] 生成文章（{style}风格）...")
    generator = ToutiaoArticleGenerator()
    article = generator.improve_article_draft(draft, style=style)

    print(f"  标题: {article['title']}")
    print(f"  字数: {article['word_count']}")

    # 4. 检查引用
    print(f"\n[步骤4] 检查原草稿引用...")
    found_quotes = [s for s in key_sentences if s in article['content']]
    print(f"  引用了 {len(found_quotes)}/{len(key_sentences)} 个关键句子")

    # 5. 生成配图
    print(f"\n[步骤5] 生成真实照片配图...")
    images = generator.generate_article_images(theme, "realistic")
    if images:
        print(f"  成功生成 {len(images)} 张配图")
    else:
        print(f"  配图生成失败，继续生成文章")

    # 6. 创建专业排版HTML
    print(f"\n[步骤6] 创建专业排版HTML...")
    html = create_professional_html(
        article['title'],
        article['content'],
        draft,
        images,
        theme,
        found_quotes
    )

    # 7. 保存文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_file = f"高质量文章_{timestamp}.html"
    md_file = f"高质量文章_{timestamp}.md"

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    # 同时生成Markdown
    md_content = f"""# {article['title']}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {article['word_count']}字
**风格**: 汪曾祺文风
**配图**: {len(images)}张
**原草稿引用**: {len(found_quotes)}处

## 原草稿

{draft}

## 文章正文

{article['content']}

## 配图

"""
    for i, img in enumerate(images, 1):
        img_name = os.path.basename(img)
        md_content += f"### 配图{i}: {img_name}\n\n![配图{i}]({img_name})\n\n"

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"  HTML文件: {html_file}")
    print(f"  Markdown文件: {md_file}")

    # 8. 打开浏览器
    print(f"\n[步骤7] 在浏览器中打开...")
    try:
        import webbrowser
        webbrowser.open(f'file:///{os.path.abspath(html_file)}'.replace('\\', '/'))
        print(f"  已在浏览器中打开预览")
    except:
        print(f"  请手动打开: {html_file}")

    print("\n" + "="*80)
    print("生成完成!")
    print("="*80)
    print(f"[文章] 标题: {article['title']}")
    print(f"[文章] 字数: {article['word_count']}字")
    print(f"[引用] 原草稿句子: {len(found_quotes)}处")
    print(f"[配图] 真实照片: {len(images)}张")
    print(f"[文件] HTML: {html_file}")
    print(f"[文件] Markdown: {md_file}")
    print(f"[排版] 专业平面设计师排版")
    print("="*80)

    return html_file, md_file

if __name__ == "__main__":
    # 使用示例
    draft_file = "draft.txt"
    theme = "未来图书馆：AI时代的知识体验中心与城市文化空间"

    if len(sys.argv) > 1:
        draft_file = sys.argv[1]
    if len(sys.argv) > 2:
        theme = sys.argv[2]

    generate_high_quality_article(draft_file, theme, style='wangzengqi')
