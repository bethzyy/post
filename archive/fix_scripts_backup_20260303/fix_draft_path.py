#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复草稿路径问题
"""
import os

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在模式2的草稿完善部分添加调试和路径处理
old_code = """        # 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):"""

new_code = """        # 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")
            print(f"[草稿完善] draft参数原始值: [{draft}]")
            print(f"[草稿完善] 当前工作目录: {os.getcwd()}")
            print(f"[草稿完善] 检查文件是否存在: {os.path.exists(draft)}")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] 已添加路径调试信息")
else:
    print("[INFO] 调试信息已存在")
