#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新 tool_manager.py 添加头条Web应用配置"""

file_path = 'tool_manager.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''    "article/": {
        "toutiao_article_generator.py": {
            "description": "生成器 - 今日头条文章生成器 v3.1 (支持主题生成+草稿完善+智能配图)",
            "needs_input": True,
            "input_fields": [
                {"name": "mode", "label": "生成模式", "type": "select", "options": [
                    {"value": "1", "label": "主题生成 (AI从零开始)"},
                    {"value": "2", "label": "草稿完善 (AI优化您的草稿)"}
                ], "default": "1"},
                {"name": "theme", "label": "文章主题 (模式1)", "type": "text", "placeholder": "如: 过年回老家", "required": False},
                {"name": "draft", "label": "草稿文件路径 (模式2)", "type": "text", "placeholder": "如: article/draft.txt 或 C:\\\\path\\\\to\\\\draft.txt", "required": False},
                {"name": "length", "label": "文章长度", "type": "select", "options": [
                    {"value": "1500", "label": "1500字 (快速阅读)"},
                    {"value": "2000", "label": "2000字 (标准长度)"},
                    {"value": "2500", "label": "2500字 (深度文章)"}
                ], "default": "2000"},
                {"name": "style", "label": "文风描述", "type": "text", "placeholder": "如: 汪曾祺风格、鲁迅杂文风、温柔婉约、幽默风趣、严谨学术等", "required": False},
                {"name": "generate_images", "label": "生成配图", "type": "select", "options": [
                    {"value": "y", "label": "是 (生成3张配图)"},
                    {"value": "n", "label": "否 (仅生成文章)"}
                ], "default": "y"},
                {"name": "image_style", "label": "配图风格", "type": "select", "options": [
                    {"value": "auto", "label": "自动 (AI智能选择)"},
                    {"value": "realistic", "label": "真实照片"},
                    {"value": "artistic", "label": "艺术创作"},
                    {"value": "cartoon", "label": "卡通插画"},
                    {"value": "technical", "label": "技术图表 (流程图/架构图)"}
                ], "default": "auto"},
            ]
        },
        "article_review_and_revision.py": "工具 - 文章审校和修订工具 (AI辅助文章优化)",'''

new_code = '''    "article/": {
        "toutiao_web_app.py": {
            "description": "📝 今日头条文章生成器 Web版 (独立Web应用，支持主题生成+草稿完善+智能配图)⭐⭐⭐",
            "is_web_service": True,
            "port": 5010,
            "url": "http://localhost:5010"
        },
        "toutiao_article_generator.py": {
            "description": "生成器 - 今日头条文章生成器 v3.1 (命令行版)",
            "needs_input": True,
            "input_fields": [
                {"name": "mode", "label": "生成模式", "type": "select", "options": [
                    {"value": "1", "label": "主题生成 (AI从零开始)"},
                    {"value": "2", "label": "草稿完善 (AI优化您的草稿)"}
                ], "default": "1"},
                {"name": "theme", "label": "文章主题 (模式1)", "type": "text", "placeholder": "如: 过年回老家", "required": False},
                {"name": "draft", "label": "草稿文件路径 (模式2)", "type": "text", "placeholder": "如: article/draft.txt 或 C:\\\\path\\\\to\\\\draft.txt", "required": False},
                {"name": "length", "label": "文章长度", "type": "select", "options": [
                    {"value": "1500", "label": "1500字 (快速阅读)"},
                    {"value": "2000", "label": "2000字 (标准长度)"},
                    {"value": "2500", "label": "2500字 (深度文章)"}
                ], "default": "2000"},
                {"name": "style", "label": "文风描述", "type": "text", "placeholder": "如: 汪曾祺风格、鲁迅杂文风、温柔婉约、幽默风趣、严谨学术等", "required": False},
                {"name": "generate_images", "label": "生成配图", "type": "select", "options": [
                    {"value": "y", "label": "是 (生成3张配图)"},
                    {"value": "n", "label": "否 (仅生成文章)"}
                ], "default": "y"},
                {"name": "image_style", "label": "配图风格", "type": "select", "options": [
                    {"value": "auto", "label": "自动 (AI智能选择)"},
                    {"value": "realistic", "label": "真实照片"},
                    {"value": "artistic", "label": "艺术创作"},
                    {"value": "cartoon", "label": "卡通插画"},
                    {"value": "technical", "label": "技术图表 (流程图/架构图)"}
                ], "default": "auto"},
            ]
        },
        "article_review_and_revision.py": "工具 - 文章审校和修订工具 (AI辅助文章优化)",'''

if old_code in content:
    new_content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("NOT_FOUND")
    # 检查是否已经修改
    if "toutiao_web_app.py" in content:
        print("ALREADY_MODIFIED")
