#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新测试进度 - 根据实际生成的图片文件
"""

import os
import json
from pathlib import Path

def scan_generated_images():
    """扫描已生成的图片文件"""
    output_dir = Path(__file__).parent / "gemini_comparison_output"

    if not output_dir.exists():
        print(f"[错误] 输出目录不存在: {output_dir}")
        return []

    png_files = list(output_dir.glob("*.png"))
    print(f"[扫描] 找到 {len(png_files)} 张图片")

    # 解析文件名，提取任务ID
    completed_tasks = []
    for png_file in png_files:
        filename = png_file.name
        # 文件名格式: {model}_{category}_{number}.png
        # 例如: gemini-3-pro-image-4k_art_1.png
        parts = filename.replace('.png', '').split('_')

        if len(parts) >= 3:
            model_id = '_'.join(parts[:-2])  # 模型ID可能包含多个下划线
            category = parts[-2]  # 类别
            number = parts[-1]  # 序号

            # 生成任务ID（需要匹配代码中的格式）
            task_id = f"{model_id}_{category}_{number}"

            # 获取文件大小
            file_size = png_file.stat().st_size

            completed_tasks.append({
                'task_id': task_id,
                'model_id': model_id,
                'category': category,
                'number': number,
                'filename': str(png_file),
                'size': file_size
            })

    return completed_tasks

def generate_progress_file(completed_tasks):
    """生成新的进度文件"""
    output_dir = Path(__file__).parent / "gemini_comparison_output"

    # 模型信息
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

    # 提示词信息
    TEST_PROMPTS = [
        {'title': '中国传统山水画', 'category': 'art', 'prompt': 'Traditional Chinese landscape painting, mountains and mist, ink wash style, serene atmosphere'},
        {'title': '可爱猫咪', 'category': 'animal', 'prompt': 'A cute fluffy cat sitting on a wooden fence, warm golden hour sunlight, realistic style'},
        {'title': '未来城市', 'category': 'scifi', 'prompt': 'Futuristic cyberpunk city at night, neon lights, flying cars, rain reflections, cinematic lighting'},
        {'title': '美食', 'category': 'food', 'prompt': 'Delicious steaming hot bowl of ramen noodles, eggs, green onions, food photography, professional lighting'},
        {'title': '花鸟画', 'category': 'art', 'prompt': 'Traditional Chinese bird and flower painting, bamboo, plum blossoms, elegant brush strokes'}
    ]

    # 构建结果数据
    all_results = {}
    completed_task_ids = set()

    for task in completed_tasks:
        task_id = task['task_id']
        model_id = task['model_id']
        category = task['category']
        number = int(task['number'])

        completed_task_ids.add(task_id)

        # 初始化模型结果
        if model_id not in all_results:
            all_results[model_id] = {
                'model_info': GEMINI_MODELS.get(model_id, {
                    'name': model_id,
                    'description': '',
                    'size': '1024x1024'
                }),
                'results': [],
                'success_count': 0,
                'total_count': 0
            }

        # 确保结果数组足够长
        model_results = all_results[model_id]['results']
        while len(model_results) < number:
            model_results.append(None)

        # 查找对应的提示词
        prompt_info = None
        for p in TEST_PROMPTS:
            if p['category'] == category:
                prompt_info = p
                break

        if prompt_info:
            # 更新结果
            result_data = {
                'prompt_title': prompt_info['title'],
                'prompt': prompt_info['prompt'],
                'category': category,
                'filename': task['filename'],
                'size': task['size'],
                'status': 'success'
            }

            model_results[number - 1] = result_data
            all_results[model_id]['success_count'] += 1
            all_results[model_id]['total_count'] = max(all_results[model_id]['total_count'], number)

    # 计算总数
    total_count = len(GEMINI_MODELS) * len(TEST_PROMPTS)

    # 生成进度文件
    from datetime import datetime

    progress = {
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'completed_count': len(completed_task_ids),
        'total_count': total_count,
        'completed_tasks': sorted(list(completed_task_ids)),
        'all_results': all_results
    }

    # 保存进度文件
    progress_file = output_dir / "test_progress.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

    return progress

def main():
    print("=" * 80)
    print("更新测试进度工具")
    print("=" * 80)
    print()

    # 扫描已生成的图片
    completed_tasks = scan_generated_images()

    if not completed_tasks:
        print("[错误] 没有找到已生成的图片")
        return

    print()

    # 按模型分组显示
    from collections import defaultdict
    models = defaultdict(list)
    for task in completed_tasks:
        models[task['model_id']].append(task)

    print("[统计] 各模型完成情况:")
    for model_id in sorted(models.keys()):
        tasks = models[model_id]
        print(f"  {model_id}: {len(tasks)}/{5} 张")

    print()

    # 生成进度文件
    print("[生成] 正在生成进度文件...")
    progress = generate_progress_file(completed_tasks)

    print(f"[完成] 进度文件已更新")
    print(f"[完成] 已记录: {progress['completed_count']}/{progress['total_count']} 个任务")
    print()
    print("[信息] 下次运行工具时将跳过这些已完成的任务")

if __name__ == '__main__':
    main()
