# -*- coding: utf-8 -*-
"""
今日头条高赞文章生成器 - 改进版
支持用户输入自定义主题,使用AI生成高质量文章
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_zhipuai_client


class ToutiaoArticleGenerator:
    """今日头条文章生成器 - AI增强版"""

    def __init__(self):
        self.client = get_zhipuai_client()

    def generate_article_with_ai(self, theme, target_length=2000):
        """使用AI生成文章"""

        print(f"\n[AI生成] 正在为主题'{theme}'生成文章...")
        print(f"[AI生成] 目标字数: {target_length}字\n")

        prompt = f"""请为一篇今日头条文章撰写高质量内容。

主题: {theme}

要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
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
"""

        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",  # 使用快速模型
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

            # 提取生成的内容
            content = response.choices[0].message.content

            # 解析标题和正文
            lines = content.split('\n')
            title = ""
            body_lines = []

            for i, line in enumerate(lines):
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else f"关于{theme}的思考"

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length
            }

        except Exception as e:
            print(f"[ERROR] AI生成失败: {e}")
            return None

    def create_article_html(self, title, content, theme):
        """创建HTML格式的文章"""

        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}

        .title {{
            font-size: 2em;
            font-weight: bold;
            color: #222;
            margin-bottom: 15px;
            line-height: 1.4;
        }}

        .meta {{
            color: #999;
            font-size: 0.9em;
        }}

        .content {{
            font-size: 1.1em;
            line-height: 2;
        }}

        .content p {{
            margin-bottom: 20px;
            text-indent: 2em;
        }}

        .content h2 {{
            font-size: 1.5em;
            color: #5a67d8;
            margin: 30px 0 15px 0;
            padding-left: 15px;
            border-left: 4px solid #5a67d8;
        }}

        .content h3 {{
            font-size: 1.3em;
            color: #6b46c1;
            margin: 25px 0 10px 0;
        }}

        .content strong {{
            color: #e53e3e;
            font-weight: bold;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}

        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">{title}</div>
            <div class="meta">
                主题: {theme} |
                字数: {len(content)}字 |
                生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>

        <div class="content">
            {self._format_content_to_html(content)}
        </div>

        <div class="footer">
            <p>本文由AI发文工具管理器生成</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

        return html_content

    def _format_content_to_html(self, content):
        """将Markdown格式内容转换为HTML"""

        html = content

        # 转换段落
        paragraphs = html.split('\n\n')
        html_paragraphs = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 处理标题
            if para.startswith('### '):
                html_paragraphs.append(f'<h3>{para[4:]}</h3>')
            elif para.startswith('## '):
                html_paragraphs.append(f'<h2>{para[3:]}</h2>')
            elif para.startswith('# '):
                html_paragraphs.append(f'<h2>{para[2:]}</h2>')
            # 处理高亮块
            elif para.startswith('>'):
                html_paragraphs.append(f'<div class="highlight">{para[1:].strip()}</div>')
            # 普通段落
            else:
                # 处理加粗
                para = para.replace('**', '<strong>').replace('**', '</strong>')
                # 处理换行
                para = para.replace('\n', '<br>')
                html_paragraphs.append(f'<p>{para}</p>')

        return '\n'.join(html_paragraphs)


def get_user_theme():
    """获取用户输入的主题"""

    print("\n" + "="*80)
    print("今日头条文章生成器 - AI增强版")
    print("="*80)
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            theme = sys.stdin.readline().strip()
            if theme:
                print(f"[Web模式] 主题: {theme}")
                return theme
        except:
            pass

    print("请输入您想要生成文章的主题")
    print()
    print("示例主题:")
    themes = [
        "过年回老家",
        "职场新人必看",
        "健康养生小贴士",
        "理财投资心得",
        "教育孩子感悟",
        "情感关系建议"
    ]

    for i, theme in enumerate(themes, 1):
        print(f"  {i}. {theme}")

    print()
    print("您可以输入上述主题,或输入自定义主题")
    print()

    while True:
        try:
            user_input = input("请输入主题 (输入 'q' 退出): ").strip()

            if user_input.lower() == 'q':
                return None

            if user_input:
                print(f"\n[确认] 主题: {user_input}")
                return user_input
            else:
                print("[提示] 主题不能为空,请重新输入")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return None


def get_target_length():
    """获取目标字数"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            length = sys.stdin.readline().strip()
            if length and length.isdigit():
                print(f"[Web模式] 字数: {length}")
                return int(length)
        except:
            pass

    print()
    print("请选择文章长度:")
    print("  1. 1500字左右 (快速阅读)")
    print("  2. 2000字左右 (标准长度)")
    print("  3. 2500字左右 (深度文章)")

    while True:
        try:
            choice = input("\n请选择 (默认为2): ").strip()

            if not choice:
                choice = "2"

            if choice in ["1", "2", "3"]:
                lengths = {"1": 1500, "2": 2000, "3": 2500}
                return lengths[choice]
            else:
                print("[提示] 请输入 1、2 或 3")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return 2000
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return 2000


def main():
    """主函数"""

    print("="*80)
    print("今日头条文章生成器")
    print("="*80)
    print()

    # 获取用户输入
    theme = get_user_theme()

    if not theme:
        print("\n[退出] 未输入主题,程序退出")
        return

    # 获取目标字数
    target_length = get_target_length()

    print(f"\n[设置] 目标字数: {target_length}字")

    # 创建生成器
    generator = ToutiaoArticleGenerator()

    if not generator.client:
        print("\n[ERROR] 无法初始化AI客户端")
        print("[ERROR] 请检查config.py中的ZHIPU_API_KEY配置")
        return

    # 生成文章
    print()
    print("-"*80)
    print()

    article = generator.generate_article_with_ai(theme, target_length)

    if not article:
        print("\n[ERROR] 文章生成失败")
        return

    # 显示生成的文章
    print()
    print("-"*80)
    print()
    print("✅ 文章生成成功!")
    print()
    print("="*80)
    print(f"标题: {article['title']}")
    print("="*80)
    print()
    print(article['content'])
    print()
    print("="*80)
    print(f"字数: {article['word_count']}字")
    print(f"目标: {article['target_length']}字")
    print(f"完成度: {article['word_count']/article['target_length']*100:.1f}%")
    print("="*80)
    print()

    # 保存为Markdown文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    md_filename = f"今日头条文章_{theme}_{timestamp}.md"

    md_content = f"""# {article['title']}

**主题**: {theme}
**字数**: {article['word_count']}字
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{article['content']}

---

*本文由AI发文工具管理器自动生成*
"""

    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"✅ Markdown文件已保存: {md_filename}")

    # 保存为HTML文件
    html_filename = f"今日头条文章_{theme}_{timestamp}.html"
    html_content = generator.create_article_html(article['title'], article['content'], theme)

    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML文件已保存: {html_filename}")

    # 自动打开HTML文件
    try:
        import webbrowser
        webbrowser.open(f'file:///{os.path.abspath(html_filename)}'.replace('\\', '/'))
        print(f"✅ 已在浏览器中打开文章预览")
    except:
        print(f"[提示] 请手动打开HTML文件查看文章: {html_filename}")

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
