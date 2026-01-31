# 百度视频下载工具 v2.0 - 使用说明

## 📌 重要提示

### ⚠️ 已知限制
本工具**无法下载以下平台**的视频:
- ❌ **百度好看视频** (haokan.baidu.com) - 需要验证码
- ❌ **B站** (bilibili.com) - 需要登录
- ❌ **VIP付费视频** - 需要会员权限
- ❌ **短视频平台** (抖音、快手等) - 有下载限制

### ✅ 支持的平台
本工具**可以尝试**下载:
- ✅ 百家号视频 (反爬虫较弱)
- ✅ 公开新闻视频
- ✅ 其他无验证要求的视频平台

## 🚀 快速开始

### 方法1: 通过Web界面 (推荐)
1. 启动工具管理器:
   ```bash
   cd C:\D\CAIE_tool\MyAIProduct\post
   python tool_manager.py
   ```

2. 打开浏览器访问: http://localhost:5000

3. 找到"视频下载工具"分类

4. 点击"百度视频下载工具"

5. 输入视频URL和文件名

6. 点击"运行工具"

### 方法2: 命令行
```bash
cd C:\D\CAIE_tool\MyAIProduct\post\video
python baidu_video_downloader.py
```

然后按提示输入:
- URL: 视频链接
- 输出文件名: (可选，留空自动生成)

### 方法3: 直接指定参数
```bash
python baidu_video_downloader.py "视频URL" "输出文件名.mp4"
```

## 📋 输入格式

### ✅ 好的URL示例
```
# 百家号视频
https://mbd.baidu.com/newspaper/data/videolanding?nid=xxx

# 其他公开平台
https://example.com/video/xxx
```

### ❌ 避免使用的URL
```
# 百度好看视频 (无法下载)
https://haokan.baidu.com/v?vid=xxx

# 需要登录的平台
https://www.bilibili.com/video/xxx

# VIP视频
https://v.qq.com/x/xxx
```

## 🔧 工作原理

### 1. 自动模式选择
工具会自动按以下顺序尝试:
1. **undetected-chromedriver** - 最强反检测 (需要安装)
2. **标准Selenium** - 基础反检测
3. **HTTP请求模式** - 最简单但最容易失败

### 2. 反检测技术
- ✅ 移除 navigator.webdriver 标识
- ✅ 隐藏自动化特征
- ✅ 模拟人类滚动行为
- ✅ 真实浏览器指纹

### 3. 自动回退
如果一种方法失败，会自动尝试下一种方法

## 📦 安装依赖

### 基础依赖 (必需)
```bash
pip install selenium requests
```

### 增强反检测 (推荐)
```bash
pip install undetected-chromedriver
```

### ChromeDriver
- 自动下载和管理 (undetected-chromedriver会自动处理)
- 或者手动下载: https://chromedriver.chromium.org/

## 📊 下载位置

### 默认位置
所有下载的视频默认保存在工具所在目录:
```
C:\D\CAIE_tool\MyAIProduct\post\video\
```

### 自定义位置
可以在输出文件名中指定完整路径:
```
D:\Videos\my_video.mp4
```

## 🛠️ 故障排除

### 问题1: "ModuleNotFoundError: No module named 'selenium'"
**解决方法**:
```bash
pip install selenium
```

### 问题2: "无法获取视频链接"
**可能原因**:
1. URL无效 (404)
2. 平台不支持 (好看视频、B站等)
3. 需要验证码
4. 需要登录

**解决方法**:
1. 检查URL是否正确
2. 尝试其他平台的视频
3. 查看调试HTML文件

### 问题3: ChromeDriver版本不匹配
**解决方法**:
```bash
pip install undetected-chromedriver
```
undetected-chromedriver会自动管理版本

### 问题4: 下载很慢
**解决方法**:
1. 检查网络连接
2. 尝试在非高峰时段下载
3. 视频文件可能很大,请耐心等待

## 📈 性能指标

### 典型下载速度
- 10MB视频: 约30秒
- 50MB视频: 约2分钟
- 100MB视频: 约4分钟

*(取决于网络速度)*

### 内存使用
- 基础模式: ~50MB
- Selenium模式: ~200MB
- undetected模式: ~250MB

## 🎯 使用技巧

### Tip 1: 预先检查URL
在工具运行前,可以先在浏览器中访问URL:
- 如果能正常播放,下载成功率较高
- 如果需要验证码,工具无法自动下载

### Tip 2: 使用正确的文件扩展名
推荐使用:
- `.mp4` - 通用视频格式
- `.mkv` - 高质量视频
- `.flv` - Flash视频

### Tip 3: 批量下载
可以编写脚本批量下载:
```bash
while read url; do
    python baidu_video_downloader.py "$url"
done < urls.txt
```

## 📚 调试功能

### 调试文件
工具会保存调试HTML文件:
- `baidu_page_undetected_debug.html` - undetected模式
- `baidu_page_selenium_debug.html` - Selenium模式
- `baidu_page_basic_debug.html` - 基础模式

### 如何使用调试文件
1. 打开HTML文件查看页面内容
2. 检查是否有验证码对话框
3. 搜索 "video" 或 ".mp4" 关键词
4. 手动查找视频URL

## ⚖️ 法律声明

### 使用须知
1. 仅用于个人学习和研究
2. 尊重版权,不要传播受版权保护的内容
3. 不要用于商业用途
4. 遵守当地法律法规

### 版权提醒
下载的视频内容版权归原作者所有,请:
- ✅ 个人观看学习
- ❌ 重新上传分享
- ❌ 用于商业项目

## 🔄 更新日志

### v2.0 (2026-01-29)
- ✅ 集成 undetected-chromedriver
- ✅ 添加自动回退机制
- ✅ 修复Windows兼容性
- ✅ 修复Chrome版本匹配
- ✅ 改进错误提示

### v1.0 (初始版本)
- 基础Selenium支持
- HTTP请求模式
- 基本下载功能

## 📞 获取帮助

### 报告问题
如果遇到问题,请提供:
1. 完整的视频URL
2. 错误截图
3. 调试HTML文件
4. Python版本和操作系统

### 推荐替代工具
如果本工具无法使用,可以尝试:
- **you-get**: `pip install you-get`
- **yt-dlp**: `pip install yt-dlp`
- **ffmpeg**: 命令行下载工具
- **浏览器插件**: Video DownloadHelper

---

**版本**: v2.0
**最后更新**: 2026-01-29
**状态**: ⚠️ 功能正常，但有平台限制
