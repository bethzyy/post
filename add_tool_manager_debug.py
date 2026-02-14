#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加tool_manager.py的调试信息
"""
import os

file_path = "C:/D/CAIE_tool/MyAIProduct/post/tool_manager.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在创建子进程前添加调试信息
old_code = """                # 设置环境变量传递参数文件路径
                env['ARTICLE_PARAMS_JSON'] = params_file

                process = subprocess.Popen("""

new_code = """                # 设置环境变量传递参数文件路径
                env['ARTICLE_PARAMS_JSON'] = params_file

                # 读取刚创建的JSON文件内容用于调试
                with open(params_file, 'r', encoding='utf-8') as debug_f:
                    json_content = debug_f.read()

                print(f"[DEBUG] ========== 创建的JSON文件内容 ==========")
                print(f"[DEBUG] 文件路径: {params_file}")
                print(f"[DEBUG] 文件存在: {os.path.exists(params_file)}")
                print(f"[DEBUG] JSON内容:\\\\n{json_content}")
                print(f"[DEBUG] ========================================\\\\n")

                print(f"[DEBUG] ========== 子进程环境 ==========")
                print(f"[DEBUG] 命令: python {tool_path}")
                print(f"[DEBUG] 工作目录: {BASE_DIR}")
                print(f"[DEBUG] ARTICLE_PARAMS_JSON: {env.get('ARTICLE_PARAMS_JSON')}")
                print(f"[DEBUG] ====================================\\\\n")

                process = subprocess.Popen("""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] 已添加tool_manager.py调试信息")
else:
    print("[INFO] 调试信息已存在,跳过")
