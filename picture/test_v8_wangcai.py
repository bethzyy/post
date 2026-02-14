#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试V8版本使用旺财.jpg进行图生图
"""
import sys
from pathlib import Path
import base64
import requests
import json

def test_v8_with_wangcai():
    """测试V8使用旺财.jpg进行图生图"""
    print("="*80)
    print("V8图生图测试 - 使用旺财.jpg")
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
    api_url = "http://localhost:5008/api/generate-image"

    payload = {
        "mode": "reference",
        "reference_image": image_base64,
        "style": "guofeng_shuimo",
        "theme": ""
    }

    print("[发送请求] 开始图生图生成...")
    print(f"[API地址] {api_url}")
    print(f"[风格] 国风水墨")
    print()

    try:
        response = requests.post(api_url, json=payload, timeout=180)

        print(f"[响应状态] HTTP {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            if result.get('success'):
                print()
                print("="*80)
                print("[✓] 生成成功!")
                print(f"  模型: {result.get('model', 'Unknown')}")
                print(f"  风格: {result.get('style', 'Unknown')}")
                print(f"  文件: {result.get('image_filename', 'Unknown')}")

                if result.get('reference_description'):
                    print(f"  参考图片描述: {result['reference_description'][:100]}...")

                # 保存生成的图片
                if result.get('image_base64'):
                    output_path = Path("test_wangcai_generated.png")
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(result['image_base64']))
                    print(f"  已保存: {output_path}")

                print("="*80)
            else:
                print()
                print("="*80)
                print("[✗] 生成失败")
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
    test_v8_with_wangcai()
