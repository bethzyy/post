#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查并修复post目录下所有工具的输出路径问题
确保所有工具的输出都保存在工具所在子目录
"""

import os
import re
from pathlib import Path

def check_output_path(file_path):
    """检查Python文件中的输出路径设置"""

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []

    # 检查硬编码的相对路径输出目录
    patterns = [
        (r'output_dir\s*=\s*["\']([^"\']+)["\']', '硬编码输出目录'),
        (r'os\.makedirs\(["\']([^"\']+)["\']', '创建目录'),
        (r'open\(["\']([^"\']+\.png)', '保存PNG文件'),
        (r'open\(["\']([^"\']+\.jpg)', '保存JPG文件'),
        (r'open\(["\']([^"\']+\.html)', '保存HTML文件'),
        (r'open\(["\']([^"\']+\.md)', '保存Markdown文件'),
        (r'open\(["\']([^"\']+\.txt)', '保存文本文件'),
    ]

    for pattern, desc in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            path = match.group(1)

            # 跳过使用 __file__ 或 script_dir 的正确做法
            if '__file__' in content[:match.start()+200] or 'script_dir' in content[:match.start()+200]:
                continue

            # 检查是否是相对路径（不包含../等上级目录引用）
            if not path.startswith('/') and not path.startswith('\\') and not path.startswith('..'):
                if 'output' in path.lower() or 'images' in path.lower() or 'results' in path.lower():
                    issues.append({
                        'type': desc,
                        'path': path,
                        'line': content[:match.start()].count('\n') + 1
                    })

    return issues

def scan_directory(directory):
    """扫描目录下所有Python文件"""

    results = {}

    for root, dirs, files in os.walk(directory):
        # 跳过__pycache__和隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('__') and not d.startswith('.')]

        # 跳过test_gemini_api和test_video_api子目录
        if 'test_gemini_api' in root or 'test_video_api' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = check_output_path(file_path)

                if issues:
                    rel_path = os.path.relpath(file_path, directory)
                    results[rel_path] = issues

    return results

def main():
    print("=" * 80)
    print("Post工具输出路径检查工具")
    print("=" * 80)
    print()

    post_dir = Path(__file__).parent

    print(f"扫描目录: {post_dir}")
    print()

    results = scan_directory(post_dir)

    if results:
        print(f"发现 {len(results)} 个文件可能存在问题:")
        print()

        for file_path, issues in results.items():
            print(f"文件: {file_path}")
            for issue in issues:
                print(f"  - 行 {issue['line']}: {issue['type']} -> {issue['path']}")
            print()

        print("=" * 80)
        print("建议修复方案:")
        print("=" * 80)
        print()
        print("在每个工具文件中添加以下代码:")
        print()
        print("# 获取工具所在目录")
        print("script_dir = os.path.dirname(os.path.abspath(__file__))")
        print("output_dir = os.path.join(script_dir, 'your_output_folder')")
        print("os.makedirs(output_dir, exist_ok=True)")
        print()

    else:
        print("[OK] 未发现明显的输出路径问题")
        print()
        print("所有工具似乎都正确使用了 __file__ 或绝对路径")

if __name__ == '__main__':
    main()
