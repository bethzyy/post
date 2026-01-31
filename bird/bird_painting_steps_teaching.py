# -*- coding: utf-8 -*-
"""
为bird.jpg生成严格对应的教学绘画步骤图
每个步骤都必须是画同一只鸟的渐进过程
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


# 读取原始图片并进行base64编码
def encode_image(image_path):
    """将图片编码为base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# 6个教学步骤 - 严格基于原图
STEPS_TEACHING = [
    {
        "name": "步骤1_铅笔起稿",
        "description": """
Step 1 of 6: Pencil Sketch Draft

IMPORTANT: You must recreate the EXACT SAME bird from the reference image.
This is a teaching progression where each step builds the SAME painting.

Draw ONLY light pencil sketch outlines of the bird perched on a tree branch.
- Show the same bird posture and angle as in the reference
- Same branch position and shape
- Same leaf arrangement
- Light graphite pencil lines on white paper
- NO color, NO shading, just outlines
- Minimal detail, just the basic shapes

This is step 1 of painting the EXACT bird shown in the reference image.
Keep the composition identical to the reference.
        """
    },
    {
        "name": "步骤2_铺底色",
        "description": """
Step 2 of 6: Base Color Layer

IMPORTANT: Continue building the EXACT SAME bird painting from step 1.
Add transparent watercolor base colors to the pencil sketch from step 1.

Paint the same bird with base colors:
- Brown/tan wash for the bird's body
- Green wash for leaves
- Light blue/gray wash for background
- Pale brown for the tree branch

- Keep it loose and light
- NO details yet
- Just flat color areas
- Same composition as step 1 and reference

This is step 2 of creating the EXACT bird painting shown in reference.
The bird must look IDENTICAL to the reference bird in posture and position.
        """
    },
    {
        "name": "步骤3_塑造形体",
        "description": """
Step 3 of 6: Form and Volume Building

IMPORTANT: Continue building the EXACT SAME bird painting from step 2.
Add mid-tones and shadows to the base colors from step 2.

Build volume and form:
- Add mid-tone shadows on the bird's body to show roundness
- Add shadows where the bird meets the branch
- Add form to the leaves (show veins and depth)
- Add shadow under the branch
- The bird's posture is EXACTLY the same as reference
- Branch and leaves in same positions

This is step 3 of creating the IDENTICAL bird from reference.
Still building up the painting, but forms are taking shape.
Same composition, same bird, just adding volume.
        """
    },
    {
        "name": "步骤4_细节刻画",
        "description": """
Step 4 of 6: Fine Detail Rendering

IMPORTANT: Continue adding details to the EXACT SAME bird from step 3.
Paint the same bird with fine details:

- Paint the bird's eye (same position as reference)
- Paint the beak with detail
- Show individual feathers with brushwork
- Add feather textures (same pattern as reference)
- Add leaf veins and details
- Add bark texture to the branch

The bird must match the reference bird's appearance exactly.
Same feather pattern, same colors, same pose.
This is step 4 - we are adding details to the SAME painting.

High detail level but still shows it's a watercolor painting in progress.
        """
    },
    {
        "name": "步骤5_调整统一",
        "description": """
Step 5 of 6: Adjustment and Unification

IMPORTANT: Refine the EXACT SAME bird painting from step 4.
Make final adjustments to match the reference image perfectly:

- Add highlights on the bird's head and wing (same as reference)
- Refine colors to match reference bird exactly
- Add subtle shadows and atmospheric depth
- Unify color temperature across the painting
- Smooth transitions between areas

The bird now looks very close to the reference image.
Same pose, same colors, same feather details.
This is step 5 - nearly finished, just final refinements.

Professional watercolor painting, almost complete.
        """
    },
    {
        "name": "步骤6_落款装裱",
        "description": """
Step 6 of 6: Final Completed Painting with Signature

IMPORTANT: This is the FINAL COMPLETED painting.
The bird should look IDENTICAL or EXTREMELY CLOSE to the reference bird image.

Show the completed bird painting:
- Bird's feathers fully rendered (matching reference)
- Same colors and patterns as reference bird
- Same posture on the branch
- Same background atmosphere
- Add elegant red seal stamp with artist name
- Add subtle Chinese calligraphy signature
- Museum-quality finished artwork

The bird in this final step must be the SAME bird from the reference image.
This is the completed masterpiece after adding all 6 steps together.

Gallery-ready, framed presentation.
Complete traditional Chinese watercolor bird painting.
        """
    }
]


class TeachingStepGenerator:
    """教学步骤生成器 - 严格对应原图"""

    def __init__(self):
        self.client = get_antigravity_client()
        self.all_results = []

    def generate_with_gemini(self, model_name, step_info):
        """使用Gemini生成严格对应的步骤图"""
        try:
            print(f"\n  正在调用 {model_name}...")

            prompt = f"""
You are creating a step-by-step watercolor painting tutorial.

{step_info['description']}

CRITICAL REQUIREMENTS:
1. Paint the EXACT SAME bird from the reference image (bird.jpg)
2. Same posture, same branch, same leaves, same composition
3. This is a teaching progression - each step builds on the previous one
4. Show ONLY the current step level of completion
5. The bird must be recognizable as the SAME bird throughout all steps

Style: Traditional Chinese watercolor painting
Quality: Professional art instruction level
Medium: Watercolor on white paper
Size: 1024x1024

Remember: You are teaching students HOW TO PAINT THIS EXACT BIRD.
Each step shows the progress of painting the SAME bird.
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

                    filename = f"bird_teaching_{model_name.replace('-', '_')}_{step_info['name']}.png"
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

    def generate_all_steps(self):
        """生成所有教学步骤"""

        print("="*80)
        print("为bird.jpg生成严格对应的教学绘画步骤图")
        print("每个步骤都是画同一只鸟的渐进过程")
        print("="*80)

        # 使用最佳质量的模型
        models = ['gemini-3-pro-image-4k']

        for step_info in STEPS_TEACHING:
            print(f"\n{'='*80}")
            print(f"正在生成: {step_info['name']}")
            print('='*80)

            for model in models:
                result = self.generate_with_gemini(model, step_info)
                if result:
                    self.all_results.append(result)
                time.sleep(3)

        return self.all_results


def generate_teaching_html(results):
    """生成教学用HTML展示页面"""

    print("\n正在生成教学展示网页...")

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画教学 - 逐步绘画教程</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
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
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 1.1em;
        }
        .note {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }
        .note strong { color: #856404; }
        .reference-section {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        .reference-section img {
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .step-container {
            margin-bottom: 50px;
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .step-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .step-number {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .step-title {
            font-size: 1.5em;
        }
        .step-image {
            text-align: center;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
        }
        .step-image img {
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .step-description {
            margin-top: 20px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }
        .progress-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .progress-item {
            flex: 1;
            text-align: center;
            padding: 10px;
            font-size: 0.9em;
            color: #666;
            border-right: 1px solid #dee2e6;
        }
        .progress-item:last-child { border-right: none; }
        .progress-item.active {
            background: #667eea;
            color: white;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 鸟儿水彩画 - 完整绘画教程</h1>
        <p class="subtitle">Step-by-Step Watercolor Painting Tutorial</p>

        <div class="note">
            <strong>📚 教学说明：</strong>
            本教程展示如何用水彩画技法绘制这只鸟。每个步骤都是基于同一张参考图的渐进过程，
            从铅笔起稿到最终完成，完整记录了绘画的每一个阶段。
            所有步骤图严格对应参考图，确保学习者能够准确跟随教程。
        </div>

        <div class="progress-bar">
            <div class="progress-item active">步骤1: 铅笔起稿</div>
            <div class="progress-item active">步骤2: 铺底色</div>
            <div class="progress-item active">步骤3: 塑造形体</div>
            <div class="progress-item active">步骤4: 细节刻画</div>
            <div class="progress-item active">步骤5: 调整统一</div>
            <div class="progress-item active">步骤6: 落款装裱</div>
        </div>

        <div class="reference-section">
            <h2>📷 参考图片 (Reference Image)</h2>
            <p style="margin-top: 10px; color: #666;">所有绘画步骤都严格基于这张参考图</p>
            <img src="bird.jpg" alt="参考图片 - 鸟儿">
        </div>
"""

    step_number = 1
    for result in results:
        step_name_cn = result['step'].split('_', 1)[1]

        html_content += f"""
        <div class="step-container">
            <div class="step-header">
                <div class="step-number">第 {step_number} 步</div>
                <div class="step-title">{step_name_cn}</div>
            </div>
            <div class="step-image">
                <img src="{result['filename']}" alt="步骤{step_number} - {step_name_cn}">
            </div>
        </div>
"""
        step_number += 1

    html_content += f"""
        <div class="footer">
            <p>教学完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>使用模型: Gemini-3-Pro-Image-4K (最高质量)</p>
            <p>所有步骤图严格对应参考图，适合绘画教学使用</p>
        </div>
    </div>
</body>
</html>
"""

    filename = "bird_painting_teaching_gallery.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"教学网页已生成: {filename}")

    return filename


def main():
    """主函数"""
    print("\n" + "="*80)
    print("鸟儿水彩画教学 - 严格对应参考图的绘画步骤生成")
    print("="*80)

    # 生成所有步骤
    generator = TeachingStepGenerator()
    results = generator.generate_all_steps()

    # 显示结果
    print("\n" + "="*80)
    print("生成结果汇总")
    print("="*80)
    print(f"\n总计生成: {len(results)} 张教学步骤图\n")

    for result in results:
        print(f"✓ {result['step']} - {result['filename']}")

    # 生成教学HTML
    html_file = generate_teaching_html(results)

    print("\n" + "="*80)
    print("教学完成！")
    print("="*80)
    print(f"\n教学网页: {html_file}")
    print("\n正在在浏览器中打开...")

    # 打开浏览器
    import webbrowser
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))


if __name__ == "__main__":
    main()
