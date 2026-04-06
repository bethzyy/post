# -*- coding: utf-8 -*-
"""
简单修复:只在main()开始处添加命令行参数解析,然后return
"""

# 读取文件
with open('toutiao_article_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在main()函数的第一行之后添加命令行参数处理
for i, line in enumerate(lines):
    if 'def main():' in line and i > 1500:  # 确保是main()函数
        # 找到main()函数后,在"""主函数"""后插入代码
        for j in range(i+1, min(i+10, len(lines))):
            if '"""主函数"""' in lines[j]:
                # 在这一行后插入新代码
                insert_pos = j + 1
                new_code = """
    # ========== 命令行参数模式(Web界面调用) ==========
    import sys
    if len(sys.argv) > 1:
        # 有命令行参数,解析它们
        import argparse
        parser = argparse.ArgumentParser(description='今日头条文章生成器 v3.1')
        parser.add_argument('--mode', choices=['theme', 'draft'], help='生成模式')
        parser.add_argument('--theme', help='文章主题(模式=theme时使用)')
        parser.add_argument('--draft', help='草稿文件路径(模式=draft时使用)')
        parser.add_argument('--length', type=int, default=2000, help='目标字数')
        parser.add_argument('--images', choices=['y', 'n'], default='y', help='是否生成配图')
        parser.add_argument('--image-style', default='realistic', help='配图风格')

        args = parser.parse_args()

        if args.mode:
            # 命令行参数模式
            mode = 1 if args.mode == 'theme' else 2
            theme = None
            draft = None

            if mode == 1 and args.theme:
                theme = args.theme
                print(f"[Web模式] 主题: {theme}")
            elif mode == 2 and args.draft:
                import os
                if os.path.exists(args.draft):
                    with open(args.draft, 'r', encoding='utf-8') as f:
                        draft = f.read()
                    print(f"[Web模式] 草稿: {args.draft} ({len(draft)}字)")
                else:
                    print(f"[错误] 文件不存在: {args.draft}")
                    return
            else:
                print(f"[错误] 缺少必要参数")
                return

            # 生成文章
            generator = ToutiaoArticleGenerator()

            if mode == 1:
                article = generator.generate_article_with_ai(theme, args.length)
            else:
                article = generator.improve_article_draft(draft, args.length)

            if not article:
                print("\\n[错误] 文章生成失败")
                return

            # 保存HTML文件
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_prefix = "今日头条文章"
            tool_dir = Path(__file__).parent

            html_filename = f"{file_prefix}_{theme if mode==1 else '草稿完善'}_{timestamp}.html"
            html_path = str(tool_dir / html_filename)

            html_content = generator.create_article_html(article['title'], article['content'],
                                                           theme if mode==1 else '草稿完善', [])

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"\\n[成功] HTML文件已保存: {html_filename}")

            try:
                import webbrowser
                webbrowser.open(f'file:///{Path(html_path).absolute()}'.replace('\\\\', '/'))
            except:
                pass

            print("\\n生成完成!")
            return

    # ========== 交互模式(命令行直接运行) ==========
"""
                lines.insert(insert_pos, new_code)
                print(f"Inserted code at line {insert_pos + 1}")
                break
        break

# 写回文件
with open('toutiao_article_generator.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Simple fix applied!")
