# -*- coding: utf-8 -*-
"""
将文风从select改为text输入框
"""

with open('tool_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换文风字段定义
old_style = '''                {"name": "style", "label": "文风风格", "type": "select", "options": [
                    {"value": "standard", "label": "标准风格 (通俗易懂,接地气)"},
                    {"value": "luxun", "label": "鲁迅风格 (简洁锋利,批判深刻)"},
                    {"value": "wangzengqi", "label": "汪曾祺风格 (淡雅质朴,形散神聚)"},
                    {"value": "gentle", "label": "温柔婉约 (温暖治愈,细腻感性)"},
                    {"value": "sharp", "label": "简洁锋利 (逻辑严密,观点鲜明)"}
                ], "default": "standard"},'''

new_style = '''                {"name": "style", "label": "文风描述", "type": "text", "placeholder": "如: 汪曾祺风格、鲁迅杂文风、温柔婉约、幽默风趣、严谨学术等", "required": False},'''

if old_style in content:
    content = content.replace(old_style, new_style)
    print("OK: 已将文风改为文本输入框")
else:
    print("ERROR: 未找到文风字段定义")

# 写回文件
with open('tool_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("完成!")
