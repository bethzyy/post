#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复草稿变量命名冲突问题
"""
import os

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复变量命名冲突 - 读取文件内容后用新变量名
old_code = """            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft_path):
                print(f"[草稿完善] 检测到草稿文件路径: {draft_path}")
                try:
                    with open(draft_path, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容")"""

new_code = """            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft_path):
                print(f"[草稿完善] 检测到草稿文件路径: {draft_path}")
                try:
                    with open(draft_path, 'r', encoding='utf-8') as f:
                        draft_content = f.read()  # 使用新变量名
                    draft = draft_content  # 将读取的内容赋值给draft
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容")"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] 已修复变量命名冲突")
    print("[OK] 现在使用draft_content存储读取的文件内容")
else:
    print("[ERROR] 未找到目标代码")
