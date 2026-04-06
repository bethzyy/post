# -*- coding: utf-8 -*-
"""小暑节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import Config

OUTPUT_DIR = Path(__file__).parent / "images" / "xiaoshu"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {'f': 'xiaoshu_group1_wind.png', 'p': 'Chinese traditional watercolor painting, hot summer wind blowing through fields, heat waves rising, reddish orange tones, no text, no watermark, pure visual art'},
    {'f': 'xiaoshu_group2_cricket.png', 'p': 'Chinese traditional watercolor painting, cricket hiding in cool corner of house, seeking shade from heat, green and blue tones, no text, no watermark, pure visual art'},
    {'f': 'xiaoshu_group3_eagle.png', 'p': 'Chinese traditional watercolor painting, eagle soaring high in clear blue sky, summer heat below, dramatic composition, no text, no watermark, pure visual art'},
    {'f': 'xiaoshu_group4_sky.png', 'p': 'Chinese traditional watercolor painting, deep blue summer sky, high altitude atmosphere, cool blue tones, serene vastness, no text, no watermark, pure visual art'},
    {'f': 'xiaoshu_summary_heat.png', 'p': 'Chinese traditional watercolor painting, Minor Heat solar term landscape, scorching summer day, cicadas singing, people seeking shade, no text, no watermark, pure visual art'}
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

print('小暑图片生成')
for i, img in enumerate(PROMPTS, 1):
    out = OUTPUT_DIR / img['f']
    if out.exists(): print(f'[{i}/5] SKIP'); continue
    if gen(img['p'], str(out)): print(f'[{i}/5] OK')
    else: print(f'[{i}/5] FAIL')
    time.sleep(0.5)
print('完成')
