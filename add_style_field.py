# -*- coding: utf-8 -*-
"""
添加文风选项到tool_manager.py
"""

with open('tool_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到插入位置 (在 "default": "2000" 之后)
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)

    # 在第61行 (索引60), "default": "2000" 之后插入
    if i == 60 and '"default": "2000' in line:
        new_lines.append('                },\n')
        new_lines.append('                {"name": "style", "label": "文风风格", "type": "select", "options": [\n')
        new_lines.append('                    {"value": "standard", "label": "标准风格 (通俗易懂,接地气)"},\n')
        new_lines.append('                    {"value": "luxun", "label": "鲁迅风格 (简洁锋利,批判深刻)"},\n')
        new_lines.append('                    {"value": "wangzengqi", "label": "汪曾祺风格 (淡雅质朴,形散神聚)"},\n')
        new_lines.append('                    {"value": "gentle", "label": "温柔婉约 (温暖治愈,细腻感性)"},\n')
        new_lines.append('                    {"value": "sharp", "label": "简洁锋利 (逻辑严密,观点鲜明)"}\n')
        new_lines.append('                ], "default": "standard"},\n')

with open('tool_manager.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("OK: 已添加文风选项")
