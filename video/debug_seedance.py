#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试Seedance API响应"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

import requests
import json
import time

volcano_api_key = os.environ.get('VOLCANO_API_KEY')

print("="*80)
print("调试Seedance API")
print("="*80)
print()

# 创建任务
api_url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

headers = {
    'Authorization': f'Bearer {volcano_api_key}',
    'Content-Type': 'application/json'
}

payload = {
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
        {
            "type": "text",
            "text": "A cute cat playing with a red ball"
        }
    ],
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 5,
    "watermark": False,
    "generate_audio": True,
    "draft": False
}

print("1. 创建任务...")
response = requests.post(api_url, json=payload, headers=headers, timeout=60)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    task_id = result.get('id')
    print(f"任务ID: {task_id}")
    print(f"完整响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"错误: {response.text}")
    exit(1)

print()
print("2. 查询任务状态...")

# 轮询查询
status_url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"

for i in range(60):
    time.sleep(5)

    status_response = requests.get(status_url, headers=headers, timeout=30)
    print(f"\n第{i+1}次查询 (状态码: {status_response.status_code})")

    if status_response.status_code == 200:
        status_result = status_response.json()
        status = status_result.get('status', 'unknown')
        print(f"状态: {status}")

        if status == 'succeeded':
            print("\n成功! 完整响应:")
            print(json.dumps(status_result, indent=2, ensure_ascii=False))
            break
        elif status == 'failed':
            print("\n失败! 完整响应:")
            print(json.dumps(status_result, indent=2, ensure_ascii=False))
            break
        elif i % 6 == 0:  # 每30秒打印一次完整响应
            print("当前完整响应:")
            print(json.dumps(status_result, indent=2, ensure_ascii=False))
    else:
        print(f"查询失败: {status_response.text}")

print()
print("="*80)
