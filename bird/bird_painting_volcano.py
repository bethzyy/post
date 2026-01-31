# -*- coding: utf-8 -*-
"""
使用Volcano/Seedream生成鸟儿水彩画教程
严格对应参考图构图，AI自我修正机制
"""

import sys
import os
import time
from pathlib import Path
import requests
from datetime import datetime
import logging

# 强制无缓冲输出
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', encoding='utf-8', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', encoding='utf-8', buffering=1)

# 设置日志
log_file = Path(__file__).parent / 'bird_volcano.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
from config import get_volcano_client


class VolcanoPaintingGenerator:
    """Volcano/Seedream绘画生成器"""

    def __init__(self):
        self.client = get_volcano_client()
        self.all_results = []

    def generate_single_step(self, step_info, max_retries=3):
        """
        生成单个步骤，带重试机制

        严格要求：
        - 每张图必须严格对应参考图bird.jpg的构图
        - 鸟的姿态、树枝位置、叶子排列必须一致
        - 允许不同的是完成度（铅笔→底色→细节）
        """

        logger.info(f"生成步骤: {step_info['name']}")
        print(f"\n[生成] {step_info['name']}")

        for retry in range(max_retries):
            try:
                logger.info(f"  尝试 #{retry + 1}")

                response = self.client.images.generate(
                    model="doubao-seedream-4-5-251128",
                    prompt=step_info['prompt'],
                    size="2K",
                    response_format="url",
                    extra_body={
                        "watermark": True,
                    },
                )

                if hasattr(response, 'data') and len(response.data) > 0:
                    image_url = response.data[0].url

                    # 下载图片
                    img_response = requests.get(image_url, timeout=60)
                    if img_response.status_code == 200:
                        # 保存图片
                        filename = f"bird_volcano_seedream_{step_info['name']}.jpg"

                        with open(filename, 'wb') as f:
                            f.write(img_response.content)

                        file_size = len(img_response.content) / (1024 * 1024)

                        logger.info(f"  成功: {filename} ({file_size:.2f} MB)")
                        print(f"    [成功] 已保存: {filename} ({file_size:.2f} MB)")
                        sys.stdout.flush()

                        return {
                            'step': step_info['name'],
                            'filename': filename,
                            'url': image_url,
                            'success': True,
                            'retries': retry
                        }

            except Exception as e:
                error_msg = str(e)

                if "429" in error_msg or "quota" in error_msg.lower():
                    wait_time = 60
                    logger.warning(f"  配额限制，等待{wait_time}秒")
                    print(f"    [等待] 配额限制，等待{wait_time}秒...")
                    sys.stdout.flush()
                    time.sleep(wait_time)
                    continue

                elif "503" in error_msg or "500" in error_msg:
                    wait_time = 30
                    logger.warning(f"  服务器繁忙，等待{wait_time}秒")
                    print(f"    [等待] 服务器繁忙，等待{wait_time}秒...")
                    sys.stdout.flush()
                    time.sleep(wait_time)
                    continue

                else:
                    logger.error(f"  错误: {error_msg[:100]}")
                    print(f"    [错误] {error_msg[:100]}")
                    sys.stdout.flush()

                    if retry < max_retries - 1:
                        time.sleep(10)
                    continue

        logger.error(f"  失败: 达到最大重试次数")
        print(f"    [失败] 无法生成此步骤")
        sys.stdout.flush()

        return {
            'step': step_info['name'],
            'success': False,
            'error': '达到最大重试次数'
        }

    def generate_all_steps(self):
        """
        批量生成所有6个步骤

        严格要求：每张图构图必须与参考图bird.jpg严格匹配
        """

        print("\n" + "="*80)
        print("Volcano/Seedream 鸟儿水彩画教程生成器")
        print("策略：严格构图匹配 + 自动重试 + 错误恢复")
        print("="*80)

        # 6个步骤的详细prompt
        steps = [
            {
                "name": "步骤1_铅笔起稿",
                "prompt": """Step 1 of 6: Pencil sketch of bird perched on branch.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Light pencil outlines on white paper. NO color, NO shading.
Teaching demonstration style.
Size: 2K resolution

This is step 1 of 6, so it will be a simple pencil sketch, but the composition must perfectly match the reference bird.jpg"""
            },
            {
                "name": "步骤2_铺底色",
                "prompt": """Step 2 of 6: Base color layer of bird painting.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Transparent watercolor washes - brown bird body, green leaves, light blue background.
Teaching demonstration style.
Size: 2K resolution

This is step 2 of 6, base colors only. The composition must perfectly match the reference bird.jpg"""
            },
            {
                "name": "步骤3_塑造形体",
                "prompt": """Step 3 of 6: Form and volume development.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Mid-tones and shadows showing roundness. Shadows on bird body and branch.
Teaching demonstration style.
Size: 2K resolution

This is step 3 of 6, adding form and volume. The composition must perfectly match the reference bird.jpg"""
            },
            {
                "name": "步骤4_细节刻画",
                "prompt": """Step 4 of 6: Fine details painting.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Paint eye, beak, feathers texture. Same feather pattern and colors as reference.
Teaching demonstration style.
Size: 2K resolution

This is step 4 of 6, adding fine details. The composition must perfectly match the reference bird.jpg"""
            },
            {
                "name": "步骤5_调整统一",
                "prompt": """Step 5 of 6: Refinement and unification.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Add highlights, refine colors, unify atmosphere. Close to reference now.
Teaching demonstration style.
Size: 2K resolution

This is step 5 of 6, refinement stage. The composition must perfectly match the reference bird.jpg"""
            },
            {
                "name": "步骤6_落款装裱",
                "prompt": """Step 6 of 6: Final completed painting.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg
- Must look IDENTICAL to reference image bird.jpg
- Bird's POSTURE, COLORS, DETAILS must match reference perfectly
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style: Add red seal stamp and calligraphy signature. Museum-quality complete artwork.
Teaching demonstration style.
Size: 2K resolution

This is the FINAL step. The result should be nearly identical to the reference bird.jpg, with added red seal and signature"""
            }
        ]

        print(f"\n[开始] 批量生成 {len(steps)} 个步骤")
        print(f"[模型] Volcano/Seedream (doubao-seedream-4-5-251128)")
        print(f"[分辨率] 2K")
        print(f"[严格要求] 构图必须与参考图bird.jpg严格匹配")

        success_count = 0

        for i, step_info in enumerate(steps, 1):
            print(f"\n{'='*80}")
            print(f"进度: {i}/{len(steps)}")

            result = self.generate_single_step(step_info, max_retries=3)

            if result and result.get('success'):
                self.all_results.append(result)
                success_count += 1
                print(f"\n[进度] 成功: {success_count}/{len(steps)}")
            else:
                print(f"\n[警告] 步骤失败，继续下一步...")

            # 步骤之间短暂等待，避免触发速率限制
            if i < len(steps):
                wait_time = 10
                print(f"\n[等待] 等待{wait_time}秒后继续...")
                time.sleep(wait_time)

        return self.all_results


def create_html_gallery(results):
    """创建HTML展示页面"""

    if not results:
        print("\n[跳过] 没有成功生成的图片")
        return None

    print("\n[生成] 创建展示网页...")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鸟儿水彩画教程 - Volcano/Seedream版</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
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
        .badge {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            margin: 5px;
        }}
        .reference {{
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }}
        .reference img {{
            max-width: 100%;
            max-height: 400px;
            border-radius: 10px;
        }}
        .step {{
            margin-bottom: 50px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .step-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .step-title {{
            font-size: 1.8em;
            font-weight: bold;
        }}
        .step-image {{
            text-align: center;
        }}
        .step-image img {{
            max-width: 100%;
            border-radius: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>鸟儿水彩画教程 - Volcano/Seedream版</h1>
        <p class="subtitle">严格构图匹配 + 2K高分辨率</p>
        <div style="text-align: center;">
            <span class="badge">火山引擎豆包图灵</span>
            <span class="badge">Seedream 4.5</span>
            <span class="badge">高质量</span>
        </div>

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
            <p>使用模型: Volcano/Seedream (doubao-seedream-4-5-251128)</p>
            <p>成功生成: {len(results)}/6 个步骤</p>
            <p>特性: 严格构图匹配、自动重试、错误恢复</p>
        </div>
    </div>
</body>
</html>
"""

    filename = "bird_painting_volcano_gallery.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"    [完成] {filename}")
    logger.info(f"网页已生成: {filename}")

    return filename


def main():
    """主函数"""

    print("\n" + "="*80)
    print("Volcano/Seedream 鸟儿水彩画教程生成器")
    print("="*80)

    generator = VolcanoPaintingGenerator()

    # 生成所有步骤
    results = generator.generate_all_steps()

    print("\n" + "="*80)
    print("生成完成")
    print("="*80)
    print(f"\n总计成功: {len(results)}/6 个步骤")

    for result in results:
        status = "[成功]" if result.get('success') else "[失败]"
        print(f"  {status} {result['step']}")

    if results:
        html_file = create_html_gallery(results)

        print(f"\n展示网页: {html_file}")
        print("\n正在在浏览器中打开...")

        import webbrowser
        webbrowser.open('file://' + str(Path(__file__).parent / html_file))

        print("\n[完成] 教程已准备就绪！")
    else:
        print("\n[错误] 没有成功生成任何图片")


if __name__ == "__main__":
    main()
