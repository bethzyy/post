# -*- coding: utf-8 -*-
"""
测试Nano Banana模型
"""

import sys
from pathlib import Path
import base64
from PIL import Image
import io

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
from config import Config, get_antigravity_client

def test_nano_banana():
    """测试Nano Banana图片生成"""

    print("="*80)
    print("测试 Nano Banana 模型")
    print("="*80)

    client = get_antigravity_client()

    prompt = "A cute banana character wearing sunglasses, cartoon style, colorful, 1024x1024"

    print(f"\n提示词: {prompt}")
    print("\n正在调用API...")

    try:
        response = client.images.generate(
            model="nano-banana",  # 尝试使用nano banana
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        if hasattr(response, 'data') and len(response.data) > 0:
            img_data = response.data[0]

            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))

                filename = "test_nano_banana.png"
                img.save(filename, 'PNG', quality=95)

                print(f"\n✓ 成功！图片已保存: {filename}")
                print(f"  图片尺寸: {img.size}")
                return True

        print("\n✗ 失败：没有返回图片数据")
        return False

    except Exception as e:
        error_msg = str(e)
        print(f"\n✗ 错误: {error_msg}")

        # 检查错误类型
        if "429" in error_msg:
            print("\n  这是 429 速率限制错误")
        elif "model" in error_msg.lower():
            print("\n  可能是模型名称错误")

        return False

if __name__ == "__main__":
    test_nano_banana()
