#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试草稿完善功能
"""
import os
import sys

# 切换到article目录
os.chdir("C:/D/CAIE_tool/MyAIProduct/post/article")

# 设置环境变量模拟Web模式
os.environ['ARTICLE_PARAMS_JSON'] = 'test_params.json'

# 创建测试参数文件
import json
params = {
    'mode': '2',
    'draft': 'article/draft.txt',
    'length': 1500,
    'generate_images': 'n',
    'image_style': 'realistic',
    'style': 'standard'
}

with open('test_params.json', 'w', encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False, indent=2)

print("="*80)
print("测试草稿完善功能")
print("="*80)
print(f"参数文件: test_params.json")
print(f"草稿文件: {params['draft']}")
print(f"目标字数: {params['length']}")
print("="*80)

# 导入并调用main_web
sys.path.insert(0, os.getcwd())
from toutiao_article_generator import main_web

result = main_web()

print("\n" + "="*80)
print("测试结果")
print("="*80)
print(f"成功: {result.get('success')}")
if result.get('success'):
    print(f"标题: {result.get('title')}")
    print(f"字数: {result.get('word_count')}")
    print(f"目标长度: {result.get('target_length')}")
    print(f"输出文件: 已生成HTML文件")
else:
    print(f"错误: {result.get('error')}")

# 清理
try:
    os.remove('test_params.json')
except:
    pass
