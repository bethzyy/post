# -*- coding: utf-8 -*-
"""
视频生成API测试程序
测试多个免费视频生成服务的可用性
"""

import sys
import os
from pathlib import Path
import requests
import time

# 添加父目录到路径
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))


def test_pollinations_video():
    """测试Pollinations.ai的视频生成功能"""

    print("\n" + "="*80)
    print("测试 1: Pollinations.ai 视频生成")
    print("="*80)

    # Pollinations视频API（基于Stable Video Diffusion）
    prompt = "A red circle on white background, minimal design"
    encoded_prompt = requests.utils.quote(prompt)

    # Pollinations视频端点
    video_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=123&nologo=true"

    print(f"\n提示词: {prompt}")
    print(f"\n正在请求视频生成...")
    print(f"URL: {video_url[:100]}...")

    try:
        # 尝试获取视频
        response = requests.get(video_url, timeout=60)

        if response.status_code == 200:
            # 检查是否是视频文件
            content_type = response.headers.get('content-type', '')
            print(f"\n[成功] 响应状态: {response.status_code}")
            print(f"[信息] Content-Type: {content_type}")

            # 保存文件
            filename = Path(__file__).parent / "test_pollinations_video.mp4"
            with open(filename, 'wb') as f:
                f.write(response.content)

            print(f"[成功] 视频已保存: {filename}")
            print(f"  大小: {len(response.content)} bytes")

            # 判断实际文件类型
            if b'ftypmp42' in response.content[:100] or b'ftypisom' in response.content[:100]:
                print(f"[确认] 这是MP4视频文件")
                return True
            elif b'PNG' in response.content[:100]:
                print(f"[注意] 返回的是PNG图片，不是视频")
                print(f"[说明] Pollinations当前可能只支持图片生成")
                return False
            else:
                print(f"[未知] 文件类型无法确定")
                return False

        else:
            print(f"\n[失败] HTTP状态码: {response.status_code}")
            print(f"[详情] {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print(f"\n[超时] 请求超过60秒")
        print(f"[说明] 视频生成可能需要更长时间")
        return False

    except Exception as e:
        print(f"\n[错误] {str(e)[:200]}")
        return False


def test_stability_ai():
    """测试Stability AI的视频生成API"""

    print("\n" + "="*80)
    print("测试 2: Stability AI (Stable Video Diffusion)")
    print("="*80)

    print("\n[信息] Stability AI提供Stable Video Diffusion模型")
    print("[说明] 需要API key，付费服务")
    print("[状态] 跳过测试（需要付费API key）")

    return False


def test_runway_ml():
    """测试RunwayML的视频生成API"""

    print("\n" + "="*80)
    print("测试 3: RunwayML Gen-2/Gen-3")
    print("="*80)

    print("\n[信息] RunwayML提供Gen-2和Gen-3视频生成模型")
    print("[说明] 需要API key，付费服务")
    print("[状态] 跳过测试（需要付费API key）")

    return False


def test_pika_labs():
    """测试Pika Labs的视频生成API"""

    print("\n" + "="*80)
    print("测试 4: Pika Labs")
    print("="*80)

    print("\n[信息] Pika Labs提供高质量视频生成")
    print("[说明] 主要通过Discord bot和Web界面，API访问有限")
    print("[状态] 跳过测试（无公开API）")

    return False


def summary_report(results):
    """生成测试总结报告"""

    print("\n" + "="*80)
    print("视频生成API测试总结")
    print("="*80)

    total = len(results)
    success = sum(1 for r in results.values() if r)

    print(f"\n测试服务数: {total}")
    print(f"成功可用: {success}")
    print(f"不可用/跳过: {total - success}")

    print("\n详细结果:")
    for service, result in results.items():
        status = "[可用]" if result else "[不可用]"
        print(f"  {status} {service}")

    if success == 0:
        print("\n[结论] 目前没有找到可用的免费视频生成API")
        print("\n推荐方案:")
        print("  1. 使用付费API:")
        print("     - Stability AI (Stable Video Diffusion)")
        print("     - RunwayML (Gen-2/Gen-3)")
        print("     - Pika Labs")
        print("\n  2. 开源方案（需要自己部署）:")
        print("     - Stable Video Diffusion (SVD)")
        print("     - ModelScope (阿里的视频生成模型)")
        print("     - AnimateDiff")
        print("\n  3. 在线工具（非API）:")
        print("     - Pika Labs (Web界面)")
        print("     - RunwayML (Web界面)")
        print("     - Kaiber (Web界面)")


def main():
    """主函数"""

    print("\n" + "="*80)
    print("视频生成API测试程序")
    print("独立测试目录: test_video_api")
    print("="*80)

    results = {}

    # 测试各个服务
    results["Pollinations.ai"] = test_pollinations_video()
    time.sleep(2)

    results["Stability AI"] = test_stability_ai()
    time.sleep(1)

    results["RunwayML"] = test_runway_ml()
    time.sleep(1)

    results["Pika Labs"] = test_pika_labs()

    # 生成总结报告
    summary_report(results)

    print("\n" + "="*80)
    print("测试完成")
    print("="*80)


if __name__ == "__main__":
    main()
