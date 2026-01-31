# 工具详细说明配置
# 用于在工具管理器中显示每个工具的详细信息

TOOL_DETAILS = {
    # ============== 文章生成工具 ==============
    "article/toutiao_article_generator.py": {
        "功能": """基于AI技术自动生成今日头条风格的完整文章或完善用户草稿,包含标题、正文和配图

✨ 使用模型:
• ZhipuAI GLM-4 Flash (文本生成/草稿完善,快速模型)
• Gemini 3 Pro Image 4K (配图生成,1024x1024)

✨ 达到效果:
• 📝 模式1 - 主题生成: 自动生成1500/2000/2500字文章(可选)
• ✍️ 模式2 - 草稿完善: AI优化用户的文章草稿,保留核心观点,补充案例和数据
• 🎨 智能生成3张配图(支持真实/艺术/卡通3种风格)
• ✨ 符合今日头条爆款风格
• 🚀 快速生成(30-60秒)
• 📱 自动在浏览器中打开预览
• 💾 保存为Markdown和HTML两种格式

✨ 草稿完善功能:
• 保留草稿核心观点和主要内容
• 补充具体案例和数据支撑
• 优化表达,使其更生动有趣
• 增加emoji增强可读性
• 优化标题,提升吸引力
• 增强情感共鸣

✨ 最终产出:
• Markdown文章文件 (.md)
• HTML预览文件 (.html,带配图画廊)
• 3张配图文件 (.jpg)

📁 输出目录: article/""",
        "技术栈": ["ZhipuAI GLM-4 Flash", "Gemini 3 Pro Image 4K", "Python PIL", "Python"]
    },
    "article/article_review_and_revision.py": {
        "功能": """AI辅助文章审校和修订工具 - 针对特定文章"冬日围炉_饮茶养生.md"进行专业点评和优化

⚠️ 注意: 此工具专门处理article/目录下的"冬日围炉_饮茶养生.md"文章,不是通用工具

✨ 使用模型:
• ZhipuAI GLM-4.6 (专业点评)
• ZhipuAI GLM-4.6 (文章修改)

✨ 达到效果:
• 📋 专业编辑角度的AI点评(至少3个优点+3个问题)
• ✍️ 基于点评意见的针对性修改
• 📊 多维度评估(标题吸引力、语言风格、实用性、文化深度、互动性、情感共鸣)
• 🔄 原版与修改版对比展示
• 🌐 生成交互式对比网页

✨ 最终产出:
• 文章专业点评意见.md (AI专业点评)
• 冬日围炉_饮茶养生_修改版.md (优化后的文章)
• 冬日饮茶_两版对比.html (交互式对比网页,含3个标签页:专业点评/两版对比/数据统计)

📁 输出目录: article/""",
        "技术栈": ["ZhipuAI GLM-4.6", "Python"]
    },
    "article/generate_article_images.py": {
        "功能": """为职场主题文章生成配图 - 硬编码工具,专门为职场类文章生成3张固定主题的配图

⚠️ 注意: 此工具专门为职场主题文章生成固定内容的配图,不是通用配图生成工具

✨ 使用模型:
• Gemini 3 Pro Image 4K (图像生成,1024x1024)

✨ 达到效果:
• 🖼️ 生成3张职场主题配图:
  1. 职场办公场景(年轻人在现代办公室工作)
  2. 薪资增长图表(从5000到30000的增长趋势)
  3. 职场成功时刻(庆祝成就,团队鼓掌)
• 🎨 专业商务摄影风格
• ⚡ 快速生成并保存为高质量JPEG

✨ 最终产出:
• 职场文章配图1_办公场景.jpg
• 职场文章配图2_薪资增长.jpg
• 职场文章配图3_成功时刻.jpg

📁 输出目录: article/""",
        "技术栈": ["Gemini 3 Pro Image 4K", "Python PIL", "Python"]
    },

    # ============== 视频工具 ==============
    "video/baidu_video_downloader.py": {
        "功能": """百度视频下载工具 v2.0 - Selenium增强版,支持绕过百度安全验证下载视频

✨ 达到效果:
• ⬇️ 稳定下载百度平台视频(百度新闻、百家号等)
• 🔓 使用undetected-chromedriver绕过安全验证(优先)或标准Selenium(备选)
• 🎯 自动识别和提取视频URL(支持mp4/m3u8/flv等格式)
• 🤖 模拟人类浏览行为(滚动、等待等)避免检测
• 🐛 保存调试HTML文件供问题排查
• ⚡ 高速下载视频文件

✨ 最终产出:
• MP4视频文件(或其他格式的视频文件)
• baidu_page_*_debug.html(调试文件)

📁 输出目录: video/""",
        "技术栈": ["Selenium 4.15", "undetected-chromedriver", "Chrome WebDriver", "Python requests"]
    },
    "video/video_generation_comparison.py": {
        "功能": """支持多个AI视频生成模型,对同一主题生成视频并进行AI评价和排序

✨ 使用模型:
• ✅ Seedance 1.5 Pro (火山引擎) - 文字转视频+音频,720p/1080p,4-12秒
• ✅ DALL-E 3 + FFmpeg动画 - 图片转视频,1280x720,5秒缩放动画
• ⚠️ Gemini Veo 3.1 (Google) - 需要配置GEMINI_API_KEY

✨ 达到效果:
• 🎬 真正的视频生成(非简单图片动画)
• 🎵 自动生成与画面匹配的音频(Seedance)
• ⚡ 快速生成(30-60秒完成)
• 🎨 高清输出(720p/1080p)
• 📊 AI智能评价和排名
• 🔄 断点续传支持
• 📄 精美HTML对比报告

✨ 最终产出:
• 📹 MP4视频文件 (每个模型独立视频)
• 📊 HTML对比报告 (包含视频播放器、AI评价、技术指标)
• 📈 统计信息 (生成时间、文件大小、成功率)
• 💾 进度文件 (支持断点续传)

✨ 特色功能:
• 断点续传: 自动保存进度,支持中断后续传已完成的模型
• AI评价: 使用ZhipuAI GLM-4.6从技术质量、创意表现、视觉效果三个维度评分
• 异步轮询: 智能轮询任务状态,自动下载生成的视频
• 有声视频: Seedance 1.5 Pro支持自动生成匹配的音频(人声、音效、背景音乐)
• 错误处理: 完善的错误处理和用户友好的提示信息

📁 输出目录: video_comparison_output/

⚙️ 配置要求:
• VOLCANO_API_KEY (已配置,用于Seedance)
• ANTIGRAVITY_API_KEY (已配置,用于DALL-E)
• ZHIPU_API_KEY (已配置,用于AI评价)
• FFmpeg (可选,用于DALL-E+FFmpeg模式)""",
        "技术栈": ["Python 3.8+", "Requests", "ZhipuAI GLM-4.6", "OpenAI API", "Volcano Engine API", "FFmpeg (可选)"]
    },

    # ============== 鸟类绘画工具 ==============
    "bird/bird_painting_optimized.py": {
        "功能": """使用多个AI模型生成鸟类绘画并进行对比 - 优化版,最大化避免触发API限制

✨ 使用模型:
• Gemini 3 Pro Image 4K (主要模型)
• 支持其他anti-gravity模型

✨ 达到效果:
• 🐦 精美鸟类绘画(6个步骤:铅笔起稿→底色→明暗→细节→背景→最终)
• 🎨 多模型对比
• 🔄 智能等待服务器容量(检测503/429错误自动等待重试)
• ⚡ 批量生成减少握手开销
• 🛡️ 错误恢复机制
• 📊 生成对比报告

✨ 最终产出:
• 多张PNG图片文件(每个步骤一张)
• bird_optimized.log(详细日志)
• 对比报告

📁 输出目录: bird/""",
        "技术栈": ["Gemini 3 Pro Image 4K", "Anti-gravity API", "Python PIL", "Python logging"]
    },
    "bird/bird_painting_volcano.py": {
        "功能": """使用火山引擎Seedream 4.5生成鸟类水彩画教程 - 6步骤完整教学

✨ 使用模型:
• Volcano Seedream 4.5 (doubao-seedream-4-5-251128)
• 输出分辨率: 2K

✨ 达到效果:
• 🎨 生成6个步骤的鸟类水彩画教程:
  1. 铅笔起稿
  2. 底色铺陈
  3. 明暗塑造
  4. 细节刻画
  5. 背景渲染
  6. 最终调整
• 🖼️ 严格对应参考图构图(bird.jpg)
• 🔄 自动重试机制(配额限制/服务器繁忙)
• 📝 生成日志文件

✨ 最终产出:
• 6张JPG图片文件(每个步骤一张,带水印)
• bird_volcano.log(详细日志)

📁 输出目录: bird/""",
        "技术栈": ["Volcano Engine API", "Seedream 4.5", "Python requests", "Python logging"]
    },

    # ============== 节日图像生成 ==============
    "picture/generate_festival_images.py": {
        "功能": """节日主题图像生成器 - 支持自定义主题,使用4个AI模型生成图像并生成HTML对比页面

✨ 使用模型:
• DALL-E 3 (通过anti-gravity)
• Flux (通过Pollinations)
• Volcano Seedream 4.5 (通过Volcano API,2K分辨率,带水印)
• Gemini 3 Pro Image 2K (通过anti-gravity,可能不可用)

✨ 达到效果:
• 🎨 节日主题图片生成(支持用户自定义主题)
• 🖼️ 4个模型并行生成,直观对比效果
• 📊 自动生成HTML对比展示页面
• 🌈 支持多种风格和主题
• 📱 响应式网页设计,易于查看对比

✨ 最终产出:
• 4张图片文件(每个模型一张)
• festival_comparison_*.html (HTML对比展示页面)

📁 输出目录: picture/""",
        "技术栈": ["DALL-E 3", "Flux/Pollinations", "Volcano Seedream 4.5", "Gemini Pro Image", "Python"]
    },

    # ============== AI热点研究 ==============
    "hotspot/ai_trends_2026_comparison.py": {
        "功能": """2026年AI趋势对比分析工具 - 多模型视角分析AI发展趋势

✨ 使用模型:
• ZhipuAI GLM-4.6 (主要分析模型)
• 其他模型提供不同视角(手动模拟总结)

✨ 达到效果:
• 📈 趋势分析(多模态AI、AI Agent、开源模型、科学研究AI、端侧AI)
• 📊 多模型视角对比(GLM-4.6、Pollinations、Claude等)
• 📄 深入浅出的分析报告(800-1000字)
• 🎯 适合普通读者阅读的技术解读

✨ 最终产出:
• AI模型总结文件(每个模型一份总结)
• 2026_AI_热点_综合报告.md(综合分析报告)

📁 输出目录: hotspot/""",
        "技术栈": ["ZhipuAI GLM-4.6", "Python", "数据分析"]
    },

    # ============== 测试工具 ==============
    "test/test_antigravity_models.py": {
        "功能": """Anti-gravity多模型测试工具 - 测试anti-gravity平台支持的文本模型可用性

✨ 使用模型:
• Gemini系列 (2.0-flash-exp, 2.5-pro, pro, 1.5-pro, 1.5-flash)
• GPT系列 (gpt-4-turbo, gpt-4o, gpt-4, gpt-3.5-turbo)
• Claude系列 (sonnet-4-5, 3-5-sonnet, 3-opus)
• GLM系列 (glm-4.6, glm-4)

✨ 达到效果:
• ✅ 批量测试14个主流AI文本模型在anti-gravity平台的可用性
• 📊 识别每个模型的状态(可用/不可用/配额耗尽)
• 🔍 快速验证API配置和模型访问权限
• ⚡ 轻量级测试(每个模型只发送"你好"测试)

✨ 最终产出:
• 控制台输出测试结果(每个模型的可用性状态)

📁 输出目录: test/""",
        "技术栈": ["Anti-gravity API", "Python"]
    },
    "test/test_non_gemini_models.py": {
        "功能": """非Gemini图像模型对比测试工具,测试anti-gravity支持的所有非Gemini图像生成模型

✨ 使用模型:
• DALL-E 3 (OpenAI最新图像模型,质量极高)
• DALL-E 2 (OpenAI经典图像模型)
• Flux 1.1 Pro (Black Forest Labs最新模型)
• Flux Schnell (Flux快速版本)
• Flux Dev (Flux开发版本)
• SD-3 (Stable Diffusion 3,Stability AI最新SD模型)
• SD XL Lightning (SD XL快速生成版本)

✨ 测试提示词:
• 中国传统山水画
• 可爱猫咪
• 未来城市
• 美食
• 花鸟画

✨ 达到效果:
• 🎨 测试7个主流AI图像生成模型
• 📊 并行对比测试结果
• ⚡ 快速生成高质量图像
• 🖼️ 每个模型生成5张不同主题的图片
• 💾 自动保存所有生成的图像
• 🔄 支持断点续传(中断后可继续)
• 📈 详细的性能统计和成功率
• 🌐 自动生成HTML对比展示页面

✨ 最终产出:
• 测试图片 (每个模型5张,共35张图片)
• HTML对比页面 (包含所有图片、统计数据、性能对比表)
• JSON测试结果文件 (详细数据)
• 进度文件 (支持断点续传)

📁 输出目录: test/non_gemini_comparison_output/""",
        "技术栈": ["Anti-gravity API", "Python", "OpenAI API", "Black Forest Labs API", "Stability AI API"]
    },
    "test/test_gemini_pro_image.py": {
        "功能": """Gemini全模型对比测试工具,测试所有可用的Gemini图像生成模型

✨ 使用模型:
• Gemini 3 Pro Image 4K (最高分辨率,细节最丰富)
• Gemini 3 Pro Image 2K (高分辨率,平衡质量和速度)
• Gemini 3 Flash Image (快速生成,适合批量处理)
• Gemini 2 Pro Image (第二代专业图像模型)
• Gemini 2 Flash Image (第二代快速图像模型)

✨ 测试提示词:
• 中国传统山水画 (art)
• 可爱猫咪 (animal)
• 未来城市 (scifi)
• 美食 (food)
• 花鸟画 (art)

✨ 达到效果:
• 🎨 并行测试5个Gemini图像模型
• 📊 对比不同模型的生成质量和速度
• 🖼️ 每个模型生成5张不同主题的图片
• 💾 自动保存所有生成的图像
• 🔄 支持断点续传(中断后可继续)
• 📈 详细的性能统计和成功率
• 🌐 自动生成HTML对比展示页面

✨ 最终产出:
• 测试图片 (每个模型5张,共25张图片)
• HTML对比页面 (包含所有图片、统计数据、性能对比表)
• JSON测试结果文件 (详细数据)
• 进度文件 (支持断点续传)

📁 输出目录: test/gemini_comparison_output/""",
        "技术栈": ["Anti-gravity API", "Python", "Google Gemini API", "HTML/CSS"]
    }
}

# 辅助函数:根据文件路径获取详细信息
def get_tool_details(path):
    """获取工具的详细信息"""
    # 统一路径格式
    normalized_path = path.replace('\\', '/').strip('/')

    return TOOL_DETAILS.get(normalized_path, {})
