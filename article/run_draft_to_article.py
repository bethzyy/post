# -*- coding: utf-8 -*-
"""
从草稿文件生成头条文章的包装脚本
"""
import sys
from pathlib import Path

# 导入主生成器
from toutiao_article_generator import ToutiaoArticleGenerator

def main():
    # 读取草稿文件
    draft_file = Path(__file__).parent / "draft.txt"

    if not draft_file.exists():
        print(f"[错误] 草稿文件不存在: {draft_file}")
        return

    with open(draft_file, 'r', encoding='utf-8') as f:
        draft_content = f.read()

    print("="*80)
    print("今日头条文章生成器 - 草稿完善模式")
    print("="*80)
    print()
    print(f"[读取] 草稿文件: {draft_file}")
    print(f"[信息] 草稿字数: {len(draft_content)}字")
    print()

    # 创建生成器
    generator = ToutiaoArticleGenerator()

    if not generator.text_client:
        print("\n[ERROR] 无法初始化AI文本客户端")
        print("[ERROR] 请检查config.py中的ZHIPU_API_KEY配置")
        return

    # 完善草稿
    target_length = 2000  # 目标字数
    print(f"[设置] 目标字数: {target_length}字")
    print()

    article = generator.improve_article_draft(draft_content, target_length)

    if not article:
        print("\n[ERROR] 草稿完善失败")
        return

    # 显示结果
    print()
    print("-"*80)
    print()
    print(f"[成功] 文章完善成功!")
    print()
    print("="*80)
    print(f"标题: {article['title']}")
    print("="*80)
    # 跳过内容显示,避免编码问题
    # print(article['content'])
    print()
    print("="*80)
    print(f"字数: {article['word_count']}字")
    print("="*80)
    print()

    # 保存为Markdown文件
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    md_filename = f"文章草稿完善_OpenClaw真相_{timestamp}.md"
    tool_dir = Path(__file__).parent
    md_path = str(tool_dir / md_filename)

    md_content = f"""# {article['title']}

**主题**: OpenClaw真相
**字数**: {article['word_count']}字
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**来源**: 基于用户草稿完善

---

{article['content']}

---

*本文由AI发文工具管理器自动生成 (基于用户草稿完善)*
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"[成功] Markdown文件已保存: {md_path}")

    # 保存为HTML文件
    html_filename = f"文章草稿完善_OpenClaw真相_{timestamp}.html"
    html_path = str(tool_dir / html_filename)
    html_content = generator.create_article_html(article['title'], article['content'], "OpenClaw真相", [])

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[成功] HTML文件已保存: {html_path}")

    # 自动打开HTML文件
    try:
        import webbrowser
        import os
        webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
        print(f"[成功] 已在浏览器中打开文章预览")
    except:
        print(f"[提示] 请手动打开HTML文件查看文章: {html_path}")

    print()
    print("="*80)
    print("生成完成!")
    print("="*80)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[提示] 程序被用户中断")
    except Exception as e:
        print(f"\n\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()
