# -*- coding: utf-8 -*-
"""测试 v9 图片生成器集成"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import urllib.request
import json

print("=" * 60)
print("测试 1: 检查 API 返回的 v9 工具描述")
print("=" * 60)

url = "http://localhost:5000/api/tools"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))

    found = False
    for cat in data['tools']:
        for t in data['tools'][cat]:
            if 'v9' in t['filename'] and 'standalone' in t['filename']:
                found = True
                print(f"找到 v9 工具:")
                print(f"  filename: {t['filename']}")
                print(f"  description: {t['description']}")

                # 检查描述是否正确
                if 'AI图像生成器' in t['description']:
                    print("  [PASS] 描述包含 'AI图像生成器'")
                else:
                    print("  [FAIL] 描述不包含 'AI图像生成器'")

                if 'V9.1' in t['description']:
                    print("  [PASS] 描述包含 'V9.1'")
                else:
                    print("  [FAIL] 描述不包含 'V9.1'")

    if not found:
        print("[FAIL] 未找到 v9 工具")

except Exception as e:
    print(f"[ERROR] API 请求失败: {e}")

print("\n" + "=" * 60)
print("测试 2: 检查运行 v9 工具")
print("=" * 60)

try:
    # 发送运行请求
    run_url = "http://localhost:5000/api/run"
    data = json.dumps({"filename": "picture/standalone_image_generator_v9.py"}).encode('utf-8')
    req = urllib.request.Request(run_url, data=data, headers={'Content-Type': 'application/json'})

    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read().decode('utf-8'))

    print(f"运行结果: {result}")

    if result.get('success'):
        print("[PASS] 工具启动成功")
        if 'url' in result:
            print(f"  URL: {result['url']}")
    else:
        print(f"[FAIL] 工具启动失败: {result.get('error', 'Unknown error')}")

except Exception as e:
    print(f"[ERROR] 运行请求失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
