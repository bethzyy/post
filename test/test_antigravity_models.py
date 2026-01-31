# -*- coding: utf-8 -*-
"""
测试anti-gravity支持的模型列表
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import get_antigravity_client


def test_available_models():
    """测试anti-gravity支持的模型"""

    client = get_antigravity_client()
    if not client:
        print("[错误] 无法获取anti-gravity客户端")
        return

    # 常见的模型名称列表
    test_models = [
        # Gemini系列
        "gemini-2.0-flash-exp",
        "gemini-2.5-pro",
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",

        # GPT系列
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo",

        # Claude系列
        "claude-sonnet-4-5-20250514",
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",

        # GLM系列（可能通过anti-gravity）
        "glm-4.6",
        "glm-4",
    ]

    print("="*80)
    print("测试anti-gravity支持的模型")
    print("="*80)

    for model in test_models:
        try:
            print(f"\n测试模型: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": "你好"
                    }
                ],
                max_tokens=10
            )
            print(f"[OK] {model} - 可用")
            print(f"   响应: {response.choices[0].message.content[:50]}")
        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "NOT_FOUND" in error_str:
                print(f"[X] {model} - 不可用 (404)")
            elif "429" in error_str:
                print(f"[!] {model} - 可用但配额已用尽 (429)")
            else:
                print(f"[X] {model} - 错误: {error_str[:100]}")


if __name__ == "__main__":
    test_available_models()
