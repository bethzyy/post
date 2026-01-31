# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AI-Powered Chinese Art and Content Creation Platform** - a comprehensive toolkit for generating traditional Chinese art, educational content, and social media articles. It serves as both a research platform for comparing AI image generation models and a production tool for content creation.

**Working Directory**: `C:\D\CAIE_tool\MyAIProduct\draw`

## Quick Start Commands

### Launch Tool Manager (Web Interface)
```bash
# Method 1: Using batch script (recommended)
启动工具管理器.bat

# Method 2: Direct Python
python tool_manager.py

# Access web interface at: http://localhost:5000
```

### Run Individual Tools
```bash
# All tools can be run directly from their directories
cd bird && python bird_painting_steps_generator.py
cd picture && python generate_festival_images.py
cd article && python generate_food_article_images.py
cd hotspot && python ai_trends_2026_comparison.py
cd test && python test_gemini_pro_image.py
```

### Generate Documentation
```bash
python generate_tool_docs.py
# Creates tool_documentation.json with descriptions of all tools
```

## Directory Structure

The project is organized into 5 functional categories:

### `/bird` - Chinese Bird Painting Tools (35 files)
Traditional Chinese painting generation with step-by-step tutorials.
- **Key Tools**: `bird_painting_steps_generator.py`, `bird_painting_self_correction.py`
- **Reference**: `bird.jpg` (reference image for composition matching)
- **Output**: 6-step painting tutorials (pencil sketch → base colors → form → details → refinement → framing)
- **Special Feature**: AI self-correction system to ensure composition matches reference

### `/picture` - Festival Image Generation (24 files)
Traditional Chinese festival themed image generation.
- **Subdirectories**: Laba Festival (腊八节), Little New Year (小年)
- **Key Tool**: `generate_festival_images.py` - customizable festival image generator
- **Models**: Gemini, Pollinations, Volcano/Seedream comparison
- **Documentation**: `画图模型选择原则.md` (model selection principles)

### `/article` - Content Creation Tools (30 files)
Article generation for social media platforms (今日头条/Toutiao).
- **Key Tools**:
  - `toutiao_article_generator.py` - viral article generator
  - `generate_food_article_images.py` - food articles with images
  - `article_review_and_revision.py` - AI-assisted editing
- **Reference Documents**:
  - `今日头条真实数据分析报告_2026.md` - platform analytics
  - `今日头条高赞范文_*.md` - high-engagement examples
- **Output**: 1500-2500 word articles with 3-5 generated images

### `/hotspot` - AI Trends Research (12 files)
2026 AI trend analysis and real-time search tools.
- **Key Tool**: `ai_trends_2026_comparison.py` - multi-model trend comparison
- **Features**: Real-time web search, multi-API comparison, HTML reports
- **Architecture**: See `realtime_search_architecture.md`

### `/test` - API Testing Tools (7 files)
Model validation and quota monitoring.
- **Key Tools**:
  - `test_gemini_pro_image.py` - test Gemini image generation
  - `test_antigravity_models.py` - test multiple models
  - `check_quota_status.py` - monitor API quotas
  - `retry_until_available.py` - auto-retry when quota exhausted

## Configuration Management

### Core Configuration: `config.py`

All API keys and settings are managed through `config.py` which reads from `.env`:

```python
from config import (
    get_antigravity_client,  # For Gemini/DALL-E via proxy
    get_volcano_client,      # For Volcano/Seedream
    get_zhipuai_client,      # For ZhipuAI GLM models
    Config                   # Access configuration values
)
```

### Required Environment Variables (`.env` file)
```bash
# anti-gravity proxy (for Gemini image generation)
ANTIGRAVITY_BASE_URL=http://127.0.0.1:8045/v1
ANTIGRAVITY_API_KEY=sk-xxx

# Volcano/Seedream (ByteDance image generation)
VOLCANO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VOLCANO_API_KEY=xxx

# ZhipuAI (GLM models for text generation)
ZHIPU_API_KEY=xxx

# Image generation defaults
IMAGE_DEFAULT_SIZE=1024x1024
IMAGE_QUALITY=standard
```

**CRITICAL**: Never commit `.env` file. API keys are loaded from environment only, no hardcoded defaults.

## Image Generation Model Priority

**MUST follow this priority order** (see `picture/画图模型选择原则.md`):

### 1. Gemini (First Priority)
```python
client = get_antigravity_client()
response = client.images.generate(
    model="gemini-3-pro-image-4k",  # or "gemini-3-pro-image-2k"
    prompt=prompt,
    size="1024x1024"
)
# Returns base64 in response.data[0].b64_json
```
- **Quality**: Best composition and detail accuracy
- **Limit**: ~250 images/day (free tier), returns HTTP 429 when exhausted
- **Use for**: All important image generation tasks

### 2. Volcano/Seedream (Second Priority)
```python
client = get_volcano_client()
response = client.images.generate(
    model="doubao-seedream-4-5-251128",
    prompt=prompt,
    size="2K",
    response_format="url",
    extra_body={"watermark": False}  # No AI watermark
)
# Must download from URL
image_url = response.data[0].url
img_response = requests.get(image_url)
with open(filename, 'wb') as f:
    f.write(img_response.content)
```
- **Advantage**: No watermark, stable performance
- **Use for**: Fallback when Gemini returns 429

### 3. Pollinations.ai (Third Priority)
```python
import requests
url = f"https://image.pollinations.ai/prompt/{prompt}"
response = requests.get(url, timeout=60)
with open(filename, 'wb') as f:
    f.write(response.content)
```
- **Advantage**: No quota limits, completely free
- **Use for**: Last resort or bulk generation

### Error Handling Pattern
```python
def generate_with_priority(prompt, filename):
    try:
        return generate_with_gemini(prompt, filename)
    except Exception as e:
        if "429" in str(e):
            print("[WARNING] Gemini quota exhausted, trying Seedream")
            try:
                return generate_with_seedream(prompt, filename)
            except Exception as e2:
                print("[WARNING] Seedream failed, trying Pollinations")
                return generate_with_pollinations(prompt, filename)
        raise
```

## Key Architecture Patterns

### Tool Manager System

The Flask-based tool manager (`tool_manager.py`) provides:
- **Web Interface**: Three-column layout (tree navigation, tool details, execution logs)
- **Process Management**: Run tools asynchronously, monitor status in real-time
- **API Endpoints**:
  - `GET /api/tools` - List all tools by category
  - `POST /api/run` - Execute a tool
  - `GET /api/status/<process_id>` - Check running status
  - `POST /api/stop` - Stop running tool
  - `POST /api/delete` - Delete tool files
- **Tool Descriptions**: Defined in `TOOL_DESCRIPTIONS` dict in `tool_manager.py`

### Multi-Model Comparison Pattern

Scripts like `xiaonian_full_comparison.py` demonstrate:
1. Generate identical prompts across multiple models
2. Standardize image generation parameters
3. Create HTML gallery for side-by-side comparison
4. Generate professional evaluation reports
5. Output comparison metrics and rankings

### AI Self-Correction for Composition Matching

**Critical for tutorial generation**: When creating step-by-step painting tutorials:

1. **Reference Image**: Start with `bird.jpg` as composition reference
2. **Generate Steps**: Create 6 steps (铅笔起稿 → 铺底色 → 塑造形体 → 细节刻画 → 调整统一 → 落款装裱)
3. **Verify Composition**: Use vision API to check each step matches reference:
   - Check posture/position matches (NOT identical appearance)
   - Allow different completion levels for intermediate steps
   - Iterate until composition alignment achieved
4. **Final Output**: HTML gallery showing progression

**Implementation**: See `bird_painting_with_verification.py`, `bird_painting_self_correction.py`

### Social Media Article Generation Pattern

**Platform**: 今日头条 (Toutiao)

**Research Phase**:
1. Use WebSearch tool to find real platform data
2. Analyze high-engagement articles in `今日头条高赞范文_*.md`
3. Reference platform analytics in `今日头条真实数据分析报告_2026.md`

**Content Structure**:
- **Title** (10%): Numbers + curiosity + benefit
  - Example: "3个技巧让我从5千到3万"
- **Hook Intro** (10%): Grab attention immediately
- **Main Content** (70%): Value delivery, storytelling
- **Summary** (15%): Key takeaways
- **Engagement** (5%): Call-to-action (comments, likes)

**Technical Requirements**:
- Length: 1500-2500 words (optimal engagement)
- Images: 3-5 relevant AI-generated images
- Style: Natural language, avoid "machine feel"
- Encoding: Use UTF-8 for Chinese characters

**Implementation**: See `article/toutiao_article_generator.py`

## Critical Constraints and Best Practices

### Windows GBK Encoding Issue

**Problem**: Windows console uses GBK encoding and CANNOT handle Unicode symbols.

**Forbidden Characters** (will cause `UnicodeEncodeError`):
- ✅ ❌ ⚠ ✓ ✗ or any emoji

**Solution**: Always use ASCII text markers:
- `[OK]` instead of ✓
- `[ERROR]` instead of ❌
- `[WARNING]` instead of ⚠
- `[FAIL]` instead of ✗

**Example**:
```python
# WRONG - will crash on Windows
print("✅ API调用成功")

# CORRECT - works on all platforms
print("[OK] API调用成功")
```

**Reference**: Fixed in `test/test_gemini_pro_image.py` (all Unicode replaced with ASCII)

### API Rate Limiting

**Gemini Free Tier**:
- Limit: ~250 requests/day
- Error: HTTP 429 Too Many Requests
- Recovery: Automatic after ~5 minutes
- Strategy: Implement immediate fallback to Seedream or Pollinations

**GLM Models**:
- Also have quota limits
- Returns different error codes
- Strategy: Monitor with `test/check_quota_status.py`

### File Organization

**Generated Images**: Saved with descriptive names including timestamp and model
- Example: `bird_gemini_3_pro_image_4k_步骤1_铅笔起稿.png`
- Format: `{subject}_{model}_{step}_{description}.{ext}`

**HTML Galleries**: Auto-generated for visual comparison
- Example: `xiaonian全模型对比_20260127_211758.html`
- Used for side-by-side model evaluation

**Logs**: Created for long-running processes
- Example: `bird_self_correction.log`, `bird_volcano.log`
- Include timestamps and detailed progress tracking

### Background Process Management

Many tools run for extended periods (hours for self-correction):

```bash
# Check running background processes
# Use BashOutput tool with process_id to monitor

# Common long-running tools:
# - bird_painting_self_correction.py (may take hours)
# - multi_model_api_call.py (API comparison)
# - ai_trends_2026_comparison.py (comprehensive analysis)
```

## Tool Manager Customization

### Adding New Tools

**Method 1: Add to Existing Category**

Edit `tool_manager.py`, add to `TOOL_DESCRIPTIONS`:
```python
TOOL_DESCRIPTIONS = {
    "bird/": {
        "your_new_tool.py": "Description of your tool",
        # ... existing tools
    }
}
```

**Method 2: Add New Category**

1. Create new subdirectory (e.g., `landscape/`)
2. Add to categories dict in `get_all_tools()`:
```python
categories = {
    "landscape": "山水画工具",  # Add this
    "bird": "鸟类绘画工具",
    # ... existing categories
}
```

**Method 3: Auto-Discovery**

Place `.py` files in any category directory - they'll be auto-discovered with default descriptions.

### Frontend Customization

Template: `templates/tool_manager.html`

**Key Features**:
- Three-column resizable layout
- Tree view navigation with collapsible categories
- Real-time status updates
- Custom scrollbar styling (purple theme: #5a67d8)
- Dark gradient background

**Modifying Colors**:
```css
/* Scrollbar theme */
.tree-view::-webkit-scrollbar-thumb {
    background: #5a67d8;  /* Purple */
}

/* Accent colors */
--primary-color: #805ad5;
--success-color: #38b2ac;
--error-color: #f56565;
```

## Common Development Tasks

### Testing API Connectivity
```bash
# Test anti-gravity proxy
cd test && python test_antigravity_simple.py

# Check Gemini quota
cd test && python check_quota_status.py

# Test all models
cd test && python test_antigravity_models.py
```

### Creating New Image Generation Tool

1. **Setup**:
```python
from config import get_antigravity_client, get_volcano_client
import requests

def generate_with_priority(prompt, filename):
    """Generate image following priority order"""
```

2. **Implement Gemini (first priority)**
3. **Implement Seedream fallback (429 handling)**
4. **Implement Pollinations fallback (last resort)**
5. **Add error handling and logging**
6. **Save with descriptive filename**
7. **Test with `test/test_gemini_pro_image.py` pattern**

### Adding Article Generation

1. **Research Platform**: Read `article/今日头条真实数据分析报告_2026.md`
2. **Study Examples**: Review `article/今日头条高赞范文_*.md`
3. **Generate Content**: Use `article/toutiao_article_generator.py` as template
4. **Generate Images**: Use model priority system
5. **Create HTML**: Combine article + images in single HTML file

### Running Model Comparison

1. **Use Existing Template**: `picture/xiaonian_full_comparison.py`
2. **Modify Prompt**: Change for your subject
3. **Run Comparison**: Generates HTML gallery automatically
4. **Evaluate Results**: Professional ranking and metrics

## Security and Best Practices

- **NEVER** commit `.env` file or any API keys
- **ALWAYS** use `config.py` for accessing configurations
- **HIDE** sensitive information in logs (use `Config.display()` pattern)
- **IMPLEMENT** graceful error handling for API failures
- **LOG** detailed progress for long-running operations
- **RESPECT** API rate limits - implement automatic fallback
- **USE** ASCII markers instead of Unicode for Windows compatibility
- **VALIDATE** composition matching in tutorial generation tools

## Troubleshooting

### Problem: Unicode Encoding Error
```
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713'
```
**Solution**: Replace all Unicode symbols (✓, ❌, ⚠) with ASCII equivalents ([OK], [ERROR], [WARNING])

### Problem: Gemini Returns 429
**Solution**: Implement automatic fallback to Seedream or Pollinations (see model priority above)

### Problem: Tool Manager Port Already in Use
**Solution**: Change port in `tool_manager.py` line 388:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Use 5001 instead of 5000
```

### Problem: Module Not Found
**Solution**: Ensure proper Python path setup in tool execution:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

## Dependencies

Install required packages:
```bash
pip install flask openai pillow requests python-dotenv zhipuai anthropic
```

**Core Dependencies**:
- `flask` - Tool manager web interface
- `openai` - OpenAI-compatible API clients
- `pillow` (PIL) - Image processing
- `requests` - HTTP requests for Pollinations/URL downloads
- `python-dotenv` - Environment variable management
- `zhipuai` - ZhipuAI GLM models
- `anthropic` - Anthropic API (optional)

## Related Documentation

- `README_CONFIG.md` - Configuration management details
- `工具管理器README.md` - Tool manager user guide
- `工具管理器使用指南.md` - Quick start guide
- `API调用问题排查清单.md` - API troubleshooting
- `picture/画图模型选择原则.md` - Model selection principles
- `article/今日头条真实数据分析报告_2026.md` - Platform analytics
