# -*- coding: utf-8 -*-
"""
创建最终的鸟儿水彩画教学网页
使用已生成的完整6步骤图片
"""

from pathlib import Path
from datetime import datetime

def create_final_teaching_html():
    """创建最终的教学展示页面"""

    # 完整的6个步骤
    steps = [
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤1_铅笔起稿.png',
            'title': '步骤1: 铅笔起稿',
            'description': '''
                <h3>📝 教学要点：</h3>
                <ul>
                    <li>用铅笔轻轻勾勒出鸟儿的基本轮廓</li>
                    <li>确定鸟儿在树枝上的位置和姿态</li>
                    <li>画出树枝和树叶的大致位置</li>
                    <li><strong>注意：</strong>线条要轻，便于后续修改</li>
                </ul>
            '''
        },
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤2_铺底色.png',
            'title': '步骤2: 铺底色',
            'description': '''
                <h3>🎨 教学要点：</h3>
                <ul>
                    <li>用淡彩铺设基本色调</li>
                    <li>鸟儿身体用棕色/赭石色</li>
                    <li>树叶用绿色</li>
                    <li>背景用淡蓝色或灰色</li>
                    <li><strong>注意：</strong>颜色要透明，不要一次涂太厚</li>
                </ul>
            '''
        },
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤3_塑造形体.png',
            'title': '步骤3: 塑造形体',
            'description': '''
                <h3>🖌️ 教学要点：</h3>
                <ul>
                    <li>添加中间色调，塑造立体感</li>
                    <li>在鸟儿身体添加阴影</li>
                    <li>加强树枝和树叶的体积感</li>
                    <li>注意光影方向的一致性</li>
                    <li><strong>注意：</strong>逐步加深，不要急于完成</li>
                </ul>
            '''
        },
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤4_细节刻画.png',
            'title': '步骤4: 细节刻画',
            'description': '''
                <h3>✏️ 教学要点：</h3>
                <ul>
                    <li>刻画鸟儿的眼睛和喙</li>
                    <li>描绘羽毛的纹理</li>
                    <li>添加树叶的叶脉</li>
                    <li>表现树皮的质感</li>
                    <li><strong>注意：</strong>细节要精致，但不要破坏整体</li>
                </ul>
            '''
        },
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤5_调整统一.png',
            'title': '步骤5: 调整统一',
            'description': '''
                <h3>🔧 教学要点：</h3>
                <ul>
                    <li>添加高光，增强立体感</li>
                    <li>调整整体色彩，使其和谐统一</li>
                    <li>加强或减弱某些部分</li>
                    <li>处理边缘，使其更自然</li>
                    <li><strong>注意：</strong>退后观察，看整体效果</li>
                </ul>
            '''
        },
        {
            'file': 'bird_gemini_3_pro_image_4k_步骤6_落款装裱.png',
            'title': '步骤6: 落款装裱',
            'description': '''
                <h3>✨ 教学要点：</h3>
                <ul>
                    <li>添加红色印章（落款）</li>
                    <li>添加书法签名</li>
                    <li>检查并做最后的微调</li>
                    <li>装裱效果展示</li>
                    <li><strong>注意：</strong>落款要与画面协调</li>
                </ul>
            '''
        }
    ]

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画完整教程 - 6步教学法</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }

        .header {
            text-align: center;
            margin-bottom: 50px;
        }

        h1 {
            font-size: 2.8em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }

        .subtitle {
            font-size: 1.3em;
            color: #666;
            margin-bottom: 10px;
        }

        .badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: bold;
            margin: 10px 5px;
        }

        .reference {
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
        }

        .reference img {
            max-width: 100%;
            max-height: 450px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .progress-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .progress-item {
            flex: 1;
            min-width: 120px;
            text-align: center;
            padding: 15px 10px;
            background: white;
            border-radius: 8px;
            font-weight: bold;
            color: #667eea;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .step-section {
            margin-bottom: 60px;
            animation: fadeIn 0.6s ease-in;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .step-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }

        .step-number {
            font-size: 1.2em;
            font-weight: bold;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .step-title {
            font-size: 2em;
            font-weight: bold;
        }

        .step-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            align-items: start;
        }

        .step-image {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }

        .step-image img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            transition: transform 0.3s;
        }

        .step-image img:hover {
            transform: scale(1.02);
        }

        .step-description {
            background: white;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .step-description h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }

        .step-description ul {
            list-style: none;
            padding-left: 0;
        }

        .step-description li {
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            color: #555;
        }

        .step-description li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }

        .step-description strong {
            color: #d63384;
            background: #fff3cd;
            padding: 2px 8px;
            border-radius: 4px;
        }

        .tips {
            background: #e7f3ff;
            border-left: 5px solid #2196f3;
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
        }

        .tips h4 {
            color: #2196f3;
            margin-bottom: 10px;
        }

        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 3px solid #e0e0e0;
            color: #666;
        }

        .footer-info {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .footer-item {
            text-align: center;
        }

        .footer-item strong {
            display: block;
            font-size: 1.5em;
            color: #667eea;
        }

        @media (max-width: 968px) {
            .step-content {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 2em;
            }

            .progress-item {
                min-width: 100px;
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 鸟儿水彩画完整教程</h1>
            <p class="subtitle">从铅笔起稿到落款装裱 - 6步完整教学</p>
            <div>
                <span class="badge">完整教程</span>
                <span class="badge">AI辅助生成</span>
                <span class="badge">高质量</span>
            </div>
        </div>

        <div class="progress-bar">
            <div class="progress-item">步骤1<br>铅笔起稿</div>
            <div class="progress-item">步骤2<br>铺底色</div>
            <div class="progress-item">步骤3<br>塑造形体</div>
            <div class="progress-item">步骤4<br>细节刻画</div>
            <div class="progress-item">步骤5<br>调整统一</div>
            <div class="progress-item">步骤6<br>落款装裱</div>
        </div>

        <div class="reference">
            <h2>📷 参考图片 (Reference Image)</h2>
            <p style="margin-top: 10px; color: #666;">本教程所有步骤都基于这张参考图进行绘制</p>
            <img src="bird.jpg" alt="参考图片 - 鸟儿">
            <div class="tips" style="margin-top: 20px;">
                <h4>💡 学习建议：</h4>
                <p>在跟随本教程学习时，请时刻对比参考图，确保每个步骤的构图、姿态与参考图保持一致。</p>
            </div>
        </div>
"""

    # 生成每个步骤的HTML
    for i, step in enumerate(steps, 1):
        html_content += f"""
        <div class="step-section">
            <div class="step-header">
                <div class="step-number">STEP {i}</div>
                <div class="step-title">{step['title']}</div>
            </div>
            <div class="step-content">
                <div class="step-image">
                    <img src="{step['file']}" alt="{step['title']}">
                </div>
                <div class="step-description">
                    {step['description']}
                </div>
            </div>
        </div>
"""
        # 添加间隔让每个步骤的动画错开
        if i < len(steps):
            import time
            time.sleep(0.1)

    html_content += f"""
        <div class="footer">
            <h3>🎓 教程说明</h3>
            <p style="margin-top: 15px;">本教程由AI（Gemini-3-Pro-Image-4K）生成，展示了完整的水彩画绘画过程。</p>
            <p>每个步骤都是基于参考图的渐进过程，适合初学者学习和参考。</p>

            <div class="footer-info">
                <div class="footer-item">
                    <strong>6</strong>
                    完整步骤
                </div>
                <div class="footer-item">
                    <strong>4K</strong>
                    超高画质
                </div>
                <div class="footer-item">
                    <strong>AI</strong>
                    辅助生成
                </div>
                <div class="footer-item">
                    <strong>教学</strong>
                    专业级别
                </div>
            </div>

            <p style="margin-top: 30px; color: #999;">
                生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}<br>
                技术支持: Python + anti-gravity + Gemini AI
            </p>
        </div>
    </div>

    <script>
        // 滚动到每个步骤时的淡入效果
        const steps = document.querySelectorAll('.step-section');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1
        });

        steps.forEach(step => {
            step.style.opacity = '0';
            step.style.transform = 'translateY(30px)';
            step.style.transition = 'opacity 0.6s ease-in, transform 0.6s ease-in';
            observer.observe(step);
        });
    </script>
</body>
</html>
"""

    # 保存文件
    filename = "bird_painting_complete_tutorial.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n完整教程网页已生成: {filename}")
    print("文件包含:")
    print("  - 参考图片展示")
    print("  - 6个完整绘画步骤")
    print("  - 详细的教学要点")
    print("  - 渐进式进度条")
    print("  - 响应式设计")
    print("  - 动画效果")

    return filename


if __name__ == "__main__":
    print("\n正在生成最终的完整教学网页...")
    print("="*80)

    html_file = create_final_teaching_html()

    print("\n" + "="*80)
    print("完成！")
    print("="*80)
    print(f"\n教学网页: {html_file}")

    # 在浏览器中打开
    import webbrowser
    print("\n正在在浏览器中打开...")
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))

    print("\n✓ 教程已准备就绪！")
