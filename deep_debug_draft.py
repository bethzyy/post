#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
深度调试草稿路径问题
"""
import os
import json
import tempfile

# 模拟Web界面传入的参数
params_dict = {
    'mode': '2',
    'theme': '',
    'draft': 'article/draft.txt',  # 这是从Web界面传入的原始值
    'length': 2000,
    'generate_images': 'n',
    'image_style': 'realistic',
    'style': 'standard',
}

# 创建临时JSON文件(模拟Web模式)
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as f:
    json.dump(params_dict, f, ensure_ascii=False, indent=2)
    params_file = f.name

print("="*80)
print("深度调试 - 草稿路径问题")
print("="*80)
print(f"临时JSON文件: {params_file}")

# 设置环境变量(模拟Web模式)
os.environ['ARTICLE_PARAMS_JSON'] = params_file

# 读取JSON参数(模拟main_web函数)
with open(params_file, 'r', encoding='utf-8') as f:
    params = json.load(f)

# 解析draft参数
draft = params.get('draft', '')

print(f"\n[步骤1] JSON读取的draft值")
print(f"  类型: {type(draft)}")
print(f"  值: [{draft}]")
print(f"  repr: {repr(draft)}")
print(f"  长度: {len(draft)}")
print(f"  包含空白符: {draft != draft.strip()}")

# 检查当前工作目录
print(f"\n[步骤2] 工作目录检查")
print(f"  os.getcwd(): {os.getcwd()}")
print(f"  __file__: {__file__}")

# 检查路径是否存在
print(f"\n[步骤3] 路径存在性检查")
print(f"  原始路径: [{draft}]")
print(f"  os.path.exists(原始路径): {os.path.exists(draft)}")

# 尝试各种路径变换
transformations = [
    ("原始值", draft),
    ("strip后", draft.strip()),
    ("绝对路径", os.path.abspath(draft)),
    ("join(article,)", os.path.join('article', 'draft.txt')),
]

for name, path in transformations:
    exists = os.path.exists(path)
    print(f"  {name:20s}: [{path}] -> 存在: {exists}")

# 列出article目录的文件
print(f"\n[步骤4] article目录内容")
if os.path.exists('article'):
    files = os.listdir('article')
    draft_files = [f for f in files if 'draft' in f.lower()]
    print(f"  总文件数: {len(files)}")
    print(f"  包含draft的文件: {draft_files}")
    if 'draft.txt' in files:
        print(f"  draft.txt存在!")
        full_path = os.path.join('article', 'draft.txt')
        print(f"  完整路径: {full_path}")
        print(f"  完整路径存在: {os.path.exists(full_path)}")
    else:
        print(f"  draft.txt不存在!")
else:
    print(f"  article目录不存在!")

# 清理
os.remove(params_file)
print(f"\n[清理] 已删除临时文件")
print("="*80)
