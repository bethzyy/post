# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import json
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

print("="*80)
print("Reference Image Test - V2")
print("="*80)

# Create a test reference image
print("\n[1] Creating test reference image...")
img = Image.new('RGB', (400, 300), color='lightblue')
draw = ImageDraw.Draw(img)

# Draw a simple scene - a red apple on a table
draw.ellipse([150, 50, 250, 150], fill='red')  # Apple
draw.rectangle([100, 150, 300, 200], fill='brown')  # Table
draw.text([150, 250], "Red Apple", fill='white')

# Save to bytes
buffer = BytesIO()
img.save(buffer, format='PNG')
buffer.seek(0)
img_bytes = buffer.read()

# Encode to base64
img_base64 = base64.b64encode(img_bytes).decode('utf-8')
print(f"[OK] Test image created ({len(img_bytes)} bytes)")

# Test API
print("\n[2] Testing API with reference image...")
params = {
    "mode": "reference",
    "reference_image": img_base64,
    "style": "guofeng_gongbi"  # Chinese traditional painting style
}

try:
    print("Sending request to http://localhost:5001/api/generate-image")
    response = requests.post(
        'http://localhost:5001/api/generate-image',
        json=params,
        timeout=120
    )

    result = response.json()

    if result.get('success'):
        print(f"\n[SUCCESS]!")
        print(f"  Model: {result['model'].upper()}")
        print(f"  Style: {result['style']}")
        print(f"  Mode: {result['mode']}")
        print(f"  Time: {result['timestamp']}")
        print(f"  File: {result['image_filename']}")
        print(f"  Prompt length: {len(result['prompt'])} chars")

        # Save generated image
        if result.get('image_base64'):
            img_data = base64.b64decode(result['image_base64'])
            output_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_reference_output_v2.png"
            with open(output_path, 'wb') as f:
                f.write(img_data)
            print(f"  Saved to: test_reference_output_v2.png")
            print(f"\n[INFO] The generated image should show the red apple in Chinese Gongbi style!")
    else:
        print(f"\n[FAILED] {result.get('error')}")

except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Test completed!")
print("="*80)
