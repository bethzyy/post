# -*- coding: utf-8 -*-
"""大暑节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import Config

OUTPUT_DIR = Path(__file__).parent / "images" / "dashu"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {'f': 'dashu_group1_firefly.png', 'p': 'Chinese traditional watercolor painting, fireflies glowing among decaying grass at night, magical summer night scene, pink and purple tones, no text, no watermark, pure visual art'},
    {'f': 'dashu_group2_heat.png', 'p': 'Chinese traditional watercolor painting, intense summer heat, soil steaming with humidity, lush green vegetation, vibrant greens, no text, no watermark, pure visual art'},
    {'f': 'dashu_group3_rain.png', 'p': 'Chinese traditional watercolor painting, heavy summer rain pouring down, cooling the earth, yellow and brown earth tones, no text, no watermark, pure visual art'},
    {'f': 'dashu_group4_mountain.png', 'p': 'Chinese traditional watercolor painting, fresh mountain scenery after rain, misty peaks, blue and green tones, serene atmosphere, no text, no watermark, pure visual art'},
    {'f': 'dashu_summary_peak.png', 'p': 'Chinese traditional watercolor painting, Major Heat solar term landscape, hottest time of year, thunderstorms, lush vegetation, people resting, no text, no watermark, pure visual art'}
]

def gen(p, out):
    try:
        api_key = Config.VOLCANO_API_KEY
        from openai import OpenAI
        c = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=api_key)
        r = c.images.generate(model='doubao-seedream-3-0-t2i-250415', prompt=p, size='1920x1080', response_format='url', extra_body={'watermark': False})
        if r.data:
            open(out, 'wb').write(requests.get(r.data[0].url, timeout=60).content)
            return True
    except: pass
    return False

print('大暑图片生成')
for i, img in enumerate(PROMPTS, 1):
    out = OUTPUT_DIR / img['f']
    if out.exists(): print(f'[{i}/5] SKIP'); continue
    if gen(img['p'], str(out)): print(f'[{i}/5] OK')
    else: print(f'[{i}/5] FAIL')
    time.sleep(0.5)
print('完成')
