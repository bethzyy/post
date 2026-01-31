# -*- coding: utf-8 -*-
"""
等待服务器可用并自动开始生成
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import get_antigravity_client
import base64
from PIL import Image
import io

def check_server_status():
    """检查服务器是否可用"""

    client = get_antigravity_client()

    try:
        response = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt="test",
            size="1024x1024",
            n=1,
        )

        return True, "服务器可用"

    except Exception as e:
        error_msg = str(e)

        if "503" in error_msg or "MODEL_CAPACITY_EXHAUSTED" in error_msg:
            return False, "服务器容量耗尽，等待中..."
        elif "429" in error_msg:
            return False, "配额限制，等待中..."
        else:
            return False, f"其他错误: {error_msg[:100]}"

def main():
    """主函数"""

    print("="*80)
    print("等待Gemini服务器可用...")
    print("="*80)

    attempt = 0
    max_attempts = 120  # 最多等待2小时

    while attempt < max_attempts:
        attempt += 1

        print(f"\n尝试 #{attempt}/{max_attempts} ", end="")

        available, message = check_server_status()

        if available:
            print(f"\n✓ {message}")
            print("\n服务器已就绪！开始生成图片...")
            print("="*80)

            # 启动生成脚本
            import subprocess
            subprocess.Popen([sys.executable, "bird_painting_self_correction.py"])

            return

        else:
            print(f"- {message}")

            if attempt < max_attempts:
                print("等待60秒后重试...")
                time.sleep(60)

    print("\n达到最大尝试次数，服务器仍不可用")
    print("请稍后手动运行: python bird_painting_self_correction.py")

if __name__ == "__main__":
    main()
