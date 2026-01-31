# API密钥配置说明

## 📝 概述

draw目录中的所有Python脚本现在都使用统一的配置管理系统。

## 🔑 配置文件

### `.env` 文件

所有API密钥和敏感配置都存储在 `.env` 文件中：

```bash
# anti-gravity配置
ANTIGRAVITY_BASE_URL=http://127.0.0.1:8045/v1
ANTIGRAVITY_API_KEY=your-antigravity-api-key-here

# ZhipuAI配置
ZHIPU_API_KEY=your-zhipuai-api-key-here

# OpenAI配置（可选）
OPENAI_API_KEY=

# 其他配置
IMAGE_DEFAULT_SIZE=1024x1024
IMAGE_QUALITY=standard
```

## 🔒 安全说明

**重要：**
- ⚠️ `.env` 文件包含敏感信息，**不要**提交到Git或公开分享
- ✅ `.gitignore` 已经配置，会自动忽略 `.env` 文件
- ✅ 如果需要分享项目，请提供 `.env.example` 模板

## 📦 配置模块

### `config.py`

统一的配置管理模块，提供：

- `Config` 类：访问所有配置
- `get_antigravity_client()`：获取anti-gravity客户端
- `get_zhipuai_client()`：获取ZhipuAI客户端
- 自动加载 `.env` 文件

### 使用示例

```python
# 导入配置
from config import Config, get_antigravity_client, get_zhipuai_client

# 使用配置
print(Config.ANTIGRAVITY_BASE_URL)

# 获取客户端
client = get_antigravity_client()
response = client.chat.completions.create(...)
```

## 📂 已更新的脚本

以下脚本已更新为使用 `.env` 配置：

1. ✅ `labafestival_antigravity.py` - anti-gravity图像生成
2. ✅ `labafestival_gemini_direct.py` - Gemini直接调用
3. ✅ `test_antigravity_simple.py` - 简单测试脚本
4. ✅ `labafestival_ai_generator.py` - ZhipuAI图像生成
5. ✅ `labafestival_cogview3_sdk.py` - CogView-3 SDK调用

## 🚀 快速开始

### 1. 配置API密钥

编辑 `.env` 文件，填入您的API密钥：

```bash
# 编辑.env文件
ZHIPU_API_KEY=your.actual.api.key.here
```

### 2. 运行脚本

```bash
# 测试anti-gravity连接
python test_antigravity_simple.py

# 使用Gemini生成图像
python labafestival_gemini_direct.py
```

## 🔧 配置参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `ANTIGRAVITY_BASE_URL` | anti-gravity服务地址 | http://127.0.0.1:8045/v1 |
| `ANTIGRAVITY_API_KEY` | anti-gravity API密钥 | your-antigravity-api-key-here |
| `ZHIPU_API_KEY` | ZhipuAI API密钥 | (必须填写) |
| `OPENAI_API_KEY` | OpenAI API密钥 | (可选) |
| `IMAGE_DEFAULT_SIZE` | 默认图像尺寸 | 1024x1024 |
| `IMAGE_QUALITY` | 默认图像质量 | standard |

## 📋 检查清单

使用前请确认：

- [ ] `.env` 文件存在
- [ ] 所需的API密钥已填写
- [ ] anti-gravity服务已启动（如果使用）
- [ ] Python依赖已安装 (`openai`, `zhipuai`, `PIL`)

## 🆘 故障排查

### 问题：找不到API密钥

**错误：** `错误: 未找到ZHIPU_API_KEY`

**解决：**
1. 检查 `.env` 文件是否存在
2. 确认密钥已填写
3. 运行 `python config.py` 测试配置加载

### 问题：无法导入config

**错误：** `ModuleNotFoundError: No module named 'config'`

**解决：**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from config import Config
```

---

**更新时间：** 2026-01-26
**版本：** v1.0
