# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AI-Powered Chinese Content Creation Platform** - 内容创作工具管理平台

## Quick Start

```bash
# Tool Manager (main entry point)
python tool_manager.py          # http://localhost:5000

# Standalone services
python picture/standalone_image_generator_v9.py  # http://localhost:5009
python article/toutiao_web_app.py                 # http://localhost:5014
```

## Architecture

### Multi-Service Platform

| Service | Port | Purpose |
|---------|------|---------|
| **Tool Manager** | 5000 | Central orchestration hub |
| **Image Generator** | 5009 | AI image generation (8-model fallback) |
| **Article Generator** | 5014 | Toutiao article generation |

### 8-Level Image Generation Fallback

```
1. Gemini 3 Flash Image → 2. Antigravity → 3. Seedream 5.0 → 4. Seedream 4.5
→ 5. Seedream 4.0 → 6. Seedream 3.0 → 7. CogView-3-flash → 8. Pollinations
```

### Configuration Management

All configuration in `config.py`:
- API keys loaded from `.env` file
- **ZhipuAI text generation**: Use `get_zhipu_anthropic_client()`

```python
from config import get_zhipu_anthropic_client
client = get_zhipu_anthropic_client()
response = client.messages.create(model="glm-4-flash", messages=[...])
content = response.content[0].text  # Anthropic-compatible format
```

## Critical Architecture Pitfalls

### toutiao_web_app.py
- HTML_TEMPLATE is embedded in Python file
- **JavaScript `\n` must be written as `\\n`** or browser syntax error

### toutiao_article_generator.py
- `create_article_html()` **returns HTML string, does not save file**
- Must manually `open().write()` to save output

### Windows Encoding Issues
- **Forbidden Unicode symbols** (✅❌⚠), use ASCII alternatives ([OK][ERROR][WARNING])
- Otherwise causes `UnicodeEncodeError: 'gbk' codec can't encode`

### Markdown to HTML Conversion
```python
# Correct: regex substitution preserves pairing
para = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', para)

# Wrong: simple replacement breaks pairing
para = para.replace('**', '<strong>').replace('**', '</strong>')
```

## Tool Manager Core Mechanisms

**Process Detection**: Uses file detection instead of process exit:
- Detects `今日头条文章_*.html` file creation
- 10-second buffer to ensure write completion
- stdout completion marker: `"[成功] HTML文件已保存"`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Server running old code | Stop Python + delete `__pycache__` + new port |
| Article generation no output | Check Chinese/English colon mixup |
| Status stuck on Running | Add `sys.stdout.flush()`, check glob pattern |
| API 429 quota | Auto-fallback to next tier |
| UnicodeEncodeError | Replace Unicode symbols with ASCII |

## Project Skills

**Location**: `.claude/skills/<skill-name>/`

| Skill | Version | Purpose |
|-------|---------|---------|
| **article-gen** | v5.3.0 | Create 今日头条 articles (fact-based, no fabrication) |
| **toutiao-img** | v3.0.0 | Generate article illustrations with table conversion |
| **image-gen** | v3.0.0 | AI images with 8-level fallback (98-99% reliability) |
| **toutiao-hot-article** | - | 爆款文章生成（命题/热搜/短句随笔） |
| **wechat-mp-operation** | - | 公众号图文交付包生成 |
| **wechat-typesetting** | - | 公众号排版格式化 |
| **xiaohongshu-card-frontend** | - | 文章转小红书卡片合集 |

```bash
python .claude/skills/article-gen/main.py create "主题"
python .claude/skills/toutiao-img/main.py article.html realistic 3
python .claude/skills/image-gen/main.py "prompt"
```

## Dependencies

```bash
pip install flask openai pillow requests python-dotenv zhipuai
```

## Version History (Recent 2)

- **2026-03-04**: v3.9/v9.8 - 8级 Fallback 链升级 + 修复图片插入bug
- **2026-03-01**: v3.8/v9.7 - 7 级 fallback 链

*Full version history in backup: `backup/claude-md-cleanup-20260312/`*

## Related Documentation

- `README_CONFIG.md` - Configuration management
- `工具管理器README.md` - Tool manager usage guide
- `API调用问题排查清单.md` - API troubleshooting checklist
