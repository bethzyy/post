# -*- coding: utf-8 -*-
"""
简化测试主题读取
"""
import sys

def get_mode():
    if not sys.stdin.isatty():
        mode = sys.stdin.readline().strip()
        print(f"[DEBUG] Mode: {mode}", file=sys.stderr)
        return int(mode) if mode else 1
    return 1

def get_theme():
    if not sys.stdin.isatty():
        theme = sys.stdin.readline().strip()
        print(f"[DEBUG] Theme: {theme}", file=sys.stderr)
        return theme
    return "默认主题"

def get_length():
    if not sys.stdin.isatty():
        length = sys.stdin.readline().strip()
        print(f"[DEBUG] Length: {length}", file=sys.stderr)
        return int(length) if length else 2000
    return 2000

mode = get_mode()
print(f"模式: {mode}\n")

theme = get_theme()
print(f"主题: {theme}\n")

length = get_length()
print(f"字数: {length}\n")

print(f"\n生成文章: 主题='{theme}', 字数={length}")
