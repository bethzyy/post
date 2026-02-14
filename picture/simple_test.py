# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import json

print("="*80)
print("AI Image Generator Test")
print("="*80)

# Test 1: Theme mode
print("\n[Test 1] Theme Mode - Northeast Glutinous Fire")
params = {
    "mode": "theme",
    "theme": "东北粘火烧外皮金黄酥脆,内里软糯拉丝。黄米面做皮,红豆做馅,香甜不腻",
    "style": "guofeng_gongbi"
}

try:
    print("Sending request...")
    response = requests.post(
        'http://localhost:5001/api/generate-image',
        json=params,
        timeout=120
    )

    result = response.json()

    if result.get('success'):
        print(f"[SUCCESS] Generated!")
        print(f"  Model: {result['model'].upper()}")
        print(f"  Style: {result['style']}")
        print(f"  File: {result['image_filename']}")
        print(f"  Prompt: {result['prompt']}")

        # Save test image
        import base64
        img_data = base64.b64decode(result['image_base64'])
        output_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_theme_output.png"
        with open(output_path, 'wb') as f:
            f.write(img_data)
        print(f"  Saved to: {output_path}")
    else:
        print(f"[FAILED] {result.get('error')}")

except Exception as e:
    print(f"[ERROR] {str(e)}")

print("\n" + "="*80)
print("Test completed!")
print("="*80)
