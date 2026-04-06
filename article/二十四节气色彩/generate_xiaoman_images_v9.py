# -*- coding: utf-8 -*-
"""
小满节气配图生成脚本 V9.7
使用7级Fallback机制生成横版配图（16:9比例）

小满三候：
1. 苦菜秀 - 苦菜开花
2. 靡草死 - 喜阴的草枯死
3. 麦秋至 - 麦子成熟

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

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import get_antigravity_client, Config

IMAGE_SIZE = "1920x1080"
OUTPUT_DIR = Path(__file__).parent / "images" / "xiaoman"

XIAOMAN_PROMPTS = [
    {
        "filename": "xiaoman_group1_herb.png",
        "prompt": """Chinese traditional watercolor painting, bitter herbs flowering in fields, red and white wild flowers, early summer meadow, soft sunlight, gentle breeze, natural countryside scene, no text, no watermark, pure visual art""",
        "desc": "苦菜开花，红白相间",
        "colors": "彤管 · 渥赭 · 唇脂 · 朱孔阳"
    },
    {
        "filename": "xiaoman_group2_lotus.png",
        "prompt": """Chinese traditional watercolor painting, lotus leaves emerging from pond, young green lotus, water surface reflection, early summer garden, fresh green colors, peaceful atmosphere, no text, no watermark, pure visual art""",
        "desc": "靡草枯萎，荷叶初生",
        "colors": "石发 · 漆姑 · 芰荷 · 官绿"
    },
    {
        "filename": "xiaoman_group3_wheat.png",
        "prompt": """Chinese traditional watercolor painting, golden wheat fields ready for harvest, wheat ears turning yellow, warm sunlight, rural landscape, farmers preparing for harvest, no text, no watermark, pure visual art""",
        "desc": "麦子渐黄，丰收在望",
        "colors": "仙米 · 黄螺 · 降真香 · 远志"
    },
    {
        "filename": "xiaoman_group4_golden.png",
        "prompt": """Chinese traditional watercolor painting, vast golden wheat harvest scene, yellow grain everywhere, summer harvest festival, warm golden tones, joyful atmosphere, no text, no watermark, pure visual art""",
        "desc": "麦收时节，金黄遍地",
        "colors": "嫩鹅黄 · 鞠衣 · 郁金裙 · 黄流"
    },
    {
        "filename": "xiaoman_summary_grain.png",
        "prompt": """Chinese traditional watercolor painting, Xiaoman solar term landscape, wheat fields half-ripe, green and golden colors mixed, early summer countryside, farmers checking crops, transition season, no text, no watermark, pure visual art""",
        "desc": "小满时节，麦粒饱满",
        "colors": "将满未满，恰到好处"
    }
]


def generate_with_seedream(prompt, output_path, model_version):
    try:
        api_key = Config.VOLCANO_API_KEY
        if not api_key:
            return False, "VOLCANO_API_KEY未配置", "unknown"

        from openai import OpenAI
        client = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=api_key)

        response = client.images.generate(
            model=model_version, prompt=prompt, size=IMAGE_SIZE,
            response_format="url", extra_body={"watermark": False}
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
            return False, f"配额用尽", "unknown"
        return False, f"错误: {error_str[:50]}", "unknown"


def generate_with_antigravity(prompt, output_path):
    try:
        client = get_antigravity_client()
        if not client:
            return False, "Antigravity客户端未配置", "unknown"
        for model in ["flux-1.1-pro", "gemini-2.0-flash-exp"]:
            try:
                response = client.images.generate(model=model, prompt=prompt, size="1024x1024")
                if response.data and len(response.data) > 0:
                    if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                        with open(output_path, 'wb') as f:
                            f.write(base64.b64decode(response.data[0].b64_json))
                        return True, "成功", f"Antigravity-{model}"
                    elif hasattr(response.data[0], 'url') and response.data[0].url:
                        img_response = requests.get(response.data[0].url, timeout=60)
                        if img_response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(img_response.content)
                            return True, "成功", f"Antigravity-{model}"
            except:
                continue
        return False, "所有Antigravity模型都失败", "unknown"
    except Exception as e:
        return False, f"错误: {str(e)[:50]}", "unknown"


def generate_with_cogview(prompt, output_path):
    try:
        api_key = Config.ZHIPU_API_KEY
        if not api_key:
            return False, "ZHIPU_API_KEY未配置", "unknown"
        from openai import OpenAI
        client = OpenAI(base_url="https://open.bigmodel.cn/api/paas/v4/", api_key=api_key)
        response = client.images.generations(model="cogview-3-flash", prompt=prompt, size="1024x1024")
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
    print(f"  [提示词] {prompt[:60]}...")

    models = ["doubao-seedream-5-0-260128", "doubao-seedream-4-5-251128",
              "doubao-seedream-4-0-250828", "doubao-seedream-3-0-t2i-250415"]

    for i, model in enumerate(models, 1):
        print(f"  [Fallback {i}/7] 尝试 {model.split('-')[2]} {model.split('-')[3]}...")
        success, msg, model_name = generate_with_seedream(prompt, output_path, model)
        if success:
            print(f"  [OK] 成功 ({model_name})")
            return True, model_name
        print(f"  [WARN] {model}: {msg}")

    print(f"  [Fallback 5/7] 尝试 Antigravity...")
    success, msg, model = generate_with_antigravity(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] Antigravity: {msg}")

    print(f"  [Fallback 6/7] 尝试 CogView-3-flash...")
    success, msg, model = generate_with_cogview(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [WARN] CogView-3-flash: {msg}")

    print(f"  [Fallback 7/7] 尝试 Pollinations...")
    success, msg, model = generate_with_pollinations(prompt, output_path)
    if success:
        print(f"  [OK] 成功 ({model})")
        return True, model
    print(f"  [ERROR] Pollinations: {msg}")

    return False, "所有图像生成服务都失败"


def main():
    print("=" * 60)
    print("小满节气配图生成脚本 V9.7 (7级Fallback)")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n输出目录: {OUTPUT_DIR}")

    results = []
    for i, img_info in enumerate(XIAOMAN_PROMPTS, 1):
        print(f"\n[{i}/{len(XIAOMAN_PROMPTS)}] 生成: {img_info['desc']}")
        output_path = OUTPUT_DIR / img_info['filename']

        if output_path.exists():
            print(f"  [SKIP] 文件已存在")
            results.append({"filename": img_info['filename'], "status": "exists", "model": "cached"})
            continue

        success, model = generate_image_with_fallback(img_info['prompt'], str(output_path))
        results.append({"filename": img_info['filename'], "status": "success" if success else "failed", "model": model if success else "failed"})
        if success:
            print(f"  [SAVED] {output_path}")
        time.sleep(1)

    print("\n" + "=" * 60)
    success_count = sum(1 for r in results if r['status'] in ['success', 'exists'])
    print(f"完成! 成功: {success_count}/{len(results)}")
    for r in results:
        status = "[OK]" if r['status'] in ['success', 'exists'] else "[FAIL]"
        print(f"  {status} {r['filename']} ({r['model']})")
    return results


if __name__ == "__main__":
    main()
