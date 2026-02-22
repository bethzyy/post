# -*- coding: utf-8 -*-
"""
春分节气配图生成脚本
为春分.html的4组颜色和节气总览生成配图
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
    """使用Seedream 4.5/4.0生成图像"""
    image_generated = False

    # 1. 尝试 Seedream 4.5
    if volcano_client:
        try:
            print(f"    [TRY] Seedream 4.5...")
            response = volcano_client.images.generate(
                model="doubao-seedream-4-5-251128",
                prompt=prompt,
                size="2048x2048",  # 正方形 2048×2048
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
                size="2048x2048",  # 正方形 2048×2048
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
    """使用Antigravity生成图像"""
    if not antigravity_client:
        return None

    try:
        print(f"    [TRY] Antigravity...")
        response = antigravity_client.images.generate(
            model="flux",
            prompt=prompt,
            size="1024x1024",
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
    """使用Pollinations (免费)生成图像"""
    try:
        print(f"    [TRY] Pollinations...")
        # Pollinations URL编码
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

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
    print("春分节气配图生成器")
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

    # 定义要生成的图片
    # 基于春分.html的色彩意象描述生成配图
    images_to_generate = [
        # 第一组：皦玉、吉量、韶粉、霜地 - 燕子归来的白色系
        {
            "filename": "chunfen_group1_swallow.jpg",
            "prompt": """Chinese traditional painting style, spring equinox scene,
swallows flying over ancient Chinese palace walls,
pure white jade color, soft cream and pale white tones,
winter fading into spring, frost melting on ground,
elegant minimalist composition, soft pastel colors,
light peach pink and cream white gradient sky,
no text, no watermark, no letters, serene atmosphere,
traditional Chinese watercolor aesthetic"""
        },
        # 第二组：夏籥、紫磨金、檀色、赭罗 - 春雷惊蛰的暖褐色系
        {
            "filename": "chunfen_group2_thunder.jpg",
            "prompt": """Chinese traditional painting style, spring thunder awakening,
dramatic spring storm over ancient Chinese landscape,
warm brown and golden ochre color palette,
sandalwood tan and rich earth tones,
ancient musical instruments in golden light,
rain clouds rolling over mountains,
no text, no watermark, no letters,
traditional ink wash with warm color washes,
atmospheric depth and mood"""
        },
        # 第三组：黄丹、洛神珠、丹雘、水华朱 - 闪电映照的红色系
        {
            "filename": "chunfen_group3_lightning_red.jpg",
            "prompt": """Chinese traditional painting style, lightning illuminating night sky,
brilliant orange-red lightning bolt across dark sky,
vermillion and cinnabar red tones,
water reflection of lightning on lake surface,
dramatic contrast between dark clouds and bright light,
ancient Chinese palace silhouette in background,
warm glowing red and orange colors,
no text, no watermark, no letters,
artistic interpretation of spring electric storm"""
        },
        # 第四组：青冥、青雘、青緺、骐驎 - 雷电天光的青色系
        {
            "filename": "chunfen_group4_lightning_cyan.jpg",
            "prompt": """Chinese traditional painting style, azure sky after storm,
deep blue-green cyan and teal color palette,
celestial mythical qilin creature in clouds,
vast atmospheric sky in traditional Chinese painting style,
mineral blue and green pigments,
translucent layers of cyan mist,
legendary creature ascending to heaven,
no text, no watermark, no letters,
ethereal and mystical atmosphere,
traditional gongbi fine brushwork style"""
        },
        # 节气总览图1：春分整体意境
        {
            "filename": "chunfen_overview_spring.jpg",
            "prompt": """Chinese traditional painting style, spring equinox day,
balanced day and night, sun at equator position,
swallows returning, spring flowers blooming,
traditional Chinese garden with peach blossoms,
ancient architecture under spring sky,
soft warm spring light, fresh green and pink colors,
poetic atmosphere of seasonal transition,
no text, no watermark, no letters,
elegant classical Chinese aesthetics,
horizontal scroll painting composition"""
        },
        # 节气总览图2：春分三候图
        {
            "filename": "chunfen_overview_three_phases.jpg",
            "prompt": """Chinese traditional painting triptych style,
three panels showing spring equinox three phases:
left - swallow arriving (white and cream),
center - thunder rumbling (brown and gold),
right - lightning flashing (red and cyan),
traditional Chinese color aesthetics,
384 traditional colors arranged by solar terms,
故宫 Forbidden City inspired palette,
no text, no watermark, no letters,
harmonious color composition,
artistic interpretation of 72 pentads"""
        },
        # 节气总览图3：春分色彩组合
        {
            "filename": "chunfen_overview_colors.jpg",
            "prompt": """Artistic color palette visualization,
spring equinox traditional Chinese colors arranged aesthetically,
sixteen colors in four groups:
white jade and cream (swallows),
brown ochre and gold (thunder),
vermillion red and orange (lightning),
cyan blue and teal (sky),
abstract color composition with subtle imagery,
swallow, cloud, lightning, and wave motifs,
no text, no watermark, no letters,
modern interpretation of traditional palette,
elegant minimalist design"""
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
