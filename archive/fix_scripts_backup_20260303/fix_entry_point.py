#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单直接的入口点修复脚本
"""
import os

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到入口点位置并替换
start_marker = "if __name__ == \"__main__\":\n"
end_marker = "        traceback.print_exc()\n"

new_entry = '''if __name__ == "__main__":
    # 添加入口点调试
    print("\\n" + "="*80)
    print("[DEBUG] ========== 入口点调试 ==========")
    print(f"[DEBUG] 当前工作目录: {os.getcwd()}")
    print(f"[DEBUG] ARTICLE_PARAMS_JSON环境变量: {os.environ.get('ARTICLE_PARAMS_JSON', 'NOT SET')}")

    # 检测是否在Web模式下运行
    if os.environ.get("ARTICLE_PARAMS_JSON"):
        print("[DEBUG] 检测到Web模式 - 调用 main_web()")
        print("="*80 + "\\n")
        main_web()
    else:
        print("[DEBUG] 检测到CLI模式 - 调用 main()")
        print("="*80 + "\\n")
        main()
'''

# 找到开始行
start_idx = None
for i, line in enumerate(lines):
    if line.strip() == "if __name__ == \"__main__\":":
        start_idx = i
        break

if start_idx is not None:
    # 删除从start_idx开始到文件末尾的所有行
    new_lines = lines[:start_idx]
    # 添加新的入口点代码
    new_lines.append(new_entry)
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"[OK] 已修复入口点 (从第{start_idx + 1}行开始)")
else:
    print("[ERROR] 未找到入口点")
