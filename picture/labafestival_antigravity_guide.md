# anti-gravity 图像生成指南

## 📝 说明

anti-gravity是一个本地API代理服务，主要用于调用**文本大语言模型**，它本身**不直接提供图像生成功能**。

但是，我们可以通过以下方式利用anti-gravity：

### 方法1: 使用anti-gravity生成优化的图像提示词

```python
from openai import OpenAI

# 连接anti-gravity
client = OpenAI(
    base_url="http://127.0.0.1:8045/v1",
    api_key="your-antigravity-api-key-here"
)

# 使用Claude生成详细的图像描述
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20240620",
    messages=[
        {
            "role": "user",
            "content": """
请为腊八节中国风水彩画生成一个详细的英文提示词，包括：

1. 画面主体：青花瓷碗装腊八粥
2. 配景：左侧竹子、右上角梅花
3. 背景：水墨晕染效果
4. 文字：书法"腊八节"
5. 印章：红色印章

要求描述详细、专业，适合AI绘图工具使用。
请直接返回英文提示词。
            """
        }
    ],
    max_tokens=1000,
    temperature=0.7
)

prompt = response.choices[0].message.content
print(prompt)
```

### 方法2: 结合anti-gravity + 免费图像生成API

```python
from openai import OpenAI
import requests
from PIL import Image
import io
import urllib.parse

# 1. 使用anti-gravity生成提示词
client = OpenAI(
    base_url="http://127.0.0.1:8045/v1",
    api_key="your-antigravity-api-key-here"
)

print("正在使用anti-gravity生成图像提示词...")
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20240620",
    messages=[{
        "role": "user",
        "content": "Generate a detailed English prompt for a Chinese watercolor painting of Laba Festival with blue and white porcelain bowl, Laba porridge, bamboo, plum blossoms, ink wash background, Chinese calligraphy, and red seal."
    }],
    max_tokens=500
)

ai_prompt = response.choices[0].message.content
print(f"AI生成的提示词:\n{ai_prompt}\n")

# 2. 使用Pollinations.ai免费API生成图像
print("正在使用Pollinations.ai生成图像...")
encoded_prompt = urllib.parse.quote(ai_prompt.strip())
url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

img_response = requests.get(url, timeout=120)
if img_response.status_code == 200:
    img = Image.open(io.BytesIO(img_response.content))
    img.save("腊八节_anti_gravity联合生成.png", 'PNG')
    print("图像已保存!")
    img.show()
```

## 🚀 快速使用步骤

### 步骤1: 启动anti-gravity服务

1. 打开 `C:\Users\yingy\AppData\Local\Antigravity Tools\antigravity_tools.exe`
2. 点击启动服务
3. 确认服务运行在 `http://127.0.0.1:8045`

### 步骤2: 运行生成脚本

```bash
cd C:\D\CAIE_tool\MyAIProduct\draw
python labafestival_antigravity.py
```

### 步骤3: 查看结果

脚本会：
- 列出anti-gravity中可用的模型
- 尝试使用支持图像生成的模型（如果有）
- 使用文本模型生成优化的图像描述
- 将描述保存为文本文件

## 💡 anti-gravity的主要用途

anti-gravity最适合用于：
- ✅ 生成详细的图像描述/提示词
- ✅ 分析和优化现有的提示词
- ✅ 多轮对话优化图像生成参数
- ❌ **不直接生成图像**（需要配合外部图像生成API）

## 🎯 推荐工作流

```
anti-gravity (文本模型)
    ↓
生成优化的英文提示词
    ↓
Pollinations.ai / DALL-E / Midjourney
    ↓
生成最终图像
```

## 📊 已生成的图像

当前已成功生成5张腊八节水彩画：

1. 腊八节水彩画.png - Python代码生成
2. 腊八节_AI生成_Pollinations.png - AI生成（主图）
3. 腊八节_版本1_写实风格.png - AI生成
4. 腊八节_版本2_艺术风格.png - AI生成
5. 腊八节_版本3_简约风格.png - AI生成

所有图像保存在：`C:\D\CAIE_tool\MyAIProduct\draw\`

## 🔧 故障排查

### 问题：anti-gravity服务未运行

**解决：**
1. 手动打开 `antigravity_tools.exe`
2. 点击启动按钮
3. 确认端口8045正在监听

### 问题：找不到图像生成模型

**说明：**
这是正常的！anti-gravity主要是文本模型代理服务。
使用方法1或方法2来生成图像。

---

**总结：** anti-gravity是强大的文本模型工具，可以配合其他图像生成API使用，达到最佳效果！
