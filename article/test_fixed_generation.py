# -*- coding: utf-8 -*-
"""
测试修复后的文章生成功能
"""
import sys
from pathlib import Path

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from article.toutiao_article_generator import ToutiaoArticleGenerator

def test_draft_improvement():
    """测试草稿完善功能"""
    print("="*80)
    print("测试修复后的草稿完善功能")
    print("="*80)

    # 读取草稿内容
    draft_file = Path(__file__).parent / "draft2.txt"
    with open(draft_file, 'r', encoding='utf-8') as f:
        draft_content = f.read()

    print(f"\n原始草稿:\n{draft_content}\n")
    print("-"*80)

    # 初始化生成器
    generator = ToutiaoArticleGenerator()

    # 完善草稿
    print("\n开始完善草稿...")
    result = generator.improve_article_draft(draft_content, target_length=1500, style='standard')

    if result:
        print("\n" + "="*80)
        print("生成成功!")
        print("="*80)
        print(f"标题: {result['title']}")
        print(f"正文字数: {result['word_count']}")
        print(f"\n正文内容预览(前500字):")
        print("-"*80)
        print(result['content'][:500] + "...")
        print("-"*80)

        # 检查是否为空
        if not result['title'] or result['title'] == "---":
            print("\n[警告] 标题为空或异常!")
        if not result['content']:
            print("\n[警告] 正文内容为空!")
        else:
            print("\n[成功] 文章生成正常!")

            # 保存HTML文件
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_filename = f"test_今日头条文章_1500_{timestamp}.html"

            tool_dir = Path(__file__).parent
            html_path = str(tool_dir / html_filename)

            html_content = generator.create_article_html(result['title'], result['content'], "测试", [])

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"\n[成功] HTML文件已保存: {html_filename}")

            # 自动打开HTML文件
            try:
                import webbrowser
                webbrowser.open(f'file:///{Path(html_path).absolute()}'.replace('\\', '/'))
                print(f"[成功] 已在浏览器中打开文章预览")
            except:
                pass
    else:
        print("\n[错误] 文章生成失败!")

if __name__ == "__main__":
    test_draft_improvement()
