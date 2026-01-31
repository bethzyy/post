# -*- coding: utf-8 -*-
"""
为冬日饮茶养生文章生成配图
优先使用Gemini,不可用时使用Seedream
"""

import sys
import os
from pathlib import Path
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import get_antigravity_client, get_volcano_client


def generate_with_gemini(prompt, filename, description):
    """使用Gemini生成图片"""
    print(f"\n[{description}] 尝试使用Gemini...")

    try:
        client = get_antigravity_client()
        response = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        if hasattr(response, 'data') and len(response.data) > 0:
            img_data = response.data[0]
            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                import base64
                from PIL import Image
                import io

                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))
                img.save(filename, 'JPEG', quality=95)

                file_size = Path(filename).stat().st_size / 1024
                print(f"    [成功] {filename} ({file_size:.1f} KB)")
                return True

        print(f"    [失败] 响应格式异常")
        return False

    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            print(f"    [切换] Gemini配额耗尽,切换到Seedream")
            return None
        else:
            print(f"    [失败] {error_str[:100]}")
            return False


def generate_with_seedream(prompt, filename, description):
    """使用Seedream生成图片(无AI水印)"""
    print(f"\n[{description}] 使用Seedream...")

    try:
        client = get_volcano_client()
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt,
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            },
        )

        if hasattr(response, 'data') and len(response.data) > 0:
            image_url = response.data[0].url

            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / 1024
                print(f"    [成功] {filename} ({file_size:.1f} KB)")
                return True
            else:
                print(f"    [失败] 图片下载失败")
                return False
        else:
            print(f"    [失败] 响应格式异常")
            return False

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")
        return False


def generate_tea_images():
    """生成饮茶文章配图"""

    # 图片1:冬日围炉煮茶场景
    prompt1 = """
Traditional Chinese winter tea ceremony scene, small charcoal stove with clay teapot,
steam rising from teapot, warm cozy atmosphere, wooden table, window with snow outside,
soft warm lighting, peaceful and serene mood, cultural aesthetic style
"""

    filename1 = "饮茶文章配图1_围炉煮茶.jpg"

    # 优先Gemini,失败则用Seedream
    result1 = generate_with_gemini(prompt1, filename1, "图片1-围炉煮茶")
    if result1 is None:  # Gemini配额耗尽
        result1 = generate_with_seedream(prompt1, filename1, "图片1-围炉煮茶")
    elif result1 is False:  # 其他错误
        result1 = generate_with_seedream(prompt1, filename1, "图片1-围炉煮茶")

    # 图片2:三种茶叶特写
    prompt2 = """
Professional tea photography, three types of tea leaves arranged side by side,
black tea (dark leaves), pu-erh tea (compressed cake), white tea (silvery buds),
on clean white background, high quality product photography, natural lighting,
showing texture and color differences
"""

    filename2 = "饮茶文章配图2_三种茶叶.jpg"

    result2 = generate_with_gemini(prompt2, filename2, "图片2-三种茶叶")
    if result2 is None:
        result2 = generate_with_seedream(prompt2, filename2, "图片2-三种茶叶")
    elif result2 is False:
        result2 = generate_with_seedream(prompt2, filename2, "图片2-三种茶叶")

    # 图片3:茶汤倒出瞬间
    prompt3 = """
Golden tea being poured from clay teapot into white porcelain teacup,
steam rising, dynamic action shot, warm lighting, traditional Chinese tea culture,
professional food photography, appetizing and elegant
"""

    filename3 = "饮茶文章配图3_倒茶瞬间.jpg"

    result3 = generate_with_gemini(prompt3, filename3, "图片3-倒茶瞬间")
    if result3 is None:
        result3 = generate_with_seedream(prompt3, filename3, "图片3-倒茶瞬间")
    elif result3 is False:
        result3 = generate_with_seedream(prompt3, filename3, "图片3-倒茶瞬间")


if __name__ == "__main__":
    print("="*80)
    print("为冬日饮茶养生文章生成配图")
    print("优先级: Gemini > Seedream")
    print("="*80)
    generate_tea_images()
    print("\n"+"="*80)
    print("配图生成完成!")
    print("="*80)
