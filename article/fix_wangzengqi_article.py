#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复汪曾祺风格文章 - 从之前生成的HTML中提取内容"""

import re
from pathlib import Path
from datetime import datetime

# 读取之前生成的HTML文件，看看AI实际返回了什么
html_file = Path(__file__).parent / "汪曾祺风格_未来图书馆_20260130_155115.html"

if html_file.exists():
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 从HTML中提取正文内容（去掉标签）
    content_match = re.search(r'<div class="content">(.*?)</div>', html_content, re.DOTALL)
    if content_match:
        raw_content = content_match.group(1)
        # 移除HTML标签
        import html as html_module
        from html.parser import HTMLParser

        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs= True
                self.text = []
            def handle_data(self, d):
                self.text.append(d)
            def get_data(self):
                return ''.join(self.text)

        stripper = MLStripper()
        stripper.feed(raw_content)
        article_content = stripper.get_data()

        # 清理多余的空行
        lines = article_content.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        article_content = '\n\n'.join(cleaned_lines)

        print(f"[成功] 从HTML中提取了 {len(article_content)} 个字符的内容")
        print("\n提取的内容预览（前500字符）：")
        print("="*80)
        print(article_content[:500])
        print("="*80)

        # 现在重新生成正确的Markdown和HTML文件
        # 使用从debug脚本中看到的实际标题
        title = "未来图书馆：城市中的心灵栖息地"

        # 读取之前生成的配图
        import os
        image_files = []
        for f in os.listdir(Path(__file__).parent):
            if f.startswith("文章配图") and f.endswith(".jpg") and "未来图书馆" not in f:
                # 只包含本次生成的图片
                if "20260130_154" in f or "20260130_155" in f:
                    image_files.append(f)

        image_files.sort()

        # 生成新的Markdown文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        md_filename = f"汪曾祺风格_未来图书馆_修复版_{timestamp}.md"
        md_path = Path(__file__).parent / md_filename

        md_content = f"""# {title}

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**字数**: {len(article_content)}字
**风格**: 汪曾祺文风（淡雅、怀旧、有生活气息）
**配图**: {len(image_files)}张真实照片

---

## 原草稿片段

> 每次走进图书馆，那种特有的静谧和书香气息总能让我心神安宁...
> 我想象中的未来图书馆，绝不仅仅是数字化升级后的"智能书库"。它应该是一座城市的"第三空间"——不是家，不是办公室，而是属于心灵的栖息地。

---

{article_content}

---

## 配图展示

"""

        for i, img in enumerate(image_files, 1):
            img_name = os.path.basename(img)
            md_content += f"### 配图 {i}: {img_name}\n\n"
            md_content += f"![配图{i}]({img_name})\n\n"

        md_content += """
---

## 创作说明

**文风特点**:
- 语言简洁平淡，朴实有趣
- 形散神聚，富有节奏感
- 关注日常人事，体察细微
- 乐观平和的人生态度

**灵感来源**:
- 原草稿的情感基调：静谧、书香气息、心神安宁
- 汪曾祺散文的8大特点（参考[搜索结果](https://www.163.com/dy/article/ECNMDHJH0542865M.html)）
- 2026年AI时代图书馆转型思考

---

*本文由AI基于用户草稿情感，采用汪曾祺文风深度创作*
"""

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"\n[成功] Markdown文件已保存: {md_filename}")

        # 使用现有的toutiao_article_generator生成HTML
        from toutiao_article_generator import ToutiaoArticleGenerator

        generator = ToutiaoArticleGenerator()

        html_filename = f"汪曾祺风格_未来图书馆_修复版_{timestamp}.html"
        html_path = Path(__file__).parent / html_filename

        # 构建完整的图片路径
        full_image_paths = [str(Path(__file__).parent / img) for img in image_files]

        html_content = generator.create_article_html(
            title,
            article_content,
            "未来图书馆",
            images=full_image_paths
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[成功] HTML文件已保存: {html_filename}")

        # 自动打开HTML文件
        try:
            import webbrowser
            webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
            print(f"[成功] 已在浏览器中打开文章预览")
        except:
            print(f"[提示] 请手动打开HTML文件查看文章: {html_path}")

        print("\n修复完成!")
        print(f"[文件] Markdown: {md_filename}")
        print(f"[文件] HTML: {html_filename}")
        print(f"[配图] {len(image_files)}张真实照片风格配图")
        print("="*80)

    else:
        print("[错误] 无法从HTML中提取内容")
else:
    print(f"[错误] HTML文件不存在: {html_file}")
