# -*- coding: utf-8 -*-
"""
为今日头条美食文章生成配图
使用Volcano Seedream模型生成3张插图(无AI水印)
"""

import sys
import os
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import get_volcano_client


def generate_article_images():
    """生成文章配图"""

    client = get_volcano_client()

    # 图片1:新鲜鸡胸肉
    print("\n[图片1] 生成新鲜鸡胸肉食材图...")
    prompt1 = """
Professional food photography of fresh raw chicken breast meat
on wooden cutting board, high quality ingredient, clean kitchen counter,
natural bright lighting, restaurant style presentation,
sharp focus, appetizing appearance
"""

    try:
        response1 = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt1.strip(),
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        if hasattr(response1, 'data') and len(response1.data) > 0:
            image_url = response1.data[0].url

            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                filename1 = "美食文章配图1_食材.jpg"
                with open(filename1, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / 1024
                print(f"    [成功] {filename1} ({file_size:.1f} KB)")
            else:
                print(f"    [失败] 图片下载失败")
        else:
            print(f"    [失败] 响应格式异常")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片2:烹饪炒菜场景
    print("\n[图片2] 生成烹饪炒菜场景...")
    prompt2 = """
Chinese home kitchen cooking scene, chef stir-frying chicken in wok,
steam rising from hot wok, vibrant colorful vegetables on counter,
warm kitchen lighting, professional food photography style,
culinary action shot
"""

    try:
        response2 = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt2.strip(),
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        if hasattr(response2, 'data') and len(response2.data) > 0:
            image_url = response2.data[0].url

            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                filename2 = "美食文章配图2_烹饪.jpg"
                with open(filename2, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / 1024
                print(f"    [成功] {filename2} ({file_size:.1f} KB)")
            else:
                print(f"    [失败] 图片下载失败")
        else:
            print(f"    [失败] 响应格式异常")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片3:美味成品菜
    print("\n[图片3] 生成美味成品菜...")
    prompt3 = """
Delicious Kung Pao chicken dish served on white plate,
glossy savory sauce, roasted peanuts, vibrant red and green colors,
restaurant quality food presentation, professional food photography,
appetizing and mouth-watering
"""

    try:
        response3 = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt3.strip(),
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        if hasattr(response3, 'data') and len(response3.data) > 0:
            image_url = response3.data[0].url

            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                filename3 = "美食文章配图3_成品.jpg"
                with open(filename3, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / 1024
                print(f"    [成功] {filename3} ({file_size:.1f} KB)")
            else:
                print(f"    [失败] 图片下载失败")
        else:
            print(f"    [失败] 响应格式异常")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")


if __name__ == "__main__":
    print("="*80)
    print("为今日头条美食文章生成配图 (Volcano Seedream - 无AI水印)")
    print("="*80)
    generate_article_images()
    print("\n"+"="*80)
    print("配图生成完成!")
    print("="*80)
