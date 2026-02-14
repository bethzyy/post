# -*- coding: utf-8 -*-
"""
调试文章生成问题
"""
import sys
from pathlib import Path

# 设置标准输出编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import get_zhipuai_client

def test_draft_improvement():
    """测试草稿完善功能"""
    print("="*80)
    print("测试草稿完善功能")
    print("="*80)

    # 读取草稿内容
    draft_file = Path(__file__).parent / "article" / "draft2.txt"
    with open(draft_file, 'r', encoding='utf-8') as f:
        draft_content = f.read()

    print(f"\n原始草稿:\n{draft_content}\n")
    print("-"*80)

    # 初始化客户端
    client = get_zhipuai_client()

    # 构建prompt
    target_length = 1500
    prompt = f"""请将以下用户草稿完善为一篇高质量的今日头条文章。

## 用户草稿:

{draft_content}

## 【重要】原句保留要求:
1. **必须保留原草稿中的大部分句子**，尽量引用原文
2. 只在必要时调整句子的顺序和连接
3. 在原句基础上补充细节，而不是替换原句
4. 原草稿中的关键句子和表达要尽量完整保留

## 完善要求:
1. 字数: {target_length}字左右
2. 风格: 通俗易懂,接地气,有感染力
3. 结构要求（重要）：
   - **逻辑清晰**：文章要有明确的逻辑主线，层层递进，论点或观点要有逻辑关系
   - **流畅完整**：段落之间过渡自然，不要生硬跳跃，前后呼应
   - **结构完整**：引人入胜的开头 + 3-5个要点（有逻辑递进）+ 感人或启发的结尾 + 互动号召
4. 内容优化（在保留原句的基础上）:
   - 在原句之间添加过渡和连接，确保逻辑连贯
   - 为原句补充具体案例和数据
   - 在原句基础上增加细节描述
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
- 【最重要】尽量保留原草稿的句子，在此基础上扩展和完善
- **确保文章逻辑清晰、流畅完整、前后呼应**
- 保留草稿的核心思想,不要偏离原意
- 标题要吸引点击,包含数字或疑问
- 内容要有真实感,避免空话套话
- 多用案例和数据说话
- 适当使用emoji增加可读性
- 结尾要有情感共鸣或行动号召
"""

    print("\n[发送请求到GLM-4-Flash]...")
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=4000,
            top_p=0.9
        )

        # 获取AI响应
        content = response.choices[0].message.content

        print("\n" + "="*80)
        print("AI原始响应:")
        print("="*80)
        print(content)
        print("\n" + "="*80)

        # 解析响应
        lines = content.split('\n')
        title = ""
        body_lines = []
        found_title = False
        found_separator = False

        for i, line in enumerate(lines):
            stripped_line = line.strip()

            if not stripped_line:
                continue

            if stripped_line.startswith("标题:"):
                title = stripped_line.replace("标题:", "").strip()
                found_title = True
                print(f"[找到标题] 第{i+1}行: {title}")
                continue

            if stripped_line == "---" or stripped_line.startswith("---"):
                found_separator = True
                print(f"[找到分隔符] 第{i+1}行")
                continue

            if found_separator and found_title:
                if not body_lines:
                    print(f"[开始收集正文] 第{i+1}行")
                body_lines.append(line)

            if not found_title and i == 0 and not stripped_line.startswith("---"):
                title = stripped_line
                found_title = True
                print(f"[第一行作为标题] {title}")

        body = '\n'.join(body_lines).strip()

        print("\n" + "="*80)
        print("解析结果:")
        print("="*80)
        print(f"标题: {title}")
        print(f"正文字数: {len(body)}")
        print(f"正文预览(前200字):\n{body[:200]}...")

        # 检查是否解析失败
        if not title or title == "---":
            print("\n[警告] 标题解析失败!")
        if not body:
            print("\n[警告] 正文内容为空!")

    except Exception as e:
        print(f"\n[ERROR] 请求失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_draft_improvement()
