# -*- coding: utf-8 -*-
"""
为 Claude Code 记忆文件说明生成配图版（今日头条发布格式）
资深编辑优化版v2：配图位置精心设计，样式专业规范
"""

import sys
import os
from pathlib import Path
import re

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from toutiao_article_generator import ToutiaoArticleGenerator


def extract_article_content_from_html(html_path):
    """从HTML文件中提取标题和内容"""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if not title_match:
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Claude Code 记忆文件说明"

    # 提取正文内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
    if not body_match:
        return None

    body_content = body_match.group(1)
    # 移除 <h1> 标签
    body_content = re.sub(r'<h1[^>]*>.*?</h1>', '', body_content, flags=re.DOTALL)

    return {
        'title': title,
        'content': body_content.strip(),
        'theme': 'Claude Code 记忆文件 CLAUDE.md 和 MEMORY.md'
    }


def generate_targeted_images(gen):
    """生成针对特定内容位置的配图"""
    print("\n开始生成针对性配图...")

    images = []

    # 配图1：双记忆系统概念图（封面）
    print("\n[配图1/3] 双记忆系统概念图...")
    prompt1 = """Clean modern infographic showing two file folders: CLAUDE.md (team documentation) and MEMORY.md (personal learning notes). Professional tech illustration, blue purple theme, minimalist white background."""
    img1 = gen.generate_article_images(
        theme="CLAUDE.md and MEMORY.md dual memory system",
        article_content=prompt1,
        image_style="technical",
        num_images=1
    )
    if img1:
        images.append(('cover', img1[0], 'Claude Code 的双记忆系统'))

    # 配图2：项目文档场景（对比表格后）
    print("\n[配图2/3] CLAUDE.md 项目文档可视化...")
    prompt2 = """Developer workspace showing CLAUDE.md file with project documentation. Professional setup with code editor displaying architecture docs and commands. Warm lighting, realistic photo focusing on document file."""
    img2 = gen.generate_article_images(
        theme="CLAUDE.md project documentation example",
        article_content=prompt2,
        image_style="realistic",
        num_images=1
    )
    if img2:
        images.append(('project_doc', img2[0], 'CLAUDE.md 作为项目的"使用说明书"'))

    # 配图3：实际应用场景（案例部分）
    print("\n[配图3/3] multicc 项目实际应用...")
    prompt3 = """Split-screen developer environment: terminal with multiple sessions (multicc project) and two markdown files - CLAUDE.md with specs, MEMORY.md with bug fix notes. Realistic dual-monitor setup, modern dark theme IDE."""
    img3 = gen.generate_article_images(
        theme="multicc project practical example CLAUDE.md MEMORY.md",
        article_content=prompt3,
        image_style="realistic",
        num_images=1
    )
    if img3:
        images.append(('practice', img3[0], 'multicc 项目的实际应用'))

    return images


def clean_html_content(content):
    """清理HTML内容中的格式问题"""
    # 修复双重嵌套的<p>标签
    content = re.sub(r'<p style="[^"]*"><p>(.*?)</p></p>', r'<p>\1</p>', content, flags=re.DOTALL)

    # 清理重复的style属性
    content = re.sub(r' style="([^"]*)"; style="([^"]*)"', r' style="\1; \2"', content)

    # 清理style中的重复定义
    def merge_styles(m):
        style_content = m.group(1)
        # 简单去重：按分号分割，去重后再合并
        parts = style_content.split(';')
        seen = {}
        unique_parts = []
        for part in parts:
            part = part.strip()
            if part and ':' in part:
                key = part.split(':')[0].strip()
                if key not in seen:
                    seen[key] = True
                    unique_parts.append(part)
        return f' style="{"; ".join(unique_parts)}"'

    content = re.sub(r' style="([^"]+)"', merge_styles, content)

    return content


def create_optimized_html(title, content, images, output_path):
    """创建优化配图位置的HTML文件（专业版）"""

    # 清理HTML内容
    content = clean_html_content(content)

    # 在特定位置插入配图
    # 插入点1：开篇简介后（第一个<h2>之前）
    content = re.sub(
        r'(\n\s*<h2[^>]*>对比表格</h2>)',
        r'\n\n<p style="text-align: center;"><img src="../' + os.path.basename(images[0][1]) + r'" alt="双记忆系统概念图" style="max-width: 650px; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"></p>\n<p style="text-align: center; color: #888; font-size: 13px; margin-top: 8px; margin-bottom: 20px;">图：' + images[0][2] + r'</p>\n\1',
        content,
        count=1
    )

    # 插入点2：对比表格之后（在</table>后，CLAUDE.md详解的<h2>前）
    if len(images) > 1:
        content = re.sub(
            r'(</table>\s*)(\s*<h2[^>]*>CLAUDE\.md 详解</h2>)',
            r'\1\n\n<p style="text-align: center;"><img src="../' + os.path.basename(images[1][1]) + r'" alt="CLAUDE.md 项目文档" style="max-width: 650px; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"></p>\n<p style="text-align: center; color: #888; font-size: 13px; margin-top: 8px; margin-bottom: 20px;">图：' + images[1][2] + r'</p>\n\2',
            content,
            count=1
        )

    # 插入点3：实际案例标题之后
    if len(images) > 2:
        content = re.sub(
            r'(<h2[^>]*>实际案例：multicc 项目</h2>)',
            r'\1\n\n<p style="text-align: center;"><img src="../' + os.path.basename(images[2][1]) + r'" alt="实际应用案例" style="max-width: 650px; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"></p>\n<p style="text-align: center; color: #888; font-size: 13px; margin-top: 8px; margin-bottom: 20px;">图：' + images[2][2] + r'</p>',
            content,
            count=1
        )

    # 生成专业的HTML文档
    from datetime import datetime
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* 全局样式 */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Microsoft YaHei', sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f8f9fa;
            margin: 0;
            padding: 20px;
        }}

        /* 主容器 - 限制阅读宽度，提升阅读体验 */
        .article-container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px 50px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        }}

        /* 标题样式 */
        h1 {{
            font-size: 28px;
            font-weight: bold;
            color: #0e639c;
            text-align: center;
            margin: 0 0 30px 0;
            padding-bottom: 20px;
            border-bottom: 3px solid #0e639c;
            line-height: 1.4;
        }}

        h2 {{
            font-size: 22px;
            color: #0e639c;
            margin: 40px 0 20px 0;
            padding-left: 15px;
            border-left: 5px solid #0e639c;
            font-weight: 600;
        }}

        h3 {{
            font-size: 18px;
            color: #0e639c;
            margin: 25px 0 12px 0;
            font-weight: 600;
        }}

        /* 段落样式 */
        p {{
            margin-bottom: 15px;
            line-height: 1.8;
            color: #333;
        }}

        /* 图片容器 - 控制图片大小 */
        .image-container {{
            text-align: center;
            margin: 25px 0;
        }}

        .image-container img {{
            max-width: 650px;
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: block;
            margin: 0 auto;
        }}

        .image-caption {{
            text-align: center;
            color: #888;
            font-size: 13px;
            margin-top: 8px;
            margin-bottom: 20px;
        }}

        /* 表格样式 */
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}

        th {{
            border: 1px solid #ddd;
            padding: 12px;
            background-color: #0e639c;
            color: white;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            border: 1px solid #ddd;
            padding: 12px;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        /* 代码块样式 */
        .code-block {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            overflow-x: auto;
            font-family: Consolas, Monaco, 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
        }}

        /* 列表样式 */
        ul, ol {{
            margin-left: 25px;
            margin-bottom: 15px;
        }}

        li {{
            margin-bottom: 8px;
            line-height: 1.7;
        }}

        /* 行内代码样式 */
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: Consolas, Monaco, 'Courier New', monospace;
            font-size: 0.9em;
        }}

        /* 页脚样式 */
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 14px;
        }}

        /* 响应式 */
        @media (max-width: 768px) {{
            .article-container {{
                padding: 20px;
            }}

            h1 {{
                font-size: 24px;
            }}

            h2 {{
                font-size: 20px;
            }}

            .image-container img {{
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="article-container">
        <h1>{title}</h1>

{content}

        <div class="footer">
            生成时间：{datetime.now().strftime('%Y-%m-%d')}<br>
            适用工具：Claude Code (claude.ai/code)
        </div>
    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n专业版HTML已保存: {output_path}")


def main():
    """主函数"""
    print("=" * 80)
    print("     Claude Code 记忆文件说明 - 配图版生成器（资深编辑优化版v2）")
    print("=" * 80)
    print()

    # 文件路径
    script_dir = Path(__file__).parent
    html_file = script_dir / "claude-code-memory-files.html"

    if not html_file.exists():
        print(f"错误: 找不到文件 {html_file}")
        return

    # 提取文章内容
    print("正在读取原始HTML文件...")
    article_data = extract_article_content_from_html(html_file)

    if not article_data:
        print("错误: 无法提取文章内容")
        return

    print(f"标题: {article_data['title']}")
    print()

    # 创建生成器实例
    gen = ToutiaoArticleGenerator()

    # 生成针对性配图
    images = generate_targeted_images(gen)

    if len(images) < 3:
        print(f"\n警告: 只生成了 {len(images)}/3 张配图")

    # 生成优化版HTML
    output_html = script_dir / "claude-code-memory-files-toutiao.html"
    create_optimized_html(
        title=article_data['title'],
        content=article_data['content'],
        images=images,
        output_path=output_html
    )

    print()
    print("=" * 80)
    print("[OK] 优化完成!")
    print(f"输出文件: {output_html}")
    print()
    print("专业版特性:")
    print("  - 图片最大宽度限制为650px，与文字比例协调")
    print("  - 主容器宽度800px，符合最佳阅读体验")
    print("  - 修复了段落嵌套和样式重复问题")
    print("  - 添加了响应式设计，移动端友好")
    print()
    print("配图说明:")
    print("  图1 - 双记忆系统概念：开篇简介后，建立直观认知")
    print("  图2 - 项目文档可视化：对比表格后，深化CLAUDE.md理解")
    print("  图3 - 实际应用案例：multicc案例部分，理论联系实际")
    print()
    print("发布步骤:")
    print(f"1. 用浏览器打开 {output_html.name}")
    print("2. 全选并复制内容 (Ctrl+A, Ctrl+C)")
    print("3. 粘贴到今日头条编辑器")
    print("4. 上传对应的图片文件")
    print("=" * 80)


if __name__ == '__main__':
    main()
