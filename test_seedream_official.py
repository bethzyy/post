# -*- coding: utf-8 -*-
"""测试 Seedream 4.0 API - 使用官网示例"""
import sys
import os

# 加载配置
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import Config

def test_seedream_official():
    """按照官网示例测试 Seedream API"""
    print("="*60)
    print("测试 Seedream 4.0 API - 官网示例方式")
    print("="*60)

    try:
        from openai import OpenAI

        # 初始化Ark客户端
        client = OpenAI(
            base_url=Config.VOLCANO_BASE_URL,
            api_key=Config.VOLCANO_API_KEY
        )

        print(f"Base URL: {Config.VOLCANO_BASE_URL}")
        print(f"API Key: {Config.VOLCANO_API_KEY[:10]}...{Config.VOLCANO_API_KEY[-10:]}")
        print()

        # 测试 Seedream 4.0
        print("正在调用 Seedream 4.0...")
        imagesResponse = client.images.generate(
            model="doubao-seedream-4-0-250828",
            prompt="一只可爱的猫咪，卡通风格",
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        print("\n[SUCCESS] 图片生成成功!")
        print(f"图片URL: {imagesResponse.data[0].url}")

        # 下载图片
        import requests
        img_response = requests.get(imagesResponse.data[0].url, timeout=60)
        if img_response.status_code == 200:
            output_path = "test_seedream_output.png"
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
            print(f"图片已保存到: {output_path}")
        else:
            print(f"下载图片失败: HTTP {img_response.status_code}")

        return True

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_seedream_official()
