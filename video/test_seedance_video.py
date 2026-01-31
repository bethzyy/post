#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试火山引擎Seedance视频生成使用client.videos.create"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from config import get_volcano_client

print("="*80)
print("测试火山引擎Seedance视频生成 - 使用client.videos.create")
print("="*80)
print()

client = get_volcano_client()

if not client:
    print("错误: 无法获取客户端")
    exit(1)

# 测试1: 使用create方法
print("测试1: client.videos.create")
print("-" * 80)

try:
    response = client.videos.create(
        model="seedance-1.0-pro",
        prompt="A red apple on a wooden table, cinematic lighting",
        extra_body={
            "duration": "5s",
            "resolution": "720p"
        }
    )

    print(f"✅ 成功!")
    print(f"Response类型: {type(response)}")
    print(f"Response: {response}")

    if hasattr(response, 'id'):
        print(f"视频ID: {response.id}")

    if hasattr(response, 'status'):
        print(f"状态: {response.status}")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print()

# 测试2: 使用create_and_poll方法
print("测试2: client.videos.create_and_poll")
print("-" * 80)

try:
    print("创建视频生成任务...")
    response = client.videos.create_and_poll(
        model="seedance-1.0-pro",
        prompt="A red apple on a wooden table, cinematic lighting",
        extra_body={
            "duration": "5s",
            "resolution": "720p"
        }
    )

    print(f"✅ 成功!")
    print(f"Response类型: {type(response)}")

    if hasattr(response, 'id'):
        print(f"视频ID: {response.id}")

    if hasattr(response, 'url'):
        print(f"视频URL: {response.url}")

    # 尝试下载
    if hasattr(response, 'url'):
        import requests
        print("\n下载视频...")
        video_response = requests.get(response.url, timeout=120)
        if video_response.status_code == 200:
            filename = "test_seedance_video.mp4"
            with open(filename, 'wb') as f:
                f.write(video_response.content)
            print(f"✅ 视频已保存: {filename}")
            print(f"   大小: {len(video_response.content)} bytes")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
