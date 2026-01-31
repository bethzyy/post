# -*- coding: utf-8 -*-
"""
测试Antigravity API连接
验证Claude、Gemini、ChatGPT模型是否可用
"""

import os
import sys
from pathlib import Path

# 添加父目录到path以导入requests
sys.path.insert(0, str(Path(__file__).parent))

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[错误] openai库未安装,请先安装: pip install openai")
    sys.exit(1)


def get_antigravity_config():
    """从.env文件读取Antigravity配置"""
    post_env_path = Path('../.env')
    config = {
        'enabled': False,
        'base_url': None,
        'api_key': None
    }

    # 从环境变量读取
    config['base_url'] = os.environ.get('ANTIGRAVITY_BASE_URL')
    config['api_key'] = os.environ.get('ANTIGRAVITY_API_KEY')

    # 从.env文件读取
    if post_env_path.exists() and not config['base_url']:
        with open(post_env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('ANTIGRAVITY_BASE_URL=') and not line.strip().startswith('#'):
                    config['base_url'] = line.strip().split('=')[1]
                elif line.startswith('ANTIGRAVITY_API_KEY=') and not line.strip().startswith('#'):
                    config['api_key'] = line.strip().split('=')[1]

    if config['base_url']:
        config['enabled'] = True

    return config


def test_antigravity_model(model_name, model_id, config):
    """测试单个Antigravity模型 - 使用OpenAI客户端"""
    base_url = config['base_url'].rstrip('/')
    api_key = config['api_key'] or 'dummy-key'

    print(f"\n[测试] {model_name} ({model_id})")
    print(f"  Base URL: {base_url}")
    print(f"  Endpoint: /chat/completions (OpenAI兼容接口)")

    try:
        # 使用OpenAI客户端(兼容Antigravity)
        client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

        # 调用chat completions API
        response = client.chat.completions.create(
            model=model_id,
            messages=[{
                "role": "user",
                "content": f"你好!请用一句话介绍你自己,你是{model_name}模型。"
            }],
            max_tokens=500,
            temperature=0.7
        )

        # 提取响应内容
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content
            print(f"  [成功] 响应: {content[:100]}...")
            return True
        else:
            print(f"  [失败] 未返回内容")
            return False

    except Exception as e:
        print(f"  [错误] {str(e)}")
        return False


def main():
    """测试Antigravity API"""
    print("=" * 60)
    print("Antigravity API 测试")
    print("=" * 60)

    # 加载配置
    config = get_antigravity_config()

    if not config['enabled']:
        print("[错误] Antigravity未配置")
        print("\n请在.env文件中配置:")
        print("  ANTIGRAVITY_BASE_URL=http://127.0.0.1:8045/v1")
        print("  ANTIGRAVITY_API_KEY=your-api-key")
        return

    print(f"[配置] Base URL: {config['base_url']}")
    print(f"[配置] API Key: {config['api_key'][:20]}...")

    # 测试各个模型
    models_to_test = [
        ("Claude Sonnet 4.5", "claude-sonnet-4.5"),
        ("Gemini 2.5 Pro", "gemini-2.5-pro"),
        ("GPT-OSS", "gpt-oss")
    ]

    results = {}
    for display_name, model_id in models_to_test:
        success = test_antigravity_model(display_name, model_id, config)
        results[display_name] = success

    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    for model_name, success in results.items():
        status = "[OK] 可用" if success else "[X] 不可用"
        print(f"  {model_name}: {status}")

    # 统计
    available = sum(1 for s in results.values() if s)
    total = len(results)

    print(f"\n总计: {available}/{total} 个模型可用")

    if available > 0:
        print("\n[成功] Antigravity API配置正确,可以正常使用!")
    else:
        print("\n[警告] 所有模型测试失败,请检查:")
        print("  1. Antigravity服务是否启动")
        print("  2. Base URL是否正确")
        print("  3. API Key是否有效")


if __name__ == "__main__":
    main()
