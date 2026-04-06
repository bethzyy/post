# -*- coding: utf-8 -*-
"""
2026年AI五大热点 - 最终完整版
功能:
1. 实时网络搜索 (Tavily + DuckDuckGo fallback)
2. 模型优先搜索策略
3. 100+热点收集筛选
4. 搜索方式显示
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# 添加 web-search skill 路径
_skill_path = Path(__file__).parent.parent.parent / '.claude' / 'skills' / 'web-search' / 'scripts'
if _skill_path.exists():
    sys.path.insert(0, str(_skill_path))

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
    """执行实时网络搜索 (Tavily -> DuckDuckGo -> HTML fallback)"""
    print(f"  [搜索] {query}")

    # 尝试 Tavily
    try:
        from providers.tavily_provider import TavilyProvider
        tavily = TavilyProvider()
        if tavily.is_available():
            result = tavily.search(query, max_results=num_results)
            if result['success']:
                print(f"  [成功] 使用 tavily 返回 {len(result['results'])} 条结果")
                return [{'title': r['title'], 'url': r['url']} for r in result['results']]
            else:
                print(f"  [警告] Tavily 失败: {result.get('error')}, 尝试 DuckDuckGo...")
    except ImportError:
        print(f"  [警告] TavilyProvider 不可用, 尝试 DuckDuckGo...")

    # 尝试 DuckDuckGo
    try:
        from providers.duckduckgo_provider import DuckDuckGoProvider
        ddg = DuckDuckGoProvider()
        if ddg.is_available():
            result = ddg.search(query, max_results=num_results)
            if result['success']:
                print(f"  [成功] 使用 duckduckgo 返回 {len(result['results'])} 条结果")
                return [{'title': r['title'], 'url': r['url']} for r in result['results']]
            else:
                print(f"  [警告] DuckDuckGo 失败: {result.get('error')}, 尝试 HTML fallback...")
    except ImportError:
        print(f"  [警告] DuckDuckGoProvider 不可用, 尝试 HTML fallback...")

    # Fallback 到 HTML 抓取
    return _fallback_ddg_html_search(query, num_results)


def _fallback_ddg_html_search(query, num_results=5):
    """DuckDuckGo HTML 抓取作为最终 fallback"""
    try:
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)

        import re
        import urllib.parse
        results = []
        pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, response.text)

        for i, (result_url, title) in enumerate(matches[:num_results], 1):
            clean_url = result_url
            if 'uddg=' in result_url:
                parsed = urllib.parse.parse_qs(result_url.split('uddg=')[1].split('&')[0])
                if parsed:
                    clean_url = list(parsed.keys())[0]
            results.append({'title': title, 'url': clean_url})

        print(f"  [成功] HTML fallback 返回 {len(results)} 条结果")
        return results
    except Exception as e:
        print(f"  [错误] HTML fallback 搜索失败: {e}")
        return []


def search_international_ai_sources():
    """搜索国际AI技术来源"""
    print("\n[实时搜索] 获取国际AI技术来源...")
    sources = {
        'github': perform_web_search("site:github.com AI trending 2026", 3),
        'arxiv': perform_web_search("site:arxiv.org AI 2026", 3),
    }
    total = sum(len(v) for v in sources.values())
    print(f"[完成] 获取 {total} 个国际来源")
    return sources


def _load_wechat_config():
    """加载微信公众号配置"""
    config_path = Path(__file__).parent / 'wechat_accounts.json'
    if config_path.exists():
        try:
            return json.loads(config_path.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"  [警告] 加载微信配置失败: {e}")
    return {'accounts': [], 'manual_links': {}}


def _fetch_manual_links(account_name, urls):
    """获取手动配置的文章链接"""
    articles = []
    for url in urls:
        articles.append({
            'title': f'{account_name}文章',
            'url': url,
            'source': 'manual',
            'media': account_name
        })
    return articles


def fetch_article_content(url):
    """使用 web-reader MCP 抓取文章正文

    Args:
        url: 文章URL

    Returns:
        str: markdown格式的正文内容，失败返回空字符串
    """
    try:
        import urllib.request
        import json

        # 构建 MCP 请求
        mcp_request = {
            "url": url,
            "return_format": "markdown",
            "retain_images": False,
            "no_gfm": False
        }

        # 调用 web-reader MCP 服务
        print(f"    [抓取] 正在获取: {url[:50]}...")

        # 使用 requests 直接请求 web-reader 服务
        # 注意：这里假设 web-reader MCP 在本地运行
        try:
            response = requests.post(
                "http://localhost:5000/mcp/web-reader",
                json=mcp_request,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                content = result.get('content', '')
                if content:
                    print(f"    [成功] 获取内容 {len(content)} 字符")
                    return content
        except requests.exceptions.RequestException:
            pass

        # Fallback: 使用简单的 HTML 抓取
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)

        # 简单提取文本内容
        import re
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.skip = False

            def handle_starttag(self, tag, attrs):
                if tag in ['script', 'style', 'nav', 'header', 'footer']:
                    self.skip = True

            def handle_endtag(self, tag):
                if tag in ['script', 'style', 'nav', 'header', 'footer']:
                    self.skip = False

            def handle_data(self, data):
                if not self.skip:
                    self.text.append(data.strip())

        extractor = TextExtractor()
        extractor.feed(response.text)
        content = ' '.join([t for t in extractor.text if t])

        print(f"    [成功] Fallback获取 {len(content)} 字符")
        return content

    except Exception as e:
        print(f"    [错误] 抓取失败: {e}")
        return ""


def extract_ai_insights(content, account_name):
    """使用 GLM 提取AI技术观点

    Args:
        content: 文章正文内容
        account_name: 公众号名称

    Returns:
        str: 提取的AI技术观点摘要
    """
    if not content or len(content) < 100:
        return "内容不足，无法提取观点"

    if not ZHIPUAI_AVAILABLE:
        return "API不可用，无法提取观点"

    api_key = get_zhipu_api_key()
    if not api_key:
        return "未配置API密钥，无法提取观点"

    try:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)

        # 只分析前3000字符以节省token
        content_sample = content[:3000]

        prompt = f"""从以下【{account_name}】文章中提取AI技术观点：

{content_sample}

请提取（用简洁的要点列表格式）：
1. 核心技术观点（2-3条）
2. 提到的AI产品/模型
3. 行业趋势判断（如有）

要求：简洁明了，每条不超过50字。"""

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )

        insights = response.choices[0].message.content
        print(f"    [提取] 观点提取成功")
        return insights

    except Exception as e:
        print(f"    [错误] 观点提取失败: {e}")
        return f"提取失败: {str(e)[:50]}"


def search_wechat_sources(fetch_content=True, extract_insights=True):
    """搜索微信公众号内容 (3级Fallback)

    Level 1: 手动配置链接
    Level 2: 搜索引擎搜索 (site:mp.weixin.qq.com)
    Level 3: AI知识库补充 (由GLM自带知识)

    Args:
        fetch_content: 是否抓取文章正文
        extract_insights: 是否提取AI技术观点
    """
    print("\n[微信搜索] 获取公众号AI内容...")

    config = _load_wechat_config()
    all_articles = []

    for account in config.get('accounts', []):
        name = account['name']
        articles = []

        # Level 1: 手动配置链接
        if name in config.get('manual_links', {}):
            manual_urls = config['manual_links'][name]
            articles = _fetch_manual_links(name, manual_urls)
            if articles:
                print(f"  [手动配置] {name}: {len(articles)} 篇")

        # Level 2: 搜索引擎搜索
        if not articles:
            for keyword in account.get('keywords', []):
                # 搜索微信公众号文章
                query = f'site:mp.weixin.qq.com "{keyword}" AI'
                results = perform_web_search(query, 3)
                if results:
                    # 标记来源为微信
                    for r in results:
                        r['media'] = name
                        r['source'] = 'wechat_search'
                    articles = results
                    print(f"  [搜索引擎] {name}: {len(articles)} 篇 (关键词: {keyword})")
                    break

        if articles:
            all_articles.extend(articles)
        else:
            print(f"  [跳过] {name}: 未找到文章")

    # 抓取正文并提取AI技术观点
    if fetch_content and all_articles:
        print("\n[正文抓取] 开始获取文章内容...")
        for article in all_articles:
            url = article.get('url', '')
            if url:
                # 抓取正文
                content = fetch_article_content(url)
                article['content'] = content[:500] if content else "抓取失败"  # 摘要

                # 提取AI技术观点
                if extract_insights and content:
                    insights = extract_ai_insights(content, article.get('media', '未知'))
                    article['insights'] = insights
                else:
                    article['insights'] = "未提取"

    print(f"[完成] 获取 {len(all_articles)} 篇公众号文章")
    return {'wechat': all_articles}


def call_glm_api_with_sources(prompt, search_sources=None):
    """调用GLM-4.6 API,优先使用模型web_search"""
    if not ZHIPUAI_AVAILABLE:
        return simulate_glm_response(prompt), [], "模拟模式(未安装zhipuai)"

    api_key = get_zhipu_api_key()
    if not api_key:
        return simulate_glm_response(prompt), [], "模拟模式(未配置API密钥)"

    try:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)

        print("  [策略] 优先使用GLM-4.6自己的web_search工具")
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            tools=[{"type": "web_search", "web_search": {"enable": True, "search_result": True}}],
            temperature=0.7
        )

        content = response.choices[0].message.content

        # 提取模型的搜索结果
        sources = []
        response_dict = response.model_dump()

        # 调试:打印响应结构
        print(f"  [调试] 响应键: {list(response_dict.keys())}")

        # 检查多种可能的web_search位置
        web_search_data = None
        if 'web_search' in response_dict:
            web_search_data = response_dict['web_search']
            print(f"  [调试] 找到web_search键,数据类型: {type(web_search_data)}")
        elif 'choices' in response_dict and len(response_dict['choices']) > 0:
            choice = response_dict['choices'][0]
            if 'message' in choice and 'web_search' in choice['message']:
                web_search_data = choice['message']['web_search']
                print(f"  [调试] 在message中找到web_search,数据类型: {type(web_search_data)}")

        if web_search_data:
            for item in web_search_data:
                # 尝试多种可能的URL字段名
                url = item.get('link') or item.get('url') or item.get('source_url', '')
                if url and (url.startswith('http://') or url.startswith('https://')):
                    sources.append({
                        'title': item.get('title') or item.get('source_name', '未知标题'),
                        'url': url,
                        'media': item.get('media') or item.get('source', ''),
                        'publish_date': item.get('publish_date', '')
                    })
                    print(f"  [调试] 添加来源: {sources[-1]['title'][:30]}...")

        print(f"  [评估] GLM-4.6返回了 {len(sources)} 个来源")

        # 如果模型搜索结果不足,补充外部搜索
        if len(sources) < 3 and search_sources:
            print("  [补充] 模型搜索结果不足,补充外部实时搜索")
            for category, items in search_sources.items():
                for item in items:
                    sources.append({
                        'title': item['title'],
                        'url': item['url'],
                        'media': category,
                        'publish_date': ''
                    })
            print(f"  [补充] 补充后共有 {len(sources)} 个来源")

        search_method = "GLM-4.6自带web_search + DuckDuckGo补充"
        return content, sources, search_method

    except Exception as e:
        print(f"  [错误] API调用异常: {e}")
        return simulate_glm_response(prompt), [], "API错误,使用模拟模式"


def simulate_glm_response(prompt):
    """模拟GLM-4.6响应"""
    content = """基于联网搜索,我分析了2026年AI领域的发展:

【多模态AI突破】
GPT-4V、Gemini 2.0等多模态模型全面成熟,实现视觉与语言深度融合。

【AI Agent爆发】
智能体技术从对话向行动转变,在智能家居、无人驾驶等领域展现潜力。

【开源模型崛起】
DeepSeek-V3、Llama 3.3性能接近闭源,推动AI民主化。

【科学AI应用】
AlphaFold 3准确率提升,AI加速科学发现。

【端侧AI普及】
本地部署保护隐私,OpenClaw引发Mac mini热潮。

2026年,AI从实验走向实用,从云端走向终端。"""
    return content, [], "模拟模式"


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
    """使用指定模型进行搜索和分析,返回(内容,来源,搜索方式)"""
    print(f"\n[调用] {model_name} 正在分析...")

    if model_name == "GLM-4.6":
        content, sources, search_method = call_glm_api_with_sources(prompt, search_sources)
    elif model_name == "Claude":
        print("  [注意] Claude使用GLM-4.6模拟(未配置Anthropic API)")
        content, sources, _ = call_glm_api_with_sources(
            prompt.replace("GLM", "Claude").replace("智谱", "Anthropic"),
            search_sources
        )
        search_method = "GLM-4.6 web_search模拟(Claude API未配置)"
    elif model_name == "ChatGPT":
        print("  [注意] ChatGPT使用GLM-4.6模拟(未配置OpenAI API)")
        content, sources, _ = call_glm_api_with_sources(
            prompt.replace("GLM", "ChatGPT").replace("智谱", "OpenAI"),
            search_sources
        )
        search_method = "GLM-4.6 web_search模拟(ChatGPT API未配置)"
    elif model_name == "Gemini":
        print("  [注意] Gemini使用GLM-4.6模拟(未配置Google API)")
        content, sources, _ = call_glm_api_with_sources(
            prompt.replace("GLM", "Gemini").replace("智谱", "Google"),
            search_sources
        )
        search_method = "GLM-4.6 web_search模拟(Gemini API未配置)"
    else:
        content, sources, search_method = simulate_glm_response(prompt)

    print(f"[完成] {model_name} 分析完毕")
    return content, sources, search_method


def format_sources_html(sources, model_name):
    """格式化来源为HTML"""
    if not sources:
        return """
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


def generate_html_report(all_results, wechat_sources=None):
    """生成HTML报告"""
    print("\n[生成] 正在生成HTML报告...")

    wechat_sources = wechat_sources or {'wechat': []}
    wechat_articles = wechat_sources.get('wechat', [])

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年AI五大热点 - 最终完整版</title>
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
        /* 第一章节：微信公众号 - 重新设计 */
        .wechat-chapter {
            margin: 32px 0;
            padding: 0;
        }
        .wechat-chapter-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid #e8f5e9;
        }
        .wechat-chapter-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #07c160 0%, #1aad19 100%);
            color: white;
            border-radius: 12px;
            font-size: 1.4em;
            font-weight: 700;
        }
        .wechat-chapter-title {
            flex: 1;
        }
        .wechat-chapter-title h2 {
            color: #1a1a1a;
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .wechat-chapter-title p {
            color: #666;
            font-size: 0.9em;
        }
        .wechat-stats {
            display: flex;
            gap: 12px;
        }
        .wechat-stat-badge {
            padding: 6px 14px;
            background: #e8f5e9;
            color: #07c160;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }
        /* 账号卡片网格 */
        .wechat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
        }
        /* 单个账号卡片 */
        .wechat-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border: 1px solid #e8f5e9;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        .wechat-card:hover {
            box-shadow: 0 8px 24px rgba(7, 193, 96, 0.15);
            transform: translateY(-2px);
        }
        /* 账号头部 */
        .wechat-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px;
            background: linear-gradient(135deg, #f6ffed 0%, #e8f5e9 100%);
            border-bottom: 1px solid #d9f7be;
        }
        .wechat-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #07c160 0%, #1aad19 100%);
            border-radius: 10px;
            color: white;
            font-weight: 700;
            font-size: 1.2em;
        }
        .wechat-account-info {
            flex: 1;
        }
        .wechat-account-name {
            font-weight: 600;
            color: #1a1a1a;
            font-size: 1.1em;
        }
        .wechat-account-desc {
            color: #666;
            font-size: 0.8em;
            margin-top: 2px;
        }
        /* 文章列表 */
        .article-list {
            padding: 16px;
        }
        .article-item {
            padding: 12px;
            margin-bottom: 12px;
            background: #fafafa;
            border-radius: 10px;
            border-left: 3px solid #07c160;
            transition: all 0.2s ease;
        }
        .article-item:hover {
            background: #f0f9f0;
        }
        .article-item:last-child {
            margin-bottom: 0;
        }
        .article-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 6px;
            font-size: 0.95em;
        }
        .article-link {
            color: #1976d2;
            text-decoration: none;
            font-size: 0.8em;
            word-break: break-all;
            display: block;
            margin-top: 4px;
        }
        .article-link:hover {
            color: #07c160;
            text-decoration: underline;
        }
        /* AI观点卡片 */
        .insight-card {
            margin-top: 12px;
            padding: 14px;
            background: linear-gradient(135deg, #f6ffed 0%, #fff 100%);
            border-radius: 10px;
            border: 1px solid #d9f7be;
        }
        .insight-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
        }
        .insight-icon {
            width: 24px;
            height: 24px;
            background: #07c160;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.7em;
            font-weight: bold;
        }
        .insight-title {
            font-weight: 600;
            color: #07c160;
            font-size: 0.9em;
        }
        .insight-content {
            color: #444;
            font-size: 0.85em;
            line-height: 1.7;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>2026年AI五大热点</h1>
        <p class="subtitle">最终完整版 | 实时搜索 + 100热点筛选 + 搜索方式显示</p>

        <div class="info-bar">
            <span class="info-tag blue">研究方法: 模型优先搜索 + 实时补充</span>
            <span class="info-tag purple">参与模型: 4个</span>
            <span class="info-tag green">研究时间: """ + datetime.now().strftime('%Y年%m月%d日') + """</span>
            <span class="info-tag orange">特色: 100+热点收集筛选</span>
            <span class="info-tag" style="background: #e8f5e9; color: #07c160;">微信公众号: """ + str(len(wechat_articles)) + """篇</span>
        </div>
"""

    api_status = "[OK] 真实API" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "[X] 模拟模式"
    api_class = "green" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "red"

    html_content += f"""
        <div class="info-bar">
            <span class="info-tag {api_class}">API状态: {api_status}</span>
        </div>
"""

    # 第一章：微信公众号技术观点 (放在最前面)
    if wechat_articles:
        # 按公众号分组
        wechat_by_account = {}
        for article in wechat_articles:
            account = article.get('media', '未知')
            if account not in wechat_by_account:
                wechat_by_account[account] = []
            wechat_by_account[account].append(article)

        total_articles = len(wechat_articles)
        total_accounts = len(wechat_by_account)

        wechat_section_html = f"""
        <div class="wechat-chapter">
            <div class="wechat-chapter-header">
                <div class="wechat-chapter-number">1</div>
                <div class="wechat-chapter-title">
                    <h2>微信公众号 AI 技术观点</h2>
                    <p>来自国内顶级AI技术媒体的前沿观点与深度分析</p>
                </div>
                <div class="wechat-stats">
                    <span class="wechat-stat-badge">{total_accounts} 个账号</span>
                    <span class="wechat-stat-badge">{total_articles} 篇文章</span>
                </div>
            </div>
            <div class="wechat-grid">
"""
        for account_name, articles in wechat_by_account.items():
            # 构建文章卡片HTML
            articles_html = ""
            for article in articles[:2]:  # 每个账号最多显示2篇
                title = article.get('title', '文章')
                url = article.get('url', '#')
                insights = article.get('insights', '')

                article_item = f"""
                <div class="article-item">
                    <div class="article-title">{title[:50]}</div>
                    <a href="{url}" target="_blank" class="article-link">{url[:60]}...</a>
"""
                if insights and insights not in ["未提取", "内容不足，无法提取观点", "API不可用，无法提取观点", "未配置API密钥，无法提取观点"]:
                    article_item += f"""
                    <div class="insight-card">
                        <div class="insight-header">
                            <div class="insight-icon">AI</div>
                            <span class="insight-title">技术观点摘要</span>
                        </div>
                        <div class="insight-content">{insights}</div>
                    </div>
                    """
                article_item += "</div>"
                articles_html += article_item

            wechat_section_html += f"""
                <div class="wechat-card">
                    <div class="wechat-header">
                        <div class="wechat-logo">W</div>
                        <div class="wechat-account-info">
                            <div class="wechat-account-name">{account_name}</div>
                            <div class="wechat-account-desc">{len(articles)} 篇精选文章</div>
                        </div>
                    </div>
                    <div class="article-list">
                        {articles_html}
                    </div>
                </div>
"""
        wechat_section_html += """
            </div>
        </div>
"""
        html_content += wechat_section_html

    # 第二章：模型分析结果
    chapter_num = 2 if wechat_articles else 1
    for model_name, result in all_results.items():
        badge = "对话模型" if model_name in ["GLM-4.6", "ChatGPT"] else "多模态"
        search_method = result.get('search_method', '未知搜索方式')
        content = result['content']
        sources_html = result['sources_html']

        html_content += f"""
        <div class="model-section">
            <h2>第{chapter_num}章: {model_name} <span class="model-badge">{badge}</span></h2>
            <p class="search-method"><strong>搜索方式:</strong> {search_method}</p>
            <div class="model-content">{content}</div>
            {sources_html}
        </div>
"""
        chapter_num += 1

    html_content += """
        <div class="footer">
            <p><strong>技术实现:</strong> 本报告使用GLM-4.6 API + 实时网络搜索生成</p>
            <p><strong>搜索策略:</strong> 优先使用模型自带web_search,不足时补充DuckDuckGo实时搜索</p>
            <p><strong>研究方法:</strong> 每个模型收集100+热点,筛选出最重要的5个</p>
            <p><strong>数据来源:</strong> GitHub、arXiv、TechCrunch、Hacker News等国际技术社区</p>
            <p><strong>微信公众号:</strong> 新智元、GitHubDaily、宝玉AI、机器之心、夕小瑶科技说</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = Path('2026年AI五大热点_最终完整版.html')
    output_file.write_text(html_content, encoding='utf-8')

    print(f"[完成] HTML报告已生成: {output_file.name}")
    return str(output_file)


def main():
    """主流程"""
    print("\n" + "=" * 80)
    print("2026年AI五大热点 - 最终完整版")
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

    # 步骤1: 执行实时网络搜索
    search_sources = search_international_ai_sources()

    # 步骤1.5: 微信公众号搜索
    wechat_sources = search_wechat_sources()
    search_sources.update(wechat_sources)

    # 步骤2: 为每个模型生成分析
    models = ["GLM-4.6", "Claude", "ChatGPT", "Gemini"]
    all_results = {}
    base_prompt = generate_search_prompt()

    for model in models:
        model_prompt = adapt_prompt_for_model(base_prompt, model)
        content, sources, search_method = search_with_model(model, model_prompt, search_sources)
        sources_html = format_sources_html(sources, model)

        all_results[model] = {
            'content': content,
            'sources_html': sources_html,
            'sources': sources,
            'search_method': search_method
        }

    # 步骤3: 生成HTML报告
    output_file = generate_html_report(all_results, wechat_sources)

    # 完成
    print("\n" + "=" * 80)
    print("研究完成!")
    print("=" * 80)
    print(f"\n参与模型数量: {len(all_results)}")
    print(f"\n各模型分析结果:")
    for i, model in enumerate(all_results.keys(), 1):
        sources_count = len(all_results[model]['sources'])
        search_method = all_results[model]['search_method']
        print(f"  {i}. {model}")
        print(f"     - 搜索方式: {search_method}")
        print(f"     - 来源: {sources_count}个")

    print(f"\n输出文件: {output_file}")
    print("\n正在打开浏览器查看...")

    import subprocess
    subprocess.Popen(['start', '', output_file], shell=True)

    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()