# -*- coding: utf-8 -*-
"""夏至节气配图生成脚本 V9.7"""
import sys
from pathlib import Path
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import Config

OUTPUT_DIR = Path(__file__).parent / "images" / "xiazhi"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {'f': 'xiazhi_group1_deer.png', 'p': 'Chinese traditional watercolor painting, deer antlers falling on ground, summer forest, warm red and brown colors, no text, no watermark, pure visual art'},
    {'f': 'xiazhi_group2_cicada.png', 'p': 'Chinese traditional watercolor painting, cicada on tree branch singing, dark clouds gathering, summer storm approaching, dramatic sky, no text, no watermark, pure visual art'},
    {'f': 'xiazhi_group3_herb.png', 'p': 'Chinese traditional watercolor painting, pinellia herb growing in shade, dappled sunlight through leaves, summer garden, warm tones, no text, no watermark, pure visual art'},
    {'f': 'xiazhi_group4_moon.png', 'p': 'Chinese traditional watercolor painting, bright moon over summer mountains, cool night scene, white and grey tones, serene atmosphere, no text, no watermark, pure visual art'},
    {'f': 'xiazhi_summary_solstice.png', 'p': 'Chinese traditional watercolor painting, summer solstice landscape, longest day of year, sun at peak, green fields and blue sky, no text, no watermark, pure visual art'}
]

def gen(p, out):
    try:
        api_key = Config.VOLCANO_API_KEY
        from openai import OpenAI
        c = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=api_key)
        r = c.images.generate(model='doubao-seedream-3-0-t2i-250415', prompt=p, size='1920x1080', response_format='url', extra_body={'watermark': False})
        if r.data:
            requests.get(r.data[0].url, timeout=60).content
            open(out, 'wb').write(requests.get(r.data[0].url, timeout=60).content)
            return True
    except Exception as e:
        print(f'  Error: {e}')
    return False

print('夏至图片生成')
for i, img in enumerate(PROMPTS, 1):
    out = OUTPUT_DIR / img['f']
    if out.exists():
        print(f'[{i}/5] SKIP (exists)')
        continue
    if gen(img['p'], str(out)):
        print(f'[{i}/5] OK')
    else:
        print(f'[{i}/5] FAIL')
    time.sleep(0.5)
print('完成')
