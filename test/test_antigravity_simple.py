# -*- coding: utf-8 -*-
"""
快速测试anti-gravity服务连接
"""

import sys
from pathlib import Path

# 导入配置
sys.path.insert(0, str(Path(__file__).parent))
from config import Config, get_antigravity_client

print("正在连接anti-gravity服务...")
print(f"Base URL: {Config.ANTIGRAVITY_BASE_URL}")

try:
    client = get_antigravity_client()
    if not client:
        print("无法创建客户端")
        sys.exit(1)

    print("\n正在测试简单对话...")
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": "你好，请用一句话介绍你自己"}],
        max_tokens=100
    )

    print(f"\n回答: {response.choices[0].message.content}")
    print("\n[成功] anti-gravity服务连接正常！")

    # 生成图像提示词
    print("\n正在生成腊八节图像提示词...")
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{
            "role": "user",
            "content": """
请为腊八节生成一个详细的英文图像提示词，用于AI绘画。

画面内容：
- 中心：青花瓷碗装腊八粥
- 左侧：竹子
- 右上角：梅花
- 背景：水墨效果
- 顶部：书法"腊八节"
- 右下角：红色印章

请直接返回英文提示词，不要太长。
            """
        }],
        max_tokens=300
    )

    prompt = response.choices[0].message.content
    print(f"\n生成的提示词:\n{'='*80}\n{prompt}\n{'='*80}")

    # 保存提示词
    with open("腊八节_anti_gravity提示词.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    print("\n提示词已保存到: 腊八节_anti_gravity提示词.txt")

except Exception as e:
    print(f"\n[错误] {e}")
    print("\n请确保:")
    print("1. anti-gravity服务已启动")
    print("2. 端口8045正在监听")
    print("3. API Key正确")
