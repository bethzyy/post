# -*- coding: utf-8 -*-
"""
添加调试日志
"""
import re

# 读取文件
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 在提取AI响应后添加调试日志
old_code = '''            # 提取生成的内容
            content = response.choices[0].message.content

            # 解析标题和正文'''

new_code = '''            # 提取生成的内容
            content = response.choices[0].message.content

            # [DEBUG] 保存AI原始响应
            debug_file = f"debug_ai_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(f"Theme: {theme}\\n")
                f.write(f"Prompt length: {len(prompt)}\\n")
                f.write(f"Response length: {len(content)}\\n")
                f.write("="*80 + "\\n")
                f.write(content)
            print(f"[DEBUG] AI响应已保存到: {debug_file}")

            # 解析标题和正文'''

if old_code in content:
    content = content.replace(old_code, new_code)
    # 避免编码错误,保存到文件
    with open('debug_add_result.txt', 'w', encoding='utf-8') as f:
        f.write("Added debug logging successfully")
    print("OK: Added debug logging")
else:
    with open('debug_add_result.txt', 'w', encoding='utf-8') as f:
        f.write("ERROR: Target code not found")
    print("ERROR: Target code not found")
    exit(1)

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
