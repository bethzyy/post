#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""完整测试视频生成对比工具"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

# 模拟input
prompt = "A beautiful sunset over the ocean with birds flying"

# 临时替换input函数
import video_generation_comparison
original_input = video_generation_comparison.input
video_generation_comparison.input = lambda x: prompt

# 运行主函数
try:
    video_generation_comparison.main()
finally:
    video_generation_comparison.input = original_input
