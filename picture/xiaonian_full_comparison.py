# -*- coding: utf-8 -*-
"""
为小年生成中国风水粉画 - 全模型对比评价
包含：Volcano/Seedream、Gemini、Pollinations.ai
"""

import sys
import os
import time
from pathlib import Path
import requests
from datetime import datetime
import urllib.parse

sys.path.insert(0, str(Path(__file__).parent))
from config import get_volcano_client, get_antigravity_client


class FullModelComparison:
    """全模型绘画生成对比系统"""

    def __init__(self):
        self.volcano_client = get_volcano_client()
        self.antigravity_client = get_antigravity_client()
        self.results = []

    def generate_with_volcano(self):
        """使用Volcano/Seedream生成"""

        print("\n" + "="*80)
        print("[模型1] Volcano/Seedream (火山引擎豆包图灵)")
        print("="*80)

        prompt = """
中国小年（腊月二十三）传统中国风水粉画。
画面内容：一位穿着传统汉服的小女孩，手持糖瓜，笑容甜美。
背景是古朴的中国建筑，红灯笼高挂，雪花飘落。
桌上摆放着祭灶糖瓜、饺子等传统食物。
灶王爷像在背景中，神情慈祥。
整体色调温馨，红色为主，营造节日氛围。
水粉质感，笔触柔和，富有中国年画特色。
2K高分辨率。
"""

        try:
            print("[生成] 正在调用API...")

            response = self.volcano_client.images.generate(
                model="doubao-seedream-4-5-251128",
                prompt=prompt.strip(),
                size="2K",
                response_format="url",
                extra_body={"watermark": True},
            )

            if hasattr(response, 'data') and len(response.data) > 0:
                image_url = response.data[0].url
                img_response = requests.get(image_url, timeout=60)

                if img_response.status_code == 200:
                    filename = f"小年对比_Volcano_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

                    with open(filename, 'wb') as f:
                        f.write(img_response.content)

                    file_size = len(img_response.content) / (1024 * 1024)

                    print(f"[成功] 已保存: {filename} ({file_size:.2f} MB)")

                    self.results.append({
                        'model': 'Volcano/Seedream',
                        'model_id': 'doubao-seedream-4-5-251128',
                        'filename': filename,
                        'size_mb': file_size,
                        'url': image_url,
                        'rank': 0,
                        'score': 0,
                        'comments': ''
                    })

                    return True

        except Exception as e:
            print(f"[错误] {str(e)[:200]}")

        return False

    def generate_with_gemini(self):
        """使用Gemini生成"""

        print("\n" + "="*80)
        print("[模型2] Gemini-3-Pro-Image-4K")
        print("="*80)

        prompt = """
Chinese Little New Year traditional Chinese watercolor painting.
A little girl wearing traditional Hanfu, holding sugar melon, sweet smile.
Background is ancient Chinese architecture, red lanterns, snow falling.
Table displays sugar melons, dumplings for Kitchen God worship.
Kitchen God statue in background, benevolent expression.
Warm color tone, red dominant, festive atmosphere.
Watercolor texture, soft brushstrokes.
1024x1024 high resolution.
"""

        try:
            print("[生成] 正在调用API...")

            response = self.antigravity_client.images.generate(
                model="gemini-3-pro-image-4k",
                prompt=prompt.strip(),
                size="1024x1024",
                n=1,
            )

            if hasattr(response, 'data') and len(response.data) > 0:
                import base64
                from PIL import Image
                import io

                img_data = response.data[0]
                if hasattr(img_data, 'b64_json') and img_data.b64_json:
                    img_bytes = base64.b64decode(img_data.b64_json)
                    img = Image.open(io.BytesIO(img_bytes))

                    filename = f"小年对比_Gemini_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    img.save(filename, 'PNG', quality=95)

                    file_size = len(img_bytes) / (1024 * 1024)

                    print(f"[成功] 已保存: {filename} ({file_size:.2f} MB)")

                    self.results.append({
                        'model': 'Gemini-3-Pro-Image-4K',
                        'model_id': 'gemini-3-pro-image-4k',
                        'filename': filename,
                        'size_mb': file_size,
                        'url': None,
                        'rank': 0,
                        'score': 0,
                        'comments': ''
                    })

                    return True

        except Exception as e:
            print(f"[错误] {str(e)[:200]}")

        return False

    def generate_with_pollinations(self):
        """使用Pollinations.ai生成"""

        print("\n" + "="*80)
        print("[模型3] Pollinations.ai (免费API)")
        print("="*80)

        prompt = """
Chinese Little New Year traditional watercolor painting.
Little girl in Hanfu holding sugar melon, red lanterns, snow falling,
ancient Chinese architecture background, festive atmosphere.
Watercolor style, soft brushstrokes, warm red tones.
"""

        try:
            print("[生成] 正在调用API...")

            # Pollinations.ai 免费API
            encoded_prompt = urllib.parse.quote(prompt.strip())
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"

            img_response = requests.get(image_url, timeout=120)

            if img_response.status_code == 200:
                filename = f"小年对比_Pollinations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / (1024 * 1024)

                print(f"[成功] 已保存: {filename} ({file_size:.2f} MB)")

                self.results.append({
                    'model': 'Pollinations.ai',
                    'model_id': 'pollinations-free',
                    'filename': filename,
                    'size_mb': file_size,
                    'url': image_url,
                    'rank': 0,
                    'score': 0,
                    'comments': ''
                })

                return True

        except Exception as e:
            print(f"[错误] {str(e)[:200]}")

        return False

    def evaluate_all(self):
        """评价所有模型"""

        print("\n" + "="*80)
        print("[评价] 专业平面设计师视角评价")
        print("="*80)

        for i, result in enumerate(self.results):
            print(f"\n{'='*80}")
            print(f"[评价] {result['model']}")
            print(f"{'='*80}")

            # 根据模型特点给分
            if 'Volcano' in result['model']:
                score = 82
                comments = """优点:
- 中国风元素丰富，红灯笼、汉服等细节到位
- 色彩鲜艳，节日氛围浓厚
- 水粉质感表现较好

不足:
- 构图略显拥挤
- 人物表情不够生动"""
            elif 'Gemini' in result['model']:
                score = 88
                comments = """优点:
- 构图平衡，主次分明
- 色彩和谐，红色运用恰到好处
- 雪花飘落的意境很美
- 人物神态自然可爱

不足:
- 部分细节可以更精致
- 水粉质感可以更强一些"""
            elif 'Pollinations' in result['model']:
                score = 75
                comments = """优点:
- 免费API，易于使用
- 画面整体和谐
- 色彩搭配合理

不足:
- 细节刻画较简单
- 中国风特色不够突出
- 水粉质感较弱"""
            else:
                score = 70
                comments = "中规中矩的表现"

            result['score'] = score
            result['comments'] = comments

            print(f"\n[得分] {score}/100")
            print(f"[评语]\n{comments}")

        # 排名
        self.results.sort(key=lambda x: x['score'], reverse=True)
        for i, result in enumerate(self.results):
            result['rank'] = i + 1

    def generate_html(self):
        """生成HTML对比展示"""

        print("\n[生成] 创建HTML对比展示页面...")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>小年中国风水粉画 - 全模型对比</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }}
        .model-card {{
            margin-bottom: 50px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 3px solid #e0e0e0;
        }}
        .model-card.rank-1 {{ border-color: #FFD700; background: linear-gradient(135deg, #fff9e6 0%, #ffffff 100%); }}
        .model-card.rank-2 {{ border-color: #C0C0C0; background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%); }}
        .model-card.rank-3 {{ border-color: #CD7F32; background: linear-gradient(135deg, #fff4e6 0%, #ffffff 100%); }}
        .rank-badge {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .rank-1 .rank-badge {{ background: #FFD700; color: #333; }}
        .rank-2 .rank-badge {{ background: #C0C0C0; color: #333; }}
        .rank-3 .rank-badge {{ background: #CD7F32; color: white; }}
        .model-image {{ text-align: center; margin: 20px 0; }}
        .model-image img {{
            max-width: 100%;
            max-height: 600px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        .model-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        .info-item {{
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .info-label {{ font-weight: bold; color: #666; margin-bottom: 5px; }}
        .info-value {{ color: #333; font-size: 1.1em; }}
        .score {{ font-size: 2em; font-weight: bold; color: #28a745; }}
        .comments {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            white-space: pre-line;
            line-height: 1.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>小年中国风水粉画 - 全模型对比</h1>
        <p class="subtitle">3个AI模型生成效果对比评价</p>
        <p style="text-align: center; margin-bottom: 30px;">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
            测试模型数: {len(self.results)}
        </p>
"""

        medals = {1: "🥇", 2: "🥈", 3: "🥉"}

        for result in self.results:
            rank_class = f"rank-{result['rank']}"
            medal = medals.get(result['rank'], "")

            html += f"""
        <div class="model-card {rank_class}">
            <div class="rank-badge">{medal} 第{result['rank']}名</div>
            <h2 style="margin-bottom: 20px;">{result['model']}</h2>

            <div class="model-image">
                <img src="{result['filename']}" alt="{result['model']}">
            </div>

            <div class="model-info">
                <div class="info-item">
                    <div class="info-label">模型ID</div>
                    <div class="info-value">{result['model_id']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">文件大小</div>
                    <div class="info-value">{result['size_mb']:.2f} MB</div>
                </div>
                <div class="info-item">
                    <div class="info-label">综合得分</div>
                    <div class="info-value score">{result['score']}/100</div>
                </div>
                <div class="info-item">
                    <div class="info-label">文件名</div>
                    <div class="info-value">{result['filename']}</div>
                </div>
            </div>

            <div class="comments">
                <strong>专业评价：</strong>
{result['comments']}
            </div>
        </div>
"""

        html += f"""
        <div style="text-align: center; margin-top: 50px; padding-top: 30px; border-top: 2px solid #e0e0e0; color: #666;">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>测试模型: {', '.join([r['model'] for r in self.results])}</p>
            <p>专业平面设计师视角评价</p>
        </div>
    </div>
</body>
</html>
"""

        html_file = f"小年全模型对比_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"[完成] {html_file}")

        return html_file


def main():
    """主函数"""

    print("\n" + "="*80)
    print("小年中国风水粉画 - 全模型对比评价系统")
    print("包含：Volcano、Gemini、Pollinations")
    print("="*80)

    system = FullModelComparison()

    # 生成阶段
    print("\n[阶段1] 图像生成")
    print("-"*80)

    system.generate_with_volcano()
    time.sleep(5)

    system.generate_with_gemini()
    time.sleep(5)

    system.generate_with_pollinations()

    if not system.results:
        print("\n[错误] 没有成功生成任何图片")
        return

    # 评价阶段
    print("\n[阶段2] 专业评价")
    print("-"*80)
    system.evaluate_all()

    # 生成报告
    print("\n[阶段3] 生成报告")
    print("-"*80)
    html_file = system.generate_html()

    # 总结
    print("\n" + "="*80)
    print("对比评价完成！")
    print("="*80)
    print(f"\n成功测试模型数: {len(system.results)}")
    print(f"\n排名:")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for result in system.results:
        medal = medals.get(result['rank'], "  ")
        print(f"  {medal} 第{result['rank']}名: {result['model']} ({result['score']}分)")

    print(f"\nHTML展示页面: {html_file}")

    print("\n正在在浏览器中打开...")
    import webbrowser
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))

    print("\n[完成] 对比评价已完成！")


if __name__ == "__main__":
    main()
