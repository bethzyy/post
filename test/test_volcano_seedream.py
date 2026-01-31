# -*- coding: utf-8 -*-
"""
测试Volcano/Seedream豆包图灵图像生成模型
为中国小年画一张中国风的水粉画
"""

import sys
import os
from pathlib import Path
import requests
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import get_volcano_client


def test_seedream_generation():
    """测试Seedream图像生成"""

    print("="*80)
    print("Volcano/Seedream 豆包图灵图像生成测试")
    print("="*80)

    # 获取客户端
    client = get_volcano_client()

    if not client:
        print("\n[错误] 无法获取Volcano客户端")
        print("[提示] 请检查.env文件中的VOLCANO_API_KEY是否正确设置")
        return False

    print("\n[信息] 模型: doubao-seedream-4-5-251128")
    print("[信息] Base URL: https://ark.cn-beijing.volces.com/api/v3")

    # 为中国小年创作中国风水粉画
    prompt = """
中国小年节日，传统中国风水粉画。

画面内容：
- 一位穿着传统汉服的小女孩，手持糖瓜，笑容甜美
- 背景是古朴的中国建筑，红灯笼高挂，雪花飘落
- 桌上摆放着祭灶糖瓜、饺子等传统食物
- 整体色调温馨，红色为主，营造节日氛围
- 水粉质感，笔触柔和，富有中国年画特色
- 1024x1024分辨率

艺术风格：
- 中国传统年画风格
- 水粉画技法
- 色彩鲜艳但不俗气
- 构图饱满，寓意吉祥
"""

    print(f"\n提示词:\n{prompt}")

    try:
        print("\n[生成] 正在调用API...")
        print("[提示] 这可能需要几十秒时间...")

        # 调用API
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt.strip(),
            size="2K",  # 使用2K分辨率
            response_format="url",
            extra_body={
                "watermark": True,  # 启用水印
            },
        )

        # 检查响应
        if hasattr(response, 'data') and len(response.data) > 0:
            image_url = response.data[0].url

            print(f"\n[成功] 图片生成成功！")
            print(f"[URL] {image_url}")

            # 下载图片
            print(f"\n[下载] 正在下载图片...")
            img_response = requests.get(image_url, timeout=30)

            if img_response.status_code == 200:
                # 保存图片
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = Path(__file__).parent / f"小年中国风水粉画_Seedream_{timestamp}.jpg"

                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / (1024 * 1024)  # MB

                print(f"[保存] {filename}")
                print(f"[大小] {file_size:.2f} MB")

                # 显示图片信息
                print(f"\n[信息] 图片详情:")
                print(f"  模型: doubao-seedream-4-5-251128")
                print(f"  分辨率: 2K")
                print(f"  水印: 已启用")
                print(f"  主题: 中国小年水粉画")

                return True
            else:
                print(f"\n[错误] 下载图片失败")
                print(f"[状态码] {img_response.status_code}")
                return False
        else:
            print(f"\n[错误] 未返回图片数据")
            return False

    except Exception as e:
        error_msg = str(e)

        print(f"\n[错误] API调用失败")
        print(f"[详情] {error_msg[:500]}")

        # 错误分类
        if "401" in error_msg or "Unauthorized" in error_msg:
            print(f"\n[类型] 认证失败 (401)")
            print(f"[说明] API Key可能无效或已过期")
            print(f"[建议] 请检查.env文件中的VOLCANO_API_KEY")

        elif "429" in error_msg or "quota" in error_msg.lower():
            print(f"\n[类型] 配额限制 (429)")
            print(f"[说明] 已达到速率限制或配额耗尽")
            print(f"[建议] 请稍后重试")

        elif "500" in error_msg or "503" in error_msg:
            print(f"\n[类型] 服务器错误 (500/503)")
            print(f"[说明] 服务器暂时不可用")
            print(f"[建议] 请稍后重试")

        else:
            print(f"\n[类型] 其他错误")
            print(f"[建议] 检查网络连接和API配置")

        return False


def main():
    """主函数"""

    print("\n" + "="*80)
    print("Volcano/Seedream 图像生成测试程序")
    print("主题: 中国小年传统水粉画")
    print("="*80)

    # 运行测试
    success = test_seedream_generation()

    print("\n" + "="*80)
    if success:
        print("测试成功完成！")
    else:
        print("测试失败，请查看上面的错误信息")
    print("="*80)


if __name__ == "__main__":
    main()
