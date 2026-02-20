# -*- coding: utf-8 -*-
"""
今日头条高赞文章生成器 v3.3 - 增强版
支持用户输入自定义主题,使用AI生成高质量文章
新增: 自动生成配图功能

v3.3更新(2026-02-20):
  ✅ 素材预搜索: 使用DuckDuckGo搜索名人美食故事/作品，确保素材真实
  ✅ 废话检测: 作者2审校时识别并删除与主题无关的冗余内容

v3.2更新(2026-02-15):
  ✅ 草稿完善模式: 强调最大程度保留原草稿内容，不大幅缩减
  ✅ 图像生成: 优先使用Seedream 4.5/4.0 (正方形1:1)，然后降级到Antigravity
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import base64
import re
from PIL import Image
import io
import time

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_zhipu_anthropic_client, get_antigravity_client, get_volcano_client


def ddg_search(query, max_results=5):
    """
    使用DuckDuckGo进行免费搜索（无需API Key）
    用于在写作前搜集名人美食故事/作品的素材

    Args:
        query: 搜索查询
        max_results: 最大结果数

    Returns:
        str: 格式化的搜索结果文本，用于注入到AI提示词中
    """
    print(f"[素材搜索] 查询: {query}")

    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))

            for r in search_results:
                results.append({
                    'title': r.get('title', ''),
                    'snippet': r.get('body', ''),
                    'url': r.get('href', '')
                })

        if results:
            content = '\n\n'.join([
                f"【{r['title']}】\n{r['snippet']}\n来源: {r['url']}"
                for r in results
            ])
            print(f"[素材搜索] 找到 {len(results)} 条相关素材")
            return content
        else:
            print(f"[素材搜索] 未找到相关素材")
            return ""

    except ImportError:
        print("[素材搜索] 未安装duckduckgo-search库，跳过预搜索")
        return ""
    except Exception as e:
        print(f"[素材搜索] 搜索异常: {e}")
        return ""


class ToutiaoArticleGenerator:
    """今日头条文章生成器 - AI增强版 v3.3"""

    def __init__(self):
        self.text_client = get_zhipu_anthropic_client()  # 使用Anthropic兼容接口
        self.image_client = get_antigravity_client()  # 使用anti-gravity代理生成配图
        self.volcano_client = get_volcano_client()  # 火山引擎Seedream客户端

    def improve_article_draft(self, draft_content, target_length=2000, style='standard'):
        """根据用户草稿完善文章

        Args:
            draft_content: 用户草稿内容
            target_length: 目标字数
            style: 写作风格 ('standard' 标准风格, 'professional' 资深写手风格)
        """

        print(f"\n[AI] Improving your draft...")
        print(f"[AI] Target length: {target_length} chars")
        print(f"[AI] Style: {'Professional' if style == 'professional' else 'Standard'}\n")

        # 清理草稿内容中的代理字符(surrogate characters)
        # 这些字符可能导致UTF-8编码错误
        try:
            # 尝试编码为UTF-8，如果失败则清理
            draft_content.encode('utf-8')
        except UnicodeEncodeError:
            # 移除代理字符
            draft_content = draft_content.encode('utf-8', errors='ignore').decode('utf-8')
            print("[INFO] Special characters cleaned from draft")

        # 根据风格选择不同的prompt
        if style == 'professional':
            prompt = f"""你是一位资深编辑，请对以下用户草稿进行**润色完善**。

## 用户草稿:

{draft_content}

## 核心原则（最重要！）:
**最大限度保留原文内容**。你的工作不是重写，而是润色和完善。

## 具体修改范围:
1. **语法修正**: 修正错别字、病句、标点错误
2. **用词优化**: 将口语化表达改为更书面化，但保留原意
3. **逻辑梳理**: 调整段落顺序，使行文逻辑更清晰
4. **句子润色**: 对表达不清的句子进行改写，但保留原意

## 禁止做的事:
- ❌ 不要删除或大幅缩减原文内容
- ❌ 不要改变原文的核心观点和思想
- ❌ 不要添加原文没有的新观点（除非原文逻辑明显缺失）
- ❌ 不要改变原文的情感基调和写作风格
- ❌ 不要使用"首先、其次、最后"等公文式表达
- ❌ 不要过度使用emoji（最多2-3处）

## 可以做的事:
- ✅ 调整段落顺序，使逻辑更清晰
- ✅ 修正明显的语法错误和错别字
- ✅ 将重复啰嗦的句子精简（但不删减意思）
- ✅ 为句子添加适当的过渡词，使行文流畅
- ✅ 生成一个合适的标题（15-25字）

## 字数要求:
- 原文多少字，完善后也应该差不多多少字
- 如果原文内容丰富，可以保持或略有增加
- 绝对不能大幅缩减原文篇幅

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

(这里输出润色后的正文内容，必须保留原文绝大部分内容)
---

记住:你的任务是**润色**，不是**重写**。原文的每一句话、每一个观点都要尽量保留。
"""
        else:
            prompt = f"""你是一位资深编辑，请对以下用户草稿进行**润色完善**。

## 用户草稿:

{draft_content}

## 核心原则（最重要！）:
**最大限度保留原文内容**。你的工作不是重写，而是润色和完善。

## 具体修改范围:
1. **语法修正**: 修正错别字、病句、标点错误
2. **用词优化**: 将过于口语化的表达稍作规范，但保留原汁原味
3. **逻辑梳理**: 调整段落顺序，使行文逻辑更清晰
4. **句子润色**: 对表达不清的句子进行改写，但保留原意

## 禁止做的事:
- ❌ 不要删除或大幅缩减原文内容
- ❌ 不要改变原文的核心观点和思想
- ❌ 不要添加原文没有的新观点（除非原文逻辑明显缺失）
- ❌ 不要改变原文的情感基调和写作风格
- ❌ 不要将原文改得面目全非

## 可以做的事:
- ✅ 调整段落顺序，使逻辑更清晰
- ✅ 修正明显的语法错误和错别字
- ✅ 将重复啰嗦的句子精简（但不删减意思）
- ✅ 为句子添加适当的过渡词，使行文流畅
- ✅ 适当添加emoji增强可读性（不要过多）
- ✅ 生成一个吸引人的标题（15-25字）

## 字数要求:
- 原文多少字，完善后也应该差不多多少字
- 如果原文内容丰富，可以保持或略有增加
- 绝对不能大幅缩减原文篇幅

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

(这里输出润色后的正文内容，必须保留原文绝大部分内容)
---

记住:你的任务是**润色**，不是**重写**。原文的每一句话、每一个观点都要尽量保留。
"""

        try:
            # 使用Anthropic兼容接口
            # 对于草稿模式，需要更大的 max_tokens 来保留原文内容
            # 根据草稿长度动态计算 max_tokens
            estimated_tokens = max(8000, len(draft_content) * 2)  # 至少8000，或草稿长度的2倍
            print(f"[DEBUG] Calling AI API with model=glm-4-flash, max_tokens={estimated_tokens}")
            print(f"[DEBUG] Draft content length: {len(draft_content)} chars")

            response = self.text_client.messages.create(
                model="glm-4-flash",  # 使用快速模型
                max_tokens=estimated_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # 提取生成的内容 (Anthropic格式)
            print(f"[DEBUG] API response received, type: {type(response)}")
            print(f"[DEBUG] response.content type: {type(response.content)}, len: {len(response.content) if response.content else 'None'}")

            if not response.content or len(response.content) == 0:
                print(f"[ERROR] API returned empty content!")
                return None

            content = response.content[0].text
            print(f"[DEBUG] Extracted text length: {len(content) if content else 0} chars")
            # 安全打印，避免GBK编码错误
            try:
                safe_content = content[:200].encode('gbk', errors='replace').decode('gbk') if content else 'EMPTY'
                print(f"[DEBUG] First 200 chars of response: {safe_content}")
            except:
                print(f"[DEBUG] Response preview: [contains special characters]")

            if not content or content.strip() == "":
                print(f"[ERROR] Extracted text is empty!")
                return None

            # 解析标题和正文
            lines = content.split('\n')
            print(f"[DEBUG] Split into {len(lines)} lines")
            title = ""
            body_lines = []

            for i, line in enumerate(lines):
                # 支持中英文冒号
                if line.startswith("标题:") or line.startswith("标题："):
                    # 同时支持中英文冒号
                    title = line.replace("标题:", "").replace("标题：", "").strip()
                    # 安全打印标题
                    try:
                        safe_title = title.encode('gbk', errors='replace').decode('gbk')
                        print(f"[DEBUG] Found title at line {i}: {safe_title}")
                    except:
                        print(f"[DEBUG] Found title at line {i}")
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()
            print(f"[DEBUG] Parsed body length: {len(body)} chars")
            # 安全打印标题
            try:
                safe_title = title.encode('gbk', errors='replace').decode('gbk') if title else 'NOT FOUND'
                print(f"[DEBUG] Parsed title: {safe_title}")
            except:
                print(f"[DEBUG] Parsed title: [title contains special chars]")

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else "基于草稿完善的文章"
                try:
                    safe_fallback = title.encode('gbk', errors='replace').decode('gbk')
                    print(f"[DEBUG] Using fallback title: {safe_fallback}")
                except:
                    print(f"[DEBUG] Using fallback title")

            # 验证最终结果
            if not body or len(body) < 50:
                print(f"[WARN] Body content too short: {len(body) if body else 0} chars")
                try:
                    safe_content = content[:500].encode('gbk', errors='replace').decode('gbk')
                    print(f"[WARN] Full response content: {safe_content}")
                except:
                    print(f"[WARN] Full response content: [contains special chars]")

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length,
                'source': 'draft_improvement'
            }

        except Exception as e:
            print(f"[ERROR] 草稿完善失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_article_with_ai(self, theme, target_length=2000, style='standard'):
        """使用AI生成文章

        Args:
            theme: 文章主题
            target_length: 目标字数
            style: 写作风格 ('standard' 标准风格, 'wangzengqi' 汪曾祺风格, 或自定义文风描述)
        """

        print(f"\n[AI] Generating article for theme: {theme}")
        print(f"[AI] Target length: {target_length} chars")
        print(f"[AI] Style: {style}\n")

        # 根据风格选择不同的prompt
        if style == 'wangzengqi':
            prompt = f"""你是汪曾祺先生，中国当代著名作家。请用你的散文风格写一篇关于"{theme}"的文章。

## 汪曾祺散文风格特点：
1. **语言特点**：
   - 简洁平淡，朴实有趣
   - 平易自然，富有节奏感
   - 不用华丽辞藻，但意味深长
   - 口语化，有生活气息

2. **结构特点**：
   - 形散神聚，看似随意实则精心
   - 从小事写起，以小见大
   - 漫不经心中见真意

3. **情感特点**：
   - 淡雅怀旧，有温度
   - 乐观平和的人生态度
   - 关注日常人事，体察细微

4. **禁忌**：
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji
   - 不得使用营销话术（"让我们一起"、"不容错过"等）
   - 不得生硬列举"5个XX"、"3大XX"

## 写作要求：
1. 字数: {target_length}字左右
2. 主题: {theme}
3. 开头: 从个人经历或感受写起
4. 内容: 用平淡朴实的语言写深刻的思想
5. 结尾: 留有余韵，引人思考
6. 标题: 简洁有意境，15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

记住:你要写的是一篇有温度、有情怀的散文，而不是营销文案。语言要平淡但有力，朴实但深刻。
"""
        elif style and style not in ['standard', 'professional']:
            # 自定义文风描述
            prompt = f"""请为一篇今日头条文章撰写高质量内容。

主题: {theme}

## 文风要求:
{style}

## 内容要求:
1. 字数: {target_length}字左右
2. 结构: 吸引人的标题 + 引人入胜的开头 + 有逻辑的正文 + 感人或启发的结尾

3. 典籍深度挖掘（重要！）:
   - 当文风描述中提及某部经典著作（如《黄帝内经》《千金方》《本草纲目》等），必须深入挖掘该典籍中与主题相关的经典论述
   - 准确引用典籍原文或核心观点，并加以阐释
   - 例如：提及春季养生，应引用《千金方》"春七十二日，省酸增甘，以养脾气"等经典论述
   - 例如：提及《黄帝内经》春季养生，应引用"春三月，此谓发陈，天地俱生，万物以荣"等原文
   - 典籍引用要精准，标明出处，不要凭空捏造

4. 内容准确性:
   - 对于涉及专业知识的内容（如中医养生、历史典故、科学知识等），必须确保准确无误
   - 如果不确定某些知识，宁可不写也不要编造
   - 引用经典著作时要准确，不要曲解原意

5. 写作禁忌:
   - 不要编造虚假信息或错误知识
   - 不要使用未经证实的"据说"、"研究表明"等表述
   - 不要生硬列举"5个XX"、"3大XX"
   - 不要使用"首先、其次、最后"等公文式表达

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

注意:
- 严格按照文风要求来组织内容
- 必须体现对典籍的深度挖掘和准确引用
- 确保内容准确、真实、有价值
- 结尾要有情感共鸣或启发
"""
        else:
            prompt = f"""请为一篇今日头条文章撰写高质量内容。

主题: {theme}

要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
3. 结构: 吸引人的标题 + 引人入胜的开头 + 3-5个要点 + 感人或启发的结尾 + 互动号召
4. 内容准确性:
   - 对于涉及专业知识的内容（如中医养生、历史典故、科学知识等），必须确保准确无误
   - 如果不确定某些知识，宁可不写也不要编造
   - 引用经典著作时要准确，不要曲解原意
5. 写作禁忌:
   - 不要编造虚假信息或错误知识
   - 不要使用未经证实的"据说"、"研究表明"等表述
5. 情感: 能引起共鸣,激发情绪(感动/激励/共鸣)
6. 标题要求: 使用数字+疑问/对比/利益点,字数15-25字

请直接输出文章内容,格式如下:

---
标题: [文章标题]

[正文内容]

---

注意:
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 确保内容准确、真实、有价值
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
"""

        try:
            # 使用Anthropic兼容接口
            print(f"[DEBUG] Calling AI API with model=glm-4-flash, max_tokens=4000")
            print(f"[DEBUG] Theme: {theme}")

            response = self.text_client.messages.create(
                model="glm-4-flash",  # 使用快速模型
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # 提取生成的内容 (Anthropic格式)
            print(f"[DEBUG] API response received, type: {type(response)}")
            print(f"[DEBUG] response.content type: {type(response.content)}, len: {len(response.content) if response.content else 'None'}")

            if not response.content or len(response.content) == 0:
                print(f"[ERROR] API returned empty content!")
                return None

            content = response.content[0].text
            print(f"[DEBUG] Extracted text length: {len(content) if content else 0} chars")
            # 安全打印，避免GBK编码错误
            try:
                safe_content = content[:200].encode('gbk', errors='replace').decode('gbk') if content else 'EMPTY'
                print(f"[DEBUG] First 200 chars of response: {safe_content}")
            except:
                print(f"[DEBUG] Response preview: [contains special characters]")

            if not content or content.strip() == "":
                print(f"[ERROR] Extracted text is empty!")
                return None

            # 解析标题和正文
            lines = content.split('\n')
            print(f"[DEBUG] Split into {len(lines)} lines")
            title = ""
            body_lines = []

            for i, line in enumerate(lines):
                # 支持中英文冒号
                if line.startswith("标题:") or line.startswith("标题："):
                    # 同时支持中英文冒号
                    title = line.replace("标题:", "").replace("标题：", "").strip()
                    # 安全打印标题
                    try:
                        safe_title = title.encode('gbk', errors='replace').decode('gbk')
                        print(f"[DEBUG] Found title at line {i}: {safe_title}")
                    except:
                        print(f"[DEBUG] Found title at line {i}")
                elif line.strip() == "---":
                    continue
                elif title:  # 已找到标题后,其余内容为正文
                    body_lines.append(line)

            body = '\n'.join(body_lines).strip()
            print(f"[DEBUG] Parsed body length: {len(body)} chars")
            print(f"[DEBUG] Parsed title: {title if title else 'NOT FOUND'}")

            # 如果没有找到标题格式,从第一行提取
            if not title:
                title = lines[0].strip() if lines else f"关于{theme}的思考"
                print(f"[DEBUG] Using fallback title: {title}")

            # 验证最终结果
            if not body or len(body) < 50:
                print(f"[WARN] Body content too short: {len(body) if body else 0} chars")
                try:
                    safe_content = content[:500].encode('gbk', errors='replace').decode('gbk')
                    print(f"[WARN] Full response content: {safe_content}")
                except:
                    print(f"[WARN] Full response content: [contains special chars]")

            return {
                'title': title,
                'content': body,
                'word_count': len(body),
                'target_length': target_length
            }

        except Exception as e:
            print(f"[ERROR] AI生成失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_article_collaborative(self, theme, target_length=2000, style='standard', max_rounds=3):
        """双作者协作生成高质量文章

        作者1负责原创写作，作者2负责审校和提出修改意见。
        两位作者反复协作，直到达成一致或达到最大轮数。

        Args:
            theme: 文章主题
            target_length: 目标字数
            style: 写作风格
            max_rounds: 最大协作轮数（默认3轮）

        Returns:
            dict: 包含标题、正文、协作历史等信息
        """
        print(f"\n{'='*60}")
        print(f"[协作模式] 双顶级文学大家协作生成文章")
        print(f"主题: {theme}")
        print(f"目标字数: {target_length}")
        print(f"文风: {style}")
        print(f"最大协作轮数: {max_rounds}")
        print(f"{'='*60}\n")

        collaboration_history = []

        # ========== 第零步：素材预搜索 ==========
        print(f"\n[素材搜集] 正在搜索相关素材...")
        search_materials = self._search_reference_materials(theme)
        if search_materials:
            print(f"[素材搜集] 成功获取素材，将用于指导创作")
            collaboration_history.append({
                'round': 0,
                'author': '系统',
                'action': '素材搜集',
                'materials': search_materials[:500] + '...' if len(search_materials) > 500 else search_materials
            })
        else:
            print(f"[素材搜集] 未获取到外部素材，将基于AI知识创作")

        # ========== 第一步：作者1原创初稿 ==========
        print(f"\n[作者1 - 原创] 正在创作初稿...")
        draft_result = self._author1_create_draft(theme, target_length, style, search_materials)

        if not draft_result:
            print("[ERROR] 作者1创作初稿失败")
            return None

        current_title = draft_result['title']
        current_content = draft_result['content']
        collaboration_history.append({
            'round': 0,
            'author': '作者1',
            'action': '创作初稿',
            'content_preview': current_content[:200] + '...'
        })
        print(f"[作者1] 初稿完成: {current_title}")
        print(f"[作者1] 字数: {len(current_content)}")

        # ========== 开始多轮协作 ==========
        for round_num in range(1, max_rounds + 1):
            print(f"\n{'─'*40}")
            print(f"[协作轮次 {round_num}]")
            print(f"{'─'*40}")

            # ========== 作者2审校 ==========
            print(f"\n[作者2 - 审校] 正在审阅文章...")
            review_result = self._author2_review(
                theme=theme,
                title=current_title,
                content=current_content,
                style=style
            )

            if not review_result:
                print("[ERROR] 作者2审校失败")
                break

            collaboration_history.append({
                'round': round_num,
                'author': '作者2',
                'action': '审校意见',
                'opinion': review_result['opinion'],
                'needs_revision': review_result['needs_revision'],
                'issues': review_result.get('issues', [])
            })

            print(f"[作者2] 审校意见: {review_result['opinion'][:100]}...")

            # 检查是否需要修改
            if not review_result['needs_revision']:
                print(f"\n[协作完成] 作者2认为文章质量达标，无需修改！")
                collaboration_history.append({
                    'round': round_num,
                    'author': '系统',
                    'action': '协作完成',
                    'message': '两位作者达成一致，文章质量达标'
                })
                break

            # 输出具体问题
            if review_result.get('fact_errors'):
                print(f"[作者2] 发现事实错误:")
                for i, err in enumerate(review_result['fact_errors'][:5], 1):
                    print(f"  {i}. {err}")
            if review_result.get('redundant_content'):
                print(f"[作者2] 发现冗余内容（需要删除的废话）:")
                for i, rc in enumerate(review_result['redundant_content'][:5], 1):
                    print(f"  {i}. {rc}")
            if review_result.get('issues'):
                print(f"[作者2] 发现其他问题:")
                for i, issue in enumerate(review_result['issues'][:5], 1):
                    print(f"  {i}. {issue}")

            # ========== 作者1根据意见修改 ==========
            print(f"\n[作者1 - 修改] 正在根据审校意见修改文章...")
            revision_result = self._author1_revise(
                theme=theme,
                title=current_title,
                content=current_content,
                review_opinion=review_result['opinion'],
                issues=review_result.get('issues', []),
                fact_errors=review_result.get('fact_errors', []),
                redundant_content=review_result.get('redundant_content', []),
                target_length=target_length,
                style=style
            )

            if not revision_result:
                print("[WARN] 作者1修改失败，保持原内容")
                break

            current_title = revision_result['title']
            current_content = revision_result['content']

            collaboration_history.append({
                'round': round_num,
                'author': '作者1',
                'action': '修改文章',
                'content_preview': current_content[:200] + '...'
            })

            print(f"[作者1] 修改完成")
            print(f"[作者1] 新字数: {len(current_content)}")

            # 如果是最后一轮，强制完成
            if round_num == max_rounds:
                print(f"\n[协作完成] 达到最大轮数({max_rounds}轮)，协作结束")
                collaboration_history.append({
                    'round': round_num,
                    'author': '系统',
                    'action': '协作完成',
                    'message': f'达到最大协作轮数({max_rounds}轮)'
                })

        # ========== 返回最终结果 ==========
        print(f"\n{'='*60}")
        print(f"[协作结束] 最终文章生成完成")
        print(f"标题: {current_title}")
        print(f"字数: {len(current_content)}")
        print(f"协作轮数: {len([h for h in collaboration_history if h['author'] == '作者2'])}")
        print(f"{'='*60}\n")

        return {
            'title': current_title,
            'content': current_content,
            'word_count': len(current_content),
            'target_length': target_length,
            'source': 'collaborative',
            'collaboration_history': collaboration_history,
            'rounds': len([h for h in collaboration_history if h['author'] == '作者2'])
        }

    def _author1_create_draft(self, theme, target_length, style, reference_materials=""):
        """作者1: 创作初稿"""

        # 构建素材部分
        materials_section = ""
        if reference_materials:
            materials_section = f"""
## 参考素材（来自网络搜索，请确保准确使用）
以下是与主题相关的真实素材，请在创作时参考，确保引用准确：

{reference_materials}

**使用素材时请注意**:
- 只使用您能确认准确性的内容
- 如果素材与您了解的不符，以您的判断为准
- 引用作品时要确认作者与作品的对应关系
"""

        prompt = f"""你是【作者1】，一位当代顶级文学大师，文坛泰斗级人物。

你的文学成就斐然：
- 深厚的古典文学功底，精通诗词歌赋
- 对现代文学有独到见解，文风自成一派
- 善于用平实的语言表达深刻的思想
- 你的文字既有文化底蕴，又平易近人，深受读者喜爱

## 核心目标
**创作一篇高质量的极具欣赏性的美文**——让读者读后回味无穷，愿意收藏、转发。

## 任务
请根据以下主题创作一篇原创文章初稿。
{materials_section}
## 主题
{theme}

## 写作要求

### 1. 整体风格
- 字数: {target_length}字左右
- 风格: {style if style and style != 'standard' else '优美雅致，有感染力，有文化底蕴'}

### 2. 结构要求
   - 标题：简洁有力，引人入胜（15-25字）
   - 开头：要有"钩子"，一句话抓住读者
   - 正文：层层递进，有起伏有节奏
   - 结尾：余韵悠长，让读者回味

### 3. 文笔美感（核心！）
   - 语言要优美、有韵味
   - 要有令人印象深刻的金句
   - 句子长短搭配，节奏舒张有度
   - 用词精准、生动，避免陈词滥调

### 4. 内容准确性
   - 涉及专业知识（如中医、历史、科学）必须准确
   - 引用典籍要精确，不可曲解原意
   - 引用名人作品时，务必确认作品与作者对应正确
   - 不确定的内容宁可不写也不要编造

### 5. 写作禁忌
   - 不使用"首先、其次、最后"等公文式表达
   - 不生硬列举"5个XX"、"3大XX"
   - 不过度使用emoji（最多2-3处）
   - 不写与主题无关的"废话"
   - 每句话都要有存在的价值

请直接输出文章，格式如下：
---
标题: [文章标题]

[正文内容]
---
"""

        try:
            response = self.text_client.messages.create(
                model="glm-4-flash",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            return self._parse_article_response(content, theme)
        except Exception as e:
            print(f"[ERROR] 作者1创作失败: {e}")
            return None

    def _search_reference_materials(self, theme):
        """搜索与主题相关的参考素材（名人故事、作品等）"""
        # 从主题中提取可能的名人名字
        import re
        # 常见文学/美食名人列表
        famous_people = [
            '汪曾祺', '梁实秋', '周作人', '林语堂', '老舍', '鲁迅',
            '蔡澜', '沈宏非', '陈晓卿', '王世襄', '唐鲁孙',
            '苏轼', '袁枚', '李渔', '张岱'
        ]

        found_names = []
        for name in famous_people:
            if name in theme:
                found_names.append(name)

        # 搜索素材
        all_materials = []

        # 如果主题中有名人名字，搜索他们的美食故事/作品
        for name in found_names[:2]:  # 最多搜索2个人物
            query = f"{name} 美食 散文 作品 故事"
            materials = ddg_search(query, max_results=3)
            if materials:
                all_materials.append(f"【{name}相关素材】\n{materials}")

        # 搜索主题相关的素材
        theme_query = f"{theme} 故事 典故 来源"
        theme_materials = ddg_search(theme_query, max_results=3)
        if theme_materials:
            all_materials.append(f"【主题相关素材】\n{theme_materials}")

        if all_materials:
            return "\n\n".join(all_materials)
        return ""

    def _author2_review(self, theme, title, content, style):
        """作者2: 审校文章，从顶级文学评论家角度提出意见"""
        prompt = f"""你是【作者2】，一位当代顶级文学评论家、资深主编，文坛泰斗级人物。

你的资历：
- 担任多家顶级文学刊物主编数十年
- 精通古今文学，对美食文学、文化散文有深入研究
- 审稿以"火眼金睛"著称，任何瑕疵都逃不过你的眼睛
- 你的标准极高，但评语中肯、建议务实

## 原文信息
- 主题: {theme}
- 标题: {title}
- 文风要求: {style if style and style != 'standard' else '通俗易懂，有感染力'}

## 原文内容
{content}

## 你的审校职责

### 🔴 第一优先级 - 内容精炼度检查（新增！）:
**核心原则：文章中的每一句话都应该有其存在的价值。**

1. **废话检测**（重点！）:
   - 是否有与主题无关的段落或句子？
   - 是否为了凑字数而添加的"填充内容"？
   - 引用的典故、名人、作品是否与主题紧密相关？
   - 例如："在《蔡澜食旅》中，虽然蔡澜并未详细描述品尝奶酪的过程"——这种内容对主题有任何助益吗？

2. **冗余内容识别**:
   - 是否有重复表达同一意思的句子？
   - 是否有"正确的废话"（虽然没错但对读者无价值）？
   - 引用某人物的作品时，该作品是否真的与主题相关？（如：主题是汪曾祺，却提《舌尖上的中国》）

3. **精炼度评分标准**:
   - 每个段落都必须推进主题
   - 每个引用都必须紧密关联主题
   - 不相关的名人/作品提及必须删除

### 🔴 第二优先级 - 事实准确性（零容忍！）:

1. **人物身份描述准确性（极易出错！）**:
   - 不能把所有人都称为"文学大家"或"文学家"
   - 汪曾祺：是文学家、作家
   - 蔡澜：是美食家、作家、主持人，不是"文学大家"
   - 于谦：是相声演员，不是"文学大家"
   - 梁实秋、周作人：是文学家
   - 称呼人物时必须使用准确的职业/身份描述
   - 如果提到多个人，不能用一个不准确的统称

2. **作品与作者对应**:
   - 《舌尖上的中国》是央视纪录片，不是汪曾祺的作品
   - 《人间有味是清欢》是苏轼的诗句，不是书名
   - 必须核实每一个作品归属

3. **引用细节准确性（所有引用都必须精确！）**:
   - **相声、小品**：郭德纲相声《我要幸福》中有"要吃鱼翅"的包袱，而不是有一段相声叫《我要吃鱼翅》
   - **文章、访谈、节目**：如果提到了具体的名称，必须确保确实存在且名称正确
   - **核心原则**：
     - 书名号《》只能用于真正存在的、有正式名称的作品
     - 引用来源要根据文章需要决定说还是不说，但如果说了就必须准确
     - 不能把作品中的某个片段、情节、包袱说成一个独立的作品
   - **不确定时的处理**：如果无法确认某个引用的准确性，宁可不写也不要编造

4. **历史准确性**:
   - 历史事件的时间、地点、人物是否准确？
   - 引用的名言是否确为该人物所说？

### 🔴 第三优先级 - 文学性与美感评估:
**核心目标：打造一篇高质量的极具欣赏性的美文**

1. **文笔美感**:
   - 语言是否优美、有韵味？
   - 是否有令人印象深刻的金句？
   - 用词是否精准、生动？
   - 是否有不必要的冗余修饰？

2. **情感共鸣**:
   - 文章是否能打动读者？
   - 情感表达是否真挚、自然？
   - 是否能引发读者的联想和共鸣？

3. **节奏与韵律**:
   - 句子长短搭配是否合理？
   - 段落节奏是否舒张有度？
   - 读起来是否朗朗上口？

4. **逻辑连贯性**: 论述是否清晰？段落之间是否流畅？
5. **文风一致性**: 是否符合要求的文风？

### 资深读者角度:
1. **吸引力**: 开头是否足够吸引人？
2. **共鸣感**: 内容是否能触动读者情感？
3. **争议点**: 是否有表述可能引起误解或争议？

## 评分标准（顶级文学标准，非常严格！）:
- 9-10分: 文学佳作，内容精炼，无一字多余
- 7-8分: 良好，有少许可优化之处
- 5-6分: 及格，有明显冗余或小问题
- 5分以下: 存在事实错误或大量废话，需要大幅修改

## 输出格式（必须严格遵循JSON格式）

{{
    "opinion": "总体评价（50-100字，必须指出是否发现事实错误或冗余内容）",
    "needs_revision": true或false,
    "score": 1-10的评分,
    "fact_errors": [
        "事实错误1：具体描述错误内容和正确信息",
        "事实错误2：..."
    ],
    "redundant_content": [
        "冗余内容1：描述需要删除的段落或句子，说明为什么与主题无关",
        "冗余内容2：例如'提及《舌尖上的中国》与汪曾祺主题无关，应删除'"
    ],
    "issues": [
        "其他问题1：描述问题所在和建议修改方向",
        "其他问题2：..."
    ],
    "suggestions": [
        "修改建议1",
        "修改建议2"
    ]
}}

## 特别注意:
- **冗余内容检测是最高优先级**：如果有与主题无关的内容，必须标记
- 如果发现任何事实错误或冗余内容，必须设置 "needs_revision": true
- fact_errors数组记录事实错误
- redundant_content数组记录需要删除的废话
- 评分要严格，存在事实错误或大量废话的文章不能超过6分

请只输出JSON，不要有其他内容。
"""

        try:
            response = self.text_client.messages.create(
                model="glm-4-flash",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # 尝试解析JSON
            # 处理可能的markdown代码块
            if response_text.startswith('```'):
                response_text = re.sub(r'^```json?\s*', '', response_text)
                response_text = re.sub(r'```\s*$', '', response_text)

            result = json.loads(response_text)

            # 验证必要字段
            if 'opinion' not in result:
                result['opinion'] = '审校完成'
            if 'needs_revision' not in result:
                result['needs_revision'] = True
            if 'issues' not in result:
                result['issues'] = []
            if 'fact_errors' not in result:
                result['fact_errors'] = []
            if 'redundant_content' not in result:
                result['redundant_content'] = []
            if 'score' not in result:
                result['score'] = 7

            # 如果有事实错误或冗余内容，强制设置needs_revision
            if result.get('fact_errors') and len(result['fact_errors']) > 0:
                result['needs_revision'] = True
                if result['score'] > 6:
                    result['score'] = 5

            # 如果有冗余内容，也需要修改
            if result.get('redundant_content') and len(result['redundant_content']) > 0:
                result['needs_revision'] = True
                if result['score'] > 7:
                    result['score'] = 6  # 有冗余内容，评分降低

            print(f"[作者2] 评分: {result.get('score', 'N/A')}/10")
            if result.get('fact_errors'):
                print(f"[作者2] 发现事实错误: {len(result['fact_errors'])}处")
            if result.get('redundant_content'):
                print(f"[作者2] 发现冗余内容: {len(result['redundant_content'])}处")

            return result

        except json.JSONDecodeError as e:
            print(f"[WARN] 作者2返回非JSON格式，尝试提取信息")
            # 尝试从文本中提取信息
            return {
                'opinion': response_text[:200] if response_text else '审校意见解析失败',
                'needs_revision': True,
                'issues': ['审校意见格式异常，建议重新审校'],
                'fact_errors': [],
                'redundant_content': [],
                'fact_errors': [],
                'score': 6
            }
        except Exception as e:
            print(f"[ERROR] 作者2审校失败: {e}")
            return None

    def _author1_revise(self, theme, title, content, review_opinion, issues, fact_errors, redundant_content, target_length, style):
        """作者1: 根据审校意见修改文章"""
        issues_text = '\n'.join([f"- {issue}" for issue in issues]) if issues else "无其他问题"
        fact_errors_text = '\n'.join([f"🔴 {err}" for err in fact_errors]) if fact_errors else "无事实错误"
        redundant_text = '\n'.join([f"🗑️ {rc}" for rc in redundant_content]) if redundant_content else "无冗余内容"

        prompt = f"""你是【作者1】，当代顶级文学大师，根据主编的审校意见修改你的文章。

## 原文
标题: {title}

{content}

## 主编审校意见
{review_opinion}

## 🔴 第一优先级 - 冗余内容删除（必须删除！）
主编指出的与主题无关的废话，必须彻底删除：

{redundant_text}

**删除原则**：
- 这些内容与主题无关，对读者没有任何价值
- 删除后不会影响文章完整性
- 删掉后文章会更加精炼、有力度

## 🔴 第二优先级 - 事实错误修正（必须修正！）
{fact_errors_text}

## 其他问题
{issues_text}

## 修改要求（严格按优先级执行）

### 🗑️ 第一优先级 - 删除冗余内容:
1. **逐条删除主编标记的废话**: 不留任何痕迹，直接删除
2. **检查关联内容**: 如果某段话是围绕冗余内容展开的，一并删除
3. **不心疼任何废话**: 好文章是改出来的，精炼才是王道

### 🔴 第二优先级 - 事实错误修正:
1. **仔细核对每一个事实错误**: 主编指出的事实错误必须100%修正
2. **删除或更正错误信息**:
   - 如果不确定某个信息是否正确，宁可不写也不要编造
   - 作品与作者的对应关系必须准确
3. **不要用模糊表述掩盖错误**: 如"据说"、"有人认为"等

### ✅ 第三优先级 - 内容优化:
1. **认真对待每一条意见**: 仔细分析主编指出的问题
2. **保持原文优点**: 不要为了修改而丢失原文的精彩之处
3. **针对性修改**:
   - 表述不清的地方重新表达
   - 逻辑不通的地方调整结构
   - 可能引起争议的地方斟酌措辞

### 📝 格式要求:
1. **字数控制**: 删除废话后字数可能会减少，这是正常的，精炼比冗长更好
2. **保持风格**: 修改后的文风要与原文一致

## 输出格式
---
标题: [修改后的标题]

[修改后的正文内容]
---

请输出修改后的完整文章（不是修改说明，而是完整的修改后文章）。
"""

        try:
            response = self.text_client.messages.create(
                model="glm-4-flash",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            return self._parse_article_response(content, theme)
        except Exception as e:
            print(f"[ERROR] 作者1修改失败: {e}")
            return None

    def _parse_article_response(self, response_text, default_theme):
        """解析AI返回的文章内容"""
        lines = response_text.split('\n')
        title = ""
        body_lines = []

        for line in lines:
            if line.startswith("标题:") or line.startswith("标题："):
                title = line.replace("标题:", "").replace("标题：", "").strip()
            elif line.strip() == "---":
                continue
            elif title:
                body_lines.append(line)

        body = '\n'.join(body_lines).strip()

        if not title:
            title = lines[0].strip() if lines else f"关于{default_theme}的思考"

        if not body or len(body) < 50:
            return None

        return {
            'title': title,
            'content': body,
            'word_count': len(body)
        }

    def generate_article_images(self, theme, article_content, image_style="realistic", num_images=3):
        """根据文章主题和内容生成配图，支持多模型降级

        Args:
            theme: 文章主题
            article_content: 文章内容
            image_style: 图片风格
            num_images: 配图数量（默认3张）

        优先级: Seedream 4.5 -> Seedream 4.0 -> Antigravity -> Pollinations
        """

        import urllib.parse
        import requests
        from io import BytesIO

        # 清理主题中的 emoji 和特殊字符
        clean_theme = re.sub(r'[^\u4e00-\u9fff\w\s\-.,]', '', theme)
        clean_theme = clean_theme.strip()[:30]  # 限制长度

        print(f"\n[INFO] Generating {num_images} images for theme: {clean_theme}")
        print(f"[INFO] Image style: {image_style}")

        # 根据文章内容提取关键词生成配图提示词
        image_prompts = self._generate_contextual_prompts(clean_theme, article_content, image_style, num_images)
        generated_images = []

        for i, (img_prompt, img_desc) in enumerate(image_prompts, 1):
            print(f"[IMAGE {i}] {img_desc}...")

            image_generated = False

            # 1. 优先尝试 Seedream 4.5 (火山引擎)
            if not image_generated and self.volcano_client:
                try:
                    print(f"    [TRY] Seedream 4.5...")
                    response = self.volcano_client.images.generate(
                        model="doubao-seedream-4-5-251128",
                        prompt=img_prompt,
                        size="2K",  # 高分辨率，不限制形状
                        response_format="url",
                        extra_body={
                            "watermark": False,
                        },
                    )

                    if hasattr(response, 'data') and len(response.data) > 0:
                        image_url = response.data[0].url
                        img_response = requests.get(image_url, timeout=60)
                        if img_response.status_code == 200:
                            img = Image.open(BytesIO(img_response.content))
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            safe_desc = "".join(c for c in img_desc if c.isalnum() or c in ('_', '-'))[:20]
                            filename = f"article_img{i}_{safe_desc}_{timestamp}.jpg"
                            tool_dir = Path(__file__).parent
                            img_path = str(tool_dir / filename)
                            img.save(img_path, 'JPEG', quality=95)
                            generated_images.append(img_path)
                            print(f"    [OK] {filename} (Seedream 4.5)")
                            image_generated = True
                        else:
                            print(f"    [WARN] Seedream 4.5 download failed: HTTP {img_response.status_code}")
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "quota" in error_str.lower():
                        print(f"    [WARN] Seedream 4.5 quota exceeded, trying 4.0...")
                    else:
                        print(f"    [WARN] Seedream 4.5 failed: {error_str[:60]}")

            # 2. 如果 Seedream 4.5 失败(配额问题)，尝试 Seedream 4.0
            if not image_generated and self.volcano_client:
                try:
                    print(f"    [TRY] Seedream 4.0...")
                    response = self.volcano_client.images.generate(
                        model="doubao-seedream-4-0-250828",
                        prompt=img_prompt,
                        size="2K",  # 高分辨率，不限制形状
                        response_format="url",
                        extra_body={
                            "watermark": False,
                        },
                    )

                    if hasattr(response, 'data') and len(response.data) > 0:
                        image_url = response.data[0].url
                        img_response = requests.get(image_url, timeout=60)
                        if img_response.status_code == 200:
                            img = Image.open(BytesIO(img_response.content))
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                            safe_desc = "".join(c for c in img_desc if c.isalnum() or c in ('_', '-'))[:20]
                            filename = f"article_img{i}_{safe_desc}_{timestamp}.jpg"
                            tool_dir = Path(__file__).parent
                            img_path = str(tool_dir / filename)
                            img.save(img_path, 'JPEG', quality=95)
                            generated_images.append(img_path)
                            print(f"    [OK] {filename} (Seedream 4.0)")
                            image_generated = True
                        else:
                            print(f"    [WARN] Seedream 4.0 download failed: HTTP {img_response.status_code}")
                except Exception as e:
                    print(f"    [WARN] Seedream 4.0 failed: {str(e)[:60]}")

            # 3. 如果 Seedream 都失败，尝试 Antigravity 模型
            if not image_generated and self.image_client:
                # 定义 Antigravity 模型优先级
                antigravity_models = [
                    {"model": "gemini-3-flash-image", "name": "Gemini 3 Flash"},
                    {"model": "flux-1.1-pro", "name": "Flux 1.1 Pro"},
                    {"model": "flux-schnell", "name": "Flux Schnell"},
                    {"model": "dall-e-3", "name": "DALL-E 3"},
                ]

                for model_info in antigravity_models:
                    if image_generated:
                        break
                    try:
                        print(f"    [TRY] {model_info['name']}...")
                        response = self.image_client.images.generate(
                            model=model_info["model"],
                            prompt=img_prompt,
                            size="1024x1024",
                            n=1,
                        )

                        if hasattr(response, 'data') and len(response.data) > 0:
                            image_data = response.data[0]
                            b64_json = getattr(image_data, 'b64_json', None)

                            if b64_json:
                                image_bytes = base64.b64decode(b64_json)
                                img = Image.open(io.BytesIO(image_bytes))
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                safe_desc = "".join(c for c in img_desc if c.isalnum() or c in ('_', '-'))[:20]
                                filename = f"article_img{i}_{safe_desc}_{timestamp}.jpg"
                                tool_dir = Path(__file__).parent
                                img_path = str(tool_dir / filename)
                                img.save(img_path, 'JPEG', quality=95)
                                generated_images.append(img_path)
                                print(f"    [OK] {filename} ({model_info['name']})")
                                image_generated = True
                    except Exception as e:
                        error_str = str(e)
                        if "404" in error_str or "NOT_FOUND" in error_str:
                            print(f"    [SKIP] {model_info['name']}: not available")
                        elif "429" in error_str or "quota" in error_str.lower():
                            print(f"    [SKIP] {model_info['name']}: quota exceeded")
                        else:
                            print(f"    [WARN] {model_info['name']} failed: {error_str[:50]}")

            # 4. 最后备选：Pollinations.ai
            if not image_generated:
                print(f"    [FALLBACK] Trying Pollinations.ai...")
                try:
                    content_lower = article_content.lower() if article_content else ""
                    if any(kw in content_lower for kw in ['ai', 'glm', 'artificial', 'model', 'code']):
                        simple_topic = "robot"
                    elif any(kw in content_lower for kw in ['food', 'cook', 'recipe', '美食']):
                        simple_topic = "food"
                    elif any(kw in content_lower for kw in ['travel', 'landscape', '风景']):
                        simple_topic = "landscape"
                    else:
                        simple_topic = "technology"

                    encoded_prompt = urllib.parse.quote(simple_topic)
                    pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

                    response = requests.get(pollinations_url, timeout=90)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"article_img{i}_{img_desc}_{timestamp}.jpg"
                        tool_dir = Path(__file__).parent
                        img_path = str(tool_dir / filename)
                        img.save(img_path, 'JPEG', quality=95)
                        generated_images.append(img_path)
                        print(f"    [OK] {filename} (Pollinations)")
                        image_generated = True
                    else:
                        print(f"    [FAIL] Pollinations HTTP {response.status_code}")

                except Exception as e2:
                    print(f"    [FAIL] Pollinations error: {str(e2)[:80]}")

            if not image_generated:
                print(f"    [FAIL] Could not generate image {i}")

        return generated_images

    def _generate_contextual_prompts(self, theme, content, style, num_images=3):
        """使用AI大模型根据文章内容智能生成上下文相关的图片提示词

        Args:
            theme: 文章主题
            content: 文章内容
            style: 图片风格
            num_images: 需要生成的图片数量
        """

        # 风格映射
        style_desc = {
            "realistic": "realistic photography, high quality, professional lighting",
            "artistic": "artistic style, creative, elegant composition",
            "cartoon": "cartoon illustration, colorful, friendly style",
            "technical": "technical diagram, flowchart, architecture diagram, clean infographic style",
            "auto": "professional quality visualization"
        }.get(style, "realistic photography, high quality")

        # 使用AI生成与内容相关的配图提示词
        ai_prompt = f"""请根据以下文章内容，为{num_images}张配图生成英文提示词(prompt)。

文章主题: {theme}

文章内容摘要（前1500字）:
{content[:1500]}

配图风格要求: {style_desc}

请生成{num_images}个配图的英文提示词，要求：
- 第1张图：概括文章核心概念或主题的场景图
- 后续图片：展示文章中提到的关键细节、场景或应用

每个提示词要求：
- 使用英文，简洁明了（50词以内）
- 包含具体的视觉元素描述
- 符合指定的配图风格
- 与文章段落内容紧密相关

请直接输出{num_images}行，每行一个提示词，格式如下：
1. [第1张图的英文提示词]
2. [第2张图的英文提示词]
...
"""

        try:
            print("[AI] Generating contextual image prompts...")

            # 使用ZhipuAI生成提示词
            response = self.text_client.messages.create(
                model="glm-4.6",
                max_tokens=500,
                messages=[{"role": "user", "content": ai_prompt}]
            )

            ai_response = response.content[0].text.strip()
            print(f"[AI] Response received: {ai_response[:100]}...")

            # 解析AI返回的3个提示词
            lines = ai_response.strip().split('\n')
            prompts = []

            for line in lines:
                # 移除行号前缀（如 "1. ", "2. ", "3. "）
                cleaned = re.sub(r'^\d+\.\s*', '', line).strip()
                if cleaned and len(cleaned) > 10:
                    # 添加风格后缀
                    prompt_with_style = f"{cleaned}, {style_desc}"
                    prompts.append((prompt_with_style, f"context_img{len(prompts)+1}"))

            # 确保有num_images个提示词
            if len(prompts) < num_images:
                # 补充默认提示词
                default_prompts = [
                    (f"{theme} main concept visualization, {style_desc}", "scene_main"),
                    (f"{theme} detailed process flow, {style_desc}", "scene_detail"),
                    (f"{theme} application scenario, {style_desc}", "scene_lifestyle"),
                    (f"{theme} key elements close-up, {style_desc}", "scene_closeup"),
                    (f"{theme} environment atmosphere, {style_desc}", "scene_atmosphere"),
                    (f"{theme} cultural context, {style_desc}", "scene_culture"),
                    (f"{theme} emotional expression, {style_desc}", "scene_emotion"),
                    (f"{theme} artistic interpretation, {style_desc}", "scene_artistic"),
                    (f"{theme} story moment, {style_desc}", "scene_story"),
                    (f"{theme} final impression, {style_desc}", "scene_final"),
                ]
                while len(prompts) < num_images and len(prompts) < len(default_prompts):
                    prompts.append(default_prompts[len(prompts)])

            return prompts[:num_images]

        except Exception as e:
            print(f"[WARN] AI prompt generation failed: {e}, using fallback")
            # 降级方案：基于关键词的简单提示词
            fallback_prompts = [
                (f"{theme} concept overview, {style_desc}", "scene_main"),
                (f"{theme} detailed view, {style_desc}", "scene_detail"),
                (f"{theme} application scene, {style_desc}", "scene_lifestyle"),
                (f"{theme} close-up shot, {style_desc}", "scene_closeup"),
                (f"{theme} atmosphere, {style_desc}", "scene_atmosphere"),
                (f"{theme} cultural background, {style_desc}", "scene_culture"),
                (f"{theme} emotional moment, {style_desc}", "scene_emotion"),
                (f"{theme} artistic view, {style_desc}", "scene_artistic"),
                (f"{theme} story scene, {style_desc}", "scene_story"),
                (f"{theme} final view, {style_desc}", "scene_final"),
            ]
            return fallback_prompts[:num_images]

    def _generate_image_prompts(self, theme, style):
        """根据主题生成配图提示词"""

        # 使用更简洁的英文提示词，避免 Pollinations 530 错误
        # 只保留核心主题，限制长度
        short_theme = theme[:30] if len(theme) > 30 else theme

        base_prompts = {
            "realistic": [
                f"{short_theme}, professional photo",
                f"{short_theme}, close up shot",
                f"{short_theme}, lifestyle scene"
            ],
            "artistic": [
                f"{short_theme}, oil painting art",
                f"{short_theme}, watercolor illustration",
                f"{short_theme}, digital art"
            ],
            "cartoon": [
                f"{short_theme}, cartoon style",
                f"{short_theme}, manga style",
                f"{short_theme}, cute illustration"
            ],
            "technical": [
                f"{short_theme}, technical architecture diagram, flowchart, clean design",
                f"{short_theme}, process flow diagram, infographic style",
                f"{short_theme}, system structure diagram, professional blueprint"
            ],
            "auto": [
                f"{short_theme}, professional visualization",
                f"{short_theme}, detailed illustration",
                f"{short_theme}, creative concept art"
            ]
        }

        descriptions = {
            "realistic": ["main_scene", "detail_shot", "lifestyle"],
            "artistic": ["art_creation", "watercolor", "digital_art"],
            "cartoon": ["cartoon", "manga", "illustration"],
            "technical": ["architecture_diagram", "flowchart", "system_structure"],
            "auto": ["main_view", "detail_view", "concept_view"]
        }

        prompts = base_prompts.get(style, base_prompts["realistic"])
        descs = descriptions.get(style, descriptions["realistic"])

        return list(zip(prompts, descs))

    def create_article_html(self, title, content, theme, images=None):
        """创建HTML格式的文章(配图插入到段落之间)"""

        # 将内容分割成段落
        formatted_content = self._format_content_with_images(content, images)

        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}

        .title {{
            font-size: 2em;
            font-weight: bold;
            color: #222;
            margin-bottom: 15px;
            line-height: 1.4;
        }}

        .meta {{
            color: #999;
            font-size: 0.9em;
        }}

        .content {{
            font-size: 1.1em;
            line-height: 2;
        }}

        .content p {{
            margin-bottom: 20px;
        }}

        .content h2 {{
            font-size: 1.5em;
            color: #5a67d8;
            margin: 30px 0 15px 0;
            padding-left: 15px;
            border-left: 4px solid #5a67d8;
        }}

        .content h3 {{
            font-size: 1.3em;
            color: #6b46c1;
            margin: 25px 0 10px 0;
        }}

        .content strong {{
            color: #c53030;
            font-weight: 600;
            background: linear-gradient(transparent 60%, #fed7d7 60%);
            padding: 0 2px;
        }}

        .article-image {{
            margin: 30px 0;
            text-align: center;
        }}

        .article-image img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .article-image .caption {{
            margin-top: 8px;
            font-size: 0.9em;
            color: #666;
            font-style: italic;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }}

        .highlight {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="title">{title}</div>
            <div class="meta">
                Theme: {theme} |
                Words: {len(content)} |
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>

        <div class="content">
            {formatted_content}
        </div>

        <div class="footer">
            <p>Generated by AI Article Tool</p>
            <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

        return html_content

    def _format_content_with_images(self, content, images=None):
        """将内容格式化为HTML，并将图片插入到段落之间"""

        import re
        import os

        html = content

        # 先修复AI可能生成的错误HTML标签
        html = re.sub(r'<strong>([^<]*)<strong>', r'<strong>\1</strong>', html)

        # 转换段落
        paragraphs = html.split('\n\n')
        html_paragraphs = []

        # 计算图片插入位置（均匀分布）
        num_paragraphs = len([p for p in paragraphs if p.strip() and not p.startswith('#')])
        num_images = len(images) if images else 0

        # 确定图片插入点
        image_insert_points = []
        if num_images > 0 and num_paragraphs > 0:
            # 在文章的 1/4, 1/2, 3/4 位置插入图片
            insert_ratios = [0.25, 0.5, 0.75][:num_images]
            image_insert_points = [int(num_paragraphs * r) for r in insert_ratios]

        current_paragraph = 0
        image_index = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 处理标题
            if para.startswith('#### '):
                html_paragraphs.append(f'<h4 style="color: #718096; font-size: 1.1em; margin: 20px 0 10px 0;">{para[5:]}</h4>')
            elif para.startswith('### '):
                html_paragraphs.append(f'<h3>{para[4:]}</h3>')
            elif para.startswith('## '):
                html_paragraphs.append(f'<h2>{para[3:]}</h2>')
            elif para.startswith('# '):
                html_paragraphs.append(f'<h2>{para[2:]}</h2>')
            elif para.startswith('>'):
                html_paragraphs.append(f'<div class="highlight">{para[1:].strip()}</div>')
            else:
                # 普通段落
                para = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', para)
                para = para.replace('\n', '<br>')
                html_paragraphs.append(f'<p>{para}</p>')

                # 检查是否需要插入图片
                if image_index < num_images and current_paragraph in image_insert_points:
                    img = images[image_index]

                    # 将图片转为Base64嵌入HTML，这样HTML单独打开时也能显示图片
                    img_url = img  # 默认使用路径
                    try:
                        with open(img, 'rb') as f:
                            img_data = f.read()
                        img_base64 = base64.b64encode(img_data).decode('utf-8')
                        img_url = f"data:image/jpeg;base64,{img_base64}"
                    except Exception as e:
                        # 如果读取失败，使用相对路径
                        img_url = os.path.basename(img)

                    # 图片描述
                    captions = ["Main scene", "Detail view", "Context view"]
                    caption = captions[image_index] if image_index < len(captions) else f"Image {image_index + 1}"

                    html_paragraphs.append(f'''
<div class="article-image">
    <img src="{img_url}" alt="Article image">
    <div class="caption">{caption}</div>
</div>''')
                    image_index += 1

                current_paragraph += 1

        return '\n'.join(html_paragraphs)


def get_user_input_mode():
    """获取用户选择:主题生成 or 草稿完善"""

    print("\n" + "="*80)
    print("今日头条文章生成器 v3.1 - 增强版")
    print("="*80)
    print()
    print("请选择文章生成方式:")
    print()
    print("  1. 主题生成 - 输入主题,AI从零开始生成文章")
    print("  2. 草稿完善 - 输入您的草稿,AI优化完善")
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            mode = sys.stdin.readline().strip()
            if mode and mode in ['1', '2']:
                print(f"[Web模式] 模式: {'主题生成' if mode == '1' else '草稿完善'}")
                return int(mode)
        except:
            pass

    while True:
        try:
            choice = input("请选择 (默认为1): ").strip()

            if not choice:
                return 1  # 默认主题生成

            if choice in ["1", "主题", "生成"]:
                return 1
            elif choice in ["2", "草稿", "完善"]:
                return 2
            else:
                print("[提示] 请输入 1 或 2")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return 1


def get_user_draft():
    """获取用户输入的草稿"""

    print("\n" + "-"*80)
    print("草稿完善模式")
    print("-"*80)
    print()
    print("请输入您的文章草稿(支持多行输入)")
    print("提示: 输入完成后,在新的一行输入 'END' 并回车结束")
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            lines = []
            for line in sys.stdin:
                line = line.strip()
                if line == 'END':
                    break
                lines.append(line)

            if lines:
                draft = '\n'.join(lines)

                # 清理草稿中的代理字符
                try:
                    draft.encode('utf-8')
                except UnicodeEncodeError:
                    draft = draft.encode('utf-8', errors='ignore').decode('utf-8')
                    print("[提示] 草稿包含特殊字符，已自动清理")

                print(f"[Web模式] 已读取草稿: {len(draft)}字")
                return draft
        except:
            pass

    # 手动输入模式
    draft_lines = []
    print("开始输入草稿内容:")
    print()

    try:
        while True:
            line = input()

            if line.strip() == 'END':
                break

            draft_lines.append(line)

        draft = '\n'.join(draft_lines).strip()

        # 清理草稿中的代理字符
        try:
            draft.encode('utf-8')
        except UnicodeEncodeError:
            draft = draft.encode('utf-8', errors='ignore').decode('utf-8')
            print("[提示] 草稿包含特殊字符，已自动清理")

        if draft:
            print(f"\n[成功] 已读取草稿: {len(draft)}字")
            return draft
        else:
            print("\n[错误] 草稿为空")
            return None

    except KeyboardInterrupt:
        print("\n\n[提示] 用户取消输入")
        return None
    except Exception as e:
        print(f"[错误] 输入错误: {e}")
        return None


def get_user_theme():
    """获取用户输入的主题"""

    print("\n" + "="*80)
    print("今日头条文章生成器 - AI增强版 v3.1")
    print("="*80)
    print()

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            theme = sys.stdin.readline().strip()
            if theme:
                print(f"[Web模式] 主题: {theme}")
                return theme
        except:
            pass

    print("请输入您想要生成文章的主题")
    print()
    print("示例主题:")
    themes = [
        "过年回老家",
        "职场新人必看",
        "健康养生小贴士",
        "理财投资心得",
        "教育孩子感悟",
        "情感关系建议"
    ]

    for i, theme in enumerate(themes, 1):
        print(f"  {i}. {theme}")

    print()
    print("您可以输入上述主题,或输入自定义主题")
    print()

    while True:
        try:
            user_input = input("请输入主题 (输入 'q' 退出): ").strip()

            if user_input.lower() == 'q':
                return None

            if user_input:
                print(f"\n[确认] 主题: {user_input}")
                return user_input
            else:
                print("[提示] 主题不能为空,请重新输入")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return None


def get_target_length():
    """获取目标字数"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            length = sys.stdin.readline().strip()
            if length and length.isdigit():
                print(f"[Web模式] 字数: {length}")
                return int(length)
        except:
            pass

    print()
    print("请选择文章长度:")
    print("  1. 1500字左右 (快速阅读)")
    print("  2. 2000字左右 (标准长度)")
    print("  3. 2500字左右 (深度文章)")

    while True:
        try:
            choice = input("\n请选择 (默认为2): ").strip()

            if not choice:
                choice = "2"

            if choice in ["1", "2", "3"]:
                lengths = {"1": 1500, "2": 2000, "3": 2500}
                return lengths[choice]
            else:
                print("[提示] 请输入 1、2 或 3")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return 2000
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return 2000


def get_generate_images():
    """询问是否生成配图"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            choice = sys.stdin.readline().strip()
            if choice:
                return choice.lower() == 'y'
        except:
            pass

    print()
    while True:
        try:
            choice = input("是否生成配图? (y/n, 默认: y): ").strip().lower()
            if not choice:
                return True
            if choice in ['y', 'yes', '是']:
                return True
            elif choice in ['n', 'no', '否']:
                return False
            else:
                print("[提示] 请输入 y 或 n")
        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return False
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return False


def get_image_style():
    """获取配图风格"""

    # 检查是否有标准输入(从Web界面调用)
    import sys
    if not sys.stdin.isatty():
        # 从管道或文件读取
        try:
            style = sys.stdin.readline().strip()
            if style:
                return style
        except:
            pass

    print()
    print("请选择配图风格:")
    print("  1. 真实照片 (realistic)")
    print("  2. 艺术创作 (artistic)")
    print("  3. 卡通插画 (cartoon)")

    while True:
        try:
            choice = input("\n请选择 (默认为1): ").strip().lower()

            if not choice:
                return "realistic"

            if choice in ["1", "realistic", "真实"]:
                return "realistic"
            elif choice in ["2", "artistic", "艺术"]:
                return "artistic"
            elif choice in ["3", "cartoon", "卡通"]:
                return "cartoon"
            else:
                print("[提示] 请输入 1、2 或 3")
        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return "realistic"
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return "realistic"


def main():
    """主函数"""

    print("="*80)
    print("今日头条文章生成器 v3.1 - 增强版")
    print("支持文章生成 + 草稿完善 + 智能配图")
    print("="*80)
    print()

    # 获取用户选择的模式
    mode = get_user_input_mode()

    if not mode:
        print("\n[退出] 未选择模式,程序退出")
        return

    # 根据模式获取输入
    theme = None
    draft = None

    if mode == 1:
        # 主题生成模式
        theme = get_user_theme()
        if not theme:
            print("\n[退出] 未输入主题,程序退出")
            return
    elif mode == 2:
        # 草稿完善模式
        draft = get_user_draft()
        if not draft:
            print("\n[退出] 未输入草稿,程序退出")
            return
        theme = "基于草稿完善"  # 用于文件命名

    # 获取目标字数
    target_length = get_target_length()

    print(f"\n[设置] 目标字数: {target_length}字")

    # 询问是否生成配图
    generate_images = get_generate_images()

    image_style = "realistic"
    if generate_images:
        image_style = get_image_style()
        print(f"[设置] 配图风格: {image_style}")

    # 创建生成器
    generator = ToutiaoArticleGenerator()

    if not generator.text_client:
        print("\n[ERROR] 无法初始化AI文本客户端")
        print("[ERROR] 请检查config.py中的ZHIPU_API_KEY配置")
        return

    if generate_images and not generator.image_client:
        print("\n[WARNING] 无法初始化AI图像客户端")
        print("[WARNING] 将跳过配图生成")
        generate_images = False

    # 生成/完善文章
    print()
    print("-"*80)
    print()

    if mode == 1:
        article = generator.generate_article_with_ai(theme, target_length)
        if not article:
            print("\n[ERROR] 文章生成失败")
            return
    else:
        article = generator.improve_article_draft(draft, target_length)
        if not article:
            print("\n[ERROR] 草稿完善失败")
            return

    # 显示生成的文章
    print()
    print("-"*80)
    print()
    print(f"[成功] {'文章生成' if mode == 1 else '草稿完善'}成功!")
    print()
    print("="*80)
    print(f"标题: {article['title']}")
    print("="*80)
    print()
    print(article['content'])
    print()
    print("="*80)
    print(f"字数: {article['word_count']}字")
    print(f"目标: {article['target_length']}字")
    print(f"完成度: {article['word_count']/article['target_length']*100:.1f}%")
    if mode == 2:
        print(f"来源: 草稿完善")
    print("="*80)
    print()

    # 生成配图
    generated_images = []
    if generate_images:
        print()
        print("-"*80)
        print()
        print("[配图] 开始生成配图...")
        print()
        generated_images = generator.generate_article_images(theme, article['content'], image_style)

        if generated_images:
            print(f"\n[成功] 成功生成 {len(generated_images)} 张配图")
        else:
            print("\n[警告] 配图生成失败,但文章已成功生成")

    # 保存为Markdown文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_prefix = "文章草稿完善" if mode == 2 else "今日头条文章"
    md_filename = f"{file_prefix}_{theme}_{timestamp}.md"

    # 保存到工具所在目录
    tool_dir = Path(__file__).parent
    md_path = str(tool_dir / md_filename)

    source_note = " (基于用户草稿完善)" if mode == 2 else ""
    md_content = f"""# {article['title']}

**主题**: {theme}
**字数**: {article['word_count']}字
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{source_note}

---

{article['content']}

---

*本文由AI发文工具管理器自动生成{source_note}*
"""

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"\n[成功] Markdown文件已保存: {md_path}")

    # 保存为HTML文件
    html_filename = f"{file_prefix}_{theme}_{timestamp}.html"
    html_path = str(tool_dir / html_filename)
    html_content = generator.create_article_html(article['title'], article['content'], theme, generated_images)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"[成功] HTML文件已保存: {html_path}")

    # 自动打开HTML文件
    try:
        import webbrowser
        webbrowser.open(f'file:///{os.path.abspath(html_path)}'.replace('\\', '/'))
        print(f"[成功] 已在浏览器中打开文章预览")
    except:
        print(f"[提示] 请手动打开HTML文件查看文章: {html_path}")

    print()
    print("="*80)
    print("生成完成!")
    if generated_images:
        print(f"[文件] 文章: {md_filename}")
        print(f"[文件] HTML: {html_filename}")
        print(f"[配图] 配图: {len(generated_images)}张")
    else:
        print(f"[文件] 文章: {md_filename}")
        print(f"[文件] HTML: {html_filename}")
    print("="*80)
    print()





def main_web():
    """Web模式主函数 - 从tool_manager.py调用"""
    print("\n" + "="*60)
    print("[INFO] Web Mode - main_web() started")
    print("="*60 + "\n")

    try:
        # 读取JSON参数文件
        params_json_path = os.environ.get('ARTICLE_PARAMS_JSON', 'article_params.json')
        print(f"[INFO] Params file: {params_json_path}")

        with open(params_json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)
        print(f"[INFO] Params loaded successfully\n")

        # 解析参数
        mode = params.get('mode', '1')
        theme = params.get('theme', '')
        draft = params.get('draft', '')
        length = params.get('length', 2000)
        generate_images = params.get('generate_images', 'y')
        image_style = params.get('image_style', 'realistic')
        style = params.get('style', 'standard')

        print(f"[PARAM] mode: {mode}")
        print(f"[PARAM] theme: {theme}")
        print(f"[PARAM] draft: {draft}")
        print(f"[PARAM] length: {length}")
        print(f"[PARAM] generate_images: {generate_images}")
        print(f"[PARAM] image_style: {image_style}")
        print(f"[PARAM] style: {style}\n")

        # 模式1: 主题生成
        if mode == '1':
            print("[STEP 1/3] Theme generation mode")
            if not theme:
                return {"error": "Theme cannot be empty"}

            # 创建生成器实例
            print("[STEP 2/3] Initializing AI client...")
            generator = ToutiaoArticleGenerator()
            if not generator.text_client:
                return {"error": "Failed to initialize AI client"}

            # 调用生成方法
            print("[STEP 3/3] Generating article with AI...")
            article = generator.generate_article_with_ai(theme, length, style)
            if not article:
                print(f"[ERROR] generate_article_with_ai returned None!")
                return {"error": "Article generation failed"}

            # 验证文章内容
            print(f"[DEBUG] Article returned: title='{article.get('title', 'N/A')}', content_len={len(article.get('content', ''))}")
            if not article.get('content') or len(article.get('content', '')) < 50:
                print(f"[ERROR] Article content is too short or empty!")
                print(f"[ERROR] Full article dict: {article}")
                return {"error": f"Generated article content is too short ({len(article.get('content', ''))} chars)"}

            result = {
                "success": True,
                "title": article['title'],
                "content": article['content'],
                "word_count": article['word_count'],
                "target_length": article['target_length']
            }

        # 模式2: 草稿完善
        elif mode == '2':
            print("[STEP 1/4] Draft improvement mode")
            print(f"[INFO] draft param: [{draft}]")
            print(f"[INFO] working dir: {os.getcwd()}")
            print(f"[INFO] script file: {__file__}")

            # 转换为绝对路径(解决相对路径问题)
            if os.path.isabs(draft):
                draft_path = draft
            else:
                # 相对路径: 基于项目根目录(post/)解析，而不是脚本目录
                # 统一处理路径分隔符
                draft_normalized = draft.replace('/', os.sep).replace('\\', os.sep)
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                draft_path = os.path.join(project_root, draft_normalized)

            print(f"[STEP 2/4] Draft path resolved: {draft_path}")
            print(f"[INFO] File exists: {os.path.exists(draft_path)}")

            # 检查draft是否是文件路径,如果是则读取文件内容
            if os.path.exists(draft_path):
                print(f"[INFO] Reading draft file...")
                try:
                    with open(draft_path, 'r', encoding='utf-8') as f:
                        draft_content = f.read()
                    draft = draft_content
                    print(f"[INFO] Draft loaded: {len(draft)} chars\n")
                except Exception as e:
                    return {"error": f"Failed to read draft file: {str(e)}"}
            else:
                print(f"[INFO] Using draft text content directly")

            if not draft:
                return {"error": "Draft content cannot be empty"}

            # 创建生成器实例
            print("[STEP 3/4] Initializing AI client...")
            generator = ToutiaoArticleGenerator()
            if not generator.text_client:
                return {"error": "Failed to initialize AI client"}

            # 调用草稿完善方法
            print("[STEP 4/4] Improving draft with AI...")
            article = generator.improve_article_draft(draft, length)
            if not article:
                print(f"[ERROR] improve_article_draft returned None!")
                return {"error": "Draft improvement failed"}

            # 验证文章内容
            print(f"[DEBUG] Article returned: title='{article.get('title', 'N/A')}', content_len={len(article.get('content', ''))}")
            if not article.get('content') or len(article.get('content', '')) < 50:
                print(f"[ERROR] Article content is too short or empty!")
                print(f"[ERROR] Full article dict: {article}")
                return {"error": f"Generated article content is too short ({len(article.get('content', ''))} chars)"}

            result = {
                "success": True,
                "title": article['title'],
                "content": article['content'],
                "word_count": article['word_count'],
                "target_length": article['target_length']
            }

        else:
            return {"error": f"Invalid mode: {mode}"}

        # 生成配图（如果启用）
        generated_images = None
        if generate_images == 'y':
            print(f"[INFO] Generating images for article...")
            try:
                generated_images = generator.generate_article_images(
                    theme if theme else article['title'],
                    article['content'],
                    image_style
                )
                if generated_images:
                    print(f"[INFO] Generated {len(generated_images)} images")
                else:
                    print(f"[WARN] Image generation returned no results")
            except Exception as e:
                print(f"[WARN] Image generation failed: {e}")
                generated_images = None

        # 保存文章到文件
        print("[INFO] Saving article to files...")
        tool_dir = Path(__file__).parent
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_theme = theme if mode == '1' else 'draft_improved'
        file_prefix = "Article" if mode == '1' else "DraftImproved"

        # 保存 Markdown 文件
        md_filename = f"{file_prefix}_{file_theme}_{timestamp}.md"
        md_path = str(tool_dir / md_filename)
        source_note = " (Improved from draft)" if mode == '2' else ""
        md_content = f"""# {article['title']}

**Theme**: {theme if mode == '1' else 'Draft Improvement'}
**Words**: {article['word_count']} chars
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{source_note}

---

{article['content']}

---

*Generated by AI Article Tool{source_note}*
"""
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"[INFO] Markdown saved: {md_filename}")

        # 保存 HTML 文件（包含配图）
        html_filename = f"{file_prefix}_{file_theme}_{timestamp}.html"
        html_path = str(tool_dir / html_filename)
        html_content = generator.create_article_html(
            article['title'],
            article['content'],
            theme if theme else 'Draft',
            generated_images  # 传入配图
        )
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[INFO] HTML saved: {html_filename}")

        # 添加文件路径到结果
        result['md_file'] = md_filename
        result['html_file'] = html_filename
        result['html_path'] = html_path

        # 清理临时参数文件
        try:
            os.remove(params_json_path)
            print(f"[CLEANUP] Temp file removed: {params_json_path}\n")
        except:
            pass

        # 自动在浏览器中打开HTML文件
        try:
            import webbrowser
            abs_html_path = os.path.abspath(html_path)
            webbrowser.open(f'file:///{abs_html_path}'.replace('\\', '/'))
            print(f"[SUCCESS] HTML opened in browser")
        except Exception as browser_error:
            print(f"[WARN] Could not open browser: {browser_error}")

        print("[SUCCESS] Article generation completed!")
        print(f"[OUTPUT] MD: {md_filename}")
        print(f"[OUTPUT] HTML: {html_filename}")
        return result

    except Exception as e:
        print(f"[ERROR] main_web failed: {e}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    # 添加入口点调试 - 使用简单的ASCII字符避免编码问题
    print("\n" + "="*60)
    print("[INFO] Toutiao Article Generator v3.1")
    print(f"[INFO] Working Dir: {os.getcwd()}")
    print(f"[INFO] Params File: {os.environ.get('ARTICLE_PARAMS_JSON', 'NOT SET')}")

    # 检测是否在Web模式下运行
    if os.environ.get("ARTICLE_PARAMS_JSON"):
        print("[INFO] Mode: WEB - Starting article generation...")
        print("="*60 + "\n")
        main_web()
    else:
        print("[INFO] Mode: CLI - Starting interactive mode...")
        print("="*60 + "\n")
        main()
