#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成更充分引用原草稿的汪曾祺风格文章"""

import os
from zhipuai import ZhipuAI
from pathlib import Path
from datetime import datetime
from toutiao_article_generator import ToutiaoArticleGenerator

# 原草稿内容
original_draft = """在这个信息爆炸的时代，我们还需要图书馆吗？

每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁。但随着AI时代的到来，知识获取变得前所未有的便捷，我不禁思考：那个承载着千年文明记忆的"藏书楼"，在2026年乃至更远的未来，将以怎样的姿态继续存在？

我想象中的未来图书馆，绝不仅仅是数字化升级后的"智能书库"。它应该是一座城市的"第三空间"——不是家，不是办公室，而是属于心灵的栖息地。

在那里，传统的纸质书与最新的AI技术和谐共存。你可以戴上VR眼镜，穿越千年与古人对话；也可以坐在复古的木质书桌前，翻阅泛黄的古籍，感受时光的重量。

最重要的是，图书馆应该是一个"活的有机体"。它不只是存储知识，更要激发创造。通过AI辅助，每一本书都能找到它的知音；每一位读者，都能在这里遇见思想的火花。

未来的图书馆，将不再只是"借书还书"的地方，而是城市的文化客厅，是思想碰撞的能量场，是人类在算法时代坚守的人文精神堡垒。"""

# 创建改进的prompt，强调要引用原草稿
theme = "未来图书馆：在AI时代，图书馆作为城市第三空间的价值"

# 更强调引用原草稿的prompt
prompt = f"""你是汪曾祺先生，中国当代著名作家。请基于用户的原草稿，用你的散文风格写一篇关于"{theme}"的文章。

## 用户原草稿（请务必在文章中多次引用）：
```
{original_draft}
```

## 写作要求（重要）：

1. **必须直接引用原草稿中的这些句子**（用引号标出，自然融入）：
   - "每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁"
   - "承载着千年文明记忆的'藏书楼'"
   - "我想象中的未来图书馆，绝不仅仅是数字化升级后的'智能书库'"
   - "它应该是一座城市的'第三空间'——不是家，不是办公室，而是属于心灵的栖息地"
   - "传统的纸质书与最新的AI技术和谐共存"
   - "你可以戴上VR眼镜，穿越千年与古人对话"
   - "也可以坐在复古的木质书桌前，翻阅泛黄的古籍，感受时光的重量"
   - "图书馆应该是一个'活的有机体'"
   - "每一本书都能找到它的知音"
   - "人类在算法时代坚守的人文精神堡垒"

2. **汪曾祺散文风格**：
   - 语言简洁平淡，朴实有趣
   - 形散神聚，富有节奏感
   - 淡雅怀旧，有温度
   - 乐观平和的人生态度
   - 口语化，有生活气息

3. **禁忌**：
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji
   - 不得使用营销话术（"让我们一起"、"不容错过"等）
   - 不得生硬列举"5个XX"、"3大XX"

4. **结构建议**：
   - 开头：引用原草稿的"每次走进图书馆..."
   - 中间：将原草稿的各个观点用汪曾祺的叙述方式串联起来
   - 结尾：引用"人文精神堡垒"，留有余韵

5. **字数**：1500-2000字

请直接输出文章内容，格式如下：

---
标题：[文章标题]

[正文内容]

---

记住：要充分引用原草稿中的句子，让用户感受到他的原话被保留和发扬。语言要平淡但有力，朴实但深刻。
"""

print("[生成] 发送AI请求，强调引用原草稿...")
print("="*80)

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

# 保存原始响应
raw_file = Path(__file__).parent / "raw_ai_response_with_quotes.txt"
with open(raw_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[成功] AI响应已保存")

# 解析文章
lines = content.split('\n')
title = None
title_idx = -1

for i, line in enumerate(lines):
    if '标题' in line or (line.strip().startswith('标题') if '标题' in line else False):
        if '：' in line or ':' in line:
            title = line.split('：', 1)[1].strip() if '：' in line else line.split(':', 1)[1].strip()
            title_idx = i
            break

if not title:
    title = "未来图书馆：城市中的心灵栖息地"

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

print(f"\n标题: {title}")
print(f"字数: {len(body)}字")

# 检查引用了哪些原草稿句子
draft_sentences = [
    "每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁",
    "承载着千年文明记忆",
    "我想象中的未来图书馆",
    "绝不仅仅是数字化升级",
    "第三空间",
    "心灵的栖息地",
    "传统的纸质书与最新的AI技术和谐共存",
    "戴上VR眼镜",
    "穿越千年与古人对话",
    "复古的木质书桌",
    "翻阅泛黄的古籍",
    "感受时光的重量",
    "活的有机体",
    "每一本书都能找到它的知音",
    "思想的火花",
    "城市的文化客厅",
    "思想碰撞的能量场",
    "人文精神堡垒"
]

found_quotes = []
for sentence in draft_sentences:
    if sentence in body:
        found_quotes.append(sentence)

print(f"\n[检查] 原草稿引用情况:")
print(f"  引用了 {len(found_quotes)}/{len(draft_sentences)} 个关键句子/短语")
for quote in found_quotes[:10]:  # 只显示前10个
    print(f"  ✓ \"{quote}\"")

# 获取配图
tool_dir = Path(__file__).parent
image_files = []
for f in os.listdir(tool_dir):
    if f.startswith("文章配图") and f.endswith(".jpg"):
        if "20260130_154" in f or "20260130_1551" in f:
            image_files.append(str(tool_dir / f))

image_files.sort()

print(f"\n[配图] 找到 {len(image_files)} 张图片")

# 生成专业排版HTML（包含引用高亮）
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
html_filename = f"汪曾祺风格_含原草稿引用_{timestamp}.html"
html_path = tool_dir / html_filename

# 创建HTML，高亮显示原草稿引用
html_body = body

# 标记原草稿引用（用特殊的样式）
for quote in found_quotes:
    # 使用HTML标记来高亮引用
    html_body = html_body.replace(quote, f'<mark class="draft-quote">{quote}</mark>')

# 生成完整的HTML
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

        .original-draft {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 25px 30px;
            margin: 40px 0;
            border-radius: 4px;
        }}

        .original-draft h3 {{
            color: #856404;
            margin-bottom: 15px;
            font-size: 1.1em;
        }}

        .original-draft p {{
            font-size: 0.95em;
            line-height: 1.8;
            color: #856404;
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

        .image-container {{
            margin: 50px 0;
            text-align: center;
        }}

        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}

        .image-caption {{
            margin-top: 12px;
            color: #7f8c8d;
            font-size: 0.9em;
            font-style: italic;
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
                原草稿引用: {len(found_quotes)}处
            </div>
        </div>

        <div class="original-draft">
            <h3>📝 用户原草稿</h3>
            <p>{original_draft.replace(chr(10), '<br>')}</p>
        </div>

        <div class="content">
            {html_body.replace(chr(10) + chr(10), '</p><p>').replace(chr(10), '<br>')}
        </div>

        <div class="quote-stats">
            <h3>✨ 原草稿引用统计</h3>
            <p style="margin-bottom: 15px;">本文共引用了原草稿中的 <strong>{len(found_quotes)}</strong> 个关键句子/短语：</p>
            <ul>
"""

# 添加引用列表
for quote in found_quotes:
    html += f'                <li>✓ "{quote}"</li>\n'

html += f"""            </ul>
        </div>

        <div class="footer">
            <p><strong>创作说明</strong></p>
            <p style="margin-top: 10px;">
                本文由AI基于用户原草稿，采用汪曾祺文风深度创作。<br>
                文中黄色高亮部分为原草稿中的句子，已被自然融入文章中。
            </p>
            <p style="margin-top: 15px; font-size: 0.85em;">
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </div>
</body>
</html>
"""

# 保存HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n[成功] HTML文件已保存: {html_filename}")

# 自动打开
try:
    import webbrowser
    webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
    print(f"[成功] 已在浏览器中打开预览")
except:
    pass

print("\n生成完成!")
print(f"[文件] HTML: {html_filename}")
print(f"[引用] {len(found_quotes)}处原草稿句子")
print("="*80)
