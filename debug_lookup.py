# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
from tool_manager import TOOL_DESCRIPTIONS

BASE_DIR = Path('.')
py_file = BASE_DIR / "picture" / "standalone_image_generator_v9.py"
rel_path = py_file.relative_to(BASE_DIR)
sub_dir = str(rel_path.parent).replace('\\', '/') + '/'
filename = py_file.name

print(f"sub_dir: [{sub_dir}]")
print(f"filename: [{filename}]")

# 检查 TOOL_DESCRIPTIONS 的 key
print(f"TOOL_DESCRIPTIONS keys: {list(TOOL_DESCRIPTIONS.keys())}")

# 检查 picture/ 下的内容
pic_config = TOOL_DESCRIPTIONS.get(sub_dir, {})
print(f"pic_config type: {type(pic_config)}")
print(f"pic_config keys: {list(pic_config.keys()) if isinstance(pic_config, dict) else 'not dict'}")

# 检查是否能找到
tool_config = pic_config.get(filename)
print(f"tool_config found: {tool_config is not None}")
if tool_config:
    print(f"tool_config description: {tool_config.get('description', 'N/A')}")
