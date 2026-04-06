#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复今日头条文章生成器的Web模式问题
1. 增强tool_manager.py中的参数打印
2. 在toutiao_article_generator.py中创建main_web函数
3. 修改入口点逻辑来检测环境变量
"""

import os
import re

def fix_tool_manager():
    """增强tool_manager.py中的参数打印"""
    file_path = "C:/D/CAIE_tool/MyAIProduct/post/tool_manager.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找并替换DEBUG打印部分
    old_pattern = r"print\(f\"\[DEBUG\] JSON参数文件: \{params_file\}\"\)\s+print\(f\"\[DEBUG\] 参数内容: mode=\{mode\}, theme=\{theme\}\"\)"

    new_code = """print(f"[DEBUG] JSON参数文件: {params_file}")
                print(f"[DEBUG] ========== 文章生成参数 ==========")
                print(f"[DEBUG] 模式(mode): {mode}")
                print(f"[DEBUG] 主题(theme): {theme}")
                print(f"[DEBUG] 草稿(draft): {draft}")
                print(f"[DEBUG] 字数(length): {length}")
                print(f"[DEBUG] 生成配图(generate_images): {generate_images}")
                print(f"[DEBUG] 配图风格(image_style): {image_style}")
                print(f"[DEBUG] 文章风格(style): {style}")
                print(f"[DEBUG] 参数字典完整内容: {params_dict}")
                print(f"[DEBUG] ===================================")"""

    content = re.sub(old_pattern, new_code, content, flags=re.MULTILINE | re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] 已增强tool_manager.py中的参数打印")

def create_main_web_function():
    """在toutiao_article_generator.py中创建main_web函数"""

    main_web_code = '''
def main_web():
    """Web模式主函数 - 从tool_manager.py调用"""
    print("\\n" + "="*80)
    print("[ENTER] 进入Web模式 main_web()")
    print("="*80 + "\\n")

    try:
        # 读取JSON参数文件
        params_json_path = os.environ.get('ARTICLE_PARAMS_JSON', 'article_params.json')
        print(f"[DEBUG] 参数文件路径: {params_json_path}")

        with open(params_json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        print(f"[DEBUG] 成功读取参数文件\\n")

        # 解析参数
        mode = params.get('mode', '1')
        theme = params.get('theme', '')
        draft = params.get('draft', '')
        length = params.get('length', 2000)
        generate_images = params.get('generate_images', 'y')
        image_style = params.get('image_style', 'realistic')
        style = params.get('style', 'standard')

        print(f"[参数] 模式: {mode}")
        print(f"[参数] 主题: {theme}")
        print(f"[参数] 草稿: {draft}")
        print(f"[参数] 字数: {length}")
        print(f"[参数] 生成配图: {generate_images}")
        print(f"[参数] 配图风格: {image_style}")
        print(f"[参数] 文章风格: {style}\\n")

        # 模式1: 主题生成
        if mode == '1':
            print("[模式] 主题生成模式")
            if not theme:
                return {"error": "主题不能为空"}
            result = generate_article(theme, length, generate_images=='y', image_style, style)

        # 模式2: 草稿完善
        elif mode == '2':
            print("[草稿完善] 检测到草稿完善模式")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft):
                print(f"[草稿完善] 检测到草稿文件路径: {draft}")
                try:
                    with open(draft, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[草稿完善] 成功读取草稿文件,长度: {len(draft)}字\\n")
                except Exception as e:
                    return {"error": f"读取草稿文件失败: {str(e)}"}
            else:
                print(f"[草稿完善] 使用草稿文本内容\\n")

            if not draft:
                return {"error": "草稿内容不能为空"}

            result = improve_draft(draft, length, generate_images=='y', image_style, style)

        else:
            return {"error": f"无效的模式: {mode}"}

        # 清理临时参数文件
        try:
            os.remove(params_json_path)
            print(f"[清理] 已删除临时参数文件: {params_json_path}")
        except:
            pass

        return result

    except Exception as e:
        print(f"[ERROR] main_web执行错误: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

'''

    return main_web_code

def fix_toutiao_generator():
    """修复toutiao_article_generator.py"""
    file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经有main_web函数
    if 'def main_web():' in content:
        print("[INFO] main_web函数已存在,跳过创建")
    else:
        # 在main函数之前插入main_web函数
        main_web_code = create_main_web_function()

        # 找到main函数的位置
        pattern = r"(def main\(\):)"
        replacement = main_web_code + r"\1"

        content = re.sub(pattern, replacement, content, count=1)
        print("[OK] 已添加main_web函数")

    # 修复入口点逻辑
    old_main_entry = r"if __name__ == \"__main__\":\s+try:\s+main\(\)\s+except KeyboardInterrupt:"
    new_main_entry = """if __name__ == "__main__":
    try:
        # 检测是否在Web模式下运行(通过环境变量ARTICLE_PARAMS_JSON)
        if os.environ.get("ARTICLE_PARAMS_JSON"):
            main_web()
        else:
            main()
    except KeyboardInterrupt:"""

    if 'if os.environ.get("ARTICLE_PARAMS_JSON"):' in content:
        print("[INFO] 入口点逻辑已修复,跳过")
    else:
        content = re.sub(old_main_entry, new_main_entry, content, flags=re.MULTILINE | re.DOTALL)
        print("[OK] 已修复入口点逻辑")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] toutiao_article_generator.py修复完成")

if __name__ == "__main__":
    print("="*80)
    print("今日头条文章生成器 - Web模式修复 v2.0")
    print("="*80)
    print()

    try:
        fix_tool_manager()
        print()
        fix_toutiao_generator()
        print()
        print("="*80)
        print("[完成] 所有修复已应用!")
        print("[提示] 请重启服务器以使更改生效")
        print("="*80)

    except Exception as e:
        print(f"[ERROR] 修复失败: {e}")
        import traceback
        traceback.print_exc()
