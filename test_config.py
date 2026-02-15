# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from tool_manager import get_all_tools, TOOL_DESCRIPTIONS

print("="*50)
print("TOOL_DESCRIPTIONS picture/ config:")
print("="*50)
pic_config = TOOL_DESCRIPTIONS.get('picture/', {})
for k, v in pic_config.items():
    if k == 'standalone_image_generator_v9.py':
        print(f"Found: {k}")
        print(f"Type: {type(v)}")
        if isinstance(v, dict):
            print(f"description: {v.get('description', 'N/A')}")

print("\n" + "="*50)
print("get_all_tools() result:")
print("="*50)
tools = get_all_tools()
for cat, items in tools.items():
    print(f"\nCategory: {cat}")
    for item in items:
        if 'v9' in item['filename'] or 'standalone' in item['filename']:
            desc = item.get('description', 'NO DESC')
            print(f"  FILE: {item['filename']}")
            print(f"  DESC: {desc}")
