# -*- coding: utf-8 -*-
"""
为今日头条美食文章生成配图
使用Pollinations.ai生成3张插图
"""

import requests
from pathlib import Path
import time


def generate_with_pollinations(prompt, filename, description):
    """使用Pollinations.ai生成图片"""
    print(f"\n[{description}] 正在生成...")

    # Pollinations.ai API endpoint
    url = f"https://image.pollinations.ai/prompt/{prompt}"

    try:
        # 发送请求
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            # 保存图片
            with open(filename, 'wb') as f:
                f.write(response.content)

            file_size = Path(filename).stat().st_size / 1024  # KB
            print(f"    [成功] {filename} ({file_size:.1f} KB)")
            return True
        else:
            print(f"    [失败] HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")
        return False


def generate_article_images():
    """生成文章配图"""

    # 图片1:新鲜鸡胸肉
    prompt1 = "Fresh raw chicken breast meat on wooden cutting board, high quality ingredient, clean kitchen counter, natural lighting, professional food photography, 1024x1024"
    filename1 = "美食文章配图1_食材.jpg"
    generate_with_pollinations(prompt1, filename1, "图片1-新鲜鸡胸肉食材图")

    time.sleep(2)  # 避免请求过快

    # 图片2:烹饪炒菜场景
    prompt2 = "Chinese home cooking scene, chef stir-frying chicken in wok, steam rising, vibrant colorful vegetables, warm kitchen lighting, appetizing food photography, culinary action shot, 1024x1024"
    filename2 = "美食文章配图2_烹饪.jpg"
    generate_with_pollinations(prompt2, filename2, "图片2-烹饪炒菜场景")

    time.sleep(2)

    # 图片3:美味成品菜
    prompt3 = "Delicious Kung Pao chicken dish served on white plate, glossy sauce, roasted peanuts, vibrant red and green colors, restaurant quality presentation, appetizing food photography, professional food styling, 1024x1024"
    filename3 = "美食文章配图3_成品.jpg"
    generate_with_pollinations(prompt3, filename3, "图片3-美味成品菜")


if __name__ == "__main__":
    print("="*80)
    print("为今日头条美食文章生成配图 (Pollinations.ai)")
    print("="*80)
    generate_article_images()
    print("\n"+"="*80)
    print("配图生成完成!")
    print("="*80)
