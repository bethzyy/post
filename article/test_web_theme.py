# -*- coding: utf-8 -*-
"""
测试Web模式逻辑
"""
import argparse
import os

# 解析命令行参数
parser = argparse.ArgumentParser(description='今日头条文章生成器 v3.1')
parser.add_argument('--mode', choices=['theme', 'draft'], help='生成模式')
parser.add_argument('--theme', help='文章主题(模式=theme时使用)')
parser.add_argument('--length', type=int, default=2000, help='目标字数')
parser.add_argument('--images', choices=['y', 'n'], default='y', help='是否生成配图')
parser.add_argument('--image-style', default='realistic', help='配图风格')

# 解析命令行参数
args = parser.parse_args()

# 确定使用哪个来源
web_mode = None
web_theme = None
web_length = None

# 命令行参数优先
if args.mode:
    web_mode = 1 if args.mode == 'theme' else 2
    web_theme = args.theme
    web_length = args.length
    print(f"[DEBUG] 检测到命令行参数: mode={args.mode}, theme={args.theme}")
    print(f"[DEBUG] web_mode={web_mode}, web_theme={web_theme}, web_theme is None: {web_theme is None}")
else:
    print("[DEBUG] 未检测到命令行参数")

# 模拟main()函数逻辑
mode = web_mode if web_mode is not None else 1

print(f"\n[DEBUG] mode={mode}")

if mode == 1:
    print(f"[DEBUG] 进入主题生成模式")
    print(f"[DEBUG] web_theme is not None: {web_theme is not None}")
    if web_theme is not None:
        theme = web_theme
        print(f"[Web模式] 使用主题: {theme}")
    else:
        print("[ERROR] 进入交互模式!")
