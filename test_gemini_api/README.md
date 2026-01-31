# Gemini API 测试目录

此目录用于独立测试Gemini API的可用性，不会影响主项目。

## 文件说明

- `test_simple_image.py` - 简单的API测试程序
  - 测试服务器状态
  - 测试图片生成功能
  - 诊断错误类型

## 使用方法

```bash
cd test_gemini_api
python test_simple_image.py
```

## 测试内容

1. **服务器状态检测**
   - 发送最小化测试请求
   - 判断服务器是否可用
   - 识别错误类型（429/503/401等）

2. **图片生成测试**
   - 生成简单的测试图片（红色圆圈）
   - 验证完整生成流程
   - 保存测试结果

## 输出文件

- `test_output_red_circle.png` - 测试生成的图片（如果成功）

## 错误诊断

程序会自动识别并报告以下错误：

- **429 Too Many Requests** - 配额限制，需等待1小时
- **503 Service Unavailable** - 服务器容量耗尽，需等待几分钟
- **401 Unauthorized** - API key问题

## 独立性

此测试目录完全独立，不会：
- 修改主项目文件
- 生成大量测试图片
- 消耗大量API配额

## 适用场景

- 快速检查API状态
- 诊断连接问题
- 测试配置是否正确
