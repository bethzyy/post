# -*- coding: utf-8 -*-
"""
添加鲁迅风格到generate_article_with_ai方法
"""

# 读取文件
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换风格打印部分
old_print = """        print(f"[AI生成] 风格: {'汪曾祺' if style == 'wangzengqi' else '标准'}\\n")"""
new_print = """        # 风格名称映射
        style_names = {
            'standard': '标准',
            'luxun': '鲁迅',
            'wangzengqi': '汪曾祺',
            'gentle': '温柔婉约',
            'sharp': '简洁锋利'
        }
        style_name = style_names.get(style, '标准')
        print(f"[AI生成] 风格: {style_name}\\n")"""

content = content.replace(old_print, new_print)

# 添加鲁迅风格的prompt (在汪曾祺风格之前)
old_wangzengqi = """        if style == 'wangzengqi':"""
new_luxun_and_wangzengqi = """        if style == 'luxun':
            prompt = f"""你是鲁迅先生，中国现代文学奠基人。请用你的杂文风格写一篇关于"{theme}"的文章。

## 鲁迅杂文风格特点：
1. **语言特点**：
   - 简洁锋利，一针见血
   - 冷峻深刻，辛辣讽刺
   - 用词精准，逻辑严密
   - 善用反语和讽刺

2. **结构特点**：
   - 开门见山，直击要害
   - 层层递进，论证严密
   - 善用对比，揭露矛盾

3. **思想特点**：
   - 批判精神，直面社会现实
   - 深刻洞察，揭示本质
   - 忧国忧民，悲天悯人

4. **禁忌**：
   - 不得使用空洞的口号
   - 不得滥用感叹号
   - 不得使用营销话术
   - 不得使用emoji

## 写作要求：
1. 字数: {target_length}字左右
2. 主题: {theme}
3. 开头: 直接切入主题，观点鲜明
4. 内容:
   - 深入分析现象背后的本质
   - 批判时弊，引人深思
   - 用事实和逻辑说话
5. 结尾: 发人深省，留有余味
6. 标题: 简洁有力，体现思想深度

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

记住:你要写的是一篇有思想深度的杂文，要敢于批评，善于批判，用文字唤醒读者。
"""
        elif style == 'wangzengqi':"""

content = content.replace(old_wangzengqi, new_luxun_and_wangzengqi)

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK: 已添加鲁迅风格选项")
