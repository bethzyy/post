# -*- coding: utf-8 -*-
"""
测试stdin读取的编码问题
"""
import tempfile
import subprocess
import sys

# 创建临时文件
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
    f.write("1\n")
    f.write("春季饮食养生\n")
    f.write("2000\n")
    f.write("n\n")
    temp_file = f.name

print(f"临时文件: {temp_file}", file=sys.stderr)

# 测试脚本
test_script = """
import sys

print(f"isatty: {sys.stdin.isatty()}", file=sys.stderr)

line1 = sys.stdin.readline()
print(f"Line1: {repr(line1)}", file=sys.stderr)

line2 = sys.stdin.readline()
print(f"Line2: {repr(line2)}", file=sys.stderr)

try:
    line2.encode('utf-8')
    print("Line2编码正常", file=sys.stderr)
except UnicodeEncodeError as e:
    print(f"Line2编码错误: {e}", file=sys.stderr)
    cleaned = line2.encode('utf-8', errors='ignore').decode('utf-8')
    print(f"清理后: {repr(cleaned)}", file=sys.stderr)

theme = line2.strip()
print(f"主题: {repr(theme)}", file=sys.stderr)
"""

# 写入测试脚本
with open('test_stdin_reader.py', 'w', encoding='utf-8') as f:
    f.write(test_script)

# 通过stdin读取
with open(temp_file, 'r', encoding='utf-8') as stdin_file:
    result = subprocess.run(
        [sys.executable, 'test_stdin_reader.py'],
        stdin=stdin_file,
        capture_output=True,
        text=False,
        encoding=None
    )

print("STDOUT:")
print(result.stdout.decode('utf-8', errors='replace'))
print("\nSTDERR:")
print(result.stderr.decode('utf-8', errors='replace'))

import os
os.unlink(temp_file)
os.unlink('test_stdin_reader.py')
