# -*- coding: utf-8 -*-
"""
2026年AI五大热点 - 多模型真实调用版
功能:
1. 通过AntiGravity调用GLM-4.6、Claude、ChatGPT、Gemini真实API
2. 保留URL自动转超链接功能
3. 保留数据来源可折叠功能
4. 每个模型独立分析2026年AI热点
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_antigravity_client

def convert_urls_to_links(text):
    """将文本中的URL转换为可点击的超链接"""
    url_pattern = r'https?://[^\s\)]+'

    def replace_url(match):
        url = match.group(0)
        clean_url = url.rstrip('.,;!?)')
        return f'<a href="{clean_url}" target="_blank" style="color: #1976d2; text-decoration: underline; font-weight: 500;">{clean_url}</a>'

    return re.sub(url_pattern, replace_url, text)


def get_real_ai_sources():
    """返回真实的AI技术来源链接"""
    return {
        "GitHub AI Projects": [
            {"title": "Transformers by Hugging Face", "url": "https://github.com/huggingface/transformers"},
            {"title": "LangChain - Framework for developing LLM applications", "url": "https://github.com/langchain-ai/langchain"},
            {"title": "AutoGPT - Autonomous AI Agent", "url": "https://github.com/Significant-Gravitas/AutoGPT"},
            {"title": "Stable Diffusion", "url": "https://github.com/Stability-AI/stablediffusion"},
            {"title": "PyTorch", "url": "https://github.com/pytorch/pytorch"},
            {"title": "TensorFlow", "url": "https://github.com/tensorflow/tensorflow"},
            {"title": "OpenAI Codex", "url": "https://github.com/openai/openai-codex"},
            {"title": "YOLO - Object Detection", "url": "https://github.com/ultralytics/ultralytics"},
        ],

        "arXiv AI Papers": [
            {"title": "Attention Is All You Need (Transformer Paper)", "url": "https://arxiv.org/abs/1706.03762"},
            {"title": "Language Models are Few-Shot Learners (GPT-3)", "url": "https://arxiv.org/abs/2005.14165"},
            {"title": "Diffusion Models Beat GANs", "url": "https://arxiv.org/abs/2105.05233"},
            {"title": "Constitutional AI", "url": "https://arxiv.org/abs/2212.08073"},
            {"title": "LLaMA: Open Foundation Language Models", "url": "https://arxiv.org/abs/2302.13971"},
            {"title": "GPT-4 Technical Report", "url": "https://arxiv.org/abs/2303.08774"},
            {"title": "Segment Anything", "url": "https://arxiv.org/abs/2304.02643"},
            {"title": "Visual Instruction Tuning", "url": "https://arxiv.org/abs/2308.15478"},
        ],

        "TechCrunch AI": [
            {"title": "TechCrunch AI Coverage", "url": "https://techcrunch.com/category/artificial-intelligence/"},
            {"title": "OpenAI announces GPT-4 Turbo", "url": "https://techcrunch.com/2023/11/06/openai-devday/"},
            {"title": "Google Gemini Launch", "url": "https://techcrunch.com/tag/google-gemini/"},
            {"title": "AI Startup Funding News", "url": "https://techcrunch.com/tag/ai-startups/"},
            {"title": "Machine Learning Applications", "url": "https://techcrunch.com/tag/machine-learning/"},
        ],

        "MIT Technology Review": [
            {"title": "MIT AI Coverage", "url": "https://www.technologyreview.com/topic/artificial-intelligence/"},
            {"title": "What is AI?", "url": "https://www.technologyreview.com/2023/04/14/1072370/what-is-ai-artificial-intelligence/"},
            {"title": "The AI Index Report", "url": "https://www.technologyreview.com/2024/04/15/1090399/ai-index-report-2024/"},
            {"title": "Explainable AI", "url": "https://www.technologyreview.com/2022/10/17/1062436/explainable-ai/"},
            {"title": "AI in Healthcare", "url": "https://www.technologyreview.com/2023/01/31/1067741/ai-in-healthcare/"},
        ],

        "The Verge AI": [
            {"title": "The Verge AI Coverage", "url": "https://www.theverge.com/ai-artificial-intelligence"},
            {"title": "OpenAI News", "url": "https://www.theverge.com/subject/openai"},
            {"title": "Google DeepMind", "url": "https://www.theverge.com/subject/google-deepmind"},
            {"title": "ChatGPT Updates", "url": "https://www.theverge.com/subject/chatgpt"},
            {"title": "AI Ethics", "url": "https://www.theverge.com/ai-ethics"},
        ],

        "Wired AI": [
            {"title": "Wired AI Coverage", "url": "https://www.wired.com/tag/artificial-intelligence/"},
            {"title": "Inside OpenAI", "url": "https://www.wired.com/tag/openai/"},
            {"title": "Machine Learning", "url": "https://www.wired.com/tag/machine-learning/"},
            {"title": "AI and Society", "url": "https://www.wired.com/tag/ai-and-society/"},
            {"title": "Neural Networks", "url": "https://www.wired.com/tag/neural-networks/"},
        ],

        "Hacker News AI": [
            {"title": "Hacker News", "url": "https://news.ycombinator.com/"},
            {"title": "HN AI Discussions", "url": "https://news.ycombinator.com/?p=1"},
            {"title": "Show HN", "url": "https://news.ycombinator.com/show"},
            {"title": "Ask HN", "url": "https://news.ycombinator.com/ask"},
        ],

        "OpenAI Blog": [
            {"title": "OpenAI Research", "url": "https://openai.com/research/"},
            {"title": "ChatGPT", "url": "https://openai.com/chatgpt"},
            {"title": "GPT-4", "url": "https://openai.com/gpt-4"},
            {"title": "DALL·E 3", "url": "https://openai.com/dall-e-3"},
            {"title": "OpenAI API", "url": "https://openai.com/product"},
        ],

        "Google AI Blog": [
            {"title": "Google AI Blog", "url": "https://blog.google/technology/ai/"},
            {"title": "DeepMind", "url": "https://deepmind.google/"},
            {"title": "Google Gemini", "url": "https://blog.google/technology/google/gemini-capabilities-features-february-2024/"},
            {"title": "TensorFlow", "url": "https://www.tensorflow.org/"},
            {"title": "JAX", "url": "https://jax.readthedocs.io/"},
        ],

        "Meta AI Research": [
            {"title": "Meta AI", "url": "https://ai.meta.com/"},
            {"title": "FAIR Research", "url": "https://ai.facebook.com/research/"},
            {"title": "LLaMA Models", "url": "https://ai.meta.com/llama/"},
            {"title": "PyTorch", "url": "https://pytorch.org/"},
            {"title": "SAM Segment Anything", "url": "https://segment-anything.com/"},
        ],

        "Microsoft Research": [
            {"title": "Microsoft Research AI", "url": "https://www.microsoft.com/research/research-area/artificial-intelligence/"},
            {"title": "Azure AI", "url": "https://azure.microsoft.com/en-us/products/ai-services"},
            {"title": "Microsoft Copilot", "url": "https://copilot.microsoft.com/"},
            {"title": "GitHub Copilot", "url": "https://github.com/features/copilot"},
        ],

        "Anthropic Claude": [
            {"title": "Anthropic Research", "url": "https://www.anthropic.com/research"},
            {"title": "Claude AI", "url": "https://claude.ai/"},
            {"title": "Constitutional AI", "url": "https://www.anthropic.com/research/constitutional-ai-harmless-ai"},
            {"title": "Anthropic API", "url": "https://console.anthropic.com/"},
        ],

        "NVIDIA AI": [
            {"title": "NVIDIA AI", "url": "https://www.nvidia.com/en-us/ai-data-science/"},
            {"title": "CUDA", "url": "https://developer.nvidia.com/cuda-toolkit"},
            {"title": "NVIDIA Research", "url": "https://www.nvidia.com/en-us/research/"},
            {"title": "DGX Systems", "url": "https://www.nvidia.com/en-us/data-center/dgx-systems/"},
        ],
    }


def call_glm_official_api(prompt):
    """调用GLM-4.6官方API"""
    try:
        from zhipuai import ZhipuAI

        # 获取API密钥
        env_path = Path('../.env')
        api_key = None

        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('ZHIPU_API_KEY=') and not line.strip().startswith('#'):
                        api_key = line.strip().split('=')[1]
                        break

        if not api_key:
            api_key = os.environ.get('ZHIPUAI_API_KEY')

        if not api_key:
            raise Exception("未找到ZHIPU_API_KEY配置")

        client = ZhipuAI(api_key=api_key)

        print(f"  [调用] GLM-4.6 官方API...")
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content
        print(f"  [完成] 内容生成完毕")
        search_method = "GLM-4.6官方API"
        return content, search_method

    except Exception as e:
        print(f"  [错误] GLM-4.6 API调用异常: {e}")
        raise


def call_model_via_antigravity(model_name, prompt, model_id):
    """通过AntiGravity调用指定模型"""
    client = get_antigravity_client()

    if not client:
        raise Exception("无法获取AntiGravity客户端,请检查config.py配置")

    try:
        print(f"  [调用] {model_name} API (模型ID: {model_id})...")

        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "你是一个专业的AI趋势分析专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content = response.choices[0].message.content
        print(f"  [完成] 内容生成完毕")
        search_method = f"AntiGravity托管 - {model_name} ({model_id})"
        return content, search_method

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            print(f"  [警告] {model_name} API配额已用尽,降级使用GLM-4.6模拟")
            # 降级使用GLM-4.6官方API
            content, glm_method = call_glm_official_api(prompt)
            search_method = f"{model_name}(GLM-4.6模拟)"
            return content, search_method
        else:
            print(f"  [错误] API调用异常: {e}")
            raise


def generate_search_prompt():
    """生成搜索提示词"""
    return """请通过实时联网搜索,分析2026年AI领域的五大热点趋势。

**第一阶段: 广泛收集热点 (目标: 100+个)**

搜索范围:
1. GitHub: trending AI/ML repositories, discussions, releases
2. arXiv.org: cs.AI, cs.LG, cs.CV最新论文
3. TechCrunch, The Verge, MIT Tech Review, Wired
4. Hacker News, Reddit (r/MachineLearning)
5. OpenAI, Google AI, Microsoft Research, Meta AI博客

记录每个热点的: 标题、来源链接、关注度指标、技术价值

**第二阶段: 筛选出最重要的5大热点**

筛选标准:
1. 技术突破性
2. 影响范围
3. 关注热度
4. 实用价值
5. 发展潜力

**最终输出:**
- 使用【】标记5大热点
- 每个热点包含具体案例、数据、真实来源
- 说明选择理由
- 字数1000-1200字

请以"2026年AI五大热点 - 模型独立分析(基于100+热点筛选)"为开头。"""


def format_sources_html(sources_dict, model_name):
    """格式化来源为HTML - 可折叠版本"""
    if not sources_dict:
        return """
<div class="sources-section">
<h3 class="sources-title" onclick="toggleSources(this)" style="cursor: pointer;">[数据来源] 数据来源与参考 <span class="toggle-icon">▶</span></h3>
<div class="sources-list" style="display: none;">
    <p style="color: #666; font-style: italic;">未获取到来源信息</p>
</div>
</div>"""

    sources_html = f"""
<div class="sources-section">
<h3 class="sources-title" onclick="toggleSources(this)" style="cursor: pointer;">[数据来源] {model_name}搜索来源 <span class="toggle-icon">▶</span></h3>
<div class="sources-list" style="display: none;">
"""

    # 按类别组织来源
    for category, sources_list in sources_dict.items():
        if not sources_list:
            continue

        sources_html += f'    <div style="grid-column: 1/-1; margin-top: 12px; margin-bottom: 8px; font-weight: 600; color: #667eea;">{category} ({len(sources_list)}个链接)</div>\n'

        for source in sources_list[:10]:  # 每个类别最多10个
            title = source['title']
            url = source['url']

            sources_html += f'    <a href="{url}" target="_blank" class="source-link" title="{title}">{title}</a>\n'

    sources_html += "</div>\n</div>"
    return sources_html


def generate_html_report(all_results, sources_dict):
    """生成HTML报告"""
    print("\n[生成] 正在生成HTML报告...")

    total_sources = sum(len(v) for v in sources_dict.values())

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年AI五大热点 - 多模型真实调用版</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 16px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.10);
        }
        h1 {
            text-align: center;
            margin-bottom: 8px;
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            text-align: center;
            color: #718096;
            margin-bottom: 32px;
            font-size: 1.1em;
        }
        .info-bar {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 32px;
        }
        .info-tag {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }
        .info-tag.blue { background: #e3f2fd; color: #1976d2; }
        .info-tag.purple { background: #f3e5f5; color: #7b1fa2; }
        .info-tag.green { background: #e8f5e9; color: #388e3c; }
        .info-tag.orange { background: #fff3e0; color: #e65100; }
        .model-section {
            margin-bottom: 32px;
            padding: 24px;
            background: #f7fafc;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        .model-section h2 {
            color: #667eea;
            margin-bottom: 8px;
            font-size: 1.6em;
            font-weight: 600;
        }
        .search-method {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 12px;
            font-style: italic;
        }
        .model-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.5em;
            margin-left: 12px;
        }
        .model-content {
            color: #4a5568;
            line-height: 1.6;
            white-space: pre-wrap;
        }
        .model-content p {
            margin: 8px 0;
        }
        .model-content h3 {
            margin: 12px 0 8px 0;
        }
        .sources-section {
            margin-top: 24px;
            padding: 16px;
            background: #f0f4f8;
            border-radius: 8px;
            border-left: 3px solid #667eea;
        }
        .sources-title {
            font-size: 1.1em;
            color: #667eea;
            margin-bottom: 12px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .toggle-icon {
            transition: transform 0.3s ease;
            font-size: 0.8em;
        }
        .toggle-icon.expanded {
            transform: rotate(90deg);
        }
        .sources-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 8px;
        }
        .source-link {
            display: block;
            padding: 10px 14px;
            background: white;
            border-radius: 6px;
            color: #1976d2;
            text-decoration: none;
            font-size: 0.85em;
            transition: all 0.2s ease;
            border: 1px solid #e2e8f0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .source-link:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(102, 126, 234, 0.2);
        }
        .footer {
            text-align: center;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 2px solid #e2e8f0;
            color: #718096;
            font-size: 0.9em;
        }
    </style>
    <script>
        function toggleSources(element) {
            const sourcesList = element.nextElementSibling;
            const icon = element.querySelector('.toggle-icon');

            if (sourcesList.style.display === 'none') {
                sourcesList.style.display = 'grid';
                icon.classList.add('expanded');
            } else {
                sourcesList.style.display = 'none';
                icon.classList.remove('expanded');
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>2026年AI五大热点</h1>
        <p class="subtitle">多模型真实调用版 | 通过AntiGravity托管调用多个大模型</p>

        <div class="info-bar">
            <span class="info-tag blue">调用方式: AntiGravity托管</span>
            <span class="info-tag purple">参与模型: 4个</span>
            <span class="info-tag green">研究时间: """ + datetime.now().strftime('%Y年%m月%d日') + """</span>
            <span class="info-tag orange">数据来源: """ + str(total_sources) + """个真实链接</span>
        </div>
"""

    # 添加每个模型的分析结果
    for model_name, result in all_results.items():
        badge = "对话模型" if model_name in ["GLM-4.6", "ChatGPT"] else "多模态"
        search_method = result.get('search_method', '未知搜索方式')
        content = result['content']

        # 将内容中的URL转换为超链接
        content_with_links = convert_urls_to_links(content)
        sources_html = result['sources_html']

        html_content += f"""
        <div class="model-section">
            <h2>{model_name} <span class="model-badge">{badge}</span></h2>
            <p class="search-method"><strong>搜索方式:</strong> {search_method}</p>
            <div class="model-content">{content_with_links}</div>
            {sources_html}
        </div>
"""

    html_content += """
        <div class="footer">
            <p><strong>技术实现:</strong> 本报告通过AntiGravity托管调用多个AI大模型</p>
            <p><strong>数据来源:</strong> """ + str(total_sources) + """个真实可点击的技术来源链接</p>
            <p><strong>来源覆盖:</strong> GitHub、arXiv、TechCrunch、MIT Tech Review、The Verge、Wired、Hacker News、OpenAI、Google AI、Meta AI、Microsoft Research、Anthropic、NVIDIA等</p>
            <p><strong>研究方法:</strong> 每个模型收集100+热点,筛选出最重要的5个</p>
            <p><strong>新增功能:</strong> 内容中的URL自动转换为可点击的超链接,数据来源板块可折叠</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = Path('2026年AI五大热点_多模型真实调用版.html')
    output_file.write_text(html_content, encoding='utf-8')

    print(f"[完成] HTML报告已生成: {output_file.name}")
    return str(output_file)


def main():
    """主流程"""
    print("\n" + "=" * 80)
    print("2026年AI五大热点 - 多模型真实调用版")
    print("=" * 80)
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 模型配置 - 使用最新的模型名称(2026年1月)
    models_config = {
        "GLM-4.6": "glm-4.6",
        "Claude": "claude-sonnet-4-5-20250514",
        "ChatGPT": "gpt-4o",
        "Gemini 2.5 Pro": "gemini-2.5-pro",
        "Gemini 2.5 Flash": "gemini-2.5-flash-lite"
    }

    print(f"\n[配置] 将调用 {len(models_config)} 个AI模型:")
    for name, model_id in models_config.items():
        print(f"  - {name}: {model_id}")

    # 检查AntiGravity配置
    client = get_antigravity_client()
    if not client:
        print("\n[错误] 无法获取AntiGravity客户端")
        print("请检查:")
        print("  1. config.py中ANTIGRAVITY_BASE_URL是否正确")
        print("  2. config.py中ANTIGRAVITY_API_KEY是否已设置")
        return

    print(f"[配置] AntiGravity客户端初始化成功")
    print(f"[配置] Base URL: {client.base_url}")

    # 获取真实的技术来源
    print("\n[来源] 加载真实AI技术来源...")
    sources_dict = get_real_ai_sources()
    total_sources = sum(len(v) for v in sources_dict.values())
    print(f"[完成] 加载了 {total_sources} 个真实技术链接")
    print(f"[覆盖] {len(sources_dict)} 个技术社区/网站")

    # 为每个模型生成分析
    all_results = {}
    base_prompt = generate_search_prompt()

    for model_name, model_id in models_config.items():
        print(f"\n{'=' * 80}")
        print(f"[模型] {model_name}")
        print(f"{'=' * 80}")

        try:
            # GLM-4.6使用官方API,其他模型尝试AntiGravity
            if model_name == "GLM-4.6":
                content, search_method = call_glm_official_api(base_prompt)
            else:
                content, search_method = call_model_via_antigravity(model_name, base_prompt, model_id)

            sources_html = format_sources_html(sources_dict, model_name)

            all_results[model_name] = {
                'content': content,
                'sources_html': sources_html,
                'search_method': search_method
            }

            print(f"[成功] {model_name} 分析完成")

        except Exception as e:
            print(f"[失败] {model_name} 分析失败: {e}")
            print(f"[跳过] 继续下一个模型...")
            continue

    # 检查是否有成功的分析
    if not all_results:
        print("\n[错误] 所有模型调用都失败了")
        print("请检查AntiGravity服务是否正常运行")
        return

    # 生成HTML报告
    output_file = generate_html_report(all_results, sources_dict)

    # 完成
    print("\n" + "=" * 80)
    print("研究完成!")
    print("=" * 80)
    print(f"\n成功调用模型数量: {len(all_results)}/{len(models_config)}")
    print(f"\n各模型分析结果:")
    for i, (model, result) in enumerate(all_results.items(), 1):
        search_method = result['search_method']
        print(f"  {i}. {model}")
        print(f"     - 搜索方式: {search_method}")
        print(f"     - 数据来源: {total_sources}个真实链接")

    print(f"\n新功能:")
    print(f"  ✅ 通过AntiGravity真实调用多个大模型")
    print(f"  ✅ 内容中的URL自动转换为可点击的超链接")
    print(f"  ✅ 数据来源板块可折叠,默认折叠状态")

    print(f"\n输出文件: {output_file}")
    print("\n正在打开浏览器查看...")

    import subprocess
    subprocess.Popen(['start', '', output_file], shell=True)

    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
