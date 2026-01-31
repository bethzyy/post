#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""运行视频生成对比工具"""

import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# 导入工具模块
import video_generation_comparison

# 模拟用户输入
test_prompt = "A peaceful mountain landscape at sunrise, birds flying in the sky"

# 保存原始input函数
import builtins
original_input = builtins.input

# 替换input函数
builtins.input = lambda x: test_prompt

try:
    # 运行主函数
    video_generation_comparison.main()
finally:
    # 恢复原始input函数
    builtins.input = original_input
