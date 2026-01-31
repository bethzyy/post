#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查火山引擎client.videos对象的方法"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from config import get_volcano_client

print("="*80)
print("检查火山引擎OpenAI客户端的videos对象")
print("="*80)

client = get_volcano_client()

# 检查videos对象
print("\n1. client.videos对象:")
print(f"   类型: {type(client.videos)}")
print(f"   属性和方法:")
if hasattr(client.videos, '__dict__'):
    for attr in dir(client.videos):
        if not attr.startswith('_'):
            print(f"     - {attr}")

# 检查images对象作为对比
print("\n2. client.images对象:")
print(f"   类型: {type(client.images)}")
print(f"   属性和方法:")
if hasattr(client.images, '__dict__'):
    for attr in dir(client.images):
        if not attr.startswith('_'):
            print(f"     - {attr}")

# 尝试找到videos相关的方法
print("\n3. 查找所有video相关的方法:")
all_attrs = dir(client)
video_attrs = [attr for attr in all_attrs if 'video' in attr.lower()]
print(f"   找到 {len(video_attrs)} 个:")
for attr in video_attrs:
    print(f"     - {attr}")

# 测试直接使用http
print("\n4. 测试HTTP调用视频生成API:")
import requests
import json

volcano_api_key = os.environ.get('VOLCANO_API_KEY')
headers = {
    'Authorization': f'Bearer {volcano_api_key}',
    'Content-Type': 'application/json'
}

# 尝试不同的路径
paths = [
    '/videos/generations',
    '/videos',
    '/video/generations',
    '/video',
]

base_url = "https://ark.cn-beijing.volces.com/api/v3"

for path in paths:
    url = base_url + path
    print(f"\n   测试: {url}")

    try:
        # 先尝试GET
        response = requests.get(url, headers=headers, timeout=10)
        print(f"     GET: {response.status_code}")

        if response.status_code != 404:
            print(f"     Response: {response.text[:200]}")
    except Exception as e:
        print(f"     Error: {str(e)[:100]}")
