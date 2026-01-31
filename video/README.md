# 视频生成对比工具使用说明

## 功能概述

视频生成对比工具支持使用多个视频生成模型为同一主题生成视频,并通过AI进行质量评价和排序,最终生成HTML对比报告。

## 支持的视频生成模型

### 当前可用模型 (2个)

#### 1. DALL-E 3 + FFmpeg动画 ✅
- **提供商**: OpenAI + FFmpeg
- **类型**: Image-to-Video
- **分辨率**: 1280x720
- **时长**: 5秒
- **效果**: 图片缓慢放大动画
- **要求**:
  - DALL-E API key (antigravity或OpenAI,已配置)
  - FFmpeg已安装
- **状态**: ✅ 功能完整(需要等待API配额恢复)

#### 2. Seedance 1.5 Pro (火山引擎) ✅ **[NEW!]**
- **提供商**: Volcano Engine (ByteDance)
- **类型**: Text-to-Video
- **分辨率**: 480P/720P/1080P
- **时长**: 4-12秒(可配置)
- **效果**: **真正的视频生成,支持文字转视频+音频!**
- **特性**:
  - 🎵 **有声视频**: 自动生成与画面匹配的音频
  - 🎨 **高质量**: 720p/1080p高清输出
  - ⚡ **快速生成**: 约30-60秒生成完成
- **要求**:
  - VOLCANO_API_KEY (已在.env中配置)
  - 支持异步任务轮询
- **状态**: ✅ **已开通并测试成功!**
- **配置**: 使用.env中的`VOLCANO_API_KEY`与SeeDream相同
- **模型**: `doubao-seedance-1-5-pro-251215`

### 测试中的模型 (1个)

#### 3. Gemini Veo 3.1 (Google) ⚠️
- **提供商**: Google
- **类型**: Text-to-Video
- **分辨率**: 720P/1080P
- **时长**: 8秒
- **效果**: 高质量视频生成,支持原生音频
- **要求**:
  - GEMINI_API_KEY (需要单独申请Google Cloud API key)
  - 安装google-generativeai SDK
- **状态**: ⚠️ 需要配置GEMINI_API_KEY
- **获取方式**: https://console.cloud.google.com/
- **安装SDK**:
  ```bash
  pip install google-generativeai
  ```
- **注意**: Gemini Veo不在antigravity下管理,需要直接使用Google API

### 未来可添加模型

需要付费API,不在antigravity管理下:
- ❌ Pika Labs (独立API)
- ❌ Runway Gen-2/Gen-3 (独立API)
- ❌ Stability SVD (独立API)

## 使用方法

### 基本使用

```bash
cd C:\D\CAIE_tool\MyAIProduct\post\video
python video_generation_comparison.py
```

然后输入提示词,例如:
```
A cute orange cat sleeping in sunlight
```

### 批处理使用

```bash
echo "Your prompt here" | python video_generation_comparison.py
```

## 输出结果

### 1. 生成的文件

所有文件保存在 `video_comparison_output/` 目录:

```
video_comparison_output/
├── Pollinations_SVD_20260130_093906.mp4    # Pollinations生成的视频
├── DALL-E_3_+_动画_20260130_093906.mp4     # DALL-E+FFmpeg生成的视频
└── video_comparison_20260130_093906.html   # HTML对比报告
```

### 2. HTML报告内容

- 📝 **提示词展示**: 显示用户输入的主题
- 🎬 **视频播放**: 内嵌视频播放器,可直接在浏览器中查看
- 🤖 **AI评价**: 使用ZhipuAI GLM模型对生成的视频进行评分和排序
- 📊 **质量对比**: 文件大小、格式等技术指标对比
- 🏆 **排名展示**: 根据AI评价对视频进行排名

### 3. AI评价标准

AI评价从以下三个维度打分(1-10分):

1. **技术质量**: 分辨率、流畅度、文件完整性
2. **创意表现**: 是否符合提示词要求
3. **视觉效果**: 色彩、构图、动画效果

## 依赖要求

### 必需依赖

```bash
pip install requests zhipuai
```

### 可选依赖(用于DALL-E+动画模式)

```bash
pip install openai
```

### FFmpeg安装(用于DALL-E+动画模式)

**Windows:**
1. 下载FFmpeg: https://ffmpeg.org/download.html
2. 解压并添加到系统PATH
3. 验证安装: `ffmpeg -version`

**或者使用Chocolatey安装:**
```bash
choco install ffmpeg
```

## 配置

### 环境变量配置

在项目根目录的 `.env` 文件中配置:

```bash
# ZhipuAI配置(用于AI评价)
ZHIPU_API_KEY=your_zhipuai_api_key

# OpenAI配置(用于DALL-E生成)
OPENAI_API_KEY=your_openai_api_key

# Anti-gravity配置(可选,用于通过代理访问OpenAI)
ANTIGRAVITY_BASE_URL=http://127.0.0.1:8045/v1
ANTIGRAVITY_API_KEY=sk-xxx
```

## 功能特性

### 1. 多模型支持

- 同时测试多个视频生成模型
- 支持Text-to-Video和Image-to-Video两种模式
- 自动跳过未配置API key的模型

### 2. AI智能评价

- 使用ZhipuAI GLM-4.6模型进行质量分析
- 从技术、创意、视觉三个维度评价
- 自动生成排名和评价报告

### 3. 精美的HTML报告

- 响应式设计,支持多种屏幕尺寸
- 内嵌视频播放器
- 排名徽章显示
- 渐变色设计,视觉效果美观

### 4. 断点续传

- 自动检测已生成的视频
- 支持中断后继续生成

## 常见问题

### Q1: DALL-E生成失败(429错误)

**原因**: API配额已用尽

**解决方案**:
- 等待配额恢复(通常5小时)
- 或使用不同的API key
- 或仅使用Pollinations SVD模型

### Q2: FFmpeg未找到

**错误信息**: `FFmpeg未安装,无法创建视频`

**解决方案**:
1. 安装FFmpeg: `choco install ffmpeg`
2. 或跳过DALL-E+动画模式

### Q3: AI评价失败

**原因**: ZhipuAI API key未配置或配额不足

**解决方案**:
- 配置正确的ZhipuAI API key
- 或跳过AI评价,仅生成视频

### Q4: 生成的文件不是视频

**说明**: Pollinations当前可能返回GIF或PNG格式

**解决方案**:
- 工具会自动识别文件类型
- HTML报告会标注实际文件格式
- GIF和PNG也可以在浏览器中查看

## 扩展开发

### 添加新的视频生成模型

在 `VIDEO_GENERATION_MODELS` 字典中添加配置:

```python
'your-model': {
    'name': 'Your Model Name',
    'description': 'Model description',
    'provider': 'Provider Name',
    'type': 'text-to-video',  # 或 'img-to-video'
    'enabled': True  # 或 False(需要API key)
}
```

然后实现对应的生成函数:

```python
def generate_with_your_model(prompt, output_path):
    # 实现生成逻辑
    return {
        'success': True/False,
        'file_path': str(output_path),
        'file_size': size,
        'file_type': 'mp4',
        'message': '成功信息'
    }
```

在 `main()` 函数中添加调用:

```python
elif model_id == 'your-model':
    result = generate_with_your_model(prompt, output_path)
```

## 示例

### 示例1: 生成猫咪视频

```bash
cd C:\D\CAIE_tool\MyAIProduct\post\video
python video_generation_comparison.py
```

输入提示词:
```
一只可爱的橘猫在阳光下打盹
```

### 示例2: 生成风景视频

提示词:
```
Aerial view of a beautiful mountain landscape at sunset
```

### 示例3: 生成科幻视频

提示词:
```
Futuristic city with flying cars and neon lights
```

## 更新日志

### v1.0.0 (2026-01-30)

- ✅ 初始版本发布
- ✅ 支持Pollinations SVD(免费)
- ✅ 支持DALL-E 3 + FFmpeg动画
- ✅ AI评价功能
- ✅ HTML对比报告生成
- ✅ 多模型对比测试

## 技术支持

如有问题,请检查:
1. 依赖是否正确安装
2. API key是否配置
3. FFmpeg是否安装(用于DALL-E+动画模式)
4. 网络连接是否正常

## 许可证

MIT License
