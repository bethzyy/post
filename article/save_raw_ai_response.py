#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""保存AI原始响应到文件，然后手动处理"""

import os
from zhipuai import ZhipuAI

# Initialize API client
api_key = os.environ.get("ZHIPU_API_KEY")
client = ZhipuAI(api_key=api_key)

# Wang Zengqi style prompt
theme = "未来图书馆：在AI时代，图书馆作为城市第三空间的价值"
target_length = 2000

prompt = f"""你是汪曾祺先生，中国当代著名作家。请用你的散文风格写一篇关于"{theme}"的文章。

## 汪曾祺散文风格特点：
1. **语言特点**：
   - 简洁平淡，朴实有趣
   - 平易自然，富有节奏感
   - 不用华丽辞藻，但意味深长
   - 口语化，有生活气息

2. **结构特点**：
   - 形散神聚，看似随意实则精心
   - 从小事写起，以小见大
   - 漫不经心中见真意

3. **情感特点**：
   - 淡雅怀旧，有温度
   - 乐观平和的人生态度
   - 关注日常人事，体察细微

4. **禁忌**：
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji
   - 不得使用营销话术（"让我们一起"、"不容错过"等）
   - 不得生硬列举"5个XX"、"3大XX"

## 用户草稿中的情感基调（请保留并发挥）：
"每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁..."
"我想象中的未来图书馆，绝不仅仅是数字化升级后的'智能书库'。它应该是一座城市的'第三空间'——不是家，不是办公室，而是属于心灵的栖息地。"

## 写作要求：
1. 字数: {target_length}字左右
2. 主题: {theme}
3. 开头: 从个人经历或感受写起（比如走进图书馆的那份安宁）
4. 内容:
   - 谈谈2026年AI时代的图书馆变化
   - 保留原草稿中"第三空间"、"心灵栖息地"等核心概念
   - 用平淡朴实的语言写深刻的思想
5. 结尾: 留有余韵，引人思考
6. 标题: 简洁有意境，15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

记住:你要写的是一篇有温度、有情怀的散文，而不是营销文案。语言要平淡但有力，朴实但深刻。
"""

print("发送AI请求...")

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

# 保存原始响应到文件
output_file = "raw_ai_response_wangzengqi.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n[成功] AI原始响应已保存到: {output_file}")
print(f"内容长度: {len(content)} 字符")

# 尝试解析
lines = content.split('\n')

# 找到标题
title = None
title_idx = -1
for i, line in enumerate(lines):
    if '标题:' in line or line.strip().startswith('标题:'):
        title = line.split(':', 1)[1].strip() if ':' in line else line.replace('标题:', '').strip()
        title_idx = i
        break

print(f"\n解析到的标题: {title}")

# 找到正文开始位置（标题后的下一行）
body_start = title_idx + 1 if title_idx >= 0 else 0

# 跳过开头的---分隔符
while body_start < len(lines) and lines[body_start].strip() in ('---', '===', ''):
    body_start += 1

# 提取正文
body_lines = []
for i in range(body_start, len(lines)):
    line = lines[i]
    # 遇到结束分隔符就停止
    if line.strip() in ('---', '==='):
        break
    body_lines.append(line)

body = '\n'.join(body_lines).strip()

print(f"正文字数: {len(body)} 字符")
print(f"正文预览:\n{body[:300]}...")

# 保存解析结果
result = {
    'title': title or '未来图书馆：城市中的心灵栖息地',
    'content': body,
    'word_count': len(body)
}

import json
with open('parsed_article.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n[成功] 解析结果已保存到: parsed_article.json")
