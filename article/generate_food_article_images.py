# -*- coding: utf-8 -*-
"""
为今日头条美食文章生成配图
使用Gemini API生成3张插图
"""

import sys
import os
from pathlib import Path
import base64
from PIL import Image
import io

sys.path.insert(0, str(Path(__file__).parent))
from config import get_antigravity_client


def generate_article_images():
    """生成文章配图"""

    client = get_antigravity_client()

    # 图片1:新鲜鸡胸肉
    print("\n[图片1] 生成新鲜鸡胸肉食材图...")
    prompt1 = """
Fresh raw chicken breast meat on wooden cutting board,
high quality ingredient, clean kitchen counter,
natural lighting, food photography style, 1024x1024
"""

    try:
        response1 = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt=prompt1.strip(),
            size="1024x1024",
            n=1,
        )

        if hasattr(response1, 'data') and len(response1.data) > 0:
            img_data = response1.data[0]
            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))
                filename1 = "美食文章配图1_食材.jpg"
                img.save(filename1, 'JPEG', quality=95)
                print(f"    [成功] {filename1}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片2:烹饪炒菜场景
    print("\n[图片2] 生成烹饪炒菜场景...")
    prompt2 = """
Chinese home cooking scene, chef stir-frying chicken in wok,
steam rising, vibrant colorful ingredients,
warm kitchen lighting, appetizing food photography,
culinary action shot, 1024x1024
"""

    try:
        response2 = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt=prompt2.strip(),
            size="1024x1024",
            n=1,
        )

        if hasattr(response2, 'data') and len(response2.data) > 0:
            img_data = response2.data[0]
            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))
                filename2 = "美食文章配图2_烹饪.jpg"
                img.save(filename2, 'JPEG', quality=95)
                print(f"    [成功] {filename2}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片3:美味成品菜
    print("\n[图片3] 生成美味成品菜...")
    prompt3 = """
Delicious Kung Pao chicken dish served on white plate,
glossy sauce, roasted peanuts, vibrant colors,
restaurant quality presentation, appetizing food photography,
professional food styling, 1024x1024
"""

    try:
        response3 = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt=prompt3.strip(),
            size="1024x1024",
            n=1,
        )

        if hasattr(response3, 'data') and len(response3.data) > 0:
            img_data = response3.data[0]
            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))
                filename3 = "美食文章配图3_成品.jpg"
                img.save(filename3, 'JPEG', quality=95)
                print(f"    [成功] {filename3}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")


if __name__ == "__main__":
    print("="*80)
    print("为今日头条美食文章生成配图")
    print("="*80)
    generate_article_images()
    print("\n"+"="*80)
    print("配图生成完成!")
    print("="*80)
