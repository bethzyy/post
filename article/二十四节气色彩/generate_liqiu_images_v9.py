# -*- coding: utf-8 -*-
"""立秋节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import Config

OUTPUT_DIR = Path(__file__).parent / "images" / "liqiu"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {'f': 'liqiu_group1_wind.png', 'p': 'Chinese traditional watercolor painting, cool autumn wind blowing, high clear sky, blue and white tones, early autumn atmosphere, no text, no watermark, pure visual art'},
    {'f': 'liqiu_group2_dew.png', 'p': 'Chinese traditional watercolor painting, white dew forming on grass at dawn, moonlight reflection, pale blue and white, no text, no watermark, pure visual art'},
    {'f': 'liqiu_group3_cicada.png', 'p': 'Chinese traditional watercolor painting, autumn cicada singing its last song, melancholic atmosphere, grey and brown tones, no text, no watermark, pure visual art'},
    {'f': 'liqiu_group4_grass.png', 'p': 'Chinese traditional watercolor painting, autumn grass turning yellow, fading green, earth tones, peaceful countryside, no text, no watermark, pure visual art'},
    {'f': 'liqiu_summary_autumn.png', 'p': 'Chinese traditional watercolor painting, Beginning of Autumn solar term landscape, cool breeze, changing leaves, harvest preparation, no text, no watermark, pure visual art'}
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

print('立秋图片生成')
for i, img in enumerate(PROMPTS, 1):
    out = OUTPUT_DIR / img['f']
    if out.exists(): print(f'[{i}/5] SKIP'); continue
    if gen(img['p'], str(out)): print(f'[{i}/5] OK')
    else: print(f'[{i}/5] FAIL')
    time.sleep(0.5)
print('完成')
