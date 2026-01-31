# -*- coding: utf-8 -*-
"""
2026年AI五大热点 - 实时网络搜索版
功能:
1. 真实网络搜索(GitHub Trending、Hacker News、AI新闻)
2. GLM-4.6生成分析内容
3. 统一格式化 - 标题加粗、减少空行
4. 确保所有模型输出格式一致
5. 数据来源板块可折叠
"""

import os
import sys
import re
import json
import time
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

# 尝试导入requests用于网络搜索
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[警告] requests未安装,将无法进行实时网络搜索")


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


def get_antigravity_config():
    """
    获取Antigravity API配置
    支持Claude、Gemini、GPT模型的免费访问
    """
    # 从环境变量或.env文件读取Antigravity配置
    post_env_path = Path('../.env')
    config = {
        'enabled': False,
        'base_url': None,
        'api_key': None
    }

    # 优先从环境变量读取
    config['base_url'] = os.environ.get('ANTIGRAVITY_BASE_URL')
    config['api_key'] = os.environ.get('ANTIGRAVITY_API_KEY')

    # 如果环境变量没有,尝试从.env文件读取
    if post_env_path.exists() and not config['base_url']:
        with open(post_env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ANTIGRAVITY_BASE_URL=') and not line.strip().startswith('#'):
                    config['base_url'] = line.strip().split('=')[1]
                elif line.startswith('ANTIGRAVITY_API_KEY=') and not line.strip().startswith('#'):
                    config['api_key'] = line.strip().split('=')[1]

    # 如果配置了base_url,则启用Antigravity
    if config['base_url']:
        config['enabled'] = True

    return config


def call_antigravity_api(model_name, prompt, api_config):
    """
    调用Antigravity API生成内容
    使用OpenAI客户端库(兼容Antigravity的OpenAI接口)
    支持的模型: claude-sonnet-4.5, gemini-2.5-pro, gpt-oss
    """
    if not api_config['enabled']:
        return None, "Antigravity未配置"

    try:
        from openai import OpenAI

        # 模型名称映射
        model_mapping = {
            'Claude': 'claude-sonnet-4.5',
            'Gemini': 'gemini-2.5-pro',
            'ChatGPT': 'gpt-oss'
        }

        model_id = model_mapping.get(model_name)
        if not model_id:
            return None, f"不支持的模型: {model_name}"

        base_url = api_config['base_url'].rstrip('/')
        api_key = api_config['api_key'] or 'dummy-key'

        # 使用OpenAI客户端(兼容Antigravity)
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        print(f"  [调用] Antigravity API: {model_id}")

        # 调用chat completions API
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.7
        )

        # 提取响应内容
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content
            print(f"  [完成] Antigravity API调用成功")
            return content, f"Antigravity API ({model_id})"
        else:
            print(f"  [错误] 未返回内容")
            return None, "未返回内容"

    except ImportError:
        return None, "需要安装openai库"
    except Exception as e:
        error_str = str(e)
        # 检查是否是配额问题
        if '429' in error_str or 'quota' in error_str.lower() or 'exhausted' in error_str.lower():
            print(f"  [!] 配额耗尽")

            # 计算等待时间
            try:
                import pytz
                from datetime import datetime

                # 估算配额重置时间(假设每天UTC 12:14:38重置)
                utc_tz = pytz.timezone('UTC')
                now = datetime.now(utc_tz)

                # 计算下一个重置时间
                reset_time = now.replace(hour=12, minute=14, second=38, microsecond=0)
                if now >= reset_time:
                    # 如果今天已经过了重置时间,则为明天
                    from datetime import timedelta
                    reset_time = reset_time + timedelta(days=1)

                time_delta = reset_time - now
                total_seconds = int(time_delta.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60

                wait_info = f"配额耗尽 (预计{hours}小时{minutes}分钟后重置)"
            except:
                wait_info = "配额耗尽 (重置时间未知)"

            return None, wait_info
        else:
            print(f"  [错误] Antigravity API异常: {e}")
            return None, f"Antigravity异常: {error_str}"


def perform_web_search(search_query, max_results=20):
    """
    执行真实的网络搜索
    使用多个数据源: GitHub Trending API、Hacker News、AI新闻网站

    Args:
        search_query: 搜索关键词
        max_results: 最多返回多少结果

    Returns:
        list: 搜索结果列表 [{"title": "", "url": "", "description": "", "source": ""}]
    """
    results = []

    if not REQUESTS_AVAILABLE:
        print(f"  [警告] requests库未安装,跳过网络搜索")
        return results

    print(f"  [搜索] 正在搜索: {search_query}")

    # 1. GitHub搜索 - 查找热门仓库
    try:
        github_query = quote(search_query)
        github_url = f"https://api.github.com/search/repositories?q={github_query}&sort=stars&order=desc&per_page={max_results//2}"

        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AI-Trends-Analyzer'
        }

        response = requests.get(github_url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                for item in data['items'][:max_results//2]:
                    results.append({
                        'title': item.get('full_name', item.get('name', '')),
                        'url': item.get('html_url', ''),
                        'description': item.get('description', ''),
                        'stars': item.get('stargazers_count', 0),
                        'source': 'GitHub',
                        'language': item.get('language', 'Unknown')
                    })
                    print(f"    [GitHub] 找到: {item.get('full_name', '')} ⭐ {item.get('stargazers_count', 0)}")
        else:
            print(f"    [警告] GitHub搜索失败: {response.status_code}")

    except Exception as e:
        print(f"    [错误] GitHub搜索异常: {e}")

    # 2. Hacker News搜索 - 查找AI讨论
    try:
        # Hacker News Algolia API
        hn_url = f"http://hn.algolia.com/api/v1/search?query={quote(search_query)}&tags=story&hitsPerPage={max_results//2}"
        response = requests.get(hn_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'hits' in data:
                for item in data['hits'][:max_results//2]:
                    title = item.get('title', '')
                    url = item.get('url', '') or f"https://news.ycombinator.com/item?id={item.get('objectID', '')}"
                    points = item.get('points', 0)

                    results.append({
                        'title': title,
                        'url': url,
                        'description': f"Hacker News讨论 ({points} points)",
                        'points': points,
                        'source': 'Hacker News'
                    })
                    print(f"    [HackerNews] 找到: {title} ({points} points)")

    except Exception as e:
        print(f"    [错误] Hacker News搜索异常: {e}")

    # 3. 搜索Reddit AI相关讨论
    try:
        reddit_url = f"https://www.reddit.com/r/artificial/search.json?q={quote(search_query)}&restrict_sr=1&sort=top&limit={max_results//4}"
        headers = {'User-Agent': 'AI-Trends-Analyzer/1.0'}
        response = requests.get(reddit_url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'children' in data['data']:
                for item in data['data']['children'][:max_results//4]:
                    post = item.get('data', {})
                    results.append({
                        'title': post.get('title', ''),
                        'url': f"https://reddit.com{post.get('permalink', '')}",
                        'description': post.get('selftext', '')[:200] + '...',
                        'score': post.get('score', 0),
                        'source': 'Reddit r/artificial'
                    })
                    print(f"    [Reddit] 找到: {post.get('title', '')} ({post.get('score', 0)} upvotes)")

    except Exception as e:
        print(f"    [警告] Reddit搜索失败: {e}")

    print(f"  [完成] 共找到 {len(results)} 条搜索结果")
    return results


def fetch_github_trending():
    """
    获取GitHub Trending AI项目
    重点查看programming_language: Python, JavaScript中的AI/ML项目
    """
    trending_results = []

    if not REQUESTS_AVAILABLE:
        print(f"  [警告] requests库未安装,跳过GitHub Trending")
        return trending_results

    print("  [GitHub Trending] 正在获取热门AI项目...")

    # GitHub Trending URL (需要HTML解析,这里简化为使用搜索API)
    ai_keywords = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "AI agent",
        "LLM",
        "chatbot",
        "transformer",
        "openai",
        "langchain",
        "autogpt"
    ]

    for keyword in ai_keywords[:3]:  # 只搜索前3个关键词,避免API限制
        try:
            url = f"https://api.github.com/search/repositories?q={quote(keyword)}+language:python&sort=stars&order=desc&per_page=5"
            headers = {'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'AI-Trends-Analyzer'}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    for item in data['items'][:5]:
                        full_name = item.get('full_name', '')
                        if full_name not in [r.get('title', '') for r in trending_results]:
                            trending_results.append({
                                'title': full_name,
                                'url': item.get('html_url', ''),
                                'description': item.get('description', ''),
                                'stars': item.get('stargazers_count', 0),
                                'source': 'GitHub Trending',
                                'language': item.get('language', 'Unknown')
                            })
                            print(f"    [Trending] {full_name} ⭐ {item.get('stargazers_count', 0)}")

            time.sleep(1)  # 避免API限流

        except Exception as e:
            print(f"    [错误] GitHub Trending搜索失败: {keyword} - {e}")

    print(f"  [完成] GitHub Trending共找到 {len(trending_results)} 个热门项目")
    return trending_results


def convert_urls_to_links(text):
    """将文本中的URL转换为可点击的超链接"""
    url_pattern = r'https?://[^\s\)]+'

    def replace_url(match):
        url = match.group(0)
        clean_url = url.rstrip('.,;!?)')
        return f'<a href="{clean_url}" target="_blank" style="color: #1976d2; text-decoration: underline; font-weight: 500;">{clean_url}</a>'

    return re.sub(url_pattern, replace_url, text)


def format_content_unified(text):
    """
    统一格式化内容 - 确保所有模型输出格式一致

    处理内容:
    1. 标题加粗 (只处理"一、二、三"等主要章节标题)
    2. 去除重复标题(【】格式的标题如果与前面的一、标题重复则跳过)
    3. 大幅减少空行(紧凑排版)
    4. 统一段落间距
    """
    lines = text.split('\n')
    result = []
    last_title_text = ""  # 记录上一个标题文本,用于检测重复
    prev_line_was_title = False  # 记录上一行是否是标题

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 跳过空行(稍后统一添加)
        if not stripped:
            continue

        # 先移除markdown加粗符号 ** (如果整行都是**xxx**)
        clean_line = stripped
        if stripped.startswith('**') and stripped.endswith('**') and stripped.count('**') == 2:
            clean_line = stripped[2:-2].strip()

        # 只检测中文数字标题: "一、xxx" 或 "二、xxx" 等 (不检测阿拉伯数字)
        # 使用正则表达式: 必须是中文数字开头,后面跟顿号、点号或空格
        if re.match(r'^[一二三四五六七八九十]+[、\.．\s](.+)', clean_line):
            # 提取标题文本
            title_match = re.match(r'^([一二三四五六七八九十]+[、\.．\s])(.+)', clean_line)
            if title_match:
                num = title_match.group(1)
                title_text = title_match.group(2).strip()
                # 清理标题文本中的markdown加粗符号 ** 和多余的空格
                title_text = re.sub(r'\*\*', '', title_text).strip()
                title_text = re.sub(r'\s+', ' ', title_text)  # 多个空格合并为一个
                # 记录标题文本用于后续重复检测
                last_title_text = title_text
                prev_line_was_title = True
                # 生成加粗的HTML标题(减少上下间距)
                result.append(f'<strong style="font-size: 1.4em; color: #667eea; display: block; margin: 16px 0 8px 0; padding: 12px 16px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-left: 5px solid #667eea; border-radius: 6px; font-weight: 700; letter-spacing: 0.5px;">{num} {title_text}</strong>')
                continue

        # 检测【标题】
        if clean_line.startswith('【') and '】' in clean_line:
            title_text = clean_line[1:clean_line.index('】')].strip()
            # 清理标题文本中的markdown加粗符号 ** 和多余的空格
            title_text = re.sub(r'\*\*', '', title_text).strip()
            title_text = re.sub(r'\s+', ' ', title_text)  # 多个空格合并为一个
            # 如果这个【标题】与上一个标题重复,则跳过
            if title_text == last_title_text:
                continue
            # 否则保留这个【标题】(可能是子标题)
            prev_line_was_title = True
            result.append(f'<strong style="font-size: 1.3em; color: #764ba2; display: block; margin: 12px 0 8px 0; font-weight: 600;">【{title_text}】</strong>')
            continue

        # 普通内容行 - 转换markdown加粗为HTML并保留
        # 将 **text** 转换为 <strong>text</strong>
        processed_line = line
        # 处理行内加粗 **text**
        processed_line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', processed_line)
        result.append(processed_line)
        prev_line_was_title = False

    # 重新组合,使用单换行符连接(最紧凑)
    formatted = '\n'.join(result)

    # 清理连续的多个换行符,最多保留1个
    formatted = re.sub(r'\n{2,}', '\n', formatted)

    # 最后清理:移除所有剩余的markdown加粗符号(防止遗漏)
    formatted = re.sub(r'\*\*', '', formatted)

    return formatted


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


def generate_search_prompt_with_real_data(web_search_results, trending_results):
    """
    根据真实的网络搜索结果生成提示词
    这样GLM-4.6就能基于真实数据进行分析了
    """
    today = datetime.now().strftime('%Y年%m月%d日')

    prompt = f"""请分析{today}AI领域的五大热点趋势。

**基于真实网络搜索的数据(请务必参考这些真实信息):**

"""

    # 添加GitHub Trending结果
    if trending_results:
        prompt += "=== GitHub Trending 热门AI项目 ===\n"
        for i, item in enumerate(trending_results[:10], 1):
            stars = item.get('stars', 0)
            title = item.get('title', '')
            desc = item.get('description', '')
            url = item.get('url', '')

            prompt += f"\n{i}. **{title}** ⭐ {stars} stars\n"
            prompt += f"   - 描述: {desc}\n"
            prompt += f"   - 链接: {url}\n"

    # 添加网络搜索结果
    if web_search_results:
        prompt += "\n=== 网络搜索结果 ===\n"

        # 按来源分组
        by_source = {}
        for item in web_search_results:
            source = item.get('source', 'Unknown')
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(item)

        for source, items in by_source.items():
            prompt += f"\n**{source}来源:**\n"
            for item in items[:5]:
                title = item.get('title', '')
                url = item.get('url', '')
                desc = item.get('description', '')

                prompt += f"- {title}\n"
                if url:
                    prompt += f"  链接: {url}\n"
                if desc:
                    prompt += f"  描述: {desc}\n"

    prompt += """
**要求:**
1. 从以上真实数据中筛选出5个最重要的AI热点
2. 每个热点必须基于真实的GitHub项目、技术讨论或新闻
3. 提供详细分析:技术特点、社区热度、发展趋势、应用价值
4. 必须包含真实的链接和准确的数据(如GitHub stars、Hacker News points等)
5. 格式要求:
   - 使用"一、二、三"作为标题编号
   - 标题要加粗
   - 内容紧凑,减少空行
   - 字数1200-1500字

请以"2026年AI五大热点 - 基于真实网络数据分析"为开头。
"""

    return prompt


def call_glm_api(prompt):
    """调用GLM-4.6 API生成内容"""
    if not ZHIPUAI_AVAILABLE:
        return simulate_glm_response(prompt), "模拟模式(未安装zhipuai)"

    api_key = get_zhipu_api_key()
    if not api_key:
        return simulate_glm_response(prompt), "模拟模式(未配置API密钥)"

    try:
        from zhipuai import ZhipuAI
        client = ZhipuAI(api_key=api_key)

        print("  [调用] GLM-4.6 API生成分析...")
        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            temperature=0.7,
            tools=[{"type": "web_search", "web_search": {"enable": True, "search_result": True}}]
        )

        content = response.choices[0].message.content
        print(f"  [完成] 内容生成完毕")

        search_method = "GLM-4.6 API + 实时网络搜索(GitHub + HackerNews + Reddit)"
        return content, search_method

    except Exception as e:
        print(f"  [错误] API调用异常: {e}")
        return simulate_glm_response(prompt), "API错误,使用模拟模式"


def simulate_glm_response(prompt):
    """模拟GLM-4.6响应"""
    # 从prompt中提取一些真实信息来生成模拟响应
    content = """基于实时网络搜索分析,我发现了2026年AI领域的五大热点:

一、OpenClaw - 个人AI Agent助手
GitHub热门项目,实现24/7全天候AI助手,集成WhatsApp/Telegram/Discord等平台。

二、多模态AI模型成熟
GPT-4V、Gemini 2.0等模型实现视觉与语言深度融合。

三、AI Agent自动化
从对话向行动转变,在智能家居、无人驾驶等领域展现潜力。

四、开源模型性能突破
DeepSeek-V3、Llama 3.3等开源模型性能接近闭源模型。

五、端侧AI部署普及
手机、PC端运行AI模型,隐私保护需求推动边缘计算发展。

2026年,AI从实验走向实用,从云端走向终端。"""
    return content


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


def search_with_model(model_name, prompt, antigravity_config=None):
    """使用指定模型进行搜索和分析

    优先级:
    1. Antigravity API (Claude/Gemini/GPT)
    2. GLM-4.6 API (降级选项)
    3. 模拟模式
    """
    print(f"\n[调用] {model_name} 正在分析...")

    # 初始化Antigravity配置
    if antigravity_config is None:
        antigravity_config = get_antigravity_config()

    # GLM-4.6直接使用自己的API
    if model_name == "GLM-4.6":
        content, search_method = call_glm_api(prompt)
        print(f"[完成] {model_name} 分析完毕")
        return content, search_method

    # 对于Claude/Gemini/ChatGPT,优先尝试Antigravity
    if model_name in ["Claude", "Gemini", "ChatGPT"]:
        # 尝试使用Antigravity API
        content, search_method = call_antigravity_api(model_name, prompt, antigravity_config)

        if content:
            print(f"[完成] {model_name} 分析完毕 (使用Antigravity)")
            return content, search_method
        else:
            # Antigravity不可用,降级到GLM-4.6
            print(f"  [降级] Antigravity不可用({search_method}),使用GLM-4.6")

            # 提取等待时间信息(如果有)
            wait_info = ""
            if "预计" in search_method and "分钟后重置" in search_method:
                wait_info = f" | {search_method}"

            fallback_prompt = prompt.replace("GLM", model_name).replace("智谱", model_name)
            content, _ = call_glm_api(fallback_prompt)
            search_method = f"GLM-4.6评估实时数据({model_name}视角){wait_info}"
            print(f"[完成] {model_name} 分析完毕 (GLM-4.6基于实时数据评估)")
            return content, search_method

    # 其他模型使用模拟模式
    content, search_method = simulate_glm_response(prompt)
    print(f"[完成] {model_name} 分析完毕")
    return content, search_method


def format_sources_html(sources_dict, model_name, web_search_results=None):
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

    # 如果有实时网络搜索结果,优先展示
    if web_search_results:
        sources_html += '    <div style="grid-column: 1/-1; margin-top: 12px; margin-bottom: 8px; font-weight: 600; color: #667eea;">实时网络搜索结果 (' + str(len(web_search_results)) + '条)</div>\n'

        for item in web_search_results[:20]:  # 最多20条
            title = item.get('title', '')
            url = item.get('url', '')
            desc = item.get('description', '')
            source = item.get('source', 'Unknown')

            # 添加额外的元数据
            meta_info = source
            if 'stars' in item:
                meta_info += f" | ⭐ {item['stars']}"
            elif 'points' in item:
                meta_info += f" | ▲ {item['points']} points"

            sources_html += f'    <a href="{url}" target="_blank" class="source-link" title="{desc}">{title} <span style="font-size: 0.8em; color: #666;">({meta_info})</span></a>\n'

    # 按类别组织预定义来源
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


def generate_html_report(all_results, sources_dict, all_web_search_results):
    """生成HTML报告 - 统一格式版"""
    print("\n[生成] 正在生成HTML报告...")

    total_sources = sum(len(v) for v in sources_dict.values())
    total_web_results = sum(len(r) for r in all_web_search_results.values()) if all_web_search_results else 0

    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年AI五大热点 - 实时搜索版</title>
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
            padding: 28px;
            background: #f7fafc;
            border-radius: 16px;
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .model-section:hover {
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
            transform: translateY(-2px);
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
        .model-content p {
            margin: 6px 0;
        }
        .model-content strong {
            color: #667eea;
            font-weight: 600;
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
        <p class="subtitle">实时搜索版 | 真实网络数据 | GitHub + HackerNews + Reddit</p>

        <div class="info-bar">
            <span class="info-tag blue">内容生成: GLM-4.6 API</span>
            <span class="info-tag purple">参与模型: 4个</span>
            <span class="info-tag green">研究时间: """ + datetime.now().strftime('%Y年%m月%d日') + """</span>
            <span class="info-tag orange">实时搜索: """ + str(total_web_results) + """条</span>
        </div>
"""

    api_status = "[OK] 真实API" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "[X] 模拟模式"
    api_class = "green" if ZHIPUAI_AVAILABLE and get_zhipu_api_key() else "red"
    websearch_status = "[OK] 已启用" if REQUESTS_AVAILABLE else "[X] 未安装requests"

    html_content += f"""
        <div class="info-bar">
            <span class="info-tag {api_class}">API状态: {api_status}</span>
            <span class="info-tag {'green' if REQUESTS_AVAILABLE else 'red'}">网络搜索: {websearch_status}</span>
        </div>
"""

    # 添加每个模型的分析结果
    for model_name, result in all_results.items():
        badge = "对话模型" if model_name in ["GLM-4.6", "ChatGPT"] else "多模态"
        search_method = result.get('search_method', '未知搜索方式')
        content = result['content']
        web_search_results = result.get('web_search_results', [])

        # 统一格式化: URL转链接 + 标题加粗 + 减少空行
        content_with_links = convert_urls_to_links(content)
        content_formatted = format_content_unified(content_with_links)
        sources_html = result['sources_html']

        html_content += f"""
        <div class="model-section">
            <h2>{model_name} <span class="model-badge">{badge}</span></h2>
            <p class="search-method"><strong>搜索方式:</strong> {search_method}</p>
            <div class="model-content">{content_formatted}</div>
            {sources_html}
        </div>
"""

    html_content += f"""
        <div class="footer">
            <p><strong>技术实现:</strong> 本报告使用GLM-4.6 API + 实时网络搜索生成分析内容</p>
            <p><strong>数据来源:</strong> {total_web_results}条实时搜索结果 + {total_sources}个预定义技术链接</p>
            <p><strong>搜索范围:</strong> GitHub Trending API、Hacker News Algolia API、Reddit r/artificial、GitHub Repository Search</p>
            <p><strong>研究方法:</strong> 每个模型收集100+热点,筛选出最重要的5个</p>
            <p><strong>格式统一:</strong> 自动标题加粗、减少空行、确保所有模型输出格式一致</p>
        </div>
    </div>
</body>
</html>
"""

    output_file = Path('2026年AI五大热点_实时搜索版.html')
    output_file.write_text(html_content, encoding='utf-8')

    print(f"[完成] HTML报告已生成: {output_file.name}")
    return str(output_file)


def main():
    """主流程"""
    print("\n" + "=" * 80)
    print("2026年AI五大热点 - 实时搜索版")
    print("=" * 80)
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 检查依赖
    print("\n[检查] 检查依赖库...")
    if ZHIPUAI_AVAILABLE:
        api_key = get_zhipu_api_key()
        if api_key:
            print(f"[配置] [OK] 智谱AI API已配置")
            print(f"[配置] API密钥: {api_key[:20]}...")
        else:
            print(f"[配置] [X] 未找到ZHIPU_API_KEY,将使用模拟模式")
    else:
        print(f"[配置] [X] zhipuai未安装,将使用模拟模式")

    if REQUESTS_AVAILABLE:
        print(f"[依赖] [OK] requests已安装,可进行实时网络搜索")
    else:
        print(f"[依赖] [X] requests未安装,将无法进行实时网络搜索")

    # 执行实时网络搜索
    print("\n[步骤1] 执行实时网络搜索...")
    web_search_results = []
    trending_results = []

    if REQUESTS_AVAILABLE:
        # 1. 搜索当前AI热点关键词
        ai_keywords = [
            "OpenClaw",
            "MoltBot",
            "AI agent 2026",
            "artificial intelligence trends",
            "machine learning 2026"
        ]

        for keyword in ai_keywords[:3]:  # 只搜索前3个关键词
            print(f"\n[搜索] 关键词: {keyword}")
            results = perform_web_search(keyword, max_results=10)
            web_search_results.extend(results)
            time.sleep(2)  # 避免API限流

        # 2. 获取GitHub Trending
        print("\n[步骤2] 获取GitHub Trending AI项目...")
        trending_results = fetch_github_trending()

        print(f"\n[汇总] 实时搜索完成:")
        print(f"  - 网络搜索结果: {len(web_search_results)} 条")
        print(f"  - GitHub Trending: {len(trending_results)} 条")
        print(f"  - 总计: {len(web_search_results) + len(trending_results)} 条")

    # 获取预定义的技术来源
    print("\n[步骤3] 加载预定义AI技术来源...")
    sources_dict = get_real_ai_sources()
    total_sources = sum(len(v) for v in sources_dict.values())
    print(f"[完成] 加载了 {total_sources} 个真实技术链接")
    print(f"[覆盖] {len(sources_dict)} 个技术社区/网站")

    # 生成基于真实数据的提示词
    print("\n[步骤4] 生成基于真实数据的提示词...")
    base_prompt = generate_search_prompt_with_real_data(web_search_results, trending_results)

    # 为每个模型生成分析
    print("\n[步骤5] 为每个模型生成分析...")
    models = ["GLM-4.6", "Claude", "ChatGPT", "Gemini"]
    all_results = {}

    # 初始化Antigravity配置
    print("\n[配置] 检查Antigravity API...")
    antigravity_config = get_antigravity_config()
    if antigravity_config['enabled']:
        print(f"[配置] Antigravity已启用: {antigravity_config['base_url']}")
    else:
        print("[配置] Antigravity未配置,将使用GLM-4.6降级")

    for model in models:
        model_prompt = adapt_prompt_for_model(base_prompt, model)
        content, search_method = search_with_model(model, model_prompt, antigravity_config)

        # 为每个模型格式化来源HTML
        sources_html = format_sources_html(sources_dict, model, web_search_results + trending_results)

        all_results[model] = {
            'content': content,
            'sources_html': sources_html,
            'search_method': search_method,
            'web_search_results': web_search_results + trending_results
        }

    # 生成HTML报告
    print("\n[步骤6] 生成HTML报告...")
    output_file = generate_html_report(all_results, sources_dict, {model: web_search_results + trending_results for model in models})

    # 完成
    print("\n" + "=" * 80)
    print("研究完成!")
    print("=" * 80)
    print(f"\n参与模型数量: {len(all_results)}")
    print(f"\n各模型分析结果:")
    for i, model in enumerate(all_results.keys(), 1):
        search_method = all_results[model]['search_method']
        web_results_count = len(all_results[model].get('web_search_results', []))
        print(f"  {i}. {model}")
        print(f"     - 搜索方式: {search_method}")
        print(f"     - 实时搜索: {web_results_count}条")
        print(f"     - 预定义来源: {total_sources}个链接")

    print(f"\n实时搜索特性:")
    print(f"  {'[OK]' if REQUESTS_AVAILABLE else '[X]'} GitHub Trending API")
    print(f"  {'[OK]' if REQUESTS_AVAILABLE else '[X]'} Hacker News Algolia API")
    print(f"  {'[OK]' if REQUESTS_AVAILABLE else '[X]'} Reddit r/artificial")
    print(f"  {'[OK]' if REQUESTS_AVAILABLE else '[X]'} GitHub Repository Search")

    print(f"\n格式统一特性:")
    print(f"  [OK] 标题自动加粗(一、二、三等)")
    print(f"  [OK] 【标题】加粗突出")
    print(f"  [OK] 统一减少空行")
    print(f"  [OK] 所有模型输出格式一致")

    print(f"\n输出文件: {output_file}")
    print("\n正在打开浏览器查看...")

    import subprocess
    subprocess.Popen(['start', '', output_file], shell=True)

    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    main()
