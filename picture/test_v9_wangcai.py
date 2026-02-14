#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试V9版本使用旺财.jpg进行图生图 - 简化版
"""
import sys
from pathlib import Path
import base64
import requests
import json

# 设置控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_v9_with_wangcai():
    """测试V9使用旺财.jpg进行图生图"""
    print("="*80)
    print("V9图生图测试 - 使用旺财.jpg (简化版)")
    print("="*80)

    # 读取参考图片
    wangcai_path = Path("C:/D/CAIE_tool/AIGC/旺财.jpg")

    if not wangcai_path.exists():
        print(f"[错误] 找不到参考图片: {wangcai_path}")
        return

    print(f"[参考图片] {wangcai_path}")
    print(f"[文件大小] {wangcai_path.stat().st_size / 1024:.1f} KB")
    print()

    # 编码为base64
    with open(wangcai_path, 'rb') as f:
        image_data = f.read()

    image_base64 = base64.b64encode(image_data).decode('utf-8')
    print(f"[Base64大小] {len(image_base64) / 1024:.1f} KB")
    print()

    # 构建API请求
    api_url = "http://localhost:5009/api/generate-image"

    payload = {
        "mode": "reference",
        "reference_image": image_base64,
        "style": "guofeng_shuimo",
        "theme": ""
    }

    print("[发送请求] 开始图生图生成...")
    print(f"[API地址] {api_url}")
    print(f"[风格] 国风水墨")
    print(f"[V9特点] 即梦AI自动识别参考图片内容")
    print()

    try:
        response = requests.post(api_url, json=payload, timeout=180)

        print(f"[响应状态] HTTP {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            if result.get('success'):
                print()
                print("="*80)
                print("[成功] 生成成功!")
                print(f"  模型: {result.get('model', 'Unknown')}")
                print(f"  风格: {result.get('style', 'Unknown')}")
                print(f"  文件: {result.get('image_filename', 'Unknown')}")
                print(f"  描述: {result.get('reference_description', 'Unknown')}")

                # 保存生成的图片
                if result.get('image_base64'):
                    output_path = Path("test_wangcai_v9_generated.png")
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(result['image_base64']))
                    print(f"  已保存: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")

                print("="*80)
            else:
                print()
                print("="*80)
                print("[失败] 生成失败")
                print(f"  错误: {result.get('error', 'Unknown error')}")
                print("="*80)
        else:
            print(f"[错误] HTTP {response.status_code}")
            print(f"  响应: {response.text[:500]}")

    except requests.exceptions.Timeout:
        print("[错误] 请求超时 (180秒)")
    except Exception as e:
        print(f"[错误] {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_v9_with_wangcai()
