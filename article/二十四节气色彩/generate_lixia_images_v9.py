# -*- coding: utf-8 -*-
"""
立夏节气配图生成脚本 V9.7
使用7级Fallback机制生成横版配图（16:9比例）

立夏三候：
1. 蝼蝈鸣 - 蝼蛄开始鸣叫
2. 蚯蚓出 - 蚯蚓钻出土
3. 王瓜生 - 王瓜藤蔓攀爬

7级Fallback:
1. Seedream 5.0 (doubao-seedream-5-0-260128)
2. Seedream 4.5 (doubao-seedream-4-5-251128)
3. Seedream 4.0 (doubao-seedream-4-0-250828)
4. Seedream 3.0 t2i (doubao-seedream-3-0-t2i-250415)
5. Antigravity: Gemini/Flux/DALL-E
6. CogView-3-flash
7. Pollinations
"""

import sys
import os
from pathlib import Path
import base64
import requests
import time
import json

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import get_volcano_client, get_antigravity_client, Config

# 图片尺寸配置 - 所有模型统一使用横版 16:9
IMAGE_SIZE = "1920x1080"

# 输出目录
OUTPUT_DIR = Path(__file__).parent / "images" / "lixia"

# 立夏配图提示词（5张图：4组颜色 + 1张总结）
LIXIA_PROMPTS = [
    {
        "filename": "lixia_group1_cicada.png",
        "prompt": """Chinese traditional watercolor painting, early summer scene with mole cricket insects chirping in grass, light blue and green tones, morning mist, fresh vegetation, soft sunlight, peaceful countryside, no text, no watermark, pure visual art""",
        "desc": "蝼蝈初鸣，夏声渐起",
        "colors": "青粲 · 翠缥 · 人籁 · 水龙吟"
    },
    {
        "filename": "lixia_group2_earthworm.png",
        "prompt": """Chinese traditional watercolor painting, earthworms emerging from soil, spring earth awakening, brown and green earth tones, morning dew on ground, fresh soil texture, natural scene, no text, no watermark, pure visual art""",
        "desc": "蚯蚓出土，大地苏醒",
        "colors": "地籁 · 大块 · 养生主 · 大云"
    },
    {
        "filename": "lixia_group3_melon.png",
        "prompt": """Chinese traditional watercolor painting, melon vines climbing on bamboo trellis, young melons forming, yellow and white flowers, lush green leaves, warm sunlight, garden scene, no text, no watermark, pure visual art""",
        "desc": "王瓜藤蔓攀爬，果实渐熟",
        "colors": "溶溶月 · 绍衣 · 石莲褐 · 黑朱"
    },
    {
        "filename": "lixia_group4_flowers.png",
        "prompt": """Chinese traditional watercolor painting, summer flowers blooming in vibrant red and orange colors, pomegranate flowers, warm sunshine, garden in full bloom, romantic atmosphere, no text, no watermark, pure visual art""",
        "desc": "夏日花开，红艳热烈",
        "colors": "朱颜酡 · 苕荣 · 檎丹 · 丹罽"
    },
    {
        "filename": "lixia_summary_summer.png",
        "prompt": """Chinese traditional watercolor painting, beginning of summer landscape, green rice paddies, farmers working in fields, warm breeze, blue sky with white clouds, transition from spring to summer, no text, no watermark, pure visual art""",
        "desc": "立夏时节，夏日初临",
        "colors": "春天的告别，夏天的开始"
    }
]


def generate_with_seedream(prompt, output_path, model_version):
    """使用Seedream生成图像"""
    try:
        api_key = Config.VOLCANO_API_KEY
        if not api_key:
            return False, "VOLCANO_API_KEY未配置", "unknown"

        from openai import OpenAI
        client = OpenAI(
            base_url=Config.VOLCANO_BASE_URL,
            api_key=api_key
        )

        response = client.images.generate(
            model=model_version,
            prompt=prompt,
            size=IMAGE_SIZE,
            response_format="url",
            extra_body={"watermark": False}
        )

        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                model_name_map = {
                    "doubao-seedream-5-0-260128": "Seedream 5.0",
                    "doubao-seedream-4-5-251128": "Seedream 4.5",
                    "doubao-seedream-4-0-250828": "Seedream 4.0",
                    "doubao-seedream-3-0-t2i-250415": "Seedream 3.0 t2i"
                }
                return True, "成功", model_name_map.get(model_version, model_version)

        return False, "响应为空", "unknown"

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "limit" in error_str.lower():
            return False, f"配额用尽: {error_str[:50]}", "unknown"
        return False, f"错误: {error_str[:50]}", "unknown"


def generate_with_antigravity(prompt, output_path):
    """使用Antigravity生成图像"""
    try:
        client = get_antigravity_client()
        if not client:
            return False, "Antigravity客户端未配置", "unknown"

        # 尝试多个模型
        models = ["flux-1.1-pro", "gemini-2.0-flash-exp"]

        for model in models:
            try:
                response = client.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024"
                )

                if response.data and len(response.data) > 0:
                    if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                        image_data = base64.b64decode(response.data[0].b64_json)
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        return True, "成功", f"Antigravity-{model}"
                    elif hasattr(response.data[0], 'url') and response.data[0].url:
                        img_response = requests.get(response.data[0].url, timeout=60)
                        if img_response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(img_response.content)
                            return True, "成功", f"Antigravity-{model}"
            except Exception as e:
                continue

        return False, "所有Antigravity模型都失败", "unknown"

    except Exception as e:
        return False, f"错误: {str(e)[:50]}", "unknown"


def generate_with_cogview(prompt, output_path):
    """使用CogView-3-flash生成图像"""
    try:
        api_key = Config.ZHIPU_API_KEY
        if not api_key:
            return False, "ZHIPU_API_KEY未配置", "unknown"

        from openai import OpenAI
        client = OpenAI(
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key=api_key
        )

        response = client.images.generations(
            model="cogview-3-flash",
            prompt=prompt,
            size="1024x1024"
        )

        if response.data and len(response.data) > 0:
            if hasattr(response.data[0], 'url') and response.data[0].url:
                img_response = requests.get(response.data[0].url, timeout=60)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    return True, "成功", "CogView-3-flash"

        return False, "响应为空", "unknown"

    except Exception as e:
        return False, f"错误: {str(e)[:50]}", "unknown"


def generate_with_pollinations(prompt, output_path):
    """使用Pollinations免费API生成图像"""
    try:
        from urllib.parse import quote
        url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True, "成功", "Pollinations"

        return False, f"HTTP {response.status_code}", "unknown"

    except Exception as e:
        return False, f"错误: {str(e)[:50]}", "unknown"


def generate_image_with_fallback(prompt, output_path):
    """7级Fallback图像生成"""
    print(f"  [提示词] {prompt[:80]}...")

    # 1. Seedream 5.0
    print(f"  [Fallback 1/7] 尝试 Seedream 5.0...")
    success, msg, model = generate_with_seedream(prompt, output_path, "doubao-seedream-5-0-260128")
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Seedream 5.0: {msg}")

    # 2. Seedream 4.5
    print(f"  [Fallback 2/7] 尝试 Seedream 4.5...")
    success, msg, model = generate_with_seedream(prompt, output_path, "doubao-seedream-4-5-251128")
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Seedream 4.5: {msg}")

    # 3. Seedream 4.0
    print(f"  [Fallback 3/7] 尝试 Seedream 4.0...")
    success, msg, model = generate_with_seedream(prompt, output_path, "doubao-seedream-4-0-250828")
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Seedream 4.0: {msg}")

    # 4. Seedream 3.0 t2i
    print(f"  [Fallback 4/7] 尝试 Seedream 3.0 t2i...")
    success, msg, model = generate_with_seedream(prompt, output_path, "doubao-seedream-3-0-t2i-250415")
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Seedream 3.0 t2i: {msg}")

    # 5. Antigravity
    print(f"  [Fallback 5/7] 尝试 Antigravity...")
    success, msg, model = generate_with_antigravity(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Antigravity: {msg}")

    # 6. CogView-3-flash
    print(f"  [Fallback 6/7] 尝试 CogView-3-flash...")
    success, msg, model = generate_with_cogview(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] CogView-3-flash: {msg}")

    # 7. Pollinations
    print(f"  [Fallback 7/7] 尝试 Pollinations...")
    success, msg, model = generate_with_pollinations(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [ERROR] Pollinations: {msg}")

    return False, "所有图像生成服务都失败"


def main():
    """主函数：生成立夏配图"""
    print("=" * 60)
    print("立夏节气配图生成脚本 V9.7 (7级Fallback)")
    print("=" * 60)

    # 创建输出目录
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n输出目录: {OUTPUT_DIR}")

    # 生成结果记录
    results = []

    # 生成每张图片
    for i, img_info in enumerate(LIXIA_PROMPTS, 1):
        print(f"\n[{i}/{len(LIXIA_PROMPTS)}] 生成: {img_info['desc']}")
        print(f"  颜色: {img_info['colors']}")

        output_path = OUTPUT_DIR / img_info['filename']

        # 如果文件已存在，跳过
        if output_path.exists():
            print(f"  [SKIP] 文件已存在: {img_info['filename']}")
            results.append({
                "filename": img_info['filename'],
                "desc": img_info['desc'],
                "status": "exists",
                "model": "cached"
            })
            continue

        success, model = generate_image_with_fallback(img_info['prompt'], str(output_path))

        results.append({
            "filename": img_info['filename'],
            "desc": img_info['desc'],
            "status": "success" if success else "failed",
            "model": model if success else "failed"
        })

        if success:
            print(f"  [SAVED] {output_path}")
        else:
            print(f"  [FAILED] 生成失败")

        # 短暂延迟避免API限流
        time.sleep(1)

    # 输出总结
    print("\n" + "=" * 60)
    print("生成完成!")
    print("=" * 60)

    success_count = sum(1 for r in results if r['status'] in ['success', 'exists'])
    print(f"成功: {success_count}/{len(results)}")

    for r in results:
        status = "[OK]" if r['status'] in ['success', 'exists'] else "[FAIL]"
        print(f"  {status} {r['filename']} ({r['model']})")

    return results


if __name__ == "__main__":
    main()
