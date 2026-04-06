# Image Gen Skill - PRD 文档

## 文档信息

| 属性 | 值 |
|------|-----|
| **名称** | image-gen |
| **版本** | v3.0.0 |
| **状态** | ✅ 已实现 |
| **入口文件** | main.py |
| **技术栈** | Python + ZhipuAI + Volcano + Antigravity + Pollinations |
| **最后更新** | 2026-03-24 |

---

## 1. 产品概述

### 1.1 产品定位

Image Gen 是一个 AI 图像生成技能，通过 8 级回退链确保 98-99% 的生成成功率。支持多种图像风格和尺寸。

### 1.2 核心价值

- **高可靠性**: 8 级回退机制，近乎 100% 成功率
- **成本优化**: 优先尝试最快选项（Gemini → CogView）
- **多风格支持**: realistic、artistic、cartoon、technical
- **批量生成**: 支持一次生成多张图片

### 1.3 触发模式

```
"generate images", "create pictures", "make AI art",
"生成图片", "创建配图", "AI绘图"
```

---

## 2. 功能需求

### F1: 8 级回退链

| 优先级 | 模型 | 分辨率 | 提供商 |
|--------|------|--------|--------|
| 1 | Gemini 3 Flash Image | 1024x1024 | Google (Antigravity) |
| 2 | Antigravity Multi-Model | 1024x1024 | Flux/DALL-E |
| 3 | Seedream 5.0 | 2048x2048 | Volcano |
| 4 | Seedream 4.5 | 2048x2048 | Volcano |
| 5 | Seedream 4.0 | 2048x2048 | Volcano |
| 6 | Seedream 3.0 t2i | 1024x1024 | Volcano |
| 7 | CogView-3-flash | 1024x1024 | ZhipuAI |
| 8 | Pollinations | Variable | 免费公共 API |

### F2: 风格支持

| 风格 | 描述 | 提示词增强 |
|------|------|-----------|
| `realistic` | 专业摄影 | "realistic photography, high quality" |
| `artistic` | 创意优雅 | "artistic style, creative, elegant" |
| `cartoon` | 彩色插图 | "cartoon illustration, colorful" |
| `technical` | 清洁信息图 | "technical diagram, flowchart, clean" |

### F3: 输出格式

- **text**: 文本输出（默认）
- **json**: 结构化 JSON（含 model_used 字段）

### F4: 错误处理

- **429 状态码**: 配额耗尽 → 自动下一级
- **网络超时**: 重试一次 → 下一级
- **API 错误**: 记录错误 → 下一级

---

## 3. 技术架构

### 3.1 模块结构

```
.claude/skills/image-gen/
├── main.py                    # CLI 入口
├── scripts/
│   └── image_generator.py     # 核心生成逻辑
└── requirements.txt
```

### 3.2 回退逻辑

```python
def generate_image(prompt):
    for level in range(1, 9):  # 8 levels
        result = try_level(prompt, level)
        if result.success:
            return result
    return Error("All 8 fallback levels exhausted")
```

### 3.3 环境变量

```bash
# Volcano / Seedream
VOLCANO_API_KEY=your_volcano_api_key

# ZhipuAI / CogView
ZHIPU_API_KEY=your_zhipuai_api_key

# Antigravity (可选)
ANTIGRAVITY_API_KEY=your_antigravity_api_key
```

---

## 4. 使用示例

### 4.1 单图生成

```bash
python .claude/skills/image-gen/main.py "A mountain landscape"
```

### 4.2 批量生成

```bash
python .claude/skills/image-gen/main.py '["cat", "dog", "bird"]' --format json
```

### 4.3 指定风格

```bash
python .claude/skills/image-gen/main.py "futuristic city" --style artistic --output-dir ./my-images
```

### 4.4 JSON 输出

```json
{
  "success": true,
  "images": [
    {
      "path": "/path/to/img_0.jpg",
      "prompt": "A mountain landscape",
      "model_used": "gemini-3-flash-image"
    }
  ]
}
```

---

## 5. 被其他 Skill 调用

### 5.1 子进程调用

```python
import subprocess
import json

cmd = [
    sys.executable,
    '.claude/skills/image-gen/main.py',
    json.dumps(["prompt1", "prompt2"]),
    '--format', 'json'
]
result = subprocess.run(cmd, capture_output=True, text=True)
output = json.loads(result.stdout)
```

---

## 6. 依赖项

```
pillow
requests
zhipuai
openai
```

---

## 7. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.0.0 | 2026-03-08 | 迁移到 Anthropic 官方标准架构 |
| v2.1.1 | 2026-03-04 | Antigravity 提升到 Level 2 |
| v2.1.0 | 2026-03-04 | Gemini 3 Flash 提升到 Level 1 |
| v2.0.0 | 2026-03-04 | 实现 7 级回退链（核心设计） |
| v1.0.0 | 2026-03-04 | 初始版本（仅 CogView） |

---

## 8. 重要原则

> ⚠️ **8 级回退机制是核心设计，不可更改**
>
> - 移除回退 = 破坏技能
> - 必须尝试所有 8 级
> - 记录每次回退尝试
> - 返回 model_used 透明度

---

## 9. 相关文件

- **SKILL.md**: `.claude/skills/image-gen/SKILL.md`
- **主入口**: `.claude/skills/image-gen/main.py`
- **核心逻辑**: `.claude/skills/image-gen/scripts/image_generator.py`
