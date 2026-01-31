# -*- coding: utf-8 -*-
"""
测试ZhipuAI Anthropic兼容API
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config import get_zhipu_anthropic_client, Config


def test_zhipu_anthropic_api():
    """测试ZhipuAI Anthropic兼容API"""

    print("="*80)
    print("测试ZhipuAI Anthropic兼容API")
    print("="*80)

    # 显示配置
    print(f"\nAPI Key: {Config.ZHIPU_API_KEY[:20]}...")
    print(f"Base URL: {Config.ZHIPU_ANTHROPIC_BASE_URL}")

    # 获取客户端
    print("\n[步骤1] 获取Anthropic兼容客户端...")
    client = get_zhipu_anthropic_client()

    if not client:
        print("[错误] 无法获取客户端")
        return False

    print("[成功] 客户端创建成功")

    # 测试API调用
    print("\n[步骤2] 测试API调用...")
    print("模型: glm-4.6")
    print("提示词: 简单测试")

    try:
        response = client.messages.create(
            model="glm-4.6",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "请用一句话介绍2026年AI领域最重要的趋势。"
                }
            ]
        )

        print("\n[成功] API调用成功!")
        print(f"\n响应内容:")
        print("-"*80)
        print(response.content[0].text)
        print("-"*80)

        print(f"\n使用Token数: {response.usage.input_tokens + response.usage.output_tokens}")
        print(f"输入Token: {response.usage.input_tokens}")
        print(f"输出Token: {response.usage.output_tokens}")

        return True

    except Exception as e:
        print(f"\n[错误] API调用失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")

        # 检查是否是认证错误
        if "401" in str(e) or "authentication" in str(e).lower():
            print("\n提示: 可能是API Key不正确")
        elif "429" in str(e) or "quota" in str(e).lower():
            print("\n提示: 可能是配额问题")
        elif "connection" in str(e).lower() or "network" in str(e).lower():
            print("\n提示: 可能是网络连接问题")

        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ZhipuAI Anthropic兼容API测试")
    print("="*80)

    success = test_zhipu_anthropic_api()

    print("\n" + "="*80)
    if success:
        print("✅ 测试成功!")
    else:
        print("❌ 测试失败!")
    print("="*80)
