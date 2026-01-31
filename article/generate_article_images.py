# -*- coding: utf-8 -*-
"""
为今日头条文章生成配图
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

    # 图片1：职场办公场景
    print("\n[图片1] 生成职场办公场景...")
    prompt1 = """
Modern office workplace, young professional Chinese office worker working at desk,
computer with spreadsheets and charts, career growth atmosphere, bright and clean office,
professional business setting, realistic photography style, 1024x1024
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
                filename1 = "职场文章配图1_办公场景.jpg"
                img.save(filename1, 'JPEG', quality=95)
                print(f"    [成功] {filename1}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片2：薪资增长图表
    print("\n[图片2] 生成薪资增长图表...")
    prompt2 = """
Business chart showing salary growth from 5000 to 30000, upward trending arrow,
financial success visualization, career progression graph, professional business infographic,
blue and green color scheme, clean design, 1024x1024
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
                filename2 = "职场文章配图2_薪资增长.jpg"
                img.save(filename2, 'JPEG', quality=95)
                print(f"    [成功] {filename2}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")

    # 图片3：职场成功场景
    print("\n[图片3] 生成职场成功场景...")
    prompt3 = """
Successful business professional celebrating achievement, young Chinese person
in modern office, holding certificate or award, confident and happy, team members
clapping in background, career success moment, inspiring atmosphere, 1024x1024
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
                filename3 = "职场文章配图3_成功时刻.jpg"
                img.save(filename3, 'JPEG', quality=95)
                print(f"    [成功] {filename3}")

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")


if __name__ == "__main__":
    print("="*80)
    print("为今日头条文章生成配图")
    print("="*80)
    generate_article_images()
    print("\n"+"="*80)
    print("配图生成完成！")
    print("="*80)
