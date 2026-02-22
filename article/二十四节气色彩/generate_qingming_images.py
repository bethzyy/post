# -*- coding: utf-8 -*-
"""
清明节气配图生成脚本
为清明.html的4组颜色和节气总览生成横版配图（16:9比例）
"""

import sys
import os
from pathlib import Path
import base64
import requests
import time

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_volcano_client, get_antigravity_client


def generate_image_with_seedream(volcano_client, prompt, filename, output_dir):
    """使用Seedream 4.5/4.0生成横版图像（16:9）"""
    image_generated = False

    # 1. 尝试 Seedream 4.5
    if volcano_client:
        try:
            print(f"    [TRY] Seedream 4.5...")
            response = volcano_client.images.generate(
                model="doubao-seedream-4-5-251128",
                prompt=prompt,
                size="1920x1080",  # 横版 16:9 比例
                response_format="url",
                extra_body={"watermark": False}
            )

            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"    [GET] URL: {image_url[:60]}...")

                # 下载图片
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    filepath = output_dir / filename
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"    [OK] {filename} (Seedream 4.5)")
                    return filepath
                else:
                    print(f"    [WARN] Seedream 4.5 download failed: HTTP {img_response.status_code}")

        except Exception as e:
            error_str = str(e)
            if "quota" in error_str.lower() or "limit" in error_str.lower():
                print(f"    [WARN] Seedream 4.5 quota exceeded, trying 4.0...")
            else:
                print(f"    [WARN] Seedream 4.5 failed: {error_str[:60]}")

    # 2. 尝试 Seedream 4.0
    if volcano_client and not image_generated:
        try:
            print(f"    [TRY] Seedream 4.0...")
            response = volcano_client.images.generate(
                model="doubao-seedream-4-0-250828",
                prompt=prompt,
                size="1920x1080",  # 横版 16:9 比例
                response_format="url",
                extra_body={"watermark": False}
            )

            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    filepath = output_dir / filename
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"    [OK] {filename} (Seedream 4.0)")
                    return filepath

        except Exception as e:
            print(f"    [WARN] Seedream 4.0 failed: {str(e)[:60]}")

    return None


def generate_image_with_antigravity(antigravity_client, prompt, filename, output_dir):
    """使用Antigravity生成横版图像"""
    if not antigravity_client:
        return None

    try:
        print(f"    [TRY] Antigravity...")
        response = antigravity_client.images.generate(
            model="flux",
            prompt=prompt,
            size="1792x1024",  # 接近16:9的横版
            response_format="url"
        )

        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                filepath = output_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                print(f"    [OK] {filename} (Antigravity)")
                return filepath

    except Exception as e:
        print(f"    [WARN] Antigravity failed: {str(e)[:60]}")

    return None


def generate_image_with_pollinations(prompt, filename, output_dir):
    """使用Pollinations (免费)生成横版图像"""
    try:
        print(f"    [TRY] Pollinations...")
        # Pollinations URL编码
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1920&height=1080&nologo=true"

        img_response = requests.get(image_url, timeout=60)
        if img_response.status_code == 200:
            filepath = output_dir / filename
            with open(filepath, 'wb') as f:
                f.write(img_response.content)
            print(f"    [OK] {filename} (Pollinations)")
            return filepath

    except Exception as e:
        print(f"    [WARN] Pollinations failed: {str(e)[:60]}")

    return None


def generate_image(clients, prompt, filename, output_dir):
    """尝试多个API生成图像，按优先级顺序"""
    print(f"\n  [生成] {filename}")
    print(f"  [提示词] {prompt[:80]}...")

    # 1. Seedream
    filepath = generate_image_with_seedream(
        clients['volcano'], prompt, filename, output_dir
    )
    if filepath:
        return filepath

    # 2. Antigravity
    filepath = generate_image_with_antigravity(
        clients['antigravity'], prompt, filename, output_dir
    )
    if filepath:
        return filepath

    # 3. Pollinations
    filepath = generate_image_with_pollinations(prompt, filename, output_dir)
    if filepath:
        return filepath

    print(f"    [FAIL] 所有图像生成API都失败了")
    return None


def main():
    """主函数"""
    print("=" * 60)
    print("清明节气配图生成器（横版16:9）")
    print("=" * 60)

    # 输出目录
    output_dir = Path(__file__).parent / "images"
    output_dir.mkdir(exist_ok=True)
    print(f"\n输出目录: {output_dir}")

    # 获取客户端
    print("\n初始化API客户端...")
    volcano_client = get_volcano_client()
    antigravity_client = get_antigravity_client()
    clients = {
        'volcano': volcano_client,
        'antigravity': antigravity_client
    }

    # 定义要生成的图片（横版16:9）
    # 基于清明.html的色彩意象描述生成配图
    images_to_generate = [
        # 第一组：紫蒲、赪紫、齐紫、凝夜紫 - 桐花盛开的紫色系
        {
            "filename": "qingming_group1_paulownia.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
paulownia trees in full bloom, cascading purple and white bell-shaped flowers,
soft purple mist from pale lavender to deep purple gradients,
ancient Chinese garden in spring morning light,
wisteria and redbud flowers adding to the purple palette,
traditional ink wash with delicate color washes,
poetic atmosphere of Qingming festival,
no text, no watermark, no letters,
elegant classical Chinese aesthetics,
wide panoramic view"""
        },
        # 第二组：冻缥、春碧、执大象、苔古 - 草木疯长的青绿色系
        {
            "filename": "qingming_group2_greenery.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
lush spring vegetation after rain,
ice-melting pale blue-green water reflecting sky,
vibrant emerald green meadows and ancient moss-covered stones,
traditional Chinese countryside with terraced fields,
fresh spring green symbolizing growth and renewal,
transparent aqua and verdant tones,
no text, no watermark, no letters,
atmospheric depth with layers of green,
serene pastoral scene in classical style,
wide panoramic view"""
        },
        # 第三组：香炉紫烟、紫菂、拂紫绵、三公子 - 紫霞与紫花的紫色系
        {
            "filename": "qingming_group3_ziwist.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
magical purple mist and rosy clouds at sunrise,
inspired by Li Bai poem 'purple smoke from incense burner',
lotus pond with purple lotus flowers,
crepe myrtle blossoms in shades of lavender and violet,
ethereal purple atmosphere blending sky and water,
traditional gongbi fine brushwork style,
no text, no watermark, no letters,
dreamy romantic spring scene,
soft gradient from pale lilac to deep amethyst,
wide panoramic view"""
        },
        # 第四组：琅玕紫、红踯躅、魏红、魏紫 - 彩虹与牡丹的紫红色系
        {
            "filename": "qingming_group4_peony.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
rainbow appearing after spring rain,
famous peony gardens of Luoyang in full bloom,
magnificent purple and crimson peonies,
azalea flowers in vibrant red-purple tones,
jasper-like purple gemstone colors,
rainbow colors reflected in garden pond,
luxurious floral abundance,
no text, no watermark, no letters,
rich saturated colors of imperial gardens,
wide panoramic view"""
        },
        # 节气总览图1：清明整体意境 - 细雨绵绵
        {
            "filename": "qingming_overview_rain.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
Qingming festival light drizzle and mist,
willow trees swaying in gentle spring rain,
ancient stone bridge over misty river,
traditional Chinese architecture in distance,
soft muted colors washed clean by rain,
purples greens and reds more vivid after rain,
poetic melancholy beauty,
no text, no watermark, no letters,
atmospheric perspective through rain,
wide panoramic scroll painting style"""
        },
        # 节气总览图2：清明三候图
        {
            "filename": "qingming_overview_three_phases.jpg",
            "prompt": """Chinese traditional painting triptych style, horizontal composition 16:9,
three connected scenes showing Qingming three phases:
left - paulownia flowers blooming (purple and white),
center - quails appearing as field mice hide (green fields),
right - rainbow appearing in sky (vivid multicolor),
traditional Chinese color aesthetics,
384 traditional colors arranged by solar terms,
故宫 Forbidden City inspired palette,
no text, no watermark, no letters,
harmonious color composition across three panels,
artistic interpretation of 72 pentads,
wide panoramic view"""
        },
        # 节气总览图3：清明色彩组合
        {
            "filename": "qingming_overview_colors.jpg",
            "prompt": """Artistic color palette visualization, horizontal composition 16:9,
Qingming festival traditional Chinese colors arranged aesthetically,
sixteen colors in four groups:
purple lavender and violet (paulownia flowers),
pale blue-green and emerald (spring growth),
amethyst and lilac (rainbow mist),
crimson and magenta (peonies),
abstract color composition with subtle imagery,
willow, flower, rainbow, and peony motifs,
no text, no watermark, no letters,
modern interpretation of traditional palette,
elegant minimalist design,
wide panoramic layout"""
        }
    ]

    # 生成图片
    generated_files = []
    for i, img_info in enumerate(images_to_generate, 1):
        print(f"\n[{i}/{len(images_to_generate)}] 生成: {img_info['filename']}")

        filepath = generate_image(
            clients,
            img_info['prompt'],
            img_info['filename'],
            output_dir
        )

        if filepath:
            generated_files.append({
                'filename': img_info['filename'],
                'filepath': filepath,
                'description': img_info['prompt'][:100]
            })
        else:
            print(f"  [SKIP] 跳过 {img_info['filename']}")

        # 避免API限流
        if i < len(images_to_generate):
            print("  等待3秒...")
            time.sleep(3)

    # 输出结果
    print("\n" + "=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"\n成功生成 {len(generated_files)}/{len(images_to_generate)} 张图片:")
    for f in generated_files:
        print(f"  - {f['filename']}")
        print(f"    路径: {f['filepath']}")

    print(f"\n图片保存在: {output_dir}")
    return generated_files


if __name__ == "__main__":
    main()
