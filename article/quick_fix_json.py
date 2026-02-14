# -*- coding: utf-8 -*-
"""
快速修复:在脚本开头插入JSON参数检测
"""
import json

# 读取备份文件
with open('toutiao_article_generator.py.backup', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在main()函数后插入JSON检测代码
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)

    # 在def main():后插入
    if i == 1458:  # main()函数所在行
        # 插入JSON检测代码
        json_code = '''    # ========== Web模式: 通过JSON文件读取参数 ==========
    import os
    params_json_path = os.environ.get('ARTICLE_PARAMS_JSON')

    if params_json_path and os.path.exists(params_json_path):
        print(f"[Web模式] 读取参数文件: {params_json_path}")

        try:
            with open(params_json_path, 'r', encoding='utf-8') as f:
                params = json.load(f)

            mode_str = params.get('mode', '1')
            mode = 1 if mode_str == '1' else 2

            theme = params.get('theme', '')
            draft = params.get('draft', '')
            length = params.get('length', 2000)
            generate_images = params.get('generate_images', 'y')
            image_style = params.get('image_style', 'realistic')

            print(f"[Web模式] 参数: mode={mode}, theme={repr(theme)}, length={length}")

            # 根据模式生成文章
            generator = ToutiaoArticleGenerator()

            if mode == 1:
                # 主题生成模式
                if not theme:
                    print("\\n[错误] 缺少主题参数")
                    return

                article = generator.generate_article_with_ai(theme, length)
                theme_for_filename = theme
            else:
                # 草稿完善模式
                if not draft:
                    print("\\n[错误] 缺少草稿文件路径")
                    return

                if os.path.exists(draft):
                    with open(draft, 'r', encoding='utf-8') as f:
                        draft_content = f.read()
                    print(f"[Web模式] 已读取草稿: {len(draft_content)}字")
                else:
                    print(f"\\n[错误] 草稿文件不存在: {draft}")
                    return

                article = generator.improve_article_draft(draft_content, length)
                theme_for_filename = '草稿完善'

            if not article:
                print("\\n[错误] 文章生成失败")
                return

            # 保存HTML文件
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_prefix = "今日头条文章"
            tool_dir = Path(__file__).parent

            html_filename = f"{file_prefix}_{theme_for_filename}_{timestamp}.html"
            html_path = str(tool_dir / html_filename)

            html_content = generator.create_article_html(article['title'], article['content'],
                                                           theme_for_filename, [])

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"\\n[成功] HTML文件已保存: {html_filename}")

            try:
                import webbrowser
                webbrowser.open(f'file:///{Path(html_path).absolute()}'.replace('\\\\', '/'))
            except:
                pass

            print("\\n生成完成!")

            # 清理JSON参数文件
            try:
                os.unlink(params_json_path)
            except:
                pass

            return

        except Exception as e:
            print(f"\\n[错误] JSON参数解析失败: {e}")
            import traceback
            traceback.print_exc()
            return

    # ========== 交互模式: 直接运行 ==========
'''
        new_lines.append(json_code)

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed! Added JSON parameter reading")
