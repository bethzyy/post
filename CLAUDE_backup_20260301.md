# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **AI-Powered Chinese Content Creation Platform** - a comprehensive toolkit for generating AI articles, images, and managing content creation workflows. It serves as both a production platform for content creation and a research tool for comparing AI models.

**Working Directory**: `C:\D\CAIE_tool\MyAIProduct\post`

**Key Components**:
- **Tool Manager**: Flask-based web interface for managing and executing tools
- **Article Generator**: AI-powered article creation with image generation
- **Image Generation**: Multi-API image generation with automatic fallback
- **Video Downloader**: Baidu video downloading with Selenium automation
- **Testing Tools**: API validation and quota monitoring

## Quick Start Commands

### Launch Tool Manager (Web Interface - Primary Method)
```bash
# Double-click the batch file (recommended)
启动工具管理器.bat

# Or direct Python execution
python tool_manager.py

# Access web interface at: http://localhost:5000
# The batch file automatically opens browser and minimizes server window
```

### Launch Standalone Web Services
```bash
# AI Image Generator V9.7 (7-level fallback)
cd picture && python standalone_image_generator_v9.py
# Access at: http://localhost:5009

# Toutiao Article Generator Web App
cd article && python toutiao_web_app.py
# Access at: http://localhost:5010
```

### Run Individual Tools
```bash
# Article generation
cd article && python toutiao_article_generator.py

# Festival image generation
cd picture && python generate_festival_images.py

# Video download
cd video && python baidu_video_downloader.py

# API testing
cd test && python test_antigravity_models_complete.py
```

## Directory Structure

The project is organized into functional categories:

### `/article` - Content Creation Tools (30+ files)
AI-powered article generation for Chinese social media platforms (今日头条/Toutiao).

**Key Tools**:
- **`toutiao_web_app.py`** - **PRIMARY WEB INTERFACE** (Standalone Flask app)
  - Port: 5010 (http://localhost:5010)
  - Two modes: Theme generation (主题生成) and Draft improvement (草稿完善)
  - SSE streaming for real-time progress updates
  - Parameter persistence via localStorage
  - Generated HTML viewable via `/view/<filename>` endpoint
  - Uses `toutiao_article_generator.py` for core generation logic

- **`toutiao_article_generator.py`** - Core article generator (v3.8)
  - Two modes: Theme generation (AI from scratch) or Draft improvement (AI optimizes user draft)
  - Supports 1500-2500 word articles with AI-generated images
  - Uses ZhipuAI GLM-4-flash for text generation
  - Image generation: 7-level fallback chain (same as standalone_image_generator_v9.py)
  - **Critical**: Image generation takes 30-60 seconds per image
  - Output: HTML files with embedded base64 images
  - Filename pattern: `今日头条文章_{theme}_{timestamp}.html`
  - **Key Method**: `create_article_html()` returns HTML string (does NOT save to file)

- `generate_food_article_images.py` - Food article generator
- `article_review_and_revision.py` - AI-assisted editing

**Reference Documents**:
- `今日头条真实数据分析报告_2026.md` - Platform analytics
- `今日头条高赞范文_*.md` - High-engagement examples

**Content Structure** (for 今日头条 articles):
- Title (10%): Numbers + curiosity + benefit
- Hook Intro (10%): Grab attention
- Main Content (70%): Value delivery, storytelling
- Summary (15%): Key takeaways
- Engagement (5%): Call-to-action

### `/picture` - Image Generation Tools (24 files)
Festival and themed image generation with multi-model comparison.

**Key Tools**:
- **`standalone_image_generator_v9.py`** (V9.7) - **PRIMARY IMAGE GENERATOR**
  - Standalone Flask web service on port 5009
  - 7-level fallback chain: Seedream 5.0/4.5/4.0/3.0 → Antigravity → CogView → Pollinations
  - Supports batch generation with custom save paths
  - 7 styles: 国风工笔, 国风水墨, 水彩画, 油画, 动漫插画, 写实摄影, 卡通插画
  - Reference image support (image-to-image via binary_data_base64)
  - Input format: Every 2 lines = 1 image (Line 1: filename, Line 2: description)
  - Launch: `python standalone_image_generator_v9.py` → http://localhost:5009

- `generate_festival_images.py` - Customizable festival image generator
- Supports multiple models: Gemini, Pollinations, Volcano/Seedream

### `/video` - Video Download Tools (7 files)
Baidu video downloader with Selenium automation.

**Key Tools**:
- **`baidu_video_downloader.py`** (v2.0) - Primary video downloader
  - Uses Selenium with undetected-chromedriver
  - Bypasses anti-scraping measures
  - Supports multiple Baidu video platforms
  - Automatic filename generation

**Dependencies**: Chrome, ChromeDriver, undetected-chromedriver

### `/hotspot` - AI Trends Research (12 files)
2026 AI trend analysis and real-time search tools.

**Key Tool**: `ai_trends_2026_comparison.py` - Multi-model trend comparison

### `/test` - API Testing and Quota Monitoring (7 files)
Model validation, quota monitoring, and API diagnostics.

**Key Tools**:
- **`test_antigravity_models_complete.py`** - **PRIMARY TESTING TOOL**
  - Tests ALL 28 Antigravity models (14 text + 14 image)
  - Automatic quota recovery time prediction
  - Generates HTML report with recovery estimates
  - Auto-opens report in browser

- `check_quota_status.py` - Monitor API quotas
- `retry_until_available.py` - Auto-retry when quota exhausted

**Documentation**:
- `配额状态说明.md` - Detailed quota status explanations
- `配额恢复功能更新说明.md` - Quota recovery feature documentation

### `/bird` - Chinese Bird Painting Tools (35 files)
Traditional Chinese painting generation with step-by-step tutorials.

**Special Feature**: AI self-correction system to ensure composition matches reference image

## Configuration Management

### Core Configuration: `config.py`

All API keys and settings are managed through `config.py` which reads from `.env`:

```python
from config import (
    get_antigravity_client,     # For Gemini/DALL-E/Flux via proxy
    get_volcano_client,         # For Volcano/Seedream
    get_zhipuai_client,         # For ZhipuAI GLM models (native SDK)
    get_zhipu_anthropic_client, # For ZhipuAI via Anthropic-compatible API (PREFERRED)
    Config                      # Access configuration values
)
```

**IMPORTANT: ZhipuAI API Selection**

When using ZhipuAI GLM models for text generation, **ALWAYS use the Anthropic-compatible interface**:

```python
# CORRECT - Use Anthropic-compatible client
from config import get_zhipu_anthropic_client

client = get_zhipu_anthropic_client()  # Returns Anthropic client
response = client.messages.create(
    model="glm-4-flash",  # or glm-4.6
    max_tokens=4000,
    messages=[{"role": "user", "content": prompt}]
)
content = response.content[0].text
```

```python
# AVOID - Native ZhipuAI SDK (different response format)
from config import get_zhipuai_client
client = get_zhipuai_client()  # Different API structure
```

**Why Anthropic-compatible?**:
- Consistent API format with other tools
- Standard `response.content[0].text` pattern
- Better error handling compatibility

### Required Environment Variables (`.env` file)
```bash
# anti-gravity proxy (PRIMARY - for most image generation)
ANTIGRAVITY_BASE_URL=http://127.0.0.1:8045/v1
ANTIGRAVITY_API_KEY=sk-xxx

# ZhipuAI (for article text generation)
ZHIPU_API_KEY=xxx

# Volcano/Seedream (fallback image generation)
VOLCANO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
VOLCANO_API_KEY=xxx

# OpenAI (optional)
OPENAI_API_KEY=xxx

# Image generation defaults
IMAGE_DEFAULT_SIZE=1024x1024
IMAGE_QUALITY=standard
```

**CRITICAL**: Never commit `.env` file. API keys are loaded from environment only.

## Tool Manager System (Flask Web Interface)

### Architecture

**File**: `tool_manager.py` (633 lines)

The Flask-based tool manager provides a web interface for:
- **Three-column layout**: Tool navigation (tree), tool details, execution logs
- **Process management**: Async tool execution with real-time status monitoring
- **Dynamic forms**: Custom input fields per tool (via `TOOL_DESCRIPTIONS` config)
- **Status detection**: Intelligent completion detection for long-running tasks

**API Endpoints**:
- `GET /` - Main web interface
- `GET /api/tools` - List all tools by category
- `POST /api/run` - Execute a tool (supports dynamic input forms)
- `GET /api/status/<process_id>` - Check running status
- `POST /api/stop` - Stop running tool
- `POST /api/delete` - Delete tool files
- `GET /api/tool-details/<path:path>` - Get detailed tool info

### Critical: Status Detection Mechanism

**Lines 464-488**: Smart completion detection for `toutiao_article_generator.py`

The tool manager uses **file-based completion detection** instead of relying on process exit:

```python
# For article generator, checks if HTML file was created
if tool_path and 'toutiao_article_generator' in str(tool_path):
    article_dir = tool_path.parent
    html_files = list(article_dir.glob('今日头条文章_*.html'))

    if html_files:
        latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
        file_age = time.time() - latest_html.stat().st_mtime

        # File must be >10s old (to ensure write complete)
        # and created after process started
        if file_age > 10 and file_age < elapsed_time:
            return jsonify({'status': 'completed', ...})
```

**Why This Approach**:
- Image generation via Anti-gravity API takes 30-60 seconds per image
- Process may stay alive waiting for browser to open
- File existence is more reliable than process polling
- 10-second buffer ensures file write completion

**Fallback Detection** (Lines 490-513):
- Checks stdout for completion markers: `"生成完成!"` or `"[成功] HTML文件已保存"`
- 5-minute timeout with success marker check
- Works on Windows where `fcntl` non-blocking I/O is unavailable

### Tool Configuration

**Tool Descriptions** are defined in `TOOL_DESCRIPTIONS` dict (lines 26-140+):

```python
TOOL_DESCRIPTIONS = {
    "article/": {
        "toutiao_article_generator.py": {
            "description": "生成器 - 今日头条文章生成器 v3.1...",
            "needs_input": True,
            "input_fields": [
                {"name": "mode", "label": "生成模式", "type": "select", ...},
                {"name": "theme", "label": "文章主题", "type": "text", ...},
                # ... more fields
            ]
        }
    }
}
```

**Input Field Types**:
- `text` - Text input
- `select` - Dropdown selection (with `options` array)
- `textarea` - Multi-line text
- Properties: `label`, `placeholder`, `required`, `default`

### Adding New Tools

**Method 1**: Add to `TOOL_DESCRIPTIONS` in `tool_manager.py`

**Method 2**: Place `.py` file in any category directory - auto-discovered with default description

**Method 3**: Create new category subdirectory

### Windows-Specific: Launcher Script

**File**: `启动工具管理器.bat`

```batch
@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "" http://localhost:5000
start /min python tool_manager.py
exit
```

**Features**:
- Sets UTF-8 encoding (chcp 65001)
- Auto-opens browser to http://localhost:5000
- Starts Python server minimized in background
- Exits launcher CMD window (clean UX)

## Image Generation Model Priority (7-Level Fallback Chain)

**MUST follow this priority order** (V9.7 - updated 2026-03-01):

The image generation system uses a 7-level fallback chain to maximize success rate:

### Fallback Chain Order
1. **Seedream 5.0** (`doubao-seedream-5-0-260128`) - Latest, highest quality
2. **Seedream 4.5** (`doubao-seedream-4-5-251128`) - High quality
3. **Seedream 4.0** (`doubao-seedream-4-0-250828`) - Stable version
4. **Seedream 3.0 t2i** (`doubao-seedream-3-0-t2i-250415`) - Free tier
5. **Antigravity** (Gemini 3 Flash → Flux 1.1 Pro → Flux Schnell → DALL-E 3)
6. **CogView-3-flash** (ZhipuAI free model)
7. **Pollinations** (Free public service, unlimited)

### Seedream Models (Volcano Engine)
```python
from config import get_volcano_client
client = get_volcano_client()

# Seedream 5.0/4.5/4.0 use 2048x2048
response = client.images.generate(
    model="doubao-seedream-5-0-260128",  # or 4-5, 4-0
    prompt=prompt,
    size="2048x2048",  # MUST use this size for 5.0/4.5/4.0
    response_format="url",
    extra_body={"watermark": False}
)
image_url = response.data[0].url

# Seedream 3.0 t2i uses 1024x1024
response = client.images.generate(
    model="doubao-seedream-3-0-t2i-250415",
    prompt=prompt,
    size="1024x1024",  # 3.0 t2i supports smaller size
    response_format="url",
    extra_body={"watermark": False}
)
```

### Model Name Mapping
When returning model names to users, use friendly names:
```python
model_name_map = {
    "doubao-seedream-5-0-260128": "Seedream 5.0",
    "doubao-seedream-4-5-251128": "Seedream 4.5",
    "doubao-seedream-4-0-250828": "Seedream 4.0",
    "doubao-seedream-3-0-t2i-250415": "Seedream 3.0 t2i"
}
```

### CogView-3-flash (ZhipuAI Free Model)
```python
from openai import OpenAI
client = OpenAI(
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    api_key=zhipu_api_key
)

response = client.images.generations(  # NOTE: generations() not generate()
    model="cogview-3-flash",
    prompt=prompt,
    size="1024x1024"
)
# Returns URL in response.data[0].url
```
- **Advantage**: Free, no quota limits
- **API Method**: Use `client.images.generations()` (plural), NOT `generate()`

### Pollinations.ai (Last Resort)
```python
import requests
from urllib.parse import quote
url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
response = requests.get(url, timeout=60)
```
- **Advantage**: No quota limits, always available
- **Use when**: All other APIs fail

### Error Handling Pattern
```python
def generate_image_with_fallback(prompt, output_path):
    """7-level fallback chain implementation"""
    # Try Seedream 5.0 → 4.5 → 4.0 → 3.0 t2i
    for model_id, friendly_name in model_name_map.items():
        try:
            return generate_with_seedream(prompt, output_path, model_id)
        except Exception as e:
            if "429" in str(e):  # Quota exhausted
                continue
            raise

    # Try Antigravity (multiple models)
    try:
        return generate_with_antigravity(prompt, output_path)
    except Exception:
        pass

    # Try CogView-3-flash
    try:
        return generate_with_cogview(prompt, output_path)
    except Exception:
        pass

    # Last resort: Pollinations
    return generate_with_pollinations(prompt, output_path)
```

## Critical Architecture Patterns

### Article Generator Flow (`toutiao_article_generator.py` and `toutiao_web_app.py`)

**`toutiao_web_app.py`** - Standalone Flask Web App:
- Port: 5010
- HTML_TEMPLATE embedded in Python file (triple-quoted string)
- **CRITICAL**: All `\n` in JavaScript strings must be escaped as `\\n`
  ```python
  # WRONG - causes "Invalid or unexpected token" in browser
  text.split('\n')  # Python interprets as actual newline

  # CORRECT - escapes for JavaScript
  text.split('\\n')  # JavaScript receives literal \n
  ```
- SSE streaming endpoint: `POST /api/generate`
- File serving: `GET /view/<filename>` for generated HTML

**`toutiao_article_generator.py`** - Core Generator:

**Lines 49-1650**: Complete article generation pipeline

**Key Methods**:
- `improve_article_draft()` (lines 56-163) - AI draft improvement with two styles
- `generate_article_from_theme()` (lines 165-260) - Theme-based generation
- `generate_article_images()` (lines 1371-1458) - Multi-API image generation

**Image Generation** (Lines 1371-1458):
```python
def generate_article_images(self, theme, article_content, style='auto'):
    # Extracts 3 key points from article
    # Generates prompt based on style
    # Tries Anti-gravity first, falls back to free APIs
    # Returns list of (image_path, caption) tuples
```

**Style Prompts**:
- `auto` - AI intelligent selection
- `realistic` - Professional photography style
- `artistic` - Artistic illustration
- `cartoon` - Cartoon/illustration style
- `technical` - Technical diagrams (flowcharts/architecture)

**Critical Fix Applied** (Lines 1494-1496):
```python
# OLD (WRONG):
theme = "基于草稿完善"  # This appeared in generated images!

# NEW (CORRECT):
theme_for_images = draft[:200] if len(draft) > 200 else draft
```
**Lesson**: Never use internal mode strings in user-facing outputs.

### Markdown to HTML Conversion

**Lines 1007-1012**: Proper regex-based conversion

```python
import re
# Convert **bold** to <strong>
para = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', para)
# Convert newlines to <br>
para = para.replace('\n', '<br>')
return f'<p>{para}</p>'
```

**Common Pitfall** (AVOID):
```python
# WRONG - replaces ALL **, breaking pairing
para = para.replace('**', '<strong>').replace('**', '</strong>')
```

### Windows Encoding Issues

**Problem**: Windows console uses GBK encoding, CANNOT handle Unicode.

**Forbidden Characters** (cause `UnicodeEncodeError`):
- ✅ ❌ ⚠ ✓ ✗ and most emoji

**Solution**: Always use ASCII text markers:
- `[OK]` instead of ✓
- `[ERROR]` instead of ❌
- `[WARNING]` instead of ⚠
- `[成功]` instead of ✅

**Example**:
```python
# WRONG - will crash on Windows
print("✅ 图片生成成功")

# CORRECT - works everywhere
print("[成功] 图片生成成功")
```

**Reference**: Fixed in `test/test_gemini_pro_image.py` (all Unicode replaced)

## Common Development Tasks

### Creating New Article Generator

1. **Study existing pattern**: `article/toutiao_article_generator.py`
2. **Define content structure**: Title → Hook → Content → Summary → CTA
3. **Use ZhipuAI GLM-4.6**: More stable than GLM-4.7 for article generation
4. **Implement image generation**: Follow model priority (Anti-gravity → Pollinations)
5. **Create HTML output**: Embed base64 images or use relative paths
6. **Add to tool_manager.py**: Configure in `TOOL_DESCRIPTIONS`
7. **Test in web interface**: Verify form inputs work correctly

### Adding Image Generation to Existing Tool

1. **Import clients**:
```python
from config import get_antigravity_client
import requests
```

2. **Implement priority fallback**:
```python
def generate_image(prompt, filename):
    try:
        # Try Anti-gravity first
        client = get_antigravity_client()
        response = client.images.generate(model="flux-1.1-pro", ...)
        return save_b64_image(response.data[0].b64_json, filename)
    except Exception as e:
        # Fallback to Pollinations
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        return download_url(url, filename)
```

3. **Handle base64 responses**:
```python
import base64
from PIL import Image
import io

image_data = base64.b64decode(b64_json)
img = Image.open(io.BytesIO(image_data))
img.save(filename)
```

### Debugging Tool Manager Status Issues

**Problem**: Tool shows "running" indefinitely after completion

**Solutions**:

1. **Check file-based detection** (lines 464-488 in `tool_manager.py`):
   - Ensure output filename matches glob pattern
   - Verify file is saved to correct directory
   - Check 10-second buffer isn't causing delay

2. **Add completion markers** in tool stdout:
```python
print("[成功] HTML文件已保存: filename.html")
import sys
sys.stdout.flush()  # Force flush
```

3. **Verify tool_path** is stored:
```python
running_processes[process_id] = {
    'process': process,
    'tool_path': tool_path,  # Required for file detection
    ...
}
```

4. **Check Windows fcntl issue**: Non-blocking output reading doesn't work on Windows
   - Solution: Use file-based detection (already implemented)
   - Or rely on stdout completion markers

## Security and Best Practices

- **NEVER** commit `.env` file or any API keys
- **ALWAYS** use `config.py` for accessing configurations
- **HIDE** sensitive information in logs (use `Config.display()` pattern)
- **IMPLEMENT** graceful error handling for API failures
- **LOG** detailed progress for long-running operations
- **RESPECT** API rate limits - implement automatic fallback
- **USE** ASCII markers instead of Unicode for Windows compatibility
- **VALIDATE** user inputs in web forms (HTML5 validation + backend checks)
- **FLUSH** stdout after completion markers for reliable status detection
- **NEVER** use internal mode strings in user-facing outputs (filenames, prompts, content)

## Troubleshooting

### Problem: Server Running Old Cached Code
**Symptoms**: After code changes, server still behaves as before (e.g., shows "[Fallback 1/3]" instead of "[Fallback 1/7]")

**Root Cause**: Python bytecode cache (`__pycache__/`) or old processes still running

**Solution**:
```bash
# 1. Kill all Python processes (use PowerShell for reliability)
powershell -Command "Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force"

# 2. Clear all Python cache
cd C:/D/CAIE_tool/MyAIProduct/post
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# 3. Restart server
python picture/standalone_image_generator_v9.py
```

**IMPORTANT**: On Windows, `taskkill /F /IM python.exe` often fails silently. Use PowerShell's `Stop-Process -Force` instead.

### Problem: Article Generator Fails Silently (No Output File)
**Symptoms**: Tool shows "运行完成" but no HTML file is generated

**Root Causes & Solutions**:

1. **Chinese/English Colon Mismatch in Title Parsing**
   - AI may return `标题：` (Chinese colon) but code only checks for `标题:` (English colon)
   - **Solution** (applied to `toutiao_article_generator.py`):
   ```python
   # Support both Chinese and English colons
   if line.startswith("标题:") or line.startswith("标题："):
       title = line.replace("标题:", "").replace("标题：", "").strip()
   ```

2. **GBK Encoding Crash When Printing AI Response**
   - AI responses contain emoji (🌟, 🔍, etc.) which crash Windows GBK console
   - **Solution**: Safe print with encoding replacement:
   ```python
   try:
       safe_content = content[:200].encode('gbk', errors='replace').decode('gbk')
       print(f"[DEBUG] Response: {safe_content}")
   except:
       print(f"[DEBUG] Response: [contains special characters]")
   ```

### Problem: Unicode Encoding Error
```
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713'
```
**Solution**: Replace all Unicode symbols (✓, ❌, ⚠, ✅) with ASCII equivalents ([OK], [ERROR], [WARNING], [成功])

### Problem: API Returns 429 Quota Exceeded
**Solution**: Implement automatic fallback:
1. Try Anti-gravity (primary)
2. Fallback to Pollinations (free, unlimited)
3. Display warning to user about quota status

### Problem: Tool Manager Port Already in Use
**Solution**: Change port in `tool_manager.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Problem: Status Stuck on "Running"
**Solution**:
1. Add `sys.stdout.flush()` after completion marker
2. Check file path matches glob pattern in status detection
3. Verify `tool_path` is in `running_processes` dict
4. Consider 10-second buffer for file write completion

### Problem: Generated Images Have Wrong Text
**Solution**: Check prompt construction:
- Never pass internal mode strings to image generation
- Extract actual content from user input
- Use descriptive prompts based on article content

## Dependencies

**Core Requirements**:
```bash
pip install flask openai pillow requests python-dotenv zhipuai
```

**Optional (for video download)**:
```bash
pip install selenium webdriver-manager
```

**Packages**:
- `flask` - Tool manager web interface
- `openai` - OpenAI-compatible API clients (Anti-gravity, Volcano)
- `pillow` (PIL) - Image processing and base64 conversion
- `requests` - HTTP requests (Pollinations, URL downloads)
- `python-dotenv` - Environment variable management
- `zhipuai` - ZhipuAI GLM models for text generation

## Related Documentation

- `README_CONFIG.md` - Configuration management details
- `工具管理器README.md` - Tool manager user guide
- `工具管理器使用指南.md` - Quick start guide
- `API调用问题排查清单.md` - API troubleshooting
- `picture/画图模型选择原则.md` - Model selection principles
- `article/今日头条真实数据分析报告_2026.md` - Platform analytics
- `article/今日头条文章生成器使用指南.md` - Article generator guide
