#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
精确修复line 1138的错误调用
使用行号直接定位,避免字符串模式匹配问题
"""

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到line 1138 (index 1137, 因为list从0开始)
# 应该是: result = improve_draft(draft, length, generate_images=='y', image_style, style)
target_line_number = 1137  # 1138行在list中是index 1137

# 检查是否找到了正确的行
if target_line_number < len(lines):
    old_line = lines[target_line_number]
    print(f"[DEBUG] 找到第1138行: {old_line.strip()}")

    # 确认这确实是要修复的行
    if "improve_draft" in old_line and "result =" in old_line:
        # 准备替换的代码块
        new_code_lines = [
            "            # 创建生成器实例\n",
            "            generator = ToutiaoArticleGenerator()\n",
            "            if not generator.text_client:\n",
            "                return {\"error\": \"无法初始化AI文本客户端\"}\n",
            "\n",
            "            # 调用草稿完善方法\n",
            "            article = generator.improve_article_draft(draft, length)\n",
            "            if not article:\n",
            "                return {\"error\": \"草稿完善失败\"}\n",
            "\n",
            "            result = {\n",
            "                \"success\": True,\n",
            "                \"title\": article['title'],\n",
            "                \"content\": article['content'],\n",
            "                \"word_count\": article['word_count'],\n",
            "                \"target_length\": article['target_length']\n",
            "            }\n"
        ]

        # 替换这一行
        lines[target_line_number:target_line_number+1] = new_code_lines

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"[OK] 已成功替换第1138行")
        print(f"[OK] 原来1行已替换为{len(new_code_lines)}行新代码")
        print(f"[OK] 现在使用 generator.improve_article_draft(draft, length)")
    else:
        print(f"[ERROR] 第1138行不是要修复的目标行")
        print(f"[ERROR] 内容: {old_line.strip()}")
else:
    print(f"[ERROR] 文件只有{len(lines)}行,无法访问第1138行")
