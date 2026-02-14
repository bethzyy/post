# -*- coding: utf-8 -*-
"""
更新文风逻辑，支持用户自定义文风描述
"""

with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换整个generate_article_with_ai方法的开头部分
old_code = '''        print(f"\\n[AI生成] 正在为主题'{theme}'生成文章...")
        print(f"[AI生成] 目标字数: {target_length}字")
        print(f"[AI生成] 风格: {'汪曾祺' if style == 'wangzengqi' else '标准'}\\n")

        # 根据风格选择不同的prompt
        if style == 'wangzengqi':
            prompt = f"""你是汪曾祺先生，中国当代著名作家。请用你的散文风格写一篇关于"{theme}"的文章。'''

new_code = '''        print(f"\\n[AI生成] 正在为主题'{theme}'生成文章...")
        print(f"[AI生成] 目标字数: {target_length}字")
        print(f"[AI生成] 文风描述: {style if style else '标准'}\\n")

        # 根据文风描述生成prompt
        if style and style.lower() != 'standard':
            # 用户提供了文风描述
            prompt = f"""请为一篇今日头条文章撰写高质量内容。

主题: {theme}

文风要求: {style}

写作要求:
1. 字数: {target_length}字左右
2. 文风: 严格按照"{style}"的风格来写
3. 结构: 吸引人的标题 + 引人入胜的开头 + 3-5个要点 + 感人或启发的结尾 + 互动号召
4. 内容: 真实案例,数据支撑,实用建议
5. 情感: 能引起共鸣,激发情绪(感动/激励/共鸣)
6. 标题要求: 使用数字+疑问/对比/利益点,字数15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

注意:
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 多用案例和数据说话
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
- **最重要的是:要体现出"{style}"的文风特点**
"""
        elif style == 'wangzengqi' or style == '汪曾祺' or '汪曾祺' in style:'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("OK: 已更新文风逻辑")
else:
    print("ERROR: 未找到目标代码")

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("完成!")
