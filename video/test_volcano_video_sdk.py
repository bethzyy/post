#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试火山引擎Seedance视频生成API使用OpenAI SDK"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from config import get_volcano_client
import requests

print("="*80)
print("测试火山引擎Seedance视频生成 (使用OpenAI SDK)")
print("="*80)
print()

# 获取火山引擎客户端
client = get_volcano_client()

if not client:
    print("错误: 无法获取火山引擎客户端")
    exit(1)

print(f"客户端类型: {type(client)}")
print(f"Base URL: {client.base_url}")
print()

# 测试视频生成
try:
    print("尝试调用视频生成API...")
    print("模型: seedance-1.0-pro")
    print("提示词: A red apple on a wooden table")
    print()

    # 方法1: 尝试使用client.videos.generate (如果存在)
    try:
        response = client.videos.generate(
            model="seedance-1.0-pro",
            prompt="A red apple on a wooden table",
            extra_body={
                "video": {
                    "duration": "5s",
                    "resolution": "720p"
                }
            }
        )
        print(f"✅ 成功! response类型: {type(response)}")
        print(f"Response: {response}")
    except AttributeError as e:
        print(f"❌ client.videos.generate 不存在: {e}")

        # 方法2: 尝试使用client.video.create
        try:
            response = client.video.create(
                model="seedance-1.0-pro",
                prompt="A red apple on a wooden table"
            )
            print(f"✅ 成功! response类型: {type(response)}")
            print(f"Response: {response}")
        except AttributeError as e2:
            print(f"❌ client.video.create 不存在: {e2}")

            # 方法3: 尝试使用images.generate作为参考
            print("\n测试: images.generate是否可用...")
            try:
                response = client.images.generate(
                    model="doubao-seedream-4-5-251128",
                    prompt="A red apple",
                    size="1024x1024"
                )
                print(f"✅ images.generate可用")
                print(f"Response: {response}")
            except Exception as e3:
                print(f"❌ images.generate错误: {e3}")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
print("检查客户端可用的方法")
print("="*80)

# 列出客户端的所有方法
methods = [m for m in dir(client) if not m.startswith('_')]
print(f"可用方法 ({len(methods)}):")
for method in sorted(methods):
    print(f"  - {method}")
