# -*- coding: utf-8 -*-
"""
为bird.jpg生成绘画步骤图
调用所有AI大模型生成6个绘画步骤
"""

import sys
from pathlib import Path
import base64
import requests
from PIL import Image
import io
import time
from datetime import datetime

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
from config import Config, get_antigravity_client


# 6个绘画步骤的详细描述
STEPS = [
    {
        "name": "步骤1_铅笔起稿",
        "description": """
Pencil sketch draft step.
Draw a light pencil sketch outline of the bird perched on a branch.
Show only the basic shapes and contours with pencil lines on white paper.
Minimal detail, just the rough composition and proportions.
Light graphite pencil strokes on clean white paper background.
Sketch style, line drawing, no color, no shading.
        """
    },
    {
        "name": "步骤2_铺底色",
        "description": """
Base color layer step.
Apply flat base colors to the pencil sketch.
Block in the main colors: brown for the bird, green for leaves, light blue for sky background.
Transparent watercolor washes, no details yet, just flat color areas.
Keep it loose and light, showing the brush strokes.
Watercolor technique, wash layer, base colors only.
        """
    },
    {
        "name": "步骤3_塑造形体",
        "description": """
Form and volume building step.
Start building volume and form on the base colors.
Add mid-tones to show the bird's roundness and feather textures.
Begin shading the branch and leaves to show depth.
Add shadows where the bird meets the branch.
Still somewhat loose, but forms are taking shape.
Building three-dimensional form, adding shadows and mid-tones.
        """
    },
    {
        "name": "步骤4_细节刻画",
        "description": """
Detail rendering step.
Add fine details to the bird: eye, beak, individual feathers, texture.
Show the feathers' texture with careful brushwork.
Add details to leaves: veins, subtle color variations.
Add texture to the tree branch: bark texture, knots.
Sharp details, fine brushwork, high detail level.
        """
    },
    {
        "name": "步骤5_调整统一",
        "description": """
Adjustment and unification step.
Refine the overall color harmony.
Add final highlights on the bird's head and wing.
Add subtle shadows and atmospheric depth.
Unify the color temperature across the painting.
Smooth transitions, adjust values, final polish.
Professional watercolor painting refinement.
        """
    },
    {
        "name": "步骤6_落款装裱",
        "description": """
Signature and framing step.
The completed bird painting with elegant signature in red seal stamp.
Add a traditional Chinese red seal stamp with artist's name.
Add subtle Chinese calligraphy text.
Presented as a finished, museum-quality artwork.
Matted and framed presentation, gallery-ready.
Complete masterpiece with traditional Chinese painting aesthetics.
        """
    }
]


class BirdPaintingGenerator:
    """鸟儿绘画步骤生成器"""

    def __init__(self):
        self.client = get_antigravity_client()
        self.all_results = []

    def generate_with_gemini(self, model_name, step_info):
        """使用Gemini生成步骤图"""
        try:
            print(f"\n  正在调用 {model_name}...")

            # 组合提示词
            prompt = f"""
Create a watercolor painting progress step showing: {step_info['name']}

{step_info['description']}

Subject: A beautiful bird perched on a tree branch with green leaves.
Style: Traditional Chinese watercolor painting technique.
Quality: High quality, detailed, professional art instruction level.
Medium: Watercolor on paper.
Size: 1024x1024

Show ONLY this specific step, not the final complete painting.
            """.strip()

            response = self.client.images.generate(
                model=model_name,
                prompt=prompt,
                size="1024x1024",
                n=1,
            )

            if hasattr(response, 'data') and len(response.data) > 0:
                img_data = response.data[0]

                if hasattr(img_data, 'b64_json') and img_data.b64_json:
                    img_bytes = base64.b64decode(img_data.b64_json)
                    img = Image.open(io.BytesIO(img_bytes))

                    filename = f"bird_{model_name.replace('-', '_')}_{step_info['name']}.png"
                    img.save(filename, 'PNG', quality=95)

                    print(f"    [成功] {filename}")

                    return {
                        'model': model_name,
                        'step': step_info['name'],
                        'filename': filename,
                        'size': img.size,
                        'success': True
                    }

            return None

        except Exception as e:
            print(f"    [失败] {str(e)[:80]}")
            return None

    def generate_with_pollinations(self, model_name, step_info):
        """使用Pollinations生成步骤图"""
        try:
            import urllib.parse

            print(f"\n  正在调用 Pollinations.ai...")

            prompt = f"""
Watercolor painting progress step: {step_info['name']}

{step_info['description']}

Subject: Beautiful bird on tree branch.
Style: Chinese watercolor painting.
Show ONLY this painting step.
            """.strip()

            encoded_prompt = urllib.parse.quote(prompt.strip())
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=768&seed={int(time.time())}&nologo=true&model=flux"

            response = requests.get(url, timeout=120)

            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                filename = f"bird_Pollinations_{step_info['name']}.png"
                img.save(filename, 'PNG', quality=95)

                print(f"    [成功] {filename}")

                return {
                    'model': 'Pollinations',
                    'step': step_info['name'],
                    'filename': filename,
                    'size': img.size,
                    'success': True
                }

            return None

        except Exception as e:
            print(f"    [失败] {str(e)[:80]}")
            return None

    def generate_all_steps(self):
        """生成所有步骤"""

        print("="*80)
        print("为bird.jpg生成完整绘画步骤图")
        print("="*80)

        models = ['gemini-3-pro-image', 'gemini-3-pro-image-4k']

        for step_info in STEPS:
            print(f"\n{'='*80}")
            print(f"正在生成: {step_info['name']}")
            print('='*80)

            step_results = []

            for model in models:
                result = self.generate_with_gemini(model, step_info)
                if result:
                    step_results.append(result)
                    self.all_results.append(result)
                time.sleep(2)

            # Pollinations
            result = self.generate_with_pollinations('Pollinations', step_info)
            if result:
                step_results.append(result)
                self.all_results.append(result)

            time.sleep(1)

        return self.all_results


def generate_html_gallery(results):
    """生成HTML展示页面"""

    print("\n" + "="*80)
    print("正在生成HTML展示页面...")
    print("="*80)

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画 - AI生成绘画步骤展示</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }

        .original-image {
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }

        .original-image img {
            max-width: 100%;
            max-height: 500px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .original-image h2 {
            margin-bottom: 20px;
            color: #333;
        }

        .step-section {
            margin-bottom: 60px;
        }

        .step-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }

        .models-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 20px;
        }

        .model-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .model-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .model-card h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2em;
        }

        .model-card img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .info {
            margin-top: 15px;
            color: #666;
            font-size: 0.9em;
        }

        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }

        @media (max-width: 768px) {
            .models-grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 鸟儿水彩画 - AI生成绘画步骤展示</h1>
        <p class="subtitle">多模型对比 | 从铅笔起稿到落款装裱的完整过程</p>

        <div class="original-image">
            <h2>📷 原始图片</h2>
            <img src="bird.jpg" alt="原始鸟儿图片">
        </div>
"""

    # 按步骤分组
    steps_dict = {}
    for result in results:
        step = result['step']
        if step not in steps_dict:
            steps_dict[step] = []
        steps_dict[step].append(result)

    # 生成每个步骤的HTML
    step_number = 1
    for step_name in ['步骤1_铅笔起稿', '步骤2_铺底色', '步骤3_塑造形体',
                      '步骤4_细节刻画', '步骤5_调整统一', '步骤6_落款装裱']:
        if step_name in steps_dict:
            html_content += f"""
        <div class="step-section">
            <h2 class="step-title">第{step_number}步: {step_name.split('_', 1)[1]}</h2>
            <div class="models-grid">
"""

            for result in steps_dict[step_name]:
                html_content += f"""
                <div class="model-card">
                    <h3>🤖 {result['model']}</h3>
                    <img src="{result['filename']}" alt="{result['model']} - {step_name}">
                    <div class="info">
                        <p>尺寸: {result['size'][0]}×{result['size'][1]}</p>
                        <p>文件: {result['filename']}</p>
                    </div>
                </div>
"""

            html_content += """
            </div>
        </div>
"""
            step_number += 1

    html_content += f"""
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>总计生成: {len(results)} 张步骤图</p>
            <p>使用模型: Gemini-3-Pro-Image, Gemini-3-Pro-Image-4k, Pollinations</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    filename = "bird_painting_steps_gallery.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML页面已生成: {filename}")

    return filename


def main():
    """主函数"""
    print("\n" + "="*80)
    print("鸟儿水彩画 - AI生成完整绘画步骤")
    print("Bird Watercolor Painting - AI Generated Step-by-Step Process")
    print("="*80)

    # 生成所有步骤
    generator = BirdPaintingGenerator()
    results = generator.generate_all_steps()

    # 显示结果
    print("\n" + "="*80)
    print("生成结果汇总")
    print("="*80)
    print(f"\n总计生成: {len(results)} 张图片\n")

    for result in results:
        print(f"✓ {result['model']} - {result['step']}")

    # 生成HTML展示页面
    html_file = generate_html_gallery(results)

    print("\n" + "="*80)
    print("完成！")
    print("="*80)
    print(f"\nHTML展示页面: {html_file}")
    print("\n正在打开浏览器...")

    # 打开HTML文件
    import webbrowser
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))


if __name__ == "__main__":
    main()
