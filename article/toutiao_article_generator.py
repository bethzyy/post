# -*- coding: utf-8 -*-
"""
今日头条高赞文章生成器 v3.0 - 增强版
支持用户输入自定义主题,使用AI生成高质量文章
新增: 自动生成配图功能
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

# 添加父目录到路径以导入config
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_zhipu_anthropic_client, get_antigravity_client, get_volcano_client


class ToutiaoArticleGenerator:
    """今日头条文章生成器 - AI增强版 v3.1"""

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
            prompt = f"""你是一位资深的专栏作家，擅长用优美的文字和深刻的思考打动读者。请将以下用户草稿完善为一篇有深度、有温度、有新意的文章。

## 用户草稿:

{draft_content}

## 写作要求:
1. **字数**: {target_length}字左右
2. **文风**: 资深写手风格
   - 语言优美流畅，避免机器感和套路化表达
   - 用词精准，句式多变，长短句结合
   - 适当运用修辞手法（比喻、排比、设问等）
   - 文字要有温度，能引起读者共鸣
3. **结构**:
   - 引人入胜的开头（可以从个人经历或时代背景切入）
   - 2-3个深度观点（不要简单罗列，要有逻辑递进）
   - 意味深长的结尾（留有思考空间）
4. **内容提升**:
   - 保留草稿的核心思想和情感基调
   - 补充2026年AI时代的最新视角和案例
   - 融入"第三空间"、"知识体验中心"等前沿概念
   - 加入对人文精神在算法时代的思考
   - 避免陈词滥调和空话套话
5. **标题**: 文学性+思想性，15-25字，避免标题党
6. **禁忌**:
   - 不得使用"首先、其次、最后"等公文式表达
   - 不得过度使用emoji（最多2-3处，且要用得恰到好处）
   - 不得使用"让我们一起"、"不容错过"等营销话术
   - 不得生硬列举"5个XX"、"3大XX"

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

[完善后的正文内容]

---

记住:你要写的是一篇能打动人心、引人深思的专栏文章，而不是一篇营销文案。
"""
        else:
            prompt = f"""请将以下用户草稿完善为一篇高质量的今日头条文章。

## 用户草稿:

{draft_content}

## 完善要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
3. 结构: 吸引人的标题 + 引人入胜的开头 + 3-5个要点 + 感人或启发的结尾 + 互动号召
4. 内容优化:
   - 保留草稿的核心观点和主要内容
   - 补充具体的案例和数据
   - 优化表达,使其更生动有趣
   - 增加适当的emoji增强可读性
5. 标题优化: 使用数字+疑问/对比/利益点,字数15-25字
6. 情感增强: 能引起共鸣,激发情绪(感动/激励/共鸣)

请直接输出完善后的文章内容,格式如下:

---
标题: [文章标题]

[完善后的正文内容]

---

注意:
- 保留草稿的核心思想,不要偏离原意
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 多用案例和数据说话
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
"""

        try:
            # 使用Anthropic兼容接口
            print(f"[DEBUG] Calling AI API with model=glm-4-flash, max_tokens=4000")
            print(f"[DEBUG] Draft content length: {len(draft_content)} chars")

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

    def generate_article_images(self, theme, article_content, image_style="realistic"):
        """根据文章主题和内容生成3张配图，支持多模型降级"""

        import urllib.parse
        import requests
        from io import BytesIO

        # 清理主题中的 emoji 和特殊字符
        clean_theme = re.sub(r'[^\u4e00-\u9fff\w\s\-.,]', '', theme)
        clean_theme = clean_theme.strip()[:30]  # 限制长度

        print(f"\n[INFO] Generating images for theme: {clean_theme}")
        print(f"[INFO] Image style: {image_style}")

        # 根据文章内容提取关键词生成配图提示词
        image_prompts = self._generate_contextual_prompts(clean_theme, article_content, image_style)
        generated_images = []

        # 定义图片生成模型优先级（按顺序尝试）
        image_models = [
            # Gemini 系列（高质量）
            {"model": "gemini-3-pro-image-2k", "name": "Gemini 3 Pro 2K", "type": "antigravity"},
            {"model": "gemini-2-flash-image", "name": "Gemini 2 Flash", "type": "antigravity"},
            # Flux 系列（高质量）
            {"model": "flux-1.1-pro", "name": "Flux 1.1 Pro", "type": "antigravity"},
            {"model": "flux-schnell", "name": "Flux Schnell", "type": "antigravity"},
            # Stable Diffusion 系列
            {"model": "sd-3", "name": "SD 3", "type": "antigravity"},
            {"model": "sdxl-turbo", "name": "SDXL Turbo", "type": "antigravity"},
            # DALL-E 系列
            {"model": "dall-e-3", "name": "DALL-E 3", "type": "antigravity"},
        ]

        # 找一个可用的模型
        available_model = None
        print(f"[INFO] Checking available image models...")

        for model_info in image_models:
            try:
                # 快速测试模型是否可用
                test_response = self.image_client.images.generate(
                    model=model_info["model"],
                    prompt="test",
                    size="1024x1024",
                    n=1,
                )
                available_model = model_info
                print(f"[INFO] Using model: {model_info['name']} ({model_info['model']})")
                break
            except Exception as e:
                error_str = str(e)
                if "404" in error_str or "NOT_FOUND" in error_str:
                    print(f"[DEBUG] {model_info['name']}: not available (404)")
                elif "429" in error_str or "quota" in error_str.lower():
                    print(f"[DEBUG] {model_info['name']}: quota exceeded")
                else:
                    print(f"[DEBUG] {model_info['name']}: {str(e)[:60]}")

        for i, (img_prompt, img_desc) in enumerate(image_prompts, 1):
            print(f"[IMAGE {i}] {img_desc}...")

            image_generated = False

            # 优先使用 anti-gravity 的可用模型
            if available_model:
                try:
                    response = self.image_client.images.generate(
                        model=available_model["model"],
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
                            print(f"    [OK] {filename} ({available_model['name']})")
                            image_generated = True

                except Exception as e:
                    print(f"    [WARN] {available_model['name']} failed: {str(e)[:60]}")

            # 如果 anti-gravity 模型失败，尝试 Seedream (火山引擎)
            if not image_generated and self.volcano_client:
                try:
                    print(f"    [FALLBACK] Trying Seedream (Volcano)...")
                    response = self.volcano_client.images.generate(
                        model="doubao-seedream-4-5-251128",
                        prompt=img_prompt,
                        size="2K",  # Seedream使用2K分辨率
                        response_format="url",  # 必须指定返回URL格式
                        extra_body={
                            "watermark": False,  # 不启用水印
                        },
                    )

                    if hasattr(response, 'data') and len(response.data) > 0:
                        image_url = response.data[0].url

                        # 从URL下载图片
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
                            print(f"    [OK] {filename} (Seedream)")
                            image_generated = True
                        else:
                            print(f"    [WARN] Seedream download failed: HTTP {img_response.status_code}")

                except Exception as e:
                    print(f"    [WARN] Seedream failed: {str(e)[:60]}")

            # 如果 Seedream 也失败，使用 Pollinations.ai
            if not image_generated:
                print(f"    [FALLBACK] Trying Pollinations.ai...")
                try:
                    # 从内容中提取简单主题
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

    def _generate_contextual_prompts(self, theme, content, style):
        """使用AI大模型根据文章内容智能生成上下文相关的图片提示词"""

        # 风格映射
        style_desc = {
            "realistic": "realistic photography, high quality, professional lighting",
            "artistic": "artistic style, creative, elegant composition",
            "cartoon": "cartoon illustration, colorful, friendly style",
            "technical": "technical diagram, flowchart, architecture diagram, clean infographic style",
            "auto": "professional quality visualization"
        }.get(style, "realistic photography, high quality")

        # 使用AI生成与内容相关的配图提示词
        ai_prompt = f"""请根据以下文章内容，为3张配图生成英文提示词(prompt)。

文章主题: {theme}

文章内容摘要（前1500字）:
{content[:1500]}

配图风格要求: {style_desc}

请生成3个配图的英文提示词，要求：
1. 第1张图：概括文章核心概念或主题的场景图
2. 第2张图：展示文章中提到的关键流程、架构或细节
3. 第3张图：展示实际应用场景或用户体验

每个提示词要求：
- 使用英文，简洁明了（50词以内）
- 包含具体的视觉元素描述
- 符合指定的配图风格
- 与文章段落内容紧密相关

请直接输出3行，每行一个提示词，格式如下：
1. [第1张图的英文提示词]
2. [第2张图的英文提示词]
3. [第3张图的英文提示词]
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

            # 确保有3个提示词
            if len(prompts) < 3:
                # 补充默认提示词
                default_prompts = [
                    (f"{theme} main concept visualization, {style_desc}", "scene_main"),
                    (f"{theme} detailed process flow, {style_desc}", "scene_detail"),
                    (f"{theme} application scenario, {style_desc}", "scene_lifestyle"),
                ]
                while len(prompts) < 3:
                    prompts.append(default_prompts[len(prompts)])

            return prompts[:3]

        except Exception as e:
            print(f"[WARN] AI prompt generation failed: {e}, using fallback")
            # 降级方案：基于关键词的简单提示词
            return [
                (f"{theme} concept overview, {style_desc}", "scene_main"),
                (f"{theme} detailed view, {style_desc}", "scene_detail"),
                (f"{theme} application scene, {style_desc}", "scene_lifestyle"),
            ]

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
