#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本位置对路径的影响
"""
import os

print("="*80)
print("测试脚本位置对相对路径的影响")
print("="*80)

print(f"\n[1] __file__ 变量:")
print(f"    {__file__}")

print(f"\n[2] os.getcwd():")
print(f"    {os.getcwd()}")

print(f"\n[3] __file__所在目录:")
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"    {script_dir}")

print(f"\n[4] 从相对路径检查文件:")
test_path = "article/draft.txt"
print(f"    检查路径: {test_path}")
print(f"    os.path.exists(): {os.path.exists(test_path)}")

print(f"\n[5] 从__file__目录检查文件:")
from_file_dir = os.path.join(script_dir, "draft.txt")
print(f"    检查路径: {from_file_dir}")
print(f"    os.path.exists(): {os.path.exists(from_file_dir)}")

print(f"\n[6] 列出当前目录文件:")
current_files = os.listdir('.')
article_dirs = [d for d in current_files if 'article' in d.lower()]
print(f"    article相关: {article_dirs}")

print(f"\n[7] 列出article目录文件:")
if os.path.exists('article'):
    article_files = os.listdir('article')
    print(f"    文件数: {len(article_files)}")
    if 'draft.txt' in article_files:
        print(f"    draft.txt存在!")
    else:
        print(f"    draft.txt不存在!")
        print(f"    前5个文件: {article_files[:5]}")
else:
    print(f"    article目录不存在!")

print("="*80)
