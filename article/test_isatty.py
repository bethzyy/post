# -*- coding: utf-8 -*-
"""
测试stdin.isatty()
"""
import sys

print(f"isatty: {sys.stdin.isatty()}", file=sys.stderr)
print(f"stdin类型: {type(sys.stdin)}", file=sys.stderr)

line = sys.stdin.readline()
print(f"读取到: '{line}'", file=sys.stderr)
print(f"stripped: '{line.strip()}'", file=sys.stderr)
