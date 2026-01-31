#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug script to see actual AI response"""

import os
from zhipuai import ZhipuAI

# Initialize API client
api_key = os.environ.get("ZHIPU_API_KEY")
if not api_key:
    print("[ERROR] ZHIPU_API_KEY environment variable not set")
    exit(1)

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

print("Sending request to AI...")
print("="*80)

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

print("\nRAW AI RESPONSE:")
print("="*80)
print(content)
print("="*80)

# Try to parse
lines = content.split('\n')
title = ""
body_lines = []

for i, line in enumerate(lines):
    if line.startswith("标题:"):
        title = line.replace("标题:", "").strip()
    elif line.strip() == "---":
        continue
    elif title:  # Only collect body after title found
        body_lines.append(line)

body = '\n'.join(body_lines).strip()

print("\nPARSED RESULT:")
print(f"Title: '{title}'")
print(f"Body length: {len(body)} characters")
print(f"Body preview (first 200 chars): {body[:200]}")
