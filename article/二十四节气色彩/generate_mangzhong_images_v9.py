# -*- coding: utf-8 -*-
"""芒种节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import base64
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import get_antigravity_client, Config

IMAGE_SIZE = "1920x1080"
OUTPUT_DIR = Path(__file__).parent / "images" / "mangzhong"

MANGZHONG_PROMPTS = [
    {"filename": "mangzhong_group1_mantis.png", "prompt": "Chinese traditional watercolor painting, green praying mantis on leaf, early summer garden, fresh green colors, delicate brushstrokes, no text, no watermark, pure visual art", "desc": "螳螂初生，通体青绿"},
    {"filename": "mangzhong_group2_bird.png", "prompt": "Chinese traditional watercolor painting, shrike bird perched on branch singing, summer morning, blue sky background, elegant composition, no text, no watermark, pure visual art", "desc": "伯劳鸟鸣，声声入耳"},
    {"filename": "mangzhong_group3_wheat.png", "prompt": "Chinese traditional watercolor painting, golden wheat harvest scene, ripe grain fields, summer afternoon, warm yellow tones, no text, no watermark, pure visual art", "desc": "麦田金黄，丰收时节"},
    {"filename": "mangzhong_group4_gem.png", "prompt": "Chinese traditional watercolor painting, precious jade and gems in blue and green colors, summer sky and water reflection, elegant still life, no text, no watermark, pure visual art", "desc": "夏日宝石，青翠欲滴"},
    {"filename": "mangzhong_summary_harvest.png", "prompt": "Chinese traditional watercolor painting, Mangzhong solar term landscape, farmers harvesting wheat and planting rice, busy countryside scene, golden and green colors, no text, no watermark, pure visual art", "desc": "芒种时节，收种繁忙"}
]

def generate_with_seedream(prompt, output_path, model_version):
    try:
        api_key = Config.VOLCANO_API_KEY
        if not api_key: return False, "未配置", "unknown"
        from openai import OpenAI
        client = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=api_key)
        response = client.images.generate(model=model_version, prompt=prompt, size=IMAGE_SIZE, response_format="url", extra_body={"watermark": False})
        if response.data and len(response.data) > 0:
            img_response = requests.get(response.data[0].url, timeout=60)
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f: f.write(img_response.content)
                return True, "成功", {"doubao-seedream-5-0-260128": "Seedream 5.0", "doubao-seedream-4-5-251128": "Seedream 4.5", "doubao-seedream-4-0-250828": "Seedream 4.0", "doubao-seedream-3-0-t2i-250415": "Seedream 3.0 t2i"}.get(model_version, model_version)
        return False, "响应为空", "unknown"
    except Exception as e: return False, f"错误:{str(e)[:30]}", "unknown"

def generate_with_antigravity(prompt, output_path):
    try:
        client = get_antigravity_client()
        if not client: return False, "未配置", "unknown"
        for model in ["flux-1.1-pro", "gemini-2.0-flash-exp"]:
            try:
                response = client.images.generate(model=model, prompt=prompt, size="1024x1024")
                if response.data and len(response.data) > 0:
                    if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                        with open(output_path, 'wb') as f: f.write(base64.b64decode(response.data[0].b64_json))
                        return True, "成功", f"Antigravity-{model}"
                    elif hasattr(response.data[0], 'url') and response.data[0].url:
                        if requests.get(response.data[0].url, timeout=60).status_code == 200:
                            with open(output_path, 'wb') as f: f.write(requests.get(response.data[0].url, timeout=60).content)
                            return True, "成功", f"Antigravity-{model}"
            except: continue
        return False, "失败", "unknown"
    except: return False, "错误", "unknown"

def generate_with_cogview(prompt, output_path):
    try:
        api_key = Config.ZHIPU_API_KEY
        if not api_key: return False, "未配置", "unknown"
        from openai import OpenAI
        client = OpenAI(base_url="https://open.bigmodel.cn/api/paas/v4/", api_key=api_key)
        response = client.images.generations(model="cogview-3-flash", prompt=prompt, size="1024x1024")
        if response.data and hasattr(response.data[0], 'url') and response.data[0].url:
            if requests.get(response.data[0].url, timeout=60).status_code == 200:
                with open(output_path, 'wb') as f: f.write(requests.get(response.data[0].url, timeout=60).content)
                return True, "成功", "CogView-3-flash"
        return False, "失败", "unknown"
    except: return False, "错误", "unknown"

def generate_with_pollinations(prompt, output_path):
    try:
        from urllib.parse import quote
        response = requests.get(f"https://image.pollinations.ai/prompt/{quote(prompt)}", timeout=120)
        if response.status_code == 200:
            with open(output_path, 'wb') as f: f.write(response.content)
            return True, "成功", "Pollinations"
        return False, f"HTTP{response.status_code}", "unknown"
    except: return False, "错误", "unknown"

def generate_image_with_fallback(prompt, output_path):
    for i, model in enumerate(["doubao-seedream-5-0-260128", "doubao-seedream-4-5-251128", "doubao-seedream-4-0-250828", "doubao-seedream-3-0-t2i-250415"], 1):
        success, msg, model_name = generate_with_seedream(prompt, output_path, model)
        if success: return True, model_name
    for fn in [generate_with_antigravity, generate_with_cogview, generate_with_pollinations]:
        success, msg, model = fn(prompt, output_path)
        if success: return True, model
    return False, "全部失败"

def main():
    print("=" * 50); print("芒种节气配图生成 V9.7"); print("=" * 50)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for i, img in enumerate(MANGZHONG_PROMPTS, 1):
        print(f"\n[{i}/5] {img['desc']}")
        out = OUTPUT_DIR / img['filename']
        if out.exists(): print("  [SKIP] 已存在"); results.append({"f": img['filename'], "s": "exists", "m": "cached"}); continue
        success, model = generate_image_with_fallback(img['prompt'], str(out))
        print(f"  {'[OK]' if success else '[FAIL]'} {model if success else 'failed'}")
        results.append({"f": img['filename'], "s": "success" if success else "failed", "m": model if success else "failed"})
        time.sleep(1)
    print(f"\n完成: {sum(1 for r in results if r['s'] in ['success','exists'])}/5")
    return results

if __name__ == "__main__": main()
