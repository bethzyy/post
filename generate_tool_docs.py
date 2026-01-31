#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具文档生成器
分析post目录下的所有Python工具，生成详细的功能文档
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

def analyze_python_file(file_path):
    """分析Python文件，提取功能信息"""

    content = file_path.read_text(encoding='utf-8', errors='ignore')

    # 提取文档字符串
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    docstring = docstring_match.group(1).strip() if docstring_match else ""

    # 提取导入的模块
    imports = []
    import_patterns = [
        r'from\s+(\S+)\s+import',
        r'import\s+(\S+)'
    ]
    for pattern in import_patterns:
        matches = re.findall(pattern, content)
        imports.extend(matches)

    # 提取使用的模型/API
    models_apis = []
    api_keywords = [
        'get_antigravity_client', 'get_volcano_client',
        'gemini', 'dall-e', 'flux', 'pollinations',
        'seedream', 'openai', 'anthropic'
    ]
    for keyword in api_keywords:
        if keyword.lower() in content.lower():
            models_apis.append(keyword)

    # 提取主要功能
    functions = []
    function_pattern = r'def\s+(\w+)\s*\('
    matches = re.findall(function_pattern, content)
    functions = [m for m in matches if not m.startswith('_')]

    # 提取类
    classes = []
    class_pattern = r'class\s+(\w+)'
    matches = re.findall(class_pattern, content)
    classes = matches

    # 提取配置参数
    params = []
    config_patterns = [
        r'API_KEY',
        r'MODEL\s*=',
        r'SIZE\s*=',
        r'temperature\s*='
    ]
    for pattern in config_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        params.extend(matches[:3])  # 限制数量

    return {
        'docstring': docstring,
        'imports': list(set(imports)),
        'models_apis': list(set(models_apis)),
        'functions': functions[:10],  # 限制显示数量
        'classes': classes,
        'params': params[:5]
    }

def generate_tool_documentation():
    """生成所有工具的文档"""

    BASE_DIR = Path(__file__).parent
    categories = ['bird', 'picture', 'article', 'hotspot', 'test']

    documentation = {}

    print("=" * 80)
    print("开始分析工具...")
    print("=" * 80)

    for category in categories:
        cat_path = BASE_DIR / category
        if not cat_path.exists():
            continue

        print(f"\n分析分类: {category}/")

        category_docs = {}

        for py_file in sorted(cat_path.glob("*.py")):
            print(f"  - {py_file.name}")

            # 分析文件
            info = analyze_python_file(py_file)

            # 生成详细描述
            detailed_info = {
                'file': py_file.name,
                'relative_path': str(py_file.relative_to(BASE_DIR)),
                'docstring': info['docstring'],
                'description': '',
                'features': [],
                'models_used': info['models_apis'],
                'main_functions': info['functions'],
                'classes': info['classes'],
                'imports': info['imports']
            }

            # 从docstring生成描述
            if info['docstring']:
                lines = info['docstring'].split('\n')
                if lines:
                    detailed_info['description'] = lines[0]
                    detailed_info['features'] = lines[1:] if len(lines) > 1 else []

            # 生成功能说明
            if not detailed_info['description']:
                detailed_info['description'] = f"{category} 工具 - {py_file.stem}"

            # 添加模型使用说明
            if info['models_apis']:
                model_desc = "使用的模型/API: " + ", ".join(info['models_apis'])
                detailed_info['features'].append(model_desc)

            # 添加主要函数说明
            if info['functions']:
                func_desc = "主要函数: " + ", ".join(info['functions'][:5])
                detailed_info['features'].append(func_desc)

            category_docs[py_file.name] = detailed_info

        if category_docs:
            documentation[category] = category_docs

    # 保存为JSON文件
    output_file = BASE_DIR / 'tool_documentation.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documentation, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 文档已生成: {output_file}")
    print(f"[OK] 共分析 {len(documentation)} 个分类")

    total_tools = sum(len(cat) for cat in documentation.values())
    print(f"[OK] 共分析 {total_tools} 个工具")

    return documentation

if __name__ == '__main__':
    generate_tool_documentation()
