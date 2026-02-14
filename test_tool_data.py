# -*- coding: utf-8 -*-
from tool_manager import TOOL_DESCRIPTIONS
import json

tool = TOOL_DESCRIPTIONS['article/']['toutiao_article_generator.py']
print("=== 今日头条文章生成器配置 ===\n")
print(f"字段数量: {len(tool['input_fields'])}\n")
for i, field in enumerate(tool['input_fields'], 1):
    print(f"{i}. {field['label']}")
    print(f"   类型: {field['type']}")
    if 'placeholder' in field:
        print(f"   占位符: {field['placeholder']}")
    if 'options' in field:
        print(f"   选项: {len(field['options'])}个")
    print()

# 验证JSON序列化
try:
    json_str = json.dumps(tool, ensure_ascii=False, indent=2)
    print("\n=== JSON序列化测试通过 ===")
except Exception as e:
    print(f"\n=== JSON序列化失败: {e} ===")
