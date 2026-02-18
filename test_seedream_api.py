# -*- coding: utf-8 -*-
"""测试 Seedream 4.0 API 直接调用"""
import sys
import os

# 加载配置
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import Config

import urllib.request
import json
import base64

def test_seedream_api(model_version="doubao-seedream-4-0-250828"):
    """直接测试 Seedream API"""
    print("="*60)
    print(f"测试 Seedream API: {model_version}")
    print("="*60)

    api_key = Config.VOLCANO_API_KEY
    base_url = Config.VOLCANO_BASE_URL

    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"Base URL: {base_url}")

    # 构建请求
    url = f"{base_url}/images/generations"
    print(f"Full URL: {url}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_version,
        "prompt": "一只可爱的猫咪，卡通风格",
        "size": "1024x1024",
        "response_format": "url"
    }

    print(f"\nRequest payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    print(f"\nSending request...")

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n[SUCCESS] Response received!")
            print(f"Response keys: {result.keys()}")

            if 'data' in result:
                for i, img_data in enumerate(result['data']):
                    if 'url' in img_data:
                        print(f"  Image {i+1} URL: {img_data['url'][:80]}...")
                    if 'b64_json' in img_data:
                        print(f"  Image {i+1} base64 length: {len(img_data['b64_json'])}")

            return True, result

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"\n[ERROR] HTTP {e.code}: {e.reason}")
        print(f"Error body: {error_body}")
        return False, error_body

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        return False, str(e)


def test_seedream_with_openai_client(model_version="doubao-seedream-4-0-250828"):
    """使用 OpenAI 客户端测试"""
    print("\n" + "="*60)
    print(f"使用 OpenAI 客户端测试: {model_version}")
    print("="*60)

    try:
        from openai import OpenAI

        client = OpenAI(
            base_url=Config.VOLCANO_BASE_URL,
            api_key=Config.VOLCANO_API_KEY
        )

        print("Sending request via OpenAI client...")

        response = client.images.generate(
            model=model_version,
            prompt="一只可爱的狗狗，卡通风格",
            size="1024x1024",
            n=1,
            response_format="url"
        )

        print("\n[SUCCESS] Response received!")
        print(f"Response type: {type(response)}")

        if hasattr(response, 'data'):
            for i, img in enumerate(response.data):
                print(f"  Image {i+1} URL: {img.url[:80]}...")

        return True, response

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response}")
        return False, str(e)


if __name__ == "__main__":
    # 测试 1: 直接 HTTP 调用
    test_seedream_api("doubao-seedream-4-0-250828")

    # 测试 2: 使用 OpenAI 客户端
    test_seedream_with_openai_client("doubao-seedream-4-0-250828")

    print("\n" + "="*60)
    print("测试完成")
    print("="*60)
