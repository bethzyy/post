#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 toutiao_web_app.py - 移除 print 中的 emoji 避免 GBK 编码错误"""

file_path = 'article/toutiao_web_app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 main 函数中的 print 语句
old_main = '''    print("=" * 80)
    print("                    今日头条文章生成器 - Web版 V1.0")
    print("=" * 80)
    print()
    print("启动Web服务器: http://localhost:5010")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  💡 主题生成 - 输入主题，AI从零开始写作")
    print("  ✏️  草稿完善 - 粘贴草稿，AI润色优化")
    print("  🖼️  智能配图 - 自动生成3张配图")
    print("  📄 多种格式 - 支持HTML和Markdown输出")
    print("=" * 80)
    print()'''

new_main = '''    print("=" * 80)
    print("                    今日头条文章生成器 - Web版 V1.0")
    print("=" * 80)
    print()
    print("启动Web服务器: http://localhost:5010")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  [1] 主题生成 - 输入主题，AI从零开始写作")
    print("  [2] 草稿完善 - 选择草稿文件，AI润色优化")
    print("  [3] 智能配图 - 自动生成3张配图")
    print("  [4] 多种格式 - 支持HTML和Markdown输出")
    print("=" * 80)
    print()'''

content = content.replace(old_main, new_main)

# 同时更新 HTML 中的草稿完善描述
old_draft_desc = '''                <div class="mode-tab" data-mode="draft" onclick="selectMode('draft')">
                    <h3>✏️ 草稿完善</h3>
                    <p>选择草稿文件，AI润色优化</p>
                </div>'''

new_draft_desc = '''                <div class="mode-tab" data-mode="draft" onclick="selectMode('draft')">
                    <h3>✏ 草稿完善</h3>
                    <p>选择草稿文件，AI润色优化</p>
                </div>'''

content = content.replace(old_draft_desc, new_draft_desc)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("SUCCESS")
