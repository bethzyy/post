#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试火山引擎Seedance视频生成API"""

import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

volcano_api_key = os.environ.get('VOLCANO_API_KEY')
volcano_base_url = os.environ.get('VOLCANO_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3')

print(f"VOLCANO_BASE_URL: {volcano_base_url}")
print(f"VOLCANO_API_KEY: {volcano_api_key[:20]}..." if volcano_api_key else "未配置")
print()

# 测试不同的端点
test_endpoints = [
    f"{volcano_base_url}/videos/generations",
    f"{volcano_base_url}/video/generations",
    "https://ark.cn-beijing.volces.com/api/v3/videos/generations",
    "https://ark.cn-beijing.volces.com/api/v3/video/generations",
]

headers = {
    'Authorization': f'Bearer {volcano_api_key}',
    'Content-Type': 'application/json'
}

for endpoint in test_endpoints:
    print(f"测试端点: {endpoint}")

    try:
        # 先发送OPTIONS请求检查端点是否存在
        response = requests.options(endpoint, headers=headers, timeout=10)
        print(f"  OPTIONS: {response.status_code}")

        # 尝试POST请求
        payload = {
            "model": "seedance-1.0-pro",
            "prompt": "A red apple",
            "video": {
                "duration": "5s",
                "resolution": "720p"
            }
        }

        response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        print(f"  POST: {response.status_code}")

        if response.status_code != 404:
            print(f"  Response: {response.text[:200]}")

    except Exception as e:
        print(f"  Error: {str(e)[:100]}")

    print()
