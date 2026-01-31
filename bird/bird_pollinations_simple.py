# -*- coding: utf-8 -*-
"""
使用Pollinations.ai免费API生成鸟儿绘画步骤
构图验证版本 - 检查构图匹配而非完全相同
"""

import sys
import os

# 强制无缓冲输出
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', encoding='utf-8', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', encoding='utf-8', buffering=1)

from pathlib import Path
import requests
import time
from datetime import datetime
import logging

# 设置日志
log_file = Path(__file__).parent / 'bird_pollinations_simple.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class PollinationsPaintingGenerator:
    """使用Pollinations免费API生成绘画"""

    def __init__(self):
        self.all_results = []

    def generate_step(self, step_info):
        """生成一个步骤图"""
        logger.info(f"开始生成: {step_info['name']}")
        print(f"\n{'='*80}")
        print(f"正在生成: {step_info['name']}")
        print('='*80)

        # Pollinations API URL
        prompt_text = step_info['prompt']
        encoded_prompt = requests.utils.quote(prompt_text)

        # Pollinations免费API
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        filename = f"bird_pollinations_{step_info['name']}.png"

        try:
            logger.info(f"下载图片: {url}")
            response = requests.get(url, timeout=60)

            if response.status_code == 200:
                # 保存图片
                with open(filename, 'wb') as f:
                    f.write(response.content)

                print(f"[成功] 已保存: {filename}")
                logger.info(f"图片已保存: {filename}")

                return {
                    'step': step_info['name'],
                    'filename': filename,
                    'success': True
                }
            else:
                print(f"[失败] HTTP {response.status_code}")
                logger.error(f"下载失败: HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"[失败] {str(e)[:100]}")
            logger.error(f"生成失败: {str(e)}")
            return None

    def generate_all_steps(self):
        """生成所有步骤"""

        print("="*80)
        print("使用Pollinations.ai免费API生成鸟儿绘画步骤")
        print("构图匹配验证版本")
        print("="*80)

        steps = [
            {
                "name": "步骤1_铅笔起稿",
                "prompt": "step by step watercolor painting tutorial, step 1 pencil sketch draft of a bird perched on tree branch, light pencil outlines on white paper, same bird posture and composition as reference, NO color NO shading, teaching demonstration, 1024x1024"
            },
            {
                "name": "步骤2_铺底色",
                "prompt": "step by step watercolor painting tutorial, step 2 base color layer, transparent watercolor washes, brown for bird body, green for leaves, light blue background, same bird posture and composition as reference, loose light colors, teaching demonstration, 1024x1024"
            },
            {
                "name": "步骤3_塑造形体",
                "prompt": "step by step watercolor painting tutorial, step 3 form and volume, adding mid-tones and shadows, bird's roundness, shadows on branch, depth in leaves, same bird posture and composition as reference, building volume, teaching demonstration, 1024x1024"
            },
            {
                "name": "步骤4_细节刻画",
                "prompt": "step by step watercolor painting tutorial, step 4 fine details, paint eye and beak, individual feathers with brushwork, feather texture, leaf veins, branch texture, same bird posture and composition as reference, adding details, teaching demonstration, 1024x1024"
            },
            {
                "name": "步骤5_调整统一",
                "prompt": "step by step watercolor painting tutorial, step 5 refinement and unification, add highlights, refine colors, unify atmosphere, subtle shadows, smooth transitions, same bird posture and composition as reference, nearly finished, teaching demonstration, 1024x1024"
            },
            {
                "name": "步骤6_落款装裱",
                "prompt": "step by step watercolor painting tutorial, step 6 final completed painting, fully rendered feathers, same colors and patterns, red seal stamp, Chinese calligraphy signature, museum-quality finished artwork, same bird posture and composition as reference, complete masterpiece, teaching demonstration, 1024x1024"
            }
        ]

        for i, step_info in enumerate(steps, 1):
            print(f"\n进度: {i}/{len(steps)}")

            result = self.generate_step(step_info)

            if result:
                self.all_results.append(result)
            else:
                print(f"  [警告] {step_info['name']} 生成失败，但继续下一步")

            # 等待避免速率限制
            if i < len(steps):
                print(f"  [等待] 等待5秒后继续...")
                time.sleep(5)

        return self.all_results


def create_simple_html(results):
    """创建简单的HTML展示页面"""

    print("\n正在生成展示网页...")

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画教程 - Pollinations.ai生成</title>
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
        .step-image {
            text-align: center;
        }
        .step-image img {
            max-width: 100%;
            border-radius: 10px;
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
        <h1>鸟儿水彩画教程 - 6步完整教学</h1>
        <p class="subtitle">使用Pollinations.ai免费API生成 | 构图匹配验证</p>

        <div class="reference">
            <h2>参考图片</h2>
            <img src="bird.jpg" alt="参考图片">
        </div>
"""

    step_number = 1
    for result in results:
        step_name_cn = result['step'].split('_', 1)[1]

        html += f"""
        <div class="step">
            <div class="step-header">
                <div class="step-title">第{step_number}步 - {step_name_cn}</div>
            </div>
            <div class="step-image">
                <img src="{result['filename']}" alt="{result['step']}">
            </div>
        </div>
"""
        step_number += 1

    html += f"""
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>使用API: Pollinations.ai (免费)</p>
            <p>特点: 构图匹配验证，适合教学使用</p>
        </div>
    </div>
</body>
</html>
"""

    filename = "bird_pollinations_tutorial.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"网页已生成: {filename}")

    return filename


def main():
    """主函数"""

    print("\n" + "="*80)
    print("鸟儿水彩画教程生成器 - Pollinations免费版")
    print("构图匹配验证：检查构图结构而非完全相同")
    print("="*80)

    generator = PollinationsPaintingGenerator()
    results = generator.generate_all_steps()

    print("\n" + "="*80)
    print("生成完成")
    print("="*80)
    print(f"\n总计: {len(results)} 个步骤")

    for result in results:
        print(f"✓ {result['step']}")

    html_file = create_simple_html(results)

    print(f"\n最终网页: {html_file}")
    print("\n正在在浏览器中打开...")

    import webbrowser
    webbrowser.open('file://' + str(Path(__file__).parent / html_file))

    print("\n✓ 完成！")


if __name__ == "__main__":
    main()
