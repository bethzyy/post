#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试正确的图生图API用法 - 使用binary_data_base64参数
参考: https://www.volcengine.com/docs/82379/1541523
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

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config

def test_correct_image2image():
    """测试使用binary_data_base64参数的正确图生图方法"""
    print("="*80)
    print("测试正确的图生图API - 使用binary_data_base64参数")
    print("="*80)
    print()

    # 读取参考图片
    wangcai_path = Path("C:/D/CAIE_tool/AIGC/旺财.jpg")

    if not wangcai_path.exists():
        print(f"[错误] 找不到参考图片: {wangcai_path}")
        return

    print(f"[参考图片] {wangcai_path}")
    print(f"[文件大小] {wangcai_path.stat().st_size / 1024:.1f} KB")
    print()

    # 读取并编码为base64
    with open(wangcai_path, 'rb') as f:
        image_data = f.read()

    image_base64 = base64.b64encode(image_data).decode('utf-8')
    print(f"[Base64大小] {len(image_base64) / 1024:.1f} KB")
    print()

    # 获取API密钥
    api_key = Config.VOLCANO_API_KEY
    if not api_key:
        print("[错误] VOLCANO_API_KEY未配置")
        return

    # 方法1: 尝试使用通用images/generations端点,但使用binary_data_base64参数
    print("[方法1] 尝试使用通用端点 + binary_data_base64参数")
    print("-" * 80)

    url = f"{Config.VOLCANO_BASE_URL}/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "doubao-seedream-4-5-251128",
        "prompt": "一只金毛犬,中国水墨画风格,传统笔墨,意境深远",
        "size": "2K",
        "response_format": "url",
        "binary_data_base64": [image_base64]  # 使用binary_data_base64而不是image_urls
    }

    print(f"[API地址] {url}")
    print(f"[模型] {payload['model']}")
    print(f"[参数] binary_data_base64 (长度: {len(image_base64)} 字符)")
    print(f"[提示词] {payload['prompt']}")
    print()

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)

        print(f"[响应状态] HTTP {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("[响应内容]")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500])

            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url')
                print()
                print(f"[图片URL] {image_url}")

                # 下载图片
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    output_path = Path("test_method1_output.png")
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"[成功] 图片已保存: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
                else:
                    print(f"[失败] 下载图片失败: HTTP {img_response.status_code}")
            else:
                print("[失败] 响应格式不符合预期")
        else:
            print(f"[失败] {response.text[:500]}")

    except Exception as e:
        print(f"[错误] {str(e)}")
        import traceback
        traceback.print_exc()

    print()
    print("="*80)

    # 方法2: 尝试查找专用的图生图端点
    print("[方法2] 尝试使用专用图生图端点")
    print("-" * 80)
    print("[提示] 根据官方文档,图生图3.0可能使用不同的端点")
    print("[建议] 需要查阅官方文档确认正确的API端点")
    print("       - 即梦图生图3.0智能参考: https://www.volcengine.com/docs/85621/1747301")
    print("       - Seedream 4.5 API参考: https://www.volcengine.com/docs/82379/1541523")
    print("       - Seedream 4.5 SDK示例: https://www.volcengine.com/docs/82379/1824121")
    print()
    print("[假设] 可能的端点格式:")
    print("  - /api/v3/images/image-to-image")
    print("  - /api/v3/images/generations/image-to-image")
    print("  - /api/v3/seedream/image-to-image")
    print()
    print("[建议] 需要实际查看官方文档或联系火山引擎技术支持获取正确的API端点")

if __name__ == "__main__":
    test_correct_image2image()
