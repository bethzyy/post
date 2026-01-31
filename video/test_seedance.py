#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试Seedance视频生成"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from video_generation_comparison import generate_video_with_seedance
from pathlib import Path
from datetime import datetime

print("="*80)
print("测试Seedance 1.5 Pro视频生成")
print("="*80)
print()

prompt = "A cute cat playing with a red ball, cinematic lighting, 3D animation style"
print(f"提示词: {prompt}")
print()

# 创建输出目录
output_dir = Path(__file__).parent / "video_comparison_output"
output_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = output_dir / f"Seedance_1.5_Pro_{timestamp}.mp4"

# 生成视频
result = generate_video_with_seedance(prompt, output_path)

print()
print("="*80)
print("结果:")
print("="*80)
print(f"成功: {result['success']}")
print(f"消息: {result.get('message', '')}")

if result['success']:
    print(f"文件: {result['file_path']}")
    print(f"大小: {result['file_size']} bytes")
else:
    print(f"错误: {result.get('error', '')}")

print()
print("="*80)
