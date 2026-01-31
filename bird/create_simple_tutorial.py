# -*- coding: utf-8 -*-
"""
创建鸟儿水彩画教学网页 - 简化版
"""

from pathlib import Path
from datetime import datetime

def create_html():
    """创建教学HTML页面"""

    steps = [
        ('bird_gemini_3_pro_image_4k_步骤1_铅笔起稿.png', '步骤1: 铅笔起稿', '用铅笔轻轻勾勒出鸟儿和树枝的基本轮廓'),
        ('bird_gemini_3_pro_image_4k_步骤2_铺底色.png', '步骤2: 铺底色', '用淡彩铺设基本色调，鸟儿身体、树叶、背景'),
        ('bird_gemini_3_pro_image_4k_步骤3_塑造形体.png', '步骤3: 塑造形体', '添加中间色调，塑造立体感和阴影'),
        ('bird_gemini_3_pro_image_4k_步骤4_细节刻画.png', '步骤4: 细节刻画', '刻画眼睛、喙、羽毛纹理等细节'),
        ('bird_gemini_3_pro_image_4k_步骤5_调整统一.png', '步骤5: 调整统一', '添加高光，调整整体色彩和谐'),
        ('bird_gemini_3_pro_image_4k_步骤6_落款装裱.png', '步骤6: 落款装裱', '添加印章签名，完成作品')
    ]

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画教程</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
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
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
        .reference {
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }
        .reference img {
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .step {
            margin-bottom: 50px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .step-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .step-title {
            font-size: 1.8em;
            font-weight: bold;
        }
        .step-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        .step-image img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .step-desc {
            padding: 20px;
            background: #f8f9fa;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>鸟儿水彩画教程</h1>
        <p class="subtitle">6步完整教学 | 从起稿到装裱</p>

        <div class="reference">
            <h2>参考图片</h2>
            <img src="bird.jpg" alt="参考图片">
        </div>
"""

    for i, (file, title, desc) in enumerate(steps, 1):
        html += f"""
        <div class="step">
            <div class="step-header">
                <div class="step-title">第{i}步 - {title}</div>
            </div>
            <div class="step-content">
                <div class="step-image">
                    <img src="{file}" alt="{title}">
                </div>
                <div class="step-desc">
                    <h3>教学要点</h3>
                    <p>{desc}</p>
                </div>
            </div>
        </div>
"""

    html += f"""
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>使用模型: Gemini-3-Pro-Image-4K</p>
            <p>技术: AI辅助生成</p>
        </div>
    </div>
</body>
</html>
"""

    filename = "bird_painting_tutorial_final.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"教学网页已生成: {filename}")

    return filename

if __name__ == "__main__":
    html_file = create_html()
    print(f"\\n正在在浏览器中打开...")
    import webbrowser
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))
    print("\\n完成！")
