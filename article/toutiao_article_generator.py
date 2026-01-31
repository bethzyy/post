# -*- coding: utf-8 -*-
"""
今日头条高赞文章生成器 v3.0 - 增强版
支持用户输入自定义主题,使用AI生成高质量文章
新增: 自动生成配图功能
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import base64
from PIL import Image
import io

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_zhipuai_client, get_antigravity_client


class ToutiaoArticleGenerator:
    """今日头条文章生成器 - AI增强版 v3.1"""

    def __init__(self):
        self.text_client = get_zhipuai_client()
        self.image_client = get_antigravity_client()

    def improve_article_draft(self, draft_content, target_length=2000, style='standard'):
        """根据用户草稿完善文章

        Args:
            draft_content: 用户草稿内容
            target_length: 目标字数
            style: 写作风格 ('standard' 标准风格, 'professional' 资深写手风格)
        """

        print(f"\n[AI完善] 正在完善您的文章草稿...")
        print(f"[AI完善] 目标字数: {target_length}字")
        print(f"[AI完善] 写作风格: {'资深写手' if style == 'professional' else '标准'}\n")

        # 清理草稿内容中的代理字符(surrogate characters)
        # 这些字符可能导致UTF-8编码错误
        try:
            # 尝试编码为UTF-8，如果失败则清理
            draft_content.encode('utf-8')
        except UnicodeEncodeError:
            # 移除代理字符
            draft_content = draft_content.encode('utf-8', errors='ignore').decode('utf-8')
            print("[提示] 草稿包含特殊字符，已自动清理")

        # 根据风格选择不同的prompt
        if style == 'professional':
            prompt = f"""你是一位资深的专栏作家，擅长用优美的文字和深刻的思考打动读者。请将以下用户草稿完善为一篇有深度、有温度、有新意的文章。

## 用户草稿:

{draft_content}

## 写作要求:
1. **字数**: {target_length}字左右
2. **文风**: 资深写手风格
   - 语言优美流畅，避免机器感和套路化表达
   - 用词精准，句式多变，长短句结合
   - 适当运用修辞手法（比喻、排比、设问等）
   - 文字要有温度，能引起读者共鸣
3. **结构**:
   - 引人入胜的开头（可以从个人经历或时代背景切入）
   - 2-3个深度观点（不要简单罗列，要有逻辑递进）
   - 意味深长的结尾（留有思考空间）
4. **内容提升**:
   - 保留草稿的核心思想和情感基调
   - 补充2026年AI时代的最新视角和案例
   - 融入"第三空间"、"知识体验中心"等前沿概念
   - 加入对人文精神在算法时代的思考
   - 避免陈词滥调和空话套话
5. **标题**: 文学性+思想性，15-25字，避免标题党
6. **禁忌**:
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji（最多2-3处，且要用得恰到好处）
   - 不得使用"让我们一起"、"不容错过"等营销话术
   - 不得生硬列举"5个XX"、"3大XX"

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

[完善后的正文内容]

---

记住:你要写的是一篇能打动人心、引人深思的专栏文章，而不是一篇营销文案。
"""
        else:
            prompt = f"""请将以下用户草稿完善为一篇高质量的今日头条文章。

## 用户草稿:

{draft_content}

## 完善要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
3. 结构: 吸引人的标题 + 引人入胜的开头 + 3-5个要点 + 感人或启发的结尾 + 互动号召
4. 内容优化:
   - 保留草稿的核心观点和主要内容
   - 补充具体的案例和数据
   - 优化表达,使其更生动有趣
   - 增加适当的emoji增强可读性
5. 标题优化: 使用数字+疑问/对比/利益点,字数15-25字
6. 情感增强: 能引起共鸣,激发情绪(感动/激励/共鸣)

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

[完善后的正文内容]

---

注意:
- 保留草稿的核心思想,不要偏离原意
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 多用案例和数据说话
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
"""

        try:
            response = self.text_client.chat.completions.create(
                model="glm-4-flash",  # 使用快速模型
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

            # 提取生成的内容
            content = response.choices[0].message.content

            # 解析标题和正文
            lines = content.split('\n')
            title = ""
            body_lines = []

            for i, line in enumerate(lines):
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else "基于草稿完善的文章"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length,
                'source': 'draft_improvement'
            }

        except Exception as e:
            print(f"[ERROR] 草稿完善失败: {e}")
            return None

    def generate_article_with_ai(self, theme, target_length=2000, style='standard'):
        """使用AI生成文章

        Args:
            theme: 文章主题
            target_length: 目标字数
            style: 写作风格 ('standard' 标准风格, 'wangzengqi' 汪曾祺风格)
        """

        print(f"\n[AI生成] 正在为主题'{theme}'生成文章...")
        print(f"[AI生成] 目标字数: {target_length}字")
        print(f"[AI生成] 风格: {'汪曾祺' if style == 'wangzengqi' else '标准'}\n")

        # 根据风格选择不同的prompt
        if style == 'wangzengqi':
            prompt = f"""你是汪曾祺先生，中国当代著名作家。请用你的散文风格写一篇关于"{theme}"的文章。

## 汪曾祺散文风格特点：
1. **语言特点**：
   - 简洁平淡，朴实有趣
   - 平易自然，富有节奏感
   - 不用华丽辞藻，但意味深长
   - 口语化，有生活气息

2. **结构特点**：
   - 形散神聚，看似随意实则精心
   - 从小事写起，以小见大
   - 漫不经心中见真意

3. **情感特点**：
   - 淡雅怀旧，有温度
   - 乐观平和的人生态度
   - 关注日常人事，体察细微

4. **禁忌**：
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji
   - 不得使用营销话术（"让我们一起"、"不容错过"等）
   - 不得生硬列举"5个XX"、"3大XX"

## 用户草稿中的情感基调（请保留并发挥）：
"每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁..."
"我想象中的未来图书馆，绝不仅仅是数字化升级后的'智能书库'。它应该是一座城市的'第三空间'——不是家，不是办公室，而是属于心灵的栖息地。"

## 写作要求：
1. 字数: {target_length}字左右
2. 主题: {theme}
3. 开头: 从个人经历或感受写起（比如走进图书馆的那份安宁）
4. 内容:
   - 谈谈2026年AI时代的图书馆变化
   - 保留原草稿中"第三空间"、"心灵栖息地"等核心概念
   - 用平淡朴实的语言写深刻的思想
5. 结尾: 留有余韵，引人思考
6. 标题: 简洁有意境，15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

记住:你要写的是一篇有温度、有情怀的散文，而不是营销文案。语言要平淡但有力，朴实但深刻。
"""
        else:
            prompt = f"""请为一篇今日头条文章撰写高质量内容。

主题: {theme}

要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
3. 结构: 吸引人的标题 + 引人入胜的开头 + 3-5个要点 + 感人或启发的结尾 + 互动号召
4. 内容: 真实案例,数据支撑,实用建议
5. 情感: 能引起共鸣,激发情绪(感动/激励/共鸣)
6. 标题要求: 使用数字+疑问/对比/利益点,字数15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

注意:
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 多用案例和数据说话
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
"""

        try:
            response = self.text_client.chat.completions.create(
                model="glm-4-flash",  # 使用快速模型
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

            # 提取生成的内容
            content = response.choices[0].message.content

            # 解析标题和正文
            lines = content.split('\n')
            title = ""
            body_lines = []

            for i, line in enumerate(lines):
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else f"关于{theme}的思考"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length
            }

        except Exception as e:
            print(f"[ERROR] AI生成失败: {e}")
            return None

    def generate_article_images(self, theme, image_style="realistic"):
        """根据文章主题生成3张配图"""

        print(f"\n[配图生成] 正在为主题'{theme}'生成配图...")
        print(f"[配图生成] 配图风格: {image_style}\n")

        # 根据主题生成3张不同场景的配图
        image_prompts = self._generate_image_prompts(theme, image_style)
        generated_images = []

        for i, (img_prompt, img_desc) in enumerate(image_prompts, 1):
            print(f"[配图{i}] {img_desc}...")

            try:
                response = self.image_client.images.generate(
                    model="gemini-3-pro-image-4k",
                    prompt=img_prompt.strip(),
                    size="1024x1024",
                    n=1,
                )

                if hasattr(response, 'data') and len(response.data) > 0:
                    img_data = response.data[0]
                    if hasattr(img_data, 'b64_json') and img_data.b64_json:
                        img_bytes = base64.b64decode(img_data.b64_json)
                        img = Image.open(io.BytesIO(img_bytes))

                        # 保存图片到工具所在目录
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"文章配图{i}_{img_desc}_{timestamp}.jpg"

                        # 获取工具所在目录
                        from pathlib import Path
                        tool_dir = Path(__file__).parent
                        img_path = str(tool_dir / filename)

                        img.save(img_path, 'JPEG', quality=95)
                        generated_images.append(img_path)
                        print(f"    [成功] {img_path}")
                    else:
                        print(f"    [失败] 未找到图片数据")
                else:
                    print(f"    [失败] API响应无数据")

            except Exception as e:
                print(f"    [失败] {str(e)[:100]}")

        return generated_images

    def _generate_image_prompts(self, theme, style):
        """根据主题生成配图提示词"""

        # 基于主题生成3个不同场景的配图提示
        base_prompts = {
            "realistic": [
                f"Professional {theme} scene, realistic photography style, high quality, 1024x1024",
                f"{theme} detail shot, close-up view, professional lighting, realistic style, 1024x1024",
                f"{theme} lifestyle scene, people interacting, natural lighting, realistic photography, 1024x1024"
            ],
            "artistic": [
                f"{theme} artistic interpretation, oil painting style, vibrant colors, creative composition, 1024x1024",
                f"{theme} watercolor illustration, soft colors, artistic style, detailed brushwork, 1024x1024",
                f"{theme} digital art, modern artistic style, creative design, colorful, 1024x1024"
            ],
            "cartoon": [
                f"{theme} cartoon style, cute characters, bright colors, friendly atmosphere, 1024x1024",
                f"{theme} manga style, expressive characters, clean lines, vibrant colors, 1024x1024",
                f"{theme} illustration style, fun and playful, colorful, engaging visual, 1024x1024"
            ]
        }

        descriptions = {
            "realistic": ["主场景", "细节特写", "生活场景"],
            "artistic": ["艺术创作", "水彩插画", "数字艺术"],
            "cartoon": ["卡通场景", "漫画风格", "插画风格"]
        }

        prompts = base_prompts.get(style, base_prompts["realistic"])
        descs = descriptions.get(style, descriptions["realistic"])

        return list(zip(prompts, descs))

    def create_article_html(self, title, content, theme, images=None):
        """创建HTML格式的文章(包含配图)"""

        # 生成配图HTML
        images_html = ""
        if images:
            images_html = "<div class='images-gallery'>\n"
            images_html += "<h3 style='color: #5a67d8; margin: 30px 0 20px 0; text-align: center;'>文章配图</h3>\n"
            images_html += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;'>\n"

            for img in images:
                images_html += f"<div style='text-align: center;'>\n"
                images_html += f"<img src='{img}' alt='{img}' style='width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>\n"
                images_html += f"<p style='color: #999; font-size: 0.9em; margin-top: 8px;'>{img}</p>\n"
                images_html += f"</div>\n"

            images_html += "</div>\n</div>\n"

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
            font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}

        .title {{
            font-size: 2em;
            font-weight: bold;
            color: #222;
            margin-bottom: 15px;
            line-height: 1.4;
        }}

        .meta {{
            color: #999;
            font-size: 0.9em;
        }}

        .content {{
            font-size: 1.1em;
            line-height: 2;
        }}

        .content p {{
            margin-bottom: 20px;
            text-indent: 2em;
        }}

        .content h2 {{
            font-size: 1.5em;
            color: #5a67d8;
            margin: 30px 0 15px 0;
            padding-left: 15px;
            border-left: 4px solid #5a67d8;
        }}

        .content h3 {{
            font-size: 1.3em;
            color: #6b46c1;
            margin: 25px 0 10px 0;
        }}

        .content strong {{
            color: #e53e3e;
            font-weight: bold;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}

        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">{title}</div>
            <div class="meta">
                主题: {theme} |
                字数: {len(content)}字 |
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>

        <div class="content">
            {self._format_content_to_html(content)}
        </div>

        {images_html}

        <div class="footer">
            <p>本文由AI发文工具管理器生成</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

        return html_content

    def _format_content_to_html(self, content):
        """将Markdown格式内容转换为HTML"""

        html = content

        # 转换段落
        paragraphs = html.split('\n\n')
        html_paragraphs = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 处理标题
            if para.startswith('### '):
                html_paragraphs.append(f'<h3>{para[4:]}</h3>')
            elif para.startswith('## '):
                html_paragraphs.append(f'<h2>{para[3:]}</h2>')
            elif para.startswith('# '):
                html_paragraphs.append(f'<h2>{para[2:]}</h2>')
            # 处理高亮块
            elif para.startswith('>'):
                html_paragraphs.append(f'<div class="highlight">{para[1:].strip()}</div>')
            # 普通段落
            else:
                # 处理加粗
                para = para.replace('**', '<strong>').replace('**', '</strong>')
                # 处理换行
                para = para.replace('\n', '<br>')
                html_paragraphs.append(f'<p>{para}</p>')

        return '\n'.join(html_paragraphs)


def get_user_input_mode():
    """获取用户选择:主题生成 or 草稿完善"""

    print("\n" + "="*80)
    print("今日头条文章生成器 v3.1 - 增强版")
    print("="*80)
    print()
    print("请选择文章生成方式:")
    print()
    print("  1. 主题生成 - 输入主题,AI从零开始生成文章")
    print("  2. 草稿完善 - 输入您的草稿,AI优化完善")
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            mode = sys.stdin.readline().strip()
            if mode and mode in ['1', '2']:
                print(f"[Web模式] 模式: {'主题生成' if mode == '1' else '草稿完善'}")
                return int(mode)
        except:
            pass

    while True:
        try:
            choice = input("请选择 (默认为1): ").strip()

            if not choice:
                return 1  # 默认主题生成

            if choice in ["1", "主题", "生成"]:
                return 1
            elif choice in ["2", "草稿", "完善"]:
                return 2
            else:
                print("[提示] 请输入 1 或 2")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return 1


def get_user_draft():
    """获取用户输入的草稿"""

    print("\n" + "-"*80)
    print("草稿完善模式")
    print("-"*80)
    print()
    print("请输入您的文章草稿(支持多行输入)")
    print("提示: 输入完成后,在新的一行输入 'END' 并回车结束")
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            lines = []
            for line in sys.stdin:
                line = line.strip()
                if line == 'END':
                    break
                lines.append(line)

            if lines:
                draft = '\n'.join(lines)

                # 清理草稿中的代理字符
                try:
                    draft.encode('utf-8')
                except UnicodeEncodeError:
                    draft = draft.encode('utf-8', errors='ignore').decode('utf-8')
                    print("[提示] 草稿包含特殊字符，已自动清理")

                print(f"[Web模式] 已读取草稿: {len(draft)}字")
                return draft
        except:
            pass

    # 手动输入模式
    draft_lines = []
    print("开始输入草稿内容:")
    print()

    try:
        while True:
            line = input()

            if line.strip() == 'END':
                break

            draft_lines.append(line)

        draft = '\n'.join(draft_lines).strip()

        # 清理草稿中的代理字符
        try:
            draft.encode('utf-8')
        except UnicodeEncodeError:
            draft = draft.encode('utf-8', errors='ignore').decode('utf-8')
            print("[提示] 草稿包含特殊字符，已自动清理")

        if draft:
            print(f"\n[成功] 已读取草稿: {len(draft)}字")
            return draft
        else:
            print("\n[错误] 草稿为空")
            return None

    except KeyboardInterrupt:
        print("\n\n[提示] 用户取消输入")
        return None
    except Exception as e:
        print(f"[错误] 输入错误: {e}")
        return None


def get_user_theme():
    """获取用户输入的主题"""

    print("\n" + "="*80)
    print("今日头条文章生成器 - AI增强版 v3.1")
    print("="*80)
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            theme = sys.stdin.readline().strip()
            if theme:
                print(f"[Web模式] 主题: {theme}")
                return theme
        except:
            pass

    print("请输入您想要生成文章的主题")
    print()
    print("示例主题:")
    themes = [
        "过年回老家",
        "职场新人必看",
        "健康养生小贴士",
        "理财投资心得",
        "教育孩子感悟",
        "情感关系建议"
    ]

    for i, theme in enumerate(themes, 1):
        print(f"  {i}. {theme}")

    print()
    print("您可以输入上述主题,或输入自定义主题")
    print()

    while True:
        try:
            user_input = input("请输入主题 (输入 'q' 退出): ").strip()

            if user_input.lower() == 'q':
                return None

            if user_input:
                print(f"\n[确认] 主题: {user_input}")
                return user_input
            else:
                print("[提示] 主题不能为空,请重新输入")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return None


def get_target_length():
    """获取目标字数"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            length = sys.stdin.readline().strip()
            if length and length.isdigit():
                print(f"[Web模式] 字数: {length}")
                return int(length)
        except:
            pass

    print()
    print("请选择文章长度:")
    print("  1. 1500字左右 (快速阅读)")
    print("  2. 2000字左右 (标准长度)")
    print("  3. 2500字左右 (深度文章)")

    while True:
        try:
            choice = input("\n请选择 (默认为2): ").strip()

            if not choice:
                choice = "2"

            if choice in ["1", "2", "3"]:
                lengths = {"1": 1500, "2": 2000, "3": 2500}
                return lengths[choice]
            else:
                print("[提示] 请输入 1、2 或 3")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return 2000
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return 2000


def get_generate_images():
    """询问是否生成配图"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            choice = sys.stdin.readline().strip()
            if choice:
                return choice.lower() == 'y'
        except:
            pass

    print()
    while True:
        try:
            choice = input("是否生成配图? (y/n, 默认: y): ").strip().lower()
            if not choice:
                return True
            if choice in ['y', 'yes', '是']:
                return True
            elif choice in ['n', 'no', '否']:
                return False
            else:
                print("[提示] 请输入 y 或 n")
        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return False
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return False


def get_image_style():
    """获取配图风格"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            style = sys.stdin.readline().strip()
            if style:
                return style
        except:
            pass

    print()
    print("请选择配图风格:")
    print("  1. 真实照片 (realistic)")
    print("  2. 艺术创作 (artistic)")
    print("  3. 卡通插画 (cartoon)")

    while True:
        try:
            choice = input("\n请选择 (默认为1): ").strip().lower()

            if not choice:
                return "realistic"

            if choice in ["1", "realistic", "真实"]:
                return "realistic"
            elif choice in ["2", "artistic", "艺术"]:
                return "artistic"
            elif choice in ["3", "cartoon", "卡通"]:
                return "cartoon"
            else:
                print("[提示] 请输入 1、2 或 3")
        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return "realistic"
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return "realistic"


def main():
    """主函数"""

    print("="*80)
    print("今日头条文章生成器 v3.1 - 增强版")
    print("支持文章生成 + 草稿完善 + 智能配图")
    print("="*80)
    print()

    # 获取用户选择的模式
    mode = get_user_input_mode()

    if not mode:
        print("\n[退出] 未选择模式,程序退出")
        return

    # 根据模式获取输入
    theme = None
    draft = None

    if mode == 1:
        # 主题生成模式
        theme = get_user_theme()
        if not theme:
            print("\n[退出] 未输入主题,程序退出")
            return
    elif mode == 2:
        # 草稿完善模式
        draft = get_user_draft()
        if not draft:
            print("\n[退出] 未输入草稿,程序退出")
            return
        theme = "基于草稿完善"  # 用于文件命名

    # 获取目标字数
    target_length = get_target_length()

    print(f"\n[设置] 目标字数: {target_length}字")

    # 询问是否生成配图
    generate_images = get_generate_images()

    image_style = "realistic"
    if generate_images:
        image_style = get_image_style()
        print(f"[设置] 配图风格: {image_style}")

    # 创建生成器
    generator = ToutiaoArticleGenerator()

    if not generator.text_client:
        print("\n[ERROR] 无法初始化AI文本客户端")
        print("[ERROR] 请检查config.py中的ZHIPU_API_KEY配置")
        return

    if generate_images and not generator.image_client:
        print("\n[WARNING] 无法初始化AI图像客户端")
        print("[WARNING] 将跳过配图生成")
        generate_images = False

    # 生成/完善文章
    print()
    print("-"*80)
    print()

    if mode == 1:
        article = generator.generate_article_with_ai(theme, target_length)
        if not article:
            print("\n[ERROR] 文章生成失败")
            return
    else:
        article = generator.improve_article_draft(draft, target_length)
        if not article:
            print("\n[ERROR] 草稿完善失败")
            return

    # 显示生成的文章
    print()
    print("-"*80)
    print()
    print(f"[成功] {'文章生成' if mode == 1 else '草稿完善'}成功!")
    print()
    print("="*80)
    print(f"标题: {article['title']}")
    print("="*80)
    print()
    print(article['content'])
    print()
    print("="*80)
    print(f"字数: {article['word_count']}字")
    print(f"目标: {article['target_length']}字")
    print(f"完成度: {article['word_count']/article['target_length']*100:.1f}%")
    if mode == 2:
        print(f"来源: 草稿完善")
    print("="*80)
    print()

    # 生成配图
    generated_images = []
    if generate_images:
        print()
        print("-"*80)
        print()
        print("[配图] 开始生成配图...")
        print()
        generated_images = generator.generate_article_images(theme, image_style)

        if generated_images:
            print(f"\n[成功] 成功生成 {len(generated_images)} 张配图")
        else:
            print("\n[警告] 配图生成失败,但文章已成功生成")

    # 保存为Markdown文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_prefix = "文章草稿完善" if mode == 2 else "今日头条文章"
    md_filename = f"{file_prefix}_{theme}_{timestamp}.md"

    # 保存到工具所在目录
    tool_dir = Path(__file__).parent
    md_path = str(tool_dir / md_filename)

    source_note = " (基于用户草稿完善)" if mode == 2 else ""
    md_content = f"""# {article['title']}

**主题**: {theme}
**字数**: {article['word_count']}字
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{source_note}

---

{article['content']}

---

*本文由AI发文工具管理器自动生成{source_note}*
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"\n[成功] Markdown文件已保存: {md_path}")

    # 保存为HTML文件
    html_filename = f"{file_prefix}_{theme}_{timestamp}.html"
    html_path = str(tool_dir / html_filename)
    html_content = generator.create_article_html(article['title'], article['content'], theme, generated_images)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[成功] HTML文件已保存: {html_path}")

    # 自动打开HTML文件
    try:
        import webbrowser
        webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
        print(f"[成功] 已在浏览器中打开文章预览")
    except:
        print(f"[提示] 请手动打开HTML文件查看文章: {html_path}")

    print()
    print("="*80)
    print("生成完成!")
    if generated_images:
        print(f"[文件] 文章: {md_filename}")
        print(f"[文件] HTML: {html_filename}")
        print(f"[配图] 配图: {len(generated_images)}张")
    else:
        print(f"[文件] 文章: {md_filename}")
        print(f"[文件] HTML: {html_filename}")
    print("="*80)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[提示] 程序被用户中断")
    except Exception as e:
        print(f"\n\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()
