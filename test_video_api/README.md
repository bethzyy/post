# 视频生成API测试目录

此目录用于测试各种视频生成API的可用性。

## 测试结论

**目前没有找到可用的免费视频生成API。**

## 测试结果

### 1. Pollinations.ai - ✗ 不支持视频
- **状态**: 仅支持图片生成，不支持视频
- **测试**: 返回JPEG图片（512x512），不是视频文件
- **说明**: Pollinations.ai主要提供图片生成服务

### 2. Stability AI - ✗ 需要付费
- **模型**: Stable Video Diffusion (SVD)
- **状态**: 需要API key，付费服务
- **官网**: https://stability.ai/
- **定价**: 按使用量计费

### 3. RunwayML - ✗ 需要付费
- **模型**: Gen-2, Gen-3
- **状态**: 需要API key，付费服务
- **官网**: https://runwayml.com/
- **定价**: 订阅制，约$12-35/月

### 4. Pika Labs - ✗ 无公开API
- **状态**: 主要通过Web界面和Discord bot使用
- **官网**: https://pika.art/
- **说明**: 没有公开的API接口

## 推荐方案

### 方案1: 付费API服务
适合商业项目，质量最高：

1. **Stability AI**
   - Stable Video Diffusion模型
   - API文档完善
   - 按使用量付费

2. **RunwayML**
   - Gen-3最新模型
   - 质量优秀
   - 月度订阅

3. **Pika Labs**
   - 高质量视频生成
   - Web界面易用

### 方案2: 开源模型自部署
适合技术团队，成本较低：

1. **Stable Video Diffusion (SVD)**
   - Stability AI开源
   - 需要GPU部署
   - GitHub: https://github.com/Stability-AI/generative-models

2. **ModelScope**
   - 阿里开源视频生成模型
   - 支持中英文
   - GitHub: https://github.com/modelscope/modelscope

3. **AnimateDiff**
   - 基于Stable Diffusion
   - 轻量级部署
   - GitHub: https://github.com/guoyww/AnimateDiff

### 方案3: 在线工具（非API）
适合个人使用，无需编程：

1. **Pika Labs** - https://pika.art/
2. **RunwayML** - https://runwayml.com/
3. **Kaiber** - https://kaiber.ai/
4. **HeyGen** - https://www.heygen.com/

## 使用方法

```bash
cd test_video_api
python test_video_generation.py
```

## 参考资源

- [Best Text-to-Video API in 2026](https://wavespeed.ai/blog/posts/best-text-to-video-api-2026)
- [Top 10 Best AI Video Generators of 2026](https://manus.im/blog/best-ai-video-generator)
- [Best Video Generation AI Models in 2026](https://pinggy.io/amp/blog/best_video_generation_ai_models/)
- [Wan AI Video API](https://wan.video/api)

## 技术说明

视频生成技术主要分为：

1. **Text-to-Video**: 从文本描述生成视频
2. **Image-to-Video**: 从图片生成动态视频
3. **Video-to-Video**: 视频风格转换

主流技术栈：
- Stable Video Diffusion (SVD)
- Generative Video Models
- Diffusion-based video generation

## 注意事项

- 视频生成比图片生成消耗更多计算资源
- API费用通常较高（几美元到几十美元/分钟）
- 生成时间较长（几秒到几分钟）
- 需要考虑视频时长、分辨率、帧率等参数
