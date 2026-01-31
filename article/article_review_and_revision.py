# -*- coding: utf-8 -*-
"""
让AI大模型点评冬日饮茶文章,提出修改建议,并生成修改版
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# 读取原文
with open('冬日围炉_饮茶养生.md', 'r', encoding='utf-8') as f:
    original_article = f.read()


def review_article():
    """让AI点评文章"""

    review_prompt = f"""
请你作为一位资深的文学编辑和今日头条内容专家,对以下这篇关于"冬季饮茶养生"的文章进行专业点评。

## 原文内容:

{original_article}

## 点评要求:

1. **优点分析**: 找出文章的亮点(至少3点)
2. **问题指出**: 指出需要改进的地方(至少3点)
3. **具体建议**: 提供可执行的修改建议
4. **今日头条适配度**: 从爆款文章角度评估

请从以下维度点评:
- 标题吸引力
- 语言风格(汪曾祺风格体现)
- 内容实用性
- 文化深度
- 读者互动性
- 情感共鸣度

请给出详细的、专业的点评意见。
"""

    return review_prompt


def create_revision_prompt(review_feedback):
    """创建修改提示词"""

    revision_prompt = f"""
基于以下专业点评意见,请对原文进行修改优化。

## 原文:

{original_article}

## 专业点评意见:

{review_feedback}

## 修改要求:

1. 保持汪曾祺式的简练、亲切风格
2. 增强标题吸引力(参考今日头条爆款文章特点)
3. 提升实用性(增加具体操作建议)
4. 加深文化内涵(引用更多经典)
5. 增强读者互动性
6. 优化文章结构,使之更符合新媒体阅读习惯

请输出修改后的完整文章,要求:
- 字数: 1500-1800字
- 保持原有的自然流畅风格
- 避免"机器味"
- 图文搭配位置标注清晰
"""

    return revision_prompt


def call_zhipu_for_review():
    """调用智谱AI进行点评"""

    try:
        from zhipuai import ZhipuAI

        # 从.env读取API key
        import os
        from dotenv import load_dotenv

        load_dotenv('.env')
        api_key = os.getenv('ZHIPU_API_KEY')

        if not api_key:
            return None

        client = ZhipuAI(api_key=api_key)

        print("\n[1/3] 正在请求智谱AI进行专业点评...")

        review_prompt = review_article()

        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "system", "content": "你是一位资深的文学编辑和今日头条内容专家,擅长点评散文类文章。"},
                {"role": "user", "content": review_prompt}
            ],
            temperature=0.7,
        )

        review_feedback = response.choices[0].message.content

        # 保存点评
        with open('文章专业点评意见.md', 'w', encoding='utf-8') as f:
            f.write(review_feedback)

        print("    [成功] 点评完成,已保存到: 文章专业点评意见.md")

        return review_feedback

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")
        return None


def call_zhipu_for_revision(review_feedback):
    """调用智谱AI进行修改"""

    try:
        from zhipuai import ZhipuAI

        import os
        from dotenv import load_dotenv

        load_dotenv('.env')
        api_key = os.getenv('ZHIPU_API_KEY')

        if not api_key:
            return None

        client = ZhipuAI(api_key=api_key)

        print("\n[2/3] 正在请求智谱AI进行文章修改...")

        revision_prompt = create_revision_prompt(review_feedback)

        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "system", "content": "你是一位擅长写作的作家,精通汪曾祺式散文风格,同时熟悉今日头条爆款文章的写作技巧。"},
                {"role": "user", "content": revision_prompt}
            ],
            temperature=0.8,
        )

        revised_article = response.choices[0].message.content

        # 保存修改版
        with open('冬日围炉_饮茶养生_修改版.md', 'w', encoding='utf-8') as f:
            f.write(revised_article)

        print("    [成功] 修改完成,已保存到: 冬日围炉_饮茶养生_修改版.md")

        return revised_article

    except Exception as e:
        print(f"    [失败] {str(e)[:100]}")
        return None


def create_comparison_web(original, revised, review):
    """创建对比网页"""

    print("\n[3/3] 正在生成对比网页...")

    # 预先计算统计数据
    original_paragraphs = original.count('\n\n')
    revised_paragraphs = revised.count('\n\n')

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>冬日饮茶文章 - 两版对比展示</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', 'Microsoft YaHei', serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.8;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}

        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}

        .tabs {{
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }}

        .tab {{
            padding: 15px 40px;
            cursor: pointer;
            background: #f5f5f5;
            margin: 0 5px;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s;
            font-size: 1.1em;
        }}

        .tab:hover {{
            background: #e0e0e0;
        }}

        .tab.active {{
            background: #667eea;
            color: white;
        }}

        .tab-content {{
            display: none;
        }}

        .tab-content.active {{
            display: block;
        }}

        .review-section {{
            background: #fff3e0;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #ff9800;
        }}

        .review-section h2 {{
            color: #e65100;
            margin-bottom: 20px;
        }}

        .comparison-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }}

        .version-box {{
            background: #fafafa;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
        }}

        .version-box h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .version-box h3 {{
            color: #333;
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        .version-box p {{
            margin-bottom: 15px;
            text-indent: 2em;
            line-height: 2;
            text-align: justify;
        }}

        .original-title {{
            background: linear-gradient(120deg, #ffc107 0%, #ffed4e 100%);
            padding: 3px 10px;
            border-radius: 5px;
        }}

        .revised-title {{
            background: linear-gradient(120deg, #4caf50 0%, #81c784 100%);
            color: white;
            padding: 3px 10px;
            border-radius: 5px;
        }}

        .highlight {{
            background: #ffeb3b;
            padding: 2px 6px;
            border-radius: 3px;
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}

        @media (max-width: 1200px) {{
            .comparison-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 冬日饮茶养生文章 - AI点评与修改对比</h1>

        <div class="tabs">
            <div class="tab active" onclick="switchTab('review')">📋 专业点评</div>
            <div class="tab" onclick="switchTab('compare')">🔄 两版对比</div>
            <div class="tab" onclick="switchTab('stats')">📊 数据统计</div>
        </div>

        <div id="review" class="tab-content active">
            <div class="review-section">
                <h2>🔍 AI专业编辑点评意见</h2>
                <div style="color: #333; line-height: 2; white-space: pre-wrap;">{review}</div>
            </div>
        </div>

        <div id="compare" class="tab-content">
            <div class="comparison-container">
                <div class="version-box">
                    <h2><span class="original-title">📄 原版</span></h2>
                    <div style="color: #333; line-height: 2; white-space: pre-wrap;">{original}</div>
                </div>

                <div class="version-box">
                    <h2><span class="revised-title">✨ 修改版</span></h2>
                    <div style="color: #333; line-height: 2; white-space: pre-wrap;">{revised}</div>
                </div>
            </div>
        </div>

        <div id="stats" class="tab-content">
            <div class="comparison-container">
                <div class="version-box">
                    <h2>📊 原版数据</h2>
                    <p><strong>字数:</strong> {len(original)} 字</p>
                    <p><strong>段落数:</strong> {original_paragraphs} 段</p>
                    <p><strong>标题:</strong> 冬日围炉,一杯茶的时间</p>
                    <p><strong>风格:</strong> 汪曾祺式散文</p>
                    <p><strong>配图:</strong> 3张</p>
                </div>

                <div class="version-box">
                    <h2>📊 修改版数据</h2>
                    <p><strong>字数:</strong> {len(revised)} 字</p>
                    <p><strong>段落数:</strong> {revised_paragraphs} 段</p>
                    <p><strong>标题:</strong> (根据AI修改调整)</p>
                    <p><strong>优化:</strong> 增强互动性和实用性</p>
                    <p><strong>配图:</strong> 3张(保持不变)</p>
                </div>
            </div>
        </div>

        <div class="footer">
            <p><strong>点评模型:</strong> 智谱AI GLM-4.6 | <strong>修改模型:</strong> 智谱AI GLM-4.6</p>
            <p><strong>生成时间:</strong> 2026年1月27日</p>
            <hr style="margin: 20px 0;">
            <p style="font-size: 0.9em; color: #999;">
                本对比展示了AI辅助内容创作的过程: 专业点评 → 针对性修改 → 两版对比
            </p>
        </div>
    </div>

    <script>
        function switchTab(tabName) {{
            // 隐藏所有内容
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});

            // 移除所有tab的active状态
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});

            // 显示选中的内容
            document.getElementById(tabName).classList.add('active');

            // 激活对应的tab
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""

    # 保存对比网页
    with open('冬日饮茶_两版对比.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("    [成功] 对比网页已生成: 冬日饮茶_两版对比.html")


def main():
    """主流程"""

    print("="*80)
    print("AI辅助文章点评与修改")
    print("="*80)

    # 1. AI点评
    review_feedback = call_zhipu_for_review()

    if not review_feedback:
        print("\n[错误] 无法获取AI点评,请检查ZHIPU_API_KEY配置")
        return

    # 2. AI修改
    revised_article = call_zhipu_for_revision(review_feedback)

    if not revised_article:
        print("\n[错误] 无法获取AI修改版本")
        return

    # 3. 生成对比网页
    create_comparison_web(original_article, revised_article, review_feedback)

    print("\n"+"="*80)
    print("✅ 全部完成!")
    print("="*80)
    print("\n生成的文件:")
    print("  1. 文章专业点评意见.md - AI专业点评")
    print("  2. 冬日围炉_饮茶养生_修改版.md - AI修改版文章")
    print("  3. 冬日饮茶_两版对比.html - 对比展示网页")


if __name__ == "__main__":
    main()
