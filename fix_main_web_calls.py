#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复main_web函数中的方法调用
"""

file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复模式1和模式2的调用
# 查找并替换错误的函数调用

# 1. 模式1的调用 - generate_article
old_mode1 = """# 模式1: 主题生成
        if mode == '1':
            print("[模式] 主题生成模式")
            if not theme:
                return {"error": "主题不能为空"}
            result = generate_article(theme, length, generate_images=='y', image_style, style)"""

new_mode1 = """# 模式1: 主题生成
        if mode == '1':
            print("[模式] 主题生成模式")
            if not theme:
                return {"error": "主题不能为空"}

            # 创建生成器实例
            generator = ToutiaoArticleGenerator()
            if not generator.text_client:
                return {"error": "无法初始化AI文本客户端"}

            # 调用生成方法
            article = generator.generate_article_with_ai(theme, length)
            if not article:
                return {"error": "文章生成失败"}

            result = {
                "success": True,
                "title": article['title'],
                "content": article['content'],
                "word_count": article['word_count'],
                "target_length": article['target_length']
            }"""

# 2. 模式2的调用 - improve_draft
old_mode2 = """# 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):
                draft_path = draft  # 保存原始路径用于调试
                print(f"[草稿完善] 检测到草稿文件路径: {draft}")
                try:
                    with open(draft, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容")

            if not draft:
                return {"error": "草稿内容不能为空"}

            result = improve_draft(draft, length, generate_images=='y', image_style, style)"""

new_mode2 = """# 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):
                draft_path = draft  # 保存原始路径用于调试
                print(f"[草稿完善] 检测到草稿文件路径: {draft}")
                try:
                    with open(draft, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容")

            if not draft:
                return {"error": "草稿内容不能为空"}

            # 创建生成器实例
            generator = ToutiaoArticleGenerator()
            if not generator.text_client:
                return {"error": "无法初始化AI文本客户端"}

            # 调用草稿完善方法
            article = generator.improve_article_draft(draft, length)
            if not article:
                return {"error": "草稿完善失败"}

            result = {
                "success": True,
                "title": article['title'],
                "content": article['content'],
                "word_count": article['word_count'],
                "target_length": article['target_length']
            }"""

# 执行替换
content = content.replace(old_mode1, new_mode1)
content = content.replace(old_mode2, new_mode2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] 已修复main_web函数中的方法调用")
print("[OK] 现在使用正确的generator.generate_article_with_ai()和generator.improve_article_draft()")
