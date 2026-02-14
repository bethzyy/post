# -*- coding: utf-8 -*-
"""
测试临时文件编码
"""
import tempfile
import sys

# 模拟工具管理器创建临时文件
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
    f.write("1\n")
    f.write("春季饮食养生\n")
    f.write("2000\n")
    f.write("n\n")
    temp_file = f.name

print(f"临时文件: {temp_file}")

# 读取临时文件
with open(temp_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print("文件内容:")
    print(repr(content))

# 模拟脚本读取
with open(temp_file, 'r', encoding='utf-8') as f:
    line1 = f.readline()
    print(f"\n第1行: {repr(line1)}")

    line2 = f.readline()
    print(f"第2行: {repr(line2)}")
    print(f"第2行 stripped: {repr(line2.strip())}")

    # 检查编码
    try:
        line2.encode('utf-8')
        print("第2行编码正常")
    except UnicodeEncodeError as e:
        print(f"第2行编码错误: {e}")
        # 清理代理字符
        cleaned = line2.encode('utf-8', errors='ignore').decode('utf-8')
        print(f"清理后: {repr(cleaned)}")

import os
os.unlink(temp_file)
