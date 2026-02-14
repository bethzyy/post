#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复草稿路径问题 - 使用绝对路径
"""
import os

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到模式2的草稿检查部分,替换为使用绝对路径
old_code = """        # 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")
            print(f"[草稿完善] draft参数原始值: [{draft}]")
            print(f"[草稿完善] 当前工作目录: {os.getcwd()}")
            print(f"[草稿完善] 检查文件是否存在: {os.path.exists(draft)}")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):
                print(f"[草稿完善] 检测到草稿文件路径: {draft}")
                try:
                    with open(draft, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容")"""

new_code = """        # 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")
            print(f"[草稿完善] draft参数原始值: [{draft}]")
            print(f"[草稿完善] 当前工作目录: {os.getcwd()}")
            print(f"[草稿完善] 脚本__file__: {__file__}")

            # 转换为绝对路径(解决相对路径问题)
            if os.path.isabs(draft):
                draft_path = draft
            else:
                # 相对路径:基于脚本所在目录解析
                script_dir = os.path.dirname(os.path.abspath(__file__))
                draft_path = os.path.join(script_dir, draft)

            print(f"[草稿完善] 解析后的绝对路径: {draft_path}")
            print(f"[草稿完善] 检查文件是否存在: {os.path.exists(draft_path)}")

            # 检查draft是否是文件路径,如果是则读取文件内容
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

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] 已修复路径解析逻辑")
    print("[OK] 现在使用绝对路径,避免工作目录问题")
else:
    print("[INFO] 代码已修改过或版本不匹配")
    print("[HINT] 请检查文件内容")
