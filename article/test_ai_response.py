# -*- coding: utf-8 -*-
"""
测试AI返回的原始内容
"""
import os
from zhipuai import ZhipuAI

# 从环境变量获取API密钥
api_key = os.environ.get('ZHIPU_API_KEY')
if not api_key:
    print("错误: 未找到ZHIPU_API_KEY环境变量")
    exit(1)

client = ZhipuAI(api_key=api_key)

# 主题生成提示词
theme = "春季饮食养生"
prompt = f"""请根据主题"{theme}"写一篇适合在今日头条发布的文章。

要求:
1. 标题要吸引眼球,使用【】符号和数字
2. 字数1500字左右
3. 内容要有实用价值
4. 使用emoji增加可读性
5. 结尾要有互动号召

请按以下格式输出:
---
标题: [文章标题]

[正文内容]
"""

print("=" * 80)
print("发送到AI的提示词:")
print(prompt)
print("=" * 80)

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.8,
    max_tokens=4000,
    top_p=0.9
)

content = response.choices[0].message.content

# 保存到文件避免编码问题
with open('ai_raw_response.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print("AI原始内容已保存到 ai_raw_response.txt")

# 尝试解析
lines = content.split('\n')
title = ""
body_lines = []
found_title = False
started_body = False

# 保存解析结果到文件
result_lines = []
result_lines.append("解析过程:\n")
result_lines.append("=" * 80 + "\n")

for i, line in enumerate(lines):
    stripped_line = line.strip()
    result_lines.append(f"行{i}: {repr(stripped_line)}\n")

    # 查找标题行
    if stripped_line.startswith("标题:"):
        title = stripped_line.replace("标题:", "").strip()
        found_title = True
        result_lines.append(f"  -> 找到标题: {title}\n")
        continue

    # 跳过分隔符和空行
    if stripped_line == "---" or stripped_line.startswith("---") or not stripped_line:
        result_lines.append(f"  -> 跳过(分隔符/空行)\n")
        continue

    # 跳过占位符文字
    if stripped_line.startswith("[") and stripped_line.endswith("]"):
        started_body = True
        result_lines.append(f"  -> 跳过(占位符), started_body=True\n")
        continue

    # 如果已经找到标题,开始收集正文
    if found_title:
        started_body = True

    if started_body:
        body_lines.append(line)
        result_lines.append(f"  -> 添加到正文\n")

result_lines.append("\n" + "=" * 80 + "\n")
result_lines.append(f"解析结果:\n")
result_lines.append(f"标题: {repr(title)}\n")
result_lines.append(f"正文行数: {len(body_lines)}\n")
result_lines.append(f"正文前200字符: {repr(''.join(body_lines)[:200])}\n")
result_lines.append("=" * 80 + "\n")

with open('ai_parse_result.txt', 'w', encoding='utf-8') as f:
    f.writelines(result_lines)
print("解析结果已保存到 ai_parse_result.txt")
