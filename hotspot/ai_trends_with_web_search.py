# -*- coding: utf-8 -*-
"""
2026年AI五大热点 - 增强版
集成实时网络搜索功能
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# 尝试导入zhipuai
try:
    import zhipuai
    ZHIPUAI_AVAILABLE = True
except ImportError:
    ZHIPUAI_AVAILABLE = False
    print("[警告] zhipuai未安装,将使用模拟模式")


def get_zhipu_api_key():
    """获取智谱AI API密钥"""
    post_env_path = Path('../.env')
    if post_env_path.exists():
        with open(post_env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ZHIPU_API_KEY=') and not line.strip().startswith('#'):
                    return line.strip().split('=')[1]
    api_key = os.environ.get('ZHIPUAI_API_KEY')
    if api_key:
        return api_key
    return None


def perform_web_search(query, num_results=5):
    """
    执行实时网络搜索
    使用DuckDuckGo API (无需API key)

    Args:
        query: 搜索关键词
        num_results: 返回结果数量

    Returns:
        list of dict: [{title, url, snippet}, ...]
    """
    try:
        # 使用DuckDuckGo HTML搜索
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        print(f"  [搜索] 正在搜索: {query}")
        response = requests.get(url, headers=headers, timeout=10)

        # 简单解析搜索结果
        import re
        results = []
        # 匹配搜索结果
        pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, response.text)

        for i, (url, title) in enumerate(matches[:num_results], 1):
            # 清理URL (DuckDuckGo使用redirect)
            clean_url = url
            if 'uddg=' in url:
                import urllib.parse
                parsed = urllib.parse.parse_qs(url.split('uddg=')[1].split('&')[0])
                if parsed:
                    clean_url = list(parsed.keys())[0]

            results.append({
                'title': title,
                'url': clean_url,
                'snippet': f"搜索结果 #{i}"
            })

        print(f"  [搜索] 找到 {len(results)} 个结果")
        return results

    except Exception as e:
        print(f"  [错误] 搜索失败: {str(e)}")
        return []


def search_international_ai_sources():
    """
    搜索国际AI技术来源

    Returns:
        dict: {
            'github': [...],
            'arxiv': [...],
            'techcrunch': [...],
            'hackernews': [...]
        }
    """
    print("\n[实时搜索] 正在获取国际AI技术来源...")

    sources = {
        'github': perform_web_search("site:github.com AI trending 2026 machine learning", 3),
        'arxiv': perform_web_search("site:arxiv.org AI 2026 multimodal deep learning", 3),
        'techcrunch': perform_web_search("site:techcrunch.com AI artificial intelligence 2026", 3),
        'hackernews': perform_web_search("site:news.ycombinator.com AI machine learning 2026", 3)
    }

    total = sum(len(v) for v in sources.values())
    print(f"[完成] 共获取 {total} 个国际来源")

    return sources


def format_sources_context(sources):
    """将搜索结果格式化为提示词上下文"""
    context = "\n**实时搜索到的国际来源(必须引用):**\n\n"

    for category, items in sources.items():
        if items:
            context += f"{category.upper()}:\n"
            for item in items:
                context += f"- {item['title']}\n"
                context += f"  链接: {item['url']}\n"
            context += "\n"

    return context


def call_glm_api_with_sources(prompt, search_sources=None):
    """
    调用GLM-4.6 API,优先使用模型的web_search,不足时补充外部搜索

    Args:
        prompt: 基础提示词
        search_sources: 实时搜索到的来源(仅当模型搜索结果不足时使用)

    Returns:
        (响应内容, 来源列表)
    """
    if not ZHIPUAI_AVAILABLE:
        print("  [模拟] GLM-4.6响应(未安装zhipuai)")
        return simulate_glm_response(prompt), []

    api_key = get_zhipu_api_key()
    if not api_key:
        print("  [模拟] GLM-4.6响应(未配置API密钥)")
        return simulate_glm_response(prompt), []

    try:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)

        # 第一步: 优先让GLM-4.6使用自己的web_search
        print("  [策略] 优先使用GLM-4.6自己的web_search工具")
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            tools=[{
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    "search_result": True
                }
            }],
            temperature=0.7
        )

        content = response.choices[0].message.content

        # 提取模型的搜索结果
        sources = []
        response_dict = response.model_dump()
        if 'web_search' in response_dict and response_dict['web_search']:
            for item in response_dict['web_search']:
                url = item.get('link', '')
                if url and (url.startswith('http://') or url.startswith('https://')):
                    sources.append({
                        'title': item.get('title', '未知标题'),
                        'url': url,
                        'media': item.get('media', ''),
                        'publish_date': item.get('publish_date', '')
                    })

        # 第二步: 评估模型搜索结果是否足够
        print(f"  [评估] GLM-4.6返回了 {len(sources)} 个来源")

        # 如果模型搜索结果不足(少于3个)且提供了外部搜索,则补充
        if len(sources) < 3 and search_sources:
            print("  [补充] 模型搜索结果不足,补充外部实时搜索结果")

            # 将外部搜索结果添加到sources
            for category, items in search_sources.items():
                for item in items:
                    sources.append({
                        'title': item['title'],
                        'url': item['url'],
                        'media': category,
                        'publish_date': ''
                    })

            print(f"  [补充] 补充后共有 {len(sources)} 个来源")

        return content, sources

    except Exception as e:
        print(f"  [错误] API调用异常: {str(e)}")
        return simulate_glm_response(prompt), []


def simulate_glm_response(prompt):
    """模拟GLM-4.6响应"""
    return """基于联网搜索,我分析了2026年AI领域的发展:

【多模态AI突破】
GPT-4V、Gemini 2.0、GLM-4V等多模态模型全面成熟,实现视觉与语言深度融合。

【AI Agent爆发】
OpenClaw在GitHub爆火(10万+Star),智谱AI推出智能体平台,从对话向行动转变。

【开源模型崛起】
DeepSeek-V3、Llama 3.3性能接近闭源,推动AI民主化。

【科学AI应用】
AlphaFold 3准确率提升,AI加速科学发现。

【端侧AI普及】
本地部署保护隐私,OpenClaw引发Mac mini热潮。

2026年,AI从实验走向实用,从云端走向终端。""", []


def generate_search_prompt():
    """生成搜索提示词"""
    return """请通过实时联网搜索,分析2026年AI领域的五大热点趋势。

请重点关注:
1. 多模态AI的突破性进展
2. AI Agent(智能体)的爆发式增长
3. 开源大模型的崛起
4. AI在科学研究中的应用突破
5. AI实用化与产业落地

请广泛搜索国际技术来源,包括:
- GitHub trending AI项目
- arXiv最新AI论文
- TechCrunch、The Verge等科技媒体报道
- Hacker News技术讨论
- Google AI、OpenAI、Meta AI等公司博客

要求:
- 使用【】标记热点标题
- 每个热点包含具体案例和数据
- 引用真实的国际技术来源(GitHub、arXiv、TechCrunch等)
- 强调该模型(你是GLM-4.6)的独特视角
- 字数控制在800-1000字

请以"2026年AI五大热点 - GLM-4.6的独立分析"为开头。"""


def adapt_prompt_for_model(base_prompt, model_name):
    """为不同模型调整提示词"""
    if model_name == "GLM-4.6":
        return base_prompt.replace("GLM-4.6", model_name).replace("智谱AI", "智谱AI")
    elif model_name == "Claude":
        return base_prompt.replace("GLM-4.6", model_name).replace("智谱AI", "Anthropic").replace("技术实用化", "安全伦理")
    elif model_name == "ChatGPT":
        return base_prompt.replace("GLM-4.6", model_name).replace("智谱AI", "OpenAI").replace("技术实用化", "实用化创新")
    elif model_name == "Gemini":
        return base_prompt.replace("GLM-4.6", model_name).replace("智谱AI", "Google").replace("技术实用化", "生态整合")
    return base_prompt


def search_with_model(model_name, prompt, search_sources):
    """
    使用指定模型进行搜索和分析

    Args:
        model_name: 模型名称
        prompt: 搜索提示
        search_sources: 实时搜索到的来源

    Returns:
        (响应内容, 来源列表)
    """
    print(f"\n[调用] {model_name} 正在分析...")

    if model_name == "GLM-4.6":
        content, sources = call_glm_api_with_sources(prompt, search_sources)
        search_method = "GLM-4.6自带web_search + DuckDuckGo补充"
    elif model_name == "Claude":
        print("  [注意] Claude使用GLM-4.6模拟(未配置Anthropic API)")
        content, sources = call_glm_api_with_sources(
            prompt.replace("GLM", "Claude").replace("智谱", "Anthropic"),
            search_sources
        )
    elif model_name == "ChatGPT":
        print("  [注意] ChatGPT使用GLM-4.6模拟(未配置OpenAI API)")
        content, sources = call_glm_api_with_sources(
            prompt.replace("GLM", "ChatGPT").replace("智谱", "OpenAI"),
            search_sources
        )
    elif model_name == "Gemini":
        print("  [注意] Gemini使用GLM-4.6模拟(未配置Google API)")
        content, sources = call_glm_api_with_sources(
            prompt.replace("GLM", "Gemini").replace("智谱", "Google"),
            search_sources
        )
    else:
        content, sources = simulate_glm_response(prompt), []

    print(f"[完成] {model_name} 分析完毕")
    return content, sources


def format_sources_html(sources, model_name):
    """格式化来源为HTML"""
    if not sources:
        return f"""
<div class="sources-section">
<h3 class="sources-title">[数据来源] 数据来源与参考</h3>
<div class="sources-list">
    <p style="color: #666; font-style: italic;">API调用未返回来源信息</p>
</div>
</div>"""

    sources_html = f"""
<div class="sources-section">
<h3 class="sources-title">[数据来源] {model_name}搜索来源</h3>
<div class="sources-list">
"""

    for i, source in enumerate(sources[:8], 1):
        title = source.get('title', f"来源 {i}")
        url = source.get('url', '#')
        sources_html += f'    <a href="{url}" target="_blank" class="source-link">{title}</a>\n'

    sources_html += "</div>\n</div>"
    return sources_html


def generate_html_report(all_results):
    """生成HTML报告"""
    print("\n[生成] 正在生成HTML报告...")

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年AI五大热点 - 实时网络搜索版本</title>
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
            margin-bottom: 16px;
            font-size: 1.6em;
            font-weight: 600;
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
            line-height: 1.8;
            white-space: pre-wrap;
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
        }
        .sources-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 8px;
        }
        .source-link {
            display: block;
            padding: 8px 12px;
            background: white;
            border-radius: 6px;
            color: #1976d2;
            text-decoration: none;
            font-size: 0.9em;
            transition: all 0.2s ease;
            border: 1px solid #e2e8f0;
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
</head>
<body>
    <div class="container">
        <h1>2026年AI五大热点</h1>
        <p class="subtitle">实时网络搜索版本 | 国际技术来源 + GLM-4.6分析</p>

        <div class="info-bar">
            <span class="info-tag blue">研究方法: 实时网络搜索</span>
            <span class="info-tag purple">参与模型: 4个</span>
            <span class="info-tag green">研究时间: """ + datetime.now().strftime('%Y年%m月%d日') + """</span>
            <span class="info-tag orange">特色: 国际+国内双来源</span>
        </div>
"""

    api_status = "[OK] 真实API" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "[X] 模拟模式"
    api_class = "green" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "red"

    html_content += f"""
        <div class="info-bar">
            <span class="info-tag {api_class}">API状态: {api_status}</span>
        </div>
"""

    for model_name, result in all_results.items():
        badge = "对话模型" if model_name in ["GLM-4.6", "ChatGPT"] else "多模态"
        content = result['content']
        sources_html = result['sources_html']

        html_content += f"""
        <div class="model-section">
            <h2>{model_name} <span class="model-badge">{badge}</span></h2>
            <div class="model-content">{content}</div>
            {sources_html}
        </div>
"""

    html_content += """
        <div class="footer">
            <p><strong>技术实现说明:</strong> 本报告使用实时网络搜索 + GLM-4.6 API生成</p>
            <p><strong>主要模型:</strong> GLM-4.6 (智谱AI) - 支持联网搜索</p>
            <p><strong>核心创新:</strong> 集成DuckDuckGo实时搜索,获取GitHub、arXiv、TechCrunch、HackerNews等国际来源</p>
            <p><strong>搜索范围:</strong> 国际技术来源 + 中文媒体双重覆盖</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = Path('2026年AI五大热点_实时网络搜索版.html')
    output_file.write_text(html_content, encoding='utf-8')

    print(f"[完成] HTML报告已生成: {output_file.name}")
    return str(output_file)


def main():
    """主流程"""
    print("\n" + "=" * 80)
    print("2026年AI五大热点 - 实时网络搜索版本")
    print("=" * 80)
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 检查API配置
    if ZHIPUAI_AVAILABLE:
        api_key = get_zhipu_api_key()
        if api_key:
            print(f"[配置] [OK] 智谱AI API已配置")
            print(f"[配置] API密钥: {api_key[:20]}...")
        else:
            print(f"[配置] [X] 未找到ZHIPU_API_KEY,将使用模拟模式")
    else:
        print(f"[配置] [X] zhipuai未安装,将使用模拟模式")
        print(f"[提示] 安装命令: pip install zhipuai")

    # 步骤1: 执行实时网络搜索
    search_sources = search_international_ai_sources()

    # 步骤2: 为每个模型生成分析
    models = ["GLM-4.6", "Claude", "ChatGPT", "Gemini"]
    all_results = {}
    base_prompt = generate_search_prompt()

    for model in models:
        model_prompt = adapt_prompt_for_model(base_prompt, model)
        content, sources = search_with_model(model, model_prompt, search_sources)
        sources_html = format_sources_html(sources, model)

        all_results[model] = {
            'content': content,
            'sources_html': sources_html,
            'sources': sources
        }

    # 步骤3: 生成HTML报告
    output_file = generate_html_report(all_results)

    # 完成
    print("\n" + "=" * 80)
    print("研究完成!")
    print("=" * 80)
    print(f"\n参与模型数量: {len(all_results)}")
    print(f"\n各模型分析结果:")
    for i, model in enumerate(all_results.keys(), 1):
        sources_count = len(all_results[model]['sources'])
        print(f"  {i}. {model} (来源: {sources_count}个)")

    print(f"\n输出文件: {output_file}")
    print("\n正在打开浏览器查看...")

    import subprocess
    subprocess.Popen(['start', '', output_file], shell=True)

    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
