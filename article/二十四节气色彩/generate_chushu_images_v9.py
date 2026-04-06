# -*- coding: utf-8 -*-
"""处暑节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import Config

OUTPUT_DIR = Path(__file__).parent / "images" / "chushu"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {'f': 'chushu_group1_eagle.png', 'p': 'Chinese traditional watercolor painting, eagle hunting prey in autumn sky, fierce gaze, brown and grey tones, no text, no watermark, pure visual art'},
    {'f': 'chushu_group2_solemn.png', 'p': 'Chinese traditional watercolor painting, solemn autumn atmosphere, plants withering, brown earth tones, melancholic beauty, no text, no watermark, pure visual art'},
    {'f': 'chushu_group3_harvest.png', 'p': 'Chinese traditional watercolor painting, autumn harvest scene, golden crops, farmers working in fields, warm yellow tones, no text, no watermark, pure visual art'},
    {'f': 'chushu_group4_gold.png', 'p': 'Chinese traditional watercolor painting, golden autumn landscape, ripe crops everywhere, warm golden colors, no text, no watermark, pure visual art'},
    {'f': 'chushu_summary_fade.png', 'p': 'Chinese traditional watercolor painting, Limit of Heat solar term, summer heat fading, cool autumn breeze, transition season, no text, no watermark, pure visual art'}
]

def gen(p, out):
    try:
        from openai import OpenAI
        c = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=Config.VOLCANO_API_KEY)
        r = c.images.generate(model='doubao-seedream-3-0-t2i-250415', prompt=p, size='1920x1080', response_format='url', extra_body={'watermark': False})
        if r.data:
            open(out, 'wb').write(requests.get(r.data[0].url, timeout=60).content)
            return True
    except: pass
    return False

print('处暑图片生成')
for i, img in enumerate(PROMPTS, 1):
    out = OUTPUT_DIR / img['f']
    if out.exists(): print(f'[{i}/5] SKIP'); continue
    if gen(img['p'], str(out)): print(f'[{i}/5] OK')
    else: print(f'[{i}/5] FAIL')
    time.sleep(0.5)
print('完成')
