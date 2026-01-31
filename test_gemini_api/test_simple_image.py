# -*- coding: utf-8 -*-
"""
简单的Gemini API测试程序
独立目录，用于测试API可用性
"""

import sys
import os
from pathlib import Path

# 添加父目录到路径以导入config
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from config import get_antigravity_client
import base64
from PIL import Image
import io

def test_simple_generation():
    """测试简单的图片生成"""

    print("="*80)
    print("Gemini API 简单测试")
    print("="*80)

    client = get_antigravity_client()

    # 简单的测试prompt
    prompt = "A simple red circle on white background, minimal design, 1024x1024"

    print(f"\n测试Prompt: {prompt}")
    print("\n正在调用API...")

    try:
        response = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )

        if hasattr(response, 'data') and len(response.data) > 0:
            img_data = response.data[0]

            if hasattr(img_data, 'b64_json') and img_data.b64_json:
                img_bytes = base64.b64decode(img_data.b64_json)
                img = Image.open(io.BytesIO(img_bytes))

                # 保存到测试目录
                filename = Path(__file__).parent / "test_output_red_circle.png"
                img.save(filename, 'PNG', quality=95)

                print(f"\n[成功] 图片已保存: {filename}")
                print(f"  尺寸: {img.size}")
                print(f"  大小: {len(img_bytes)} bytes")

                return True

        print("\n[失败] 未返回图片数据")
        return False

    except Exception as e:
        error_msg = str(e)

        print(f"\n[错误] API调用失败")

        # 解析错误类型
        if "429" in error_msg:
            print(f"  类型: 配额限制 (429 Too Many Requests)")
            print(f"  说明: 已达到速率限制，需要等待")
        elif "503" in error_msg or "MODEL_CAPACITY_EXHAUSTED" in error_msg:
            print(f"  类型: 服务器容量耗尽 (503 Service Unavailable)")
            print(f"  说明: 服务器过载，请稍后重试")
        elif "401" in error_msg:
            print(f"  类型: 认证失败 (401 Unauthorized)")
            print(f"  说明: API key无效或过期")
        else:
            print(f"  类型: 其他错误")
            print(f"  详情: {error_msg[:200]}")

        return False

def test_server_status():
    """测试服务器状态（最小化调用）"""

    print("\n" + "="*80)
    print("服务器状态检测")
    print("="*80)

    client = get_antigravity_client()

    print("\n发送最小化测试请求...")

    try:
        # 使用最小的参数测试
        response = client.images.generate(
            model="gemini-3-pro-image-4k",
            prompt="test",  # 最短prompt
            size="512x512",  # 最小尺寸
            n=1,
        )

        print("\n[状态] 服务器可用 ✓")
        print("[建议] 可以开始生成图片")

        return True

    except Exception as e:
        error_msg = str(e)

        if "503" in error_msg:
            print("\n[状态] 服务器繁忙 (503)")
            print("[建议] 等待几分钟后重试")

            # 尝试提取等待时间
            if "quotaResetDelay" in error_msg or "retryDelay" in error_msg:
                print("[提示] 错误中包含重试时间信息")

        elif "429" in error_msg:
            print("\n[状态] 配额限制 (429)")
            print("[建议] 等待配额重置（通常1小时）")

        else:
            print(f"\n[状态] 其他错误")
            print(f"[详情] {error_msg[:200]}")

        return False

def main():
    """主函数"""

    print("\n" + "="*80)
    print("Gemini API 测试程序")
    print("独立测试目录: test_gemini_api")
    print("="*80)

    # 步骤1：测试服务器状态
    server_ok = test_server_status()

    # 步骤2：如果服务器可用，测试图片生成
    if server_ok:
        print("\n" + "="*80)
        print("服务器可用，开始图片生成测试...")
        print("="*80)

        test_simple_generation()

    print("\n" + "="*80)
    print("测试完成")
    print("="*80)

if __name__ == "__main__":
    main()
