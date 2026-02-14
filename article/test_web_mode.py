#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 Web 模式的文章生成"""

import os
import sys
import json
import tempfile

# 设置工作目录
os.chdir(r'C:\D\CAIE_tool\MyAIProduct\post\article')

# 创建临时参数文件
params = {
    'mode': '2',
    'theme': '',
    'draft': 'article/draft_v3.txt',
    'length': 1500,
    'style': 'standard',
    'generate_images': 'y',
    'image_style': 'realistic'
}

with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False)
    temp_path = f.name

print(f"[TEST] Temp params file: {temp_path}")
print(f"[TEST] Params: {json.dumps(params, ensure_ascii=False, indent=2)}")

# 设置环境变量
os.environ['ARTICLE_PARAMS_JSON'] = temp_path

try:
    # 导入并运行
    import toutiao_article_generator
    print("\n[TEST] Starting main_web()...")
    result = toutiao_article_generator.main_web()
    print(f"\n[TEST] Result: {json.dumps(result, ensure_ascii=False, indent=2)}")
finally:
    # 清理
    if os.path.exists(temp_path):
        os.remove(temp_path)
        print(f"\n[TEST] Cleaned up temp file: {temp_path}")
