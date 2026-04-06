# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This directory contains the **二十四节气与中国传统色彩 (24 Solar Terms and Chinese Traditional Colors)** document collection - a cultural documentation project based on the book《中国传统色：故宫里的色彩美学》. It presents 384 traditional Chinese colors organized by the 24 solar terms (节气) and 72 micro-seasons (候).

**Location**: `C:\D\CAIE_tool\MyAIProduct\post\article\二十四节气色彩`

## Key Commands

### Generate Images for a Solar Term
```bash
cd "C:\D\CAIE_tool\MyAIProduct\post\article\二十四节气色彩"

# Generate images using Volcano Seedream API (V9 scripts - recommended)
python generate_guyu_images_v9.py      # 谷雨
python generate_lixia_images_v9.py     # 立夏
python generate_xiaoman_images_v9.py   # 小满
# ... etc for each solar term
```

### Generate MHTML Document (with embedded images)
```bash
python generate_mhtml.py 谷雨  # Generate MHTML for specific term
```

### View Documents via Tool Manager
Access through: http://localhost:5000 → 文档库 → 二十四节气配图文档索引

## File Structure

```
二十四节气色彩/
├── {节气名}.html                    # Original text-only documents (24 files)
├── {节气名}_配图版.html              # Illustrated HTML versions (with local images)
├── {节气名}_配图版.mhtml             # Illustrated MHTML versions (embedded images)
├── images/                          # Image storage directory
│   ├── guyu/                        # Images organized by solar term (pinyin)
│   │   ├── guyu_group1_duckweed.png
│   │   ├── guyu_group2_dove.png
│   │   ├── guyu_group3_hoopoe.png
│   │   ├── guyu_group4_twilight.png
│   │   └── guyu_summary_rain.png
│   ├── lixia/
│   ├── xiaoman/
│   └── ... (18 solar terms with images)
├── generate_{term}_images_v9.py     # Image generation scripts (V9 = Seedream API)
├── generate_mhtml.py                # MHTML document generator
├── 二十四节气与中国传统色彩.html      # Main index page
├── 二十四节气配图文档索引.html        # Illustrated documents index
├── README.md                        # Project documentation
└── 配图文档生成说明.md               # Illustration generation guide
```

## Document Types

### HTML Version (`{节气}_配图版.html`)
- References local images in `images/{term}/` directory
- Opens directly in browser
- Smaller file size, requires image files to accompany

### MHTML Version (`{节气}_配图版.mhtml`)
- Images embedded as Base64
- Self-contained single file
- Larger file size (3-4 MB each)
- Can be shared/exported independently

## Image Generation Architecture

### V9 Scripts (Current Standard)
All `generate_{term}_images_v9.py` scripts follow the same pattern:

```python
from config import Config
from openai import OpenAI

# Volcano Seedream 3.0 t2i model
client = OpenAI(base_url=Config.VOLCANO_BASE_URL, api_key=Config.VOLCANO_API_KEY)
response = client.images.generate(
    model='doubao-seedream-3-0-t2i-250415',
    prompt='Chinese traditional watercolor painting, ...',
    size='1920x1080',  # 16:9 horizontal format
    response_format='url',
    extra_body={'watermark': False}
)
```

### Image Size Convention
- **Horizontal 16:9**: `size='1920x1080'` (for illustrated documents)
- **Square 1:1**: `size='2048x2048'` (for other purposes)

### Image Naming Convention
Each solar term has 5 images:
- `{term}_group1_{theme}.png` - First color group illustration
- `{term}_group2_{theme}.png` - Second color group illustration
- `{term}_group3_{theme}.png` - Third color group illustration
- `{term}_group4_{theme}.png` - Fourth color group illustration
- `{term}_summary_{theme}.png` - Summary/conclusion illustration

## Solar Term Pinyin Mapping

| Spring | Summer | Autumn | Winter |
|--------|--------|--------|--------|
| lichun (立春) | lixia (立夏) | liqiu (立秋) | lidong (立冬) |
| yushui (雨水) | xiaoman (小满) | chushu (处暑) | xiaoxue (小雪) |
| jingzhe (惊蛰) | mangzhong (芒种) | bailu (白露) | daxue (大雪) |
| chunfen (春分) | xiazhi (夏至) | qiufen (秋分) | dongzhi (冬至) |
| qingming (清明) | xiaoshu (小暑) | hanlu (寒露) | xiaohan (小寒) |
| guyu (谷雨) | dashu (大暑) | shuangjiang (霜降) | dahan (大寒) |

## Document Format Requirements

### Color Description Format
Each color must have a specific description:
```html
<ul class="color-list">
<li>"昌荣"是草木昌盛的荣光之色</li>
<li>"紫薄汗"是薄汗浸出的淡淡紫红</li>
<li>"茈藐"是紫草的深紫色</li>
<li>"紫紶"是紫色丝带的华贵</li>
</ul>
```

### Summary Sentence
Each color group must have a summary:
```html
<p>水面上的浮萍，从嫩绿到深紫，是春天末尾水色变幻的写照。</p>
```

### Disclaimer Placement
Must appear directly after the last paragraph:
```html
<p class="disclaimer">（以上解读不代表原书观点）</p>
```

## Integration with Tool Manager

The documents are registered in `C:\D\CAIE_tool\MyAIProduct\post\tool_manager.py`:

```python
TOOL_DESCRIPTIONS = {
    "docs/": {
        "二十四节气配图文档索引.html": {
            "description": "🖼️ 二十四节气配图文档索引 (AI生成配图版)",
            "is_document": True,
            "category": "article/二十四节气色彩",
            "readme_file": "article/二十四节气色彩/配图文档生成说明.md"
        }
    }
}
```

## Current Status (2026-03-01)

| Season | Illustrated Status |
|--------|-------------------|
| Spring | 3/6 (春分, 清明, 谷雨) |
| Summer | 6/6 ✅ |
| Autumn | 6/6 ✅ |
| Winter | 6/6 ✅ |

**Total**: 21/24 solar terms have illustrated versions (HTML + MHTML)

## Adding New Solar Term Illustrations

1. Create `generate_{term}_images_v9.py` with 5 prompts
2. Run the script to generate images
3. Create HTML version with proper format
4. Generate MHTML version using `generate_mhtml.py`
5. Update `二十四节气配图文档索引.html` with links

## Dependencies

- **API**: Volcano Engine Seedream (doubao-seedream-3-0-t2i-250415)
- **Config**: Uses `config.py` from parent directory (`C:\D\CAIE_tool\MyAIProduct\post`)
- **Image Format**: PNG, 1920x1080 (horizontal)
