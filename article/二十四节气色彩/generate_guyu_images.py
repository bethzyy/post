# -*- coding: utf-8 -*-
"""
谷雨节气配图生成脚本
为谷雨.html的4组颜色和节气总览生成横版配图（16:9比例）

谷雨三候：
1. 萍始生 - 浮萍初生，水面泛紫
2. 鸣鸠拂其羽 - 斑鸠拂羽，春意更浓
3. 戴胜降于桑 - 戴胜鸟落在桑树上，头顶五彩羽冠
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
    print("谷雨节气配图生成器（横版16:9）")
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
    # 基于谷雨.html的色彩意象描述生成配图
    images_to_generate = [
        # 第一组：昌荣、紫薄汗、茈藐、紫紶 - 浮萍初生，水面泛紫
        {
            "filename": "guyu_group1_duckweed.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
late spring pond with duckweed floating on water surface,
color transitions from tender green to deep purple on water,
lotus leaves emerging, purple and lavender duckweed patterns,
morning mist over ancient Chinese garden pond,
subtle purple reflections on calm water,
lush vegetation surrounding the pond,
"changrong" flourishing plant glow,
"zibohan" light purple sweat color,
no text, no watermark, no letters,
traditional ink wash with delicate purple-green washes,
poetic atmosphere of Guyu grain rain,
wide panoramic view"""
        },
        # 第二组：苍葭、庭芜绿、翠微、翠虬 - 斑鸠拂羽，春意更浓
        {
            "filename": "guyu_group2_greenery.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
turtledove birds preening feathers on mulberry tree branches,
lush late spring greenery in full abundance,
"cangjia" blue-green reeds swaying by waterside,
"tingwulu" vibrant courtyard grass emerald green,
"cuiwei" distant mountains in soft green mist,
"cuqiu" deep dragon-like verdant green,
layers of green from nearby garden to far hills,
traditional Chinese countryside pastoral scene,
peak of spring vegetation before summer,
no text, no watermark, no letters,
atmospheric depth with multiple green layers,
serene pastoral beauty in classical style,
wide panoramic view"""
        },
        # 第三组：碧落、挼蓝、青雀头黛、螺子黛 - 戴胜鸟青蓝色系羽冠
        {
            "filename": "guyu_group3_hoopoe.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
beautiful hoopoe bird with colorful crest landing on mulberry tree,
"biluo" azure sky color as background,
"ruolan" indigo blue from rubbed dyer's woad,
"qinguetoudai" bluebird feather blue-black,
"luozidai" snail-shell eyebrow pigment deep blue,
brilliant blue and cyan crest feathers,
mulberry tree with ripening fruits,
spring sky meeting water in harmonious blue,
bird and nature in perfect harmony,
no text, no watermark, no letters,
exquisite gongbi fine brushwork details,
vibrant yet elegant color palette,
wide panoramic view"""
        },
        # 第四组：露褐、檀褐、緅絺、目童子 - 暮春褐色的过渡
        {
            "filename": "guyu_group4_transition.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
late spring transitioning to early summer,
vegetation turning from fresh green to mature brownish-green,
"lutab" dew-drenched brown earth tones,
"tantab" sandalwood light brown wood color,
"zouchi" reddish-brown coarse linen texture,
"mutongzi" deep brown of human pupils,
earthy warm browns and muted tones,
grass and leaves beginning to deepen,
golden hour warm light on landscape,
sense of spring ending and summer approaching,
no text, no watermark, no letters,
warm nostalgic atmosphere,
mature autumnal feeling in spring,
wide panoramic view"""
        },
        # 节气总览图1：谷雨整体意境 - 雨水把庄稼喂饱
        {
            "filename": "guyu_overview_rain.jpg",
            "prompt": """Chinese traditional painting style, horizontal landscape composition 16:9,
Guyu grain rain nourishing rice fields and crops,
gentle spring rain falling on fertile farmland,
young seedlings drinking rainwater, growing tall,
colors becoming richer and more saturated,
purple deeper, green thicker, red more intense,
traditional Chinese agricultural scene,
rainbow may appear in distance,
farmers tending to spring crops,
poetic celebration of spring's final rain,
no text, no watermark, no letters,
warm humid atmosphere,
rich earthy tones with vivid accents,
wide panoramic scroll painting style"""
        },
        # 节气总览图2：谷雨三候图
        {
            "filename": "guyu_overview_three_phases.jpg",
            "prompt": """Chinese traditional painting triptych style, horizontal composition 16:9,
three connected scenes showing Guyu three phases:
left - duckweed beginning to grow on pond surface (purple-green water),
center - turtledove preening feathers in lush garden (emerald greenery),
right - hoopoe bird landing on mulberry tree (blue-brown crest),
traditional Chinese color aesthetics,
384 traditional colors arranged by solar terms,
故宫 Forbidden City inspired palette,
transition from spring to summer,
no text, no watermark, no letters,
harmonious color composition across three panels,
artistic interpretation of 72 pentads,
wide panoramic view"""
        },
        # 节气总览图3：谷雨色彩组合 - 春天的告别色
        {
            "filename": "guyu_overview_colors.jpg",
            "prompt": """Artistic color palette visualization, horizontal composition 16:9,
Guyu festival traditional Chinese colors arranged aesthetically,
sixteen colors in four groups:
purple and lavender (duckweed on water),
emerald and verdant green (lush spring vegetation),
azure and indigo blue (hoopoe crest feathers),
warm brown and tan (spring-to-summer transition),
abstract color composition with subtle imagery,
duckweed, mulberry, hoopoe, and rain motifs,
no text, no watermark, no letters,
modern interpretation of traditional palette,
spring's final bow before summer,
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
