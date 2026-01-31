#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""专业平面设计师排版版本"""

import os
from pathlib import Path
from datetime import datetime

# 文章内容
title = "城市的第三空间：未来图书馆的沉思"
content = """每当我走进图书馆，那份特有的静谧和书香气息总能让我心神安宁。仿佛时光在这里凝固，喧嚣的尘世被隔绝在外，只剩下我与书页间微妙的对话。我常想，这不仅仅是一间藏书之地，更是一处心灵的栖息地。

如今，站在2026年的门槛上，AI时代的浪潮正席卷而来。我想象中的未来图书馆，绝不仅仅是数字化升级后的"智能书库"。它应该是一座城市的"第三空间"——不是家，不是办公室，而是属于心灵的栖息地。

在这个"第三空间"里，图书馆的职能已经超越了传统意义上的藏书与借阅。2026年的图书馆，更像是一座融合了知识、科技与人文的综合性平台。

首先，图书馆的书籍不再是简单的纸质载体。电子书、有声书、VR阅读等多种形式，让知识的获取变得更加便捷。你可以坐在舒适的沙发上，通过VR眼镜沉浸在一个虚拟的图书馆里，感受知识的海洋。

其次，图书馆的智能推荐系统将变得更加精准。根据你的阅读习惯、兴趣偏好，系统会为你推荐最适合你的书籍。甚至，当你走进图书馆时，它就能预知你的需求，为你准备好所需资料。

然而，这并不意味着纸质书籍的消失。相反，随着数字化的发展，人们对纸质书籍的热爱愈发浓厚。未来图书馆，将是一个纸质与数字化并存的空间。

在这个空间里，除了阅读，还有更多可能性。比如，你可以参加各类讲座、研讨会，与专家学者面对面交流；你可以在这里举办沙龙、分享会，与志同道合的人探讨人生、哲学、艺术等话题。

更重要的是，未来图书馆将成为一个文化交流的场所。各国文化在这里交融碰撞，为读者带来多元化的视野。在这里，你不仅能读到中国古典名著，还能领略到世界各地的文化精髓。

当然，作为一座城市的"第三空间"，未来图书馆还需具备一定的社会责任。它将关注弱势群体，为残障人士提供无障碍阅读服务；它将关注青少年成长，举办各类亲子活动，传承优秀文化。

在这个充满挑战与机遇的AI时代，未来图书馆的价值愈发凸显。它不仅为人们提供知识储备，更是一个心灵栖息地、文化交流平台、社会责任载体。

每当我走进图书馆，总能感受到一种淡淡的怀旧。那些泛黄的书籍、厚重的笔记本，仿佛在诉说着岁月的故事。而未来图书馆，则是在这个时代背景下，对传统图书馆的传承与革新。

我想，未来图书馆的价值，在于它始终关注人的内心世界。在这个喧嚣的世界里，它为我们提供一片宁静的港湾，让我们在知识的海洋中找到心灵的慰藉。

站在2026年的门槛上，我期待着未来图书馆的诞生。它将成为城市的一道风景线，见证着人类文明的进步，承载着无数人的梦想与希望。

在这个充满变化的AI时代，让我们共同期待这座"第三空间"的崛起，为我们的心灵筑起一座永恒的家园。"""

# 获取图片
tool_dir = Path(__file__).parent
image_files = [
    "文章配图1_主场景_20260130_154745.jpg",
    "文章配图2_细节特写_20260130_154913.jpg",
    "文章配图3_生活场景_20260130_155115.jpg"
]

# 设计师排版原则：
# 1. 第一张图：主场景，放在文章开头，建立视觉氛围
# 2. 第二张图：细节特写，放在文章中段（约1/3处），配合"智能推荐系统"部分
# 3. 第三张图：生活场景，放在文章后段（约2/3处），配合"文化交流场所"部分

# 分割文章段落
paragraphs = content.split('\n\n')

# 插入图片位置（基于平面设计原则）
# 图1: 在开头后（第1段后）
# 图2: 在中间（第6段后，"智能推荐系统"部分）
# 图3: 在后半部分（第10段后，"文化交流场所"部分）

image_positions = {
    0: (image_files[0], "未来图书馆的主场景 - 融合传统与现代的知识空间"),
    5: (image_files[1], "智能阅读细节 - 科技与人文的完美结合"),
    9: (image_files[2], "文化生活场景 - 读者交流与思想碰撞")
}

# 生成专业排版HTML
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
html_filename = f"汪曾祺风格_未来图书馆_专业排版_{timestamp}.html"
html_path = tool_dir / html_filename

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

        .draft-quote {{
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px 25px;
            margin: 40px 0;
            font-style: italic;
            color: #555;
            border-radius: 0 4px 4px 0;
        }}

        .draft-quote::before {{
            content: '"';
            font-size: 3em;
            color: #3498db;
            float: left;
            margin-right: 15px;
            line-height: 0.8;
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

        .content p:first-of-type::first-letter {{
            font-size: 3.5em;
            float: left;
            margin-right: 10px;
            line-height: 0.8;
            color: #2c3e50;
            font-weight: bold;
        }}

        /* 图片容器设计 */
        .image-container {{
            margin: 50px 0;
            text-align: center;
            position: relative;
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
            margin-top: 15px;
            color: #7f8c8d;
            font-size: 0.9em;
            font-style: italic;
        }}

        /* 不同图片的特殊样式 */
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

        .detail-image img {{
            border-radius: 4px;
        }}

        .life-image {{
            margin: 50px 0;
        }}

        .life-image img {{
            max-height: 450px;
            object-fit: cover;
        }}

        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e8e8e8;
            text-align: center;
            color: #95a5a6;
            font-size: 0.9em;
        }}

        .style-notes {{
            background: #fff9e6;
            border-left: 4px solid #f39c12;
            padding: 20px 25px;
            margin: 40px 0;
            border-radius: 4px;
        }}

        .style-notes h3 {{
            color: #d68910;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}

        .style-notes ul {{
            list-style: none;
            padding-left: 0;
        }}

        .style-notes li {{
            padding: 5px 0;
            color: #7f8c8d;
            font-size: 0.95em;
        }}

        .style-notes li::before {{
            content: '• ';
            color: #f39c12;
            font-weight: bold;
            margin-right: 8px;
        }}

        /* 响应式设计 */
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

        /* 打印样式 */
        @media print {{
            body {{
                background: white;
            }}

            .container {{
                box-shadow: none;
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
                风格: 汪曾祺文风
            </div>
        </div>

        <div class="draft-quote">
            <strong>原草稿片段：</strong><br>
            每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁...<br>
            我想象中的未来图书馆，绝不仅仅是数字化升级后的"智能书库"。<br>
            它应该是一座城市的"第三空间"——不是家，不是办公室，而是属于心灵的栖息地。
        </div>

        <div class="content">
"""

# 添加段落和图片
for i, paragraph in enumerate(paragraphs):
    if i in image_positions:
        img_file, img_caption = image_positions[i]

        # 根据位置选择不同的图片样式
        if i == 0:  # 第一张图 - 主场景图
            html += f"""
            <div class="image-container hero-image">
                <img src="{img_file}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """
        elif i == 5:  # 第二张图 - 细节特写（右侧浮动）
            html += f"""
            <div class="image-container detail-image">
                <img src="{img_file}" alt="{img_caption}">
                <div class="image-caption" style="font-size: 0.85em;">{img_caption}</div>
            </div>
            """
        elif i == 9:  # 第三张图 - 生活场景
            html += f"""
            <div class="image-container life-image">
                <img src="{img_file}" alt="{img_caption}">
                <div class="image-caption">{img_caption}</div>
            </div>
            """

    html += f"            <p>{paragraph}</p>\n"

# 添加清除浮动（如果使用了浮动图片）
html += """
            <div style="clear: both;"></div>
        </div>

        <div class="style-notes">
            <h3>📖 文风特点</h3>
            <ul>
                <li>语言简洁平淡，朴实有趣</li>
                <li>形散神聚，富有节奏感</li>
                <li>关注日常人事，体察细微</li>
                <li>乐观平和的人生态度</li>
            </ul>
        </div>

        <div class="style-notes" style="background: #f0f8ff; border-left-color: #3498db;">
            <h3 style="color: #2980b9;">🎨 排版设计说明</h3>
            <ul>
                <li><strong>首图布局</strong>: 开篇使用大尺寸主场景图，营造沉浸式氛围</li>
                <li><strong>中段插入</strong>: 细节特写图采用右侧浮动布局，打破单调感</li>
                <li><strong>尾图呼应</strong>: 生活场景图置于后段，呼应主题</li>
                <li><strong>字体选择</strong>: 使用衬线字体（宋体/Georgia），符合文学气质</li>
                <li><strong>色彩搭配</strong>: 渐变背景+白色卡片，现代而不失温暖</li>
                <li><strong>视觉节奏</strong>: 图片位置精心安排，形成"起-承-转-合"的视觉流</li>
            </ul>
        </div>

        <div class="footer">
            <p><strong>创作说明</strong></p>
            <p style="margin-top: 10px;">
                本文由AI基于用户草稿情感，采用汪曾祺文风深度创作。<br>
                灵感来源：原草稿的情感基调、汪曾祺散文的8大特点、2026年AI时代图书馆转型思考
            </p>
            <p style="margin-top: 15px; font-size: 0.85em;">
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </div>
</body>
</html>
"""

# 保存HTML文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n[成功] 专业排版HTML文件已生成: {html_filename}")

# 自动打开浏览器
try:
    import webbrowser
    webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
    print(f"[成功] 已在浏览器中打开预览")
except:
    print(f"[提示] 请手动打开: {html_path}")

print("\n📐 排版设计亮点:")
print("  ✓ 开篇大图: 营造氛围")
print("  ✓ 浮动插图: 打破单调")
print("  ✓ 结尾呼应: 完整收束")
print("  ✓ 衬线字体: 文学气质")
print("  ✓ 渐变背景: 现代温暖")
print("  ✓ 响应式布局: 多端适配")
print("="*80)
