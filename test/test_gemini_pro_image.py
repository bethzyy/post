#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gemini全模型对比测试工具
测试所有可用的Gemini图像生成模型,生成HTML对比展示
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_antigravity_client
from datetime import datetime
import base64
import json

# 所有Gemini模型配置
GEMINI_MODELS = {
    'gemini-3-pro-image-4k': {
        'name': 'Gemini 3 Pro Image 4K',
        'description': '最高分辨率,细节最丰富',
        'size': '1024x1024'
    },
    'gemini-3-pro-image-2k': {
        'name': 'Gemini 3 Pro Image 2K',
        'description': '高分辨率,平衡质量和速度',
        'size': '1024x1024'
    },
    'gemini-3-flash-image': {
        'name': 'Gemini 3 Flash Image',
        'description': '快速生成,适合批量处理',
        'size': '1024x1024'
    },
    'gemini-2-pro-image': {
        'name': 'Gemini 2 Pro Image',
        'description': '第二代专业图像模型',
        'size': '1024x1024'
    },
    'gemini-2-flash-image': {
        'name': 'Gemini 2 Flash Image',
        'description': '第二代快速图像模型',
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
        return {
            'success': False,
            'error': str(e)
        }

def load_progress(output_dir):
    """加载之前的测试进度"""
    progress_file = f"{output_dir}/test_progress.json"

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

    progress_file = f"{output_dir}/test_progress.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def test_all_gemini_models():
    """测试所有Gemini模型 - 支持断点续传"""

    print("=" * 80)
    print("Gemini全模型对比测试工具")
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
    output_dir = os.path.join(script_dir, "gemini_comparison_output")
    os.makedirs(output_dir, exist_ok=True)

    # 计算总任务数
    total_tasks = len(GEMINI_MODELS) * len(TEST_PROMPTS)

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
        print(f"[新测试] 测试模型数: {len(GEMINI_MODELS)}")
        print(f"[新测试] 测试提示词数: {len(TEST_PROMPTS)}")
        print(f"[新测试] 总计生成: {total_tasks} 张图像")
        print()
        print("-" * 80)
        print()

    # 遍历所有模型
    for model_id, model_info in GEMINI_MODELS.items():
        print(f"[模型] {model_info['name']} ({model_id})")
        print(f"  说明: {model_info['description']}")
        print(f"  尺寸: {model_info['size']}")
        print()

        # 初始化模型结果(如果不存在)
        if model_id not in all_results:
            all_results[model_id] = {
                'model_info': model_info,
                'results': [],
                'success_count': 0,
                'total_count': 0
            }

        model_results = all_results[model_id]['results']

        # 如果结果已存在,确保长度正确
        if len(model_results) < len(TEST_PROMPTS):
            # 需要填充缺失的占位符
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

                print(f"    [OK] 生成成功: {filename} ({result['size']} bytes)")

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
                completed_tasks.add(task_id)  # 失败的也标记为完成,避免重复尝试

            print()

            # 每完成一个任务就保存进度
            save_progress(output_dir, completed_tasks, total_tasks, all_results)

        # 更新模型统计
        all_results[model_id]['results'] = model_results
        all_results[model_id]['success_count'] = sum(1 for r in model_results if r and r['status'] == 'success')
        all_results[model_id]['total_count'] = len(model_results)

        print("-" * 80)
        print()

    # 保存最终测试结果JSON
    result_file = f"{output_dir}/test_results_{timestamp}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"[OK] 测试结果已保存: {result_file}")
    print()

    # 生成HTML对比页面
    html_file = generate_html_comparison(all_results, output_dir, timestamp)
    print(f"[OK] HTML对比页面已生成: {html_file}")
    print()

    # 统计信息
    print("=" * 80)
    print("测试完成统计")
    print("=" * 80)
    print()

    total_success = sum(r['success_count'] for r in all_results.values())
    total_attempts = sum(r['total_count'] for r in all_results.values())
    success_rate = (total_success / total_attempts * 100) if total_attempts > 0 else 0

    print(f"总计生成: {total_success}/{total_attempts} 成功 ({success_rate:.1f}%)")
    print()

    for model_id, model_data in all_results.items():
        model_name = model_data['model_info']['name']
        success = model_data['success_count']
        total = model_data['total_count']
        rate = (success / total * 100) if total > 0 else 0
        status = "[OK]" if success == total else "[PARTIAL]" if success > 0 else "[FAIL]"

        print(f"  {status} {model_name}: {success}/{total} ({rate:.1f}%)")

    print()
    print("=" * 80)
    print()

    # 显示断点续传提示
    if total_success < total_attempts:
        remaining = total_attempts - total_success
        print(f"[提示] 有 {remaining} 个任务未成功完成")
        print(f"[提示] 您可以稍后重新运行此工具,它将自动跳过已完成的任务")
        print(f"[提示] 进度已保存在: {output_dir}/test_progress.json")
        print()
    else:
        print("[提示] 所有任务已完成! 可以删除进度文件重新开始测试")
        print()

    # 自动打开HTML文件
    try:
        import webbrowser
        webbrowser.open(f'file:///{os.path.abspath(html_file)}'.replace('\\', '/'))
        print("[OK] 已在浏览器中打开对比页面")
    except:
        print("[INFO] 请手动打开HTML文件查看对比结果")

    print()

def generate_html_comparison(results, output_dir, timestamp):
    """生成HTML对比页面"""

    html_filename = f"{output_dir}/gemini_models_comparison_{timestamp}.html"

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini全模型对比测试 - """ + timestamp + """</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        .content {
            padding: 40px;
        }

        .model-section {
            margin-bottom: 60px;
        }

        .model-title {
            font-size: 2em;
            color: #5a67d8;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 3px solid #5a67d8;
        }

        .model-info {
            background: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #4a5568;
        }

        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .image-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .image-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        }

        .image-card img {
            width: 100%;
            height: 300px;
            object-fit: cover;
        }

        .image-info {
            padding: 15px;
        }

        .image-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 8px;
        }

        .image-prompt {
            color: #718096;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .image-meta {
            color: #a0aec0;
            font-size: 0.85em;
        }

        .error-card {
            background: #fed7d7;
            padding: 20px;
            border-radius: 10px;
            color: #c53030;
        }

        .comparison-table {
            margin-top: 40px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }

        th {
            background: #5a67d8;
            color: white;
            padding: 15px;
            text-align: left;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #e2e8f0;
        }

        tr:hover {
            background: #f7fafc;
        }

        .footer {
            background: #2d3748;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            font-weight: bold;
        }

        .badge-success {
            background: #48bb78;
            color: white;
        }

        .badge-error {
            background: #f56565;
            color: white;
        }

        .badge-warning {
            background: #ed8936;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 Gemini全模型对比测试</h1>
            <p>测试时间: """ + timestamp + """</p>
            <div class="stats">
"""

    # 添加统计信息
    total_models = len(results)
    total_prompts = len(TEST_PROMPTS)
    total_success = sum(r['success_count'] for r in results.values())
    total_attempts = sum(r['total_count'] for r in results.values())

    html_content += f"""
                <div class="stat-item">
                    <div>🤖 模型数量</div>
                    <div style="font-size: 1.5em; font-weight: bold;">{total_models}</div>
                </div>
                <div class="stat-item">
                    <div>📝 测试提示词</div>
                    <div style="font-size: 1.5em; font-weight: bold;">{total_prompts}</div>
                </div>
                <div class="stat-item">
                    <div>✅ 成功生成</div>
                    <div style="font-size: 1.5em; font-weight: bold;">{total_success}/{total_attempts}</div>
                </div>
                <div class="stat-item">
                    <div>📊 成功率</div>
                    <div style="font-size: 1.5em; font-weight: bold;">{total_success/total_attempts*100:.1f}%</div>
                </div>
            </div>
        </div>

        <div class="content">
"""

    # 为每个模型生成展示区域
    for model_id, model_data in results.items():
        model_info = model_data['model_info']
        model_results = model_data['results']
        success_count = model_data['success_count']
        total_count = model_data['total_count']

        html_content += f"""
            <div class="model-section">
                <h2 class="model-title">{model_info['name']}</h2>
                <div class="model-info">
                    <strong>模型ID:</strong> {model_id}<br>
                    <strong>说明:</strong> {model_info['description']}<br>
                    <strong>分辨率:</strong> {model_info['size']}<br>
                    <strong>成功率:</strong> {success_count}/{total_count} ({success_count/total_count*100:.1f}%)
                </div>

                <div class="image-grid">
"""

        for result in model_results:
            if result['status'] == 'success':
                # 提取文件名(不包含路径)
                import os
                filename_only = os.path.basename(result['filename'])
                html_content += f"""
                    <div class="image-card">
                        <img src="{filename_only}" alt="{result['prompt_title']}">
                        <div class="image-info">
                            <div class="image-title">{result['prompt_title']}</div>
                            <div class="image-prompt">{result['prompt'][:80]}...</div>
                            <div class="image-meta">
                                <span class="badge badge-success">成功</span>
                                大小: {result['size']:,} bytes
                            </div>
                        </div>
                    </div>
"""
            else:
                html_content += f"""
                    <div class="error-card">
                        <div class="image-title">{result['prompt_title']}</div>
                        <div>错误: {result.get('error', 'Unknown error')}</div>
                    </div>
"""

        html_content += """
                </div>
            </div>
"""

    # 添加对比表格
    html_content += """
            <h2 style="font-size: 2em; color: #5a67d8; margin-bottom: 20px;">📊 模型性能对比表</h2>
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>模型</th>
                            <th>分辨率</th>
                            <th>成功/总数</th>
                            <th>成功率</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for model_id, model_data in results.items():
        model_info = model_data['model_info']
        success_count = model_data['success_count']
        total_count = model_data['total_count']
        rate = success_count / total_count * 100 if total_count > 0 else 0

        badge_class = 'badge-success' if success_count == total_count else 'badge-warning' if success_count > 0 else 'badge-error'
        status_text = '优秀' if success_count == total_count else '部分成功' if success_count > 0 else '失败'

        html_content += f"""
                        <tr>
                            <td><strong>{model_info['name']}</strong></td>
                            <td>{model_info['size']}</td>
                            <td>{success_count}/{total_count}</td>
                            <td>{rate:.1f}%</td>
                            <td><span class="badge {badge_class}">{status_text}</span></td>
                        </tr>
"""

    html_content += """
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Generated by AI发文工具管理器 - Gemini模型对比测试工具</p>
            <p>测试时间: """ + timestamp + """</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_filename

if __name__ == '__main__':
    try:
        test_all_gemini_models()
    except KeyboardInterrupt:
        print("\n\n[WARNING] 测试被用户中断")
    except Exception as e:
        print(f"\n\n[ERROR] 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
