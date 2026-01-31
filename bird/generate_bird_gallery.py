# -*- coding: utf-8 -*-
"""
生成鸟儿绘画步骤展示网页
"""

from pathlib import Path
from datetime import datetime

def generate_html():
    """生成HTML展示页面"""

    # 所有生成的图片
    images = {
        '步骤1_铅笔起稿': [
            ('bird_gemini_3_pro_image_步骤1_铅笔起稿.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤1_铅笔起稿.png', 'Gemini-3-Pro-Image-4K'),
            ('bird_Pollinations_步骤1_铅笔起稿.png', 'Pollinations')
        ],
        '步骤2_铺底色': [
            ('bird_gemini_3_pro_image_步骤2_铺底色.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤2_铺底色.png', 'Gemini-3-Pro-Image-4K'),
        ],
        '步骤3_塑造形体': [
            ('bird_gemini_3_pro_image_步骤3_塑造形体.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤3_塑造形体.png', 'Gemini-3-Pro-Image-4K'),
            ('bird_Pollinations_步骤3_塑造形体.png', 'Pollinations')
        ],
        '步骤4_细节刻画': [
            ('bird_gemini_3_pro_image_步骤4_细节刻画.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤4_细节刻画.png', 'Gemini-3-Pro-Image-4K'),
            ('bird_Pollinations_步骤4_细节刻画.png', 'Pollinations')
        ],
        '步骤5_调整统一': [
            ('bird_gemini_3_pro_image_步骤5_调整统一.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤5_调整统一.png', 'Gemini-3-Pro-Image-4K'),
            ('bird_Pollinations_步骤5_调整统一.png', 'Pollinations')
        ],
        '步骤6_落款装裱': [
            ('bird_gemini_3_pro_image_步骤6_落款装裱.png', 'Gemini-3-Pro-Image'),
            ('bird_gemini_3_pro_image_4k_步骤6_落款装裱.png', 'Gemini-3-Pro-Image-4K'),
            ('bird_Pollinations_步骤6_落款装裱.png', 'Pollinations')
        ]
    }

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

        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: #f8f9fa;
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            margin-top: 5px;
        }

        @media (max-width: 768px) {
            .models-grid {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }

            .stats {
                flex-direction: column;
                gap: 15px;
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

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">6</div>
                <div class="stat-label">绘画步骤</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">3</div>
                <div class="stat-label">AI模型</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">17</div>
                <div class="stat-label">生成图片</div>
            </div>
        </div>
"""

    step_number = 1
    for step_name in ['步骤1_铅笔起稿', '步骤2_铺底色', '步骤3_塑造形体',
                      '步骤4_细节刻画', '步骤5_调整统一', '步骤6_落款装裱']:
        if step_name in images:
            html_content += f"""
        <div class="step-section">
            <h2 class="step-title">第{step_number}步: {step_name.split('_', 1)[1]}</h2>
            <div class="models-grid">
"""

            for img_file, model_name in images[step_name]:
                html_content += f"""
                <div class="model-card">
                    <h3>🤖 {model_name}</h3>
                    <img src="{img_file}" alt="{model_name} - {step_name}">
                    <div class="info">
                        <p>文件: {img_file}</p>
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
            <p>使用模型: Gemini-3-Pro-Image, Gemini-3-Pro-Image-4K, Pollinations</p>
            <p>技术: Python + anti-gravity + OpenAI SDK</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    filename = "bird_painting_steps_gallery.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\nHTML文件已生成: {filename}")

    return filename

if __name__ == "__main__":
    print("正在生成HTML展示页面...")
    html_file = generate_html()
    print(f"\n完成！")
    print(f"HTML文件: {html_file}")

    # 打开浏览器
    import webbrowser
    print("\n正在在浏览器中打开...")
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))
