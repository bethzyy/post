# -*- coding: utf-8 -*-
"""
直接测试即梦AI(Seedream) API
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, 'C:/D/CAIE_tool/MyAIProduct/post')

from config import get_volcano_client
from pathlib import Path
import requests

def test_seedream_text_to_image():
    """测试文生图功能"""
    print("\n" + "="*80)
    print("测试1: 即梦AI文生图(Text-to-Image)")
    print("="*80)

    try:
        client = get_volcano_client()

        if not client:
            print("❌ Volcano客户端未配置")
            print("请检查 .env 文件中的 VOLCANO_API_KEY")
            return False

        print(f"✅ Volcano客户端已连接")
        print(f"✅ API地址: {client.base_url}")

        # 测试1: 文生图
        print("\n[测试1.1] 文生图 - 一只红色苹果")
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt="一只红色苹果,放在桌子上,中国风水墨画风格,高质量",
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,
            }
        )

        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"✅ 生成成功!")
            print(f"   图片URL: {image_url}")

            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                output_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_seedream_text.png"
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"✅ 已下载到: {output_path}")
                print(f"   文件大小: {len(img_response.content)} bytes")
                return True
            else:
                print(f"❌ 下载失败: HTTP {img_response.status_code}")
                return False
        else:
            print(f"❌ 返回空数据")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_seedream_image_to_image():
    """测试图生图功能(如果支持)"""
    print("\n" + "="*80)
    print("测试2: 即梦AI图生图(Image-to-Image)")
    print("="*80)

    try:
        client = get_volcano_client()

        if not client:
            print("❌ Volcano客户端未配置")
            return False

        # 读取测试图片
        test_image_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_reference_v3.png"

        if not Path(test_image_path).exists():
            print(f"❌ 测试图片不存在: {test_image_path}")
            print("请先上传测试图片")
            return False

        # 编码为base64
        import base64
        with open(test_image_path, 'rb') as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

        print(f"✅ 测试图片已读取: {len(image_data)} bytes")
        print(f"✅ Base64编码长度: {len(base64_image)} chars")

        # 测试图生图API调用
        print("\n[测试2.1] 尝试图生图API调用...")

        # 尝试方式1: 使用image参数(OpenAI兼容格式)
        try:
            response = client.images.generate(
                model="doubao-seedream-4-5-251128",
                prompt="用中国风水墨画风格重新绘制这张图片",
                size="2K",
                response_format="url",
                extra_body={
                    "watermark": False,
                    "image": base64_image,  # 尝试添加image参数
                }
            )

            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"✅ 图生图成功(image参数方式)!")
                print(f"   图片URL: {image_url}")

                # 下载图片
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    output_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_seedream_image_output.png"
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"✅ 已下载到: {output_path}")
                    file_size = len(img_response.content)
                    print(f"   文件大小: {file_size} bytes")

                    # 比较文件大小
                    original_size = len(image_data)
                    if file_size > 0:
                        ratio = file_size / original_size
                        print(f"   文件大小比: {ratio:.2%}")
                    return True
                else:
                    print(f"❌ 下载失败: HTTP {img_response.status_code}")
                    return False
            else:
                print(f"❌ 返回空数据")
        except Exception as e:
            print(f"⚠️ image参数方式失败: {str(e)}")

        # 尝试方式2: 查看官方文档的其他参数
        print("\n[测试2.2] 尝试其他可能的参数...")
        print("提示: 根据搜索结果,Seedream可能使用不同的参数名称")
        print("      请参考: https://www.volcengine.com/docs/823791541523")

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*80)
    print("                    即梦AI(Seedream) API直接测试")
    print("="*80)
    print()
    print("测试目标:")
    print("  1. 验证Seedream文生图功能是否正常")
    print("  2. 检查是否支持Image-to-Image功能")
    print("  3. 定位API调用失败的原因")
    print()
    print("开始测试...\n")

    # 测试1: 文生图
    result1 = test_seedream_text_to_image()

    print()

    # 测试2: 图生图(如果API支持)
    # result2 = test_seedream_image_to_image()

    print("\n" + "="*80)
    print("测试完成!")
    print("="*80)

    print("\n结论:")
    if result1:
        print("✅ Seedream文生图功能正常")
    else:
        print("❌ Seedream API调用失败,请检查:")
        print("   1. VOLCANO_API_KEY是否正确")
        print("   2. 网络连接是否正常")
        print("   3. API密钥是否有效")

if __name__ == "__main__":
    main()
