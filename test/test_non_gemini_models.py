#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
非Gemini图像模型对比测试工具
测试anti-gravity支持的所有非Gemini图像生成模型(DALL-E、Flux、Stable Diffusion等)
注意: 不包含SeeDream,因为SeeDream是Volcano引擎管理的,不是antigravity管理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_antigravity_client
from datetime import datetime
import base64
import json

# 非Gemini图像模型配置
NON_GEMINI_IMAGE_MODELS = {
    'dall-e-3': {
        'name': 'DALL-E 3',
        'description': 'OpenAI最新图像模型,质量极高',
        'provider': 'OpenAI',
        'size': '1024x1024'
    },
    'dall-e-2': {
        'name': 'DALL-E 2',
        'description': 'OpenAI经典图像模型',
        'provider': 'OpenAI',
        'size': '1024x1024'
    },
    'flux-1.1-pro': {
        'name': 'Flux 1.1 Pro',
        'description': 'Black Forest Labs最新模型',
        'provider': 'Black Forest Labs',
        'size': '1024x1024'
    },
    'flux-schnell': {
        'name': 'Flux Schnell',
        'description': 'Flux快速版本',
        'provider': 'Black Forest Labs',
        'size': '1024x1024'
    },
    'flux-dev': {
        'name': 'Flux Dev',
        'description': 'Flux开发版本',
        'provider': 'Black Forest Labs',
        'size': '1024x1024'
    },
    'sd-3': {
        'name': 'Stable Diffusion 3',
        'description': 'Stability AI最新SD模型',
        'provider': 'Stability AI',
        'size': '1024x1024'
    },
    'sd-xl-lightning': {
        'name': 'SD XL Lightning',
        'description': 'SD XL快速生成版本',
        'provider': 'Stability AI',
        'size': '1024x1024'
    }
}

# 测试提示词
TEST_PROMPTS = [
    {
        'title': '中国传统山水画',
        'prompt': 'Traditional Chinese landscape painting, mountains and mist, ink wash style, serene atmosphere',
        'category': 'art'
    },
    {
        'title': '可爱猫咪',
        'prompt': 'A cute fluffy cat sitting on a wooden fence, warm golden hour sunlight, realistic style',
        'category': 'animal'
    },
    {
        'title': '未来城市',
        'prompt': 'Futuristic cyberpunk city at night, neon lights, flying cars, rain reflections, cinematic lighting',
        'category': 'scifi'
    },
    {
        'title': '美食',
        'prompt': 'Delicious steaming hot bowl of ramen noodles, eggs, green onions, food photography, professional lighting',
        'category': 'food'
    },
    {
        'title': '花鸟画',
        'prompt': 'Traditional Chinese bird and flower painting, bamboo, plum blossoms, elegant brush strokes',
        'category': 'art'
    }
]

def generate_image(client, model_id, prompt, size):
    """生成单张图像"""
    try:
        response = client.images.generate(
            model=model_id,
            prompt=prompt,
            size=size,
            n=1,
        )

        if hasattr(response, 'data') and len(response.data) > 0:
            image_data = response.data[0]
            b64_json = getattr(image_data, 'b64_json', None)

            if b64_json:
                image_bytes = base64.b64decode(b64_json)
                return {
                    'success': True,
                    'data': image_bytes,
                    'size': len(image_bytes)
                }

        return {
            'success': False,
            'error': 'No image data in response'
        }

    except Exception as e:
        error_str = str(e)
        # 检查是否是配额问题
        if '429' in error_str or 'quota' in error_str.lower() or 'exhausted' in error_str.lower():
            return {
                'success': False,
                'error': 'QUOTA_EXHAUSTED',
                'details': error_str
            }
        # 检查是否是模型不支持
        elif '404' in error_str or 'not found' in error_str.lower() or 'not supported' in error_str.lower():
            return {
                'success': False,
                'error': 'MODEL_NOT_SUPPORTED',
                'details': error_str
            }
        else:
            return {
                'success': False,
                'error': error_str
            }

def load_progress(output_dir):
    """加载之前的测试进度"""
    progress_file = f"{output_dir}/non_gemini_progress.json"

    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
                print(f"[INFO] 发现已保存的测试进度")
                print(f"[INFO] 上次测试时间: {progress.get('timestamp', 'Unknown')}")
                print(f"[INFO] 已完成: {progress.get('completed_count', 0)}/{progress.get('total_count', 0)}")
                print()
                return progress
        except Exception as e:
            print(f"[WARNING] 无法加载进度文件: {e}")

    return None

def save_progress(output_dir, completed_tasks, total_count, all_results):
    """保存测试进度"""
    progress = {
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'completed_count': len(completed_tasks),
        'total_count': total_count,
        'completed_tasks': list(completed_tasks),
        'all_results': all_results
    }

    progress_file = f"{output_dir}/non_gemini_progress.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def generate_html_comparison(results, output_dir, timestamp):
    """生成HTML对比展示"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>非Gemini图像模型对比测试 - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
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
            font-size: 2.5em;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}

        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .summary h2 {{
            margin-bottom: 15px;
            font-size: 1.5em;
        }}

        .summary-stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
        }}

        .model-section {{
            margin-bottom: 50px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            background: #f9f9f9;
        }}

        .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #ddd;
        }}

        .model-title {{
            font-size: 1.8em;
            color: #333;
            font-weight: bold;
        }}

        .model-meta {{
            color: #666;
            font-size: 0.9em;
        }}

        .images-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .image-card {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}

        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}

        .image-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .image-info {{
            padding: 15px;
        }}

        .image-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .image-prompt {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
            font-style: italic;
        }}

        .image-meta {{
            font-size: 0.8em;
            color: #999;
        }}

        .status-success {{
            color: #4caf50;
            font-weight: bold;
        }}

        .status-error {{
            color: #f44336;
            font-weight: bold;
        }}

        .status-quota {{
            color: #ff9800;
            font-weight: bold;
        }}

        footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 非Gemini图像模型对比测试</h1>
        <p class="subtitle">测试时间: {timestamp} | 测试平台: anti-gravity</p>

        <div class="summary">
            <h2>📊 测试概览</h2>
            <div class="summary-stats">
"""

    # 计算统计数据
    total_models = len(results)
    total_prompts = len(TEST_PROMPTS)
    total_tasks = total_models * total_prompts
    completed_count = sum(len([r for r in model_results['results'] if r and r.get('status') == 'success'])
                          for model_results in results.values())
    success_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0

    html += f"""
                <div class="stat">
                    <div class="stat-value">{total_models}</div>
                    <div>测试模型数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{total_prompts}</div>
                    <div>测试提示词数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{completed_count}/{total_tasks}</div>
                    <div>成功生成</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{success_rate:.1f}%</div>
                    <div>成功率</div>
                </div>
            </div>
        </div>
"""

    # 生成每个模型的展示
    for model_id, model_data in results.items():
        model_info = model_data['model_info']
        model_results = model_data['results']

        html += f"""
        <div class="model-section">
            <div class="model-header">
                <div class="model-title">{model_info['name']} ({model_id})</div>
                <div class="model-meta">
                    提供商: {model_info.get('provider', 'Unknown')} |
                    描述: {model_info.get('description', 'N/A')}
                </div>
            </div>

            <div class="images-grid">
"""

        for i, result in enumerate(model_results):
            if result:
                if result.get('status') == 'success':
                    html += f"""
                <div class="image-card">
                    <img src="{os.path.basename(result['filename'])}" alt="{result['prompt_title']}">
                    <div class="image-info">
                        <div class="image-title">{result['prompt_title']}</div>
                        <div class="image-prompt">{result['prompt'][:80]}...</div>
                        <div class="image-meta">
                            <span class="status-success">✓ 成功</span> |
                            大小: {result['size']//1024}KB
                        </div>
                    </div>
                </div>
"""
                elif result.get('error') == 'QUOTA_EXHAUSTED':
                    html += f"""
                <div class="image-card">
                    <div class="image-info">
                        <div class="image-title">{result['prompt_title']}</div>
                        <div class="image-prompt">{result['prompt'][:80]}...</div>
                        <div class="image-meta">
                            <span class="status-quota">⚠ 配额耗尽</span>
                        </div>
                    </div>
                </div>
"""
                elif result.get('error') == 'MODEL_NOT_SUPPORTED':
                    html += f"""
                <div class="image-card">
                    <div class="image-info">
                        <div class="image-title">{result['prompt_title']}</div>
                        <div class="image-prompt">{result['prompt'][:80]}...</div>
                        <div class="image-meta">
                            <span class="status-error">✗ 模型不支持</span>
                        </div>
                    </div>
                </div>
"""
                else:
                    html += f"""
                <div class="image-card">
                    <div class="image-info">
                        <div class="image-title">{result['prompt_title']}</div>
                        <div class="image-prompt">{result['prompt'][:80]}...</div>
                        <div class="image-meta">
                            <span class="status-error">✗ 失败</span>
                        </div>
                    </div>
                </div>
"""

        html += """
            </div>
        </div>
"""

    html += f"""
        <footer>
            <p>测试完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>测试平台: anti-gravity | 输出目录: {os.path.basename(output_dir)}/</p>
        </footer>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    html_file = f"{output_dir}/non_gemini_models_comparison_{timestamp}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] HTML对比页面已生成: {html_file}")

    return html_file

def test_all_non_gemini_models():
    """测试所有非Gemini图像模型"""

    print("=" * 80)
    print("非Gemini图像模型对比测试工具")
    print("=" * 80)
    print()

    # 获取客户端
    client = get_antigravity_client()

    if not client:
        print("[ERROR] 无法获取API客户端")
        print("请检查config.py中的API密钥配置")
        return

    print("[OK] API客户端初始化成功")
    print()

    # 创建输出目录 - 放在工具所在目录下
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "non_gemini_comparison_output")
    os.makedirs(output_dir, exist_ok=True)

    # 计算总任务数
    total_tasks = len(NON_GEMINI_IMAGE_MODELS) * len(TEST_PROMPTS)

    # 尝试加载之前的进度
    saved_progress = load_progress(output_dir)

    # 初始化结果存储
    all_results = {}
    completed_tasks = set()

    if saved_progress:
        # 恢复之前的进度
        all_results = saved_progress.get('all_results', {})
        completed_tasks = set(saved_progress.get('completed_tasks', []))

        print(f"[恢复模式] 将跳过已完成的 {len(completed_tasks)} 个任务")
        print(f"[恢复模式] 剩余任务: {total_tasks - len(completed_tasks)}/{total_tasks}")
        print()
        print("-" * 80)
        print()

    # 时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not saved_progress:
        print(f"[新测试] 输出目录: {output_dir}/")
        print(f"[新测试] 测试模型数: {len(NON_GEMINI_IMAGE_MODELS)}")
        print(f"[新测试] 测试提示词数: {len(TEST_PROMPTS)}")
        print(f"[新测试] 总计生成: {total_tasks} 张图像")
        print()
        print("-" * 80)
        print()

    # 遍历所有模型
    for model_id, model_info in NON_GEMINI_IMAGE_MODELS.items():
        print(f"[模型] {model_info['name']} ({model_id})")
        print(f"  提供商: {model_info.get('provider', 'Unknown')}")
        print(f"  说明: {model_info['description']}")
        print(f"  尺寸: {model_info['size']}")
        print()

        # 初始化模型结果
        if model_id not in all_results:
            all_results[model_id] = {
                'model_info': model_info,
                'results': [],
                'success_count': 0,
                'total_count': 0
            }

        model_results = all_results[model_id]['results']

        # 确保结果数组长度正确
        if len(model_results) < len(TEST_PROMPTS):
            while len(model_results) < len(TEST_PROMPTS):
                model_results.append(None)

        # 遍历所有提示词
        for i, prompt_info in enumerate(TEST_PROMPTS, 1):
            # 生成任务唯一标识
            task_id = f"{model_id}_{prompt_info['category']}_{i}"

            # 检查是否已完成
            if task_id in completed_tasks:
                print(f"  [{i}/{len(TEST_PROMPTS)}] [SKIP] {prompt_info['title']} (已完成)")
                print()

                continue

            print(f"  [{i}/{len(TEST_PROMPTS)}] {prompt_info['title']}")
            print(f"    Prompt: {prompt_info['prompt'][:60]}...")

            # 生成图像
            result = generate_image(
                client,
                model_id,
                prompt_info['prompt'],
                model_info['size']
            )

            if result['success']:
                # 保存图像
                filename = f"{output_dir}/{model_id}_{prompt_info['category']}_{i}.png"
                with open(filename, 'wb') as f:
                    f.write(result['data'])

                print(f"    [OK] 生成成功: {os.path.basename(filename)} ({result['size']} bytes)")

                # 保存结果
                result_data = {
                    'prompt_title': prompt_info['title'],
                    'prompt': prompt_info['prompt'],
                    'category': prompt_info['category'],
                    'filename': filename,
                    'size': result['size'],
                    'status': 'success'
                }

                model_results[i-1] = result_data
                completed_tasks.add(task_id)

                # 每完成一个任务就保存进度
                save_progress(output_dir, completed_tasks, total_tasks, all_results)

            elif result['error'] == 'QUOTA_EXHAUSTED':
                print(f"    [!] 配额耗尽 - 跳过此模型的剩余测试")

                # 记录配额耗尽
                result_data = {
                    'prompt_title': prompt_info['title'],
                    'prompt': prompt_info['prompt'],
                    'category': prompt_info['category'],
                    'status': 'error',
                    'error': result['error']
                }

                model_results[i-1] = result_data

                # 跳出此模型的剩余测试
                break

            elif result['error'] == 'MODEL_NOT_SUPPORTED':
                print(f"    [X] 模型不支持 - 跳过此模型")

                # 记录不支持
                result_data = {
                    'prompt_title': prompt_info['title'],
                    'prompt': prompt_info['prompt'],
                    'category': prompt_info['category'],
                    'status': 'error',
                    'error': result['error']
                }

                model_results[i-1] = result_data

                # 跳出此模型的剩余测试
                break

            else:
                print(f"    [ERROR] 生成失败: {result['error']}")

                # 保存错误结果
                result_data = {
                    'prompt_title': prompt_info['title'],
                    'prompt': prompt_info['prompt'],
                    'category': prompt_info['category'],
                    'status': 'error',
                    'error': result['error']
                }

                model_results[i-1] = result_data

            print()

        print("-" * 80)
        print()

    # 生成HTML对比页面
    print("[生成] 正在生成HTML对比页面...")
    html_file = generate_html_comparison(all_results, output_dir, timestamp)

    # 保存最终结果
    print("[保存] 测试结果已保存")
    print()

    # 统计结果
    success_count = 0
    error_count = 0
    quota_count = 0
    unsupported_count = 0

    for model_data in all_results.values():
        for result in model_data['results']:
            if result:
                if result.get('status') == 'success':
                    success_count += 1
                elif result.get('error') == 'QUOTA_EXHAUSTED':
                    quota_count += 1
                elif result.get('error') == 'MODEL_NOT_SUPPORTED':
                    unsupported_count += 1
                else:
                    error_count += 1

    total_count = success_count + error_count + quota_count + unsupported_count

    print("=" * 80)
    print("测试完成统计")
    print("=" * 80)
    print(f"总任务数: {total_count}")
    print(f"成功生成: {success_count} ({success_count/total_count*100:.1f}%)" if total_count > 0 else "")
    print(f"配额耗尽: {quota_count}")
    print(f"模型不支持: {unsupported_count}")
    print(f"其他错误: {error_count}")
    print()
    print(f"输出目录: {output_dir}/")
    print(f"HTML对比页面: {html_file}")
    print("=" * 80)

def main():
    """主函数"""

    print("\n" + "=" * 80)
    print("非Gemini图像模型对比测试工具")
    print("测试anti-gravity支持的所有非Gemini图像生成模型")
    print("=" * 80)
    print()

    try:
        test_all_non_gemini_models()

        print("\n[成功] 测试完成")

    except KeyboardInterrupt:
        print("\n\n[提示] 程序被用户中断")
    except Exception as e:
        print(f"\n\n[错误] 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
