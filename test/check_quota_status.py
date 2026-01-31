# -*- coding: utf-8 -*-
"""
快速检查anti-gravity配额状态
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import get_antigravity_client
import re

def check_quota():
    """检查配额状态"""

    print("="*80)
    print("anti-gravity配额状态检查")
    print("="*80)

    client = get_antigravity_client()

    # 测试3个主要模型
    test_models = [
        ("Claude", "claude-sonnet-4-5-20250514"),
        ("ChatGPT", "gpt-4-turbo"),
        ("Gemini", "gemini-2.5-pro")
    ]

    for model_name, model_id in test_models:
        try:
            print(f"\n[测试] {model_name} ({model_id})")

            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )

            print(f"[OK] {model_name} - 配额可用！")
            print(f"    响应: {response.choices[0].message.content[:50]}")

        except Exception as e:
            error_str = str(e)

            if "429" in error_str or "QUOTA_EXHAUSTED" in error_str or "Resource has been exhausted" in error_str:
                print(f"[429] {model_name} - 配额已用尽")

                # 尝试提取等待时间 - 支持多种格式
                wait_seconds = None

                # 格式1: "after 2h23m33s"
                match1 = re.search(r'after\s+(\d+)h(\d+)m(\d+)s', error_str)
                if match1:
                    wait_seconds = int(match1.group(1)) * 3600 + int(match1.group(2)) * 60 + int(match1.group(3))

                # 格式2: quotaResetDelay格式
                if not wait_seconds:
                    match2 = re.search(r'quotaResetDelay["\s:]+(\d+)s', error_str)
                    if match2:
                        wait_seconds = int(match2.group(1))

                if wait_seconds:
                    wait_hours = wait_seconds / 3600
                    wait_minutes = (wait_seconds % 3600) / 60

                    print(f"    等待时间: {int(wait_hours)}小时{int(wait_minutes)}分钟 ({wait_seconds}秒)")

                    # 估算恢复时间
                    import datetime
                    recovery_time = datetime.datetime.now() + datetime.timedelta(seconds=wait_seconds)
                    print(f"    预计恢复: {recovery_time.strftime('%Y-%m-%d %H:%M:%S')}")

                else:
                    print(f"    无法从错误信息中提取等待时间")
                    print(f"    错误详情: {error_str[:300]}")

            elif "404" in error_str:
                print(f"[404] {model_name} - 模型不可用")
            else:
                print(f"[错误] {model_name} - {error_str[:100]}")

    print("\n" + "="*80)
    print("检查完成")
    print("="*80)


if __name__ == "__main__":
    check_quota()
