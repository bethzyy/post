#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""补充图片到已生成的文章"""

import os
import re
from pathlib import Path
from datetime import datetime

# 找到最新的HTML文件
html_files = list(Path(".").glob("汪曾祺风格_完整版_*.html"))
if not html_files:
    print("[错误] 未找到HTML文件")
    exit(1)

latest_html = max(html_files, key=lambda f: f.stat().st_mtime)
print(f"[找到] HTML文件: {latest_html.name}")

# 读取HTML内容
with open(latest_html, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到现有的图片
existing_images = [
    "文章配图1_主场景_20260130_154745.jpg",
    "文章配图2_细节特写_20260130_154913.jpg",
    "文章配图3_生活场景_20260130_155115.jpg"
]

# 检查图片是否存在
available_images = []
for img_name in existing_images:
    img_path = Path(img_name)
    if img_path.exists():
        available_images.append(img_name)
        print(f"[图片] 找到: {img_name}")
    else:
        print(f"[警告] 图片不存在: {img_name}")

if not available_images:
    print("[错误] 没有可用的图片")
    exit(1)

# 在HTML中插入图片
# 找到content div的开始位置
content_match = re.search(r'<div class="content">(.+?)</div>', html_content, re.DOTALL)
if not content_match:
    print("[错误] 无法找到content区域")
    exit(1)

content_section = content_match.group(1)
paragraphs = content_section.split('</p>')

# 确定图片插入位置
new_content = ""

for i, para in enumerate(paragraphs):
    new_content += para

    # 在第1段后插入主场景图
    if i == 0 and len(available_images) >= 1:
        new_content += f"""
            <div class="image-container hero-image">
                <img src="{available_images[0]}" alt="未来图书馆主场景 - 融合传统与现代的知识空间">
                <div class="image-caption">未来图书馆主场景 - 融合传统与现代的知识空间</div>
            </div>
        """

    # 在第6段后插入细节图（右侧浮动）
    elif i == 5 and len(available_images) >= 2:
        new_content += f"""
            <div class="image-container detail-image">
                <img src="{available_images[1]}" alt="智能阅读空间 - AI赋能的知识体验">
                <div class="image-caption" style="font-size: 0.85em;">智能阅读空间 - AI赋能的知识体验</div>
            </div>
        """

    # 在第10段后插入生活场景图
    elif i == 9 and len(available_images) >= 3:
        new_content += f"""
            <div class="image-container life-image">
                <img src="{available_images[2]}" alt="文化生活空间 - 思想碰撞的线下客厅">
                <div class="image-caption">文化生活空间 - 思想碰撞的线下客厅</div>
            </div>
        """

    new_content += '</p>'

# 替换原HTML中的content部分
new_html = re.sub(
    r'<div class="content">(.+?)</div>',
    f'<div class="content">{new_content}</div>',
    html_content,
    flags=re.DOTALL
)

# 更新meta信息中的配图数量
new_html = re.sub(
    r'配图: \d+张',
    f'配图: {len(available_images)}张',
    new_html
)

# 保存更新后的HTML
output_html = latest_html.name.replace('.html', '_含图片.html')
output_path = Path(output_html)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\n[成功] 更新后的HTML已保存: {output_html}")
print(f"[配图] 添加了 {len(available_images)} 张真实照片风格配图")

# 自动打开
try:
    import webbrowser
    webbrowser.open(f'file:///{os.path.abspath(output_path)}'.replace('\\', '/'))
    print(f"[成功] 已在浏览器中打开预览")
except:
    print(f"[提示] 请手动打开: {output_path}")

print("\n图片插入位置说明:")
print("  ✓ 开篇主场景图 - 营造沉浸式氛围")
print("  ✓ 中段细节图 - 右侧浮动，配合AI技术描述")
print("  ✓ 尾段生活图 - 呼应'线下客厅'概念")
print("="*80)
