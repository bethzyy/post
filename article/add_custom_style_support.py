# -*- coding: utf-8 -*-
"""
添加自定义文风支持
"""

with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到prompt生成部分（else:之后）
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)

    # 在第317行 (else:) 之后插入文风处理逻辑
    if i == 316 and line.strip() == 'else:':
        # 插入文风处理代码
        new_lines.append('            # 根据用户提供的文风描述生成prompt\n')
        new_lines.append('            style_desc = f"\\n文风要求: {style}" if style and style.lower() != \\'standard\\' else ""\n')
        new_lines.append('\n')

with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("OK: Step 1 - Added style handling")

# 第二步：修改prompt中的theme行
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_theme = '主题: {theme}'
new_theme = '主题: {theme}{style_desc}'

content = content.replace(old_theme, new_theme)

with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: Step 2 - Modified theme line")

# 第三步：修改风格要求行
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_style_req = '2. 风格: 通俗易懂,接地气,有感染力'
new_style_req = '''2. 风格: 通俗易懂,接地气,有感染力{f"，特别注意要体现{style}的文风特点" if style and style.lower() != 'standard' else ""}'''

content = content.replace(old_style_req, new_style_req)

with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: Step 3 - Modified style requirement")
print("完成!")
