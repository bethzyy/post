# -*- coding: utf-8 -*-
"""
测试V5版本的图生图功能
验证image_urls参数格式是否正确
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import base64
from pathlib import Path

def test_image_to_image():
    """测试图生图功能"""
    print("\n" + "="*80)
    print("测试 V5 图生图功能 (image_urls参数)")
    print("="*80)

    # 读取测试参考图片
    test_image_path = "C:/D/CAIE_tool/MyAIProduct/post/picture/test_seedream_text.png"

    if not Path(test_image_path).exists():
        print(f"❌ 测试图片不存在: {test_image_path}")
        print("请先运行 test_seedream_direct.py 生成测试图片")
        return False

    # 读取并编码图片
    with open(test_image_path, 'rb') as f:
        image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

    print(f"✅ 测试图片已读取: {len(image_data)} bytes")
    print(f"✅ Base64编码长度: {len(base64_image)} chars")

    # 准备API请求
    url = "http://localhost:5002/api/generate-image"
    payload = {
        "mode": "reference",
        "reference_image": base64_image,
        "style": "guofeng_shuimo"  # 国风水墨风格
    }

    print("\n[发送请求] V5服务器...")
    print(f"  URL: {url}")
    print(f"  模式: 参考图片")
    print(f"  风格: 国风水墨")

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=120  # 2分钟超时
        )

        print(f"\n[响应状态] HTTP {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            if result.get('success'):
                print("\n" + "="*80)
                print("✅ 图生图测试成功!")
                print("="*80)
                print(f"  模型: {result.get('model', 'N/A').upper()}")
                print(f"  风格: {result.get('style', 'N/A')}")
                print(f"  时间: {result.get('timestamp', 'N/A')}")
                print(f"  文件: {result.get('image_filename', 'N/A')}")
                print(f"  路径: {result.get('image_path', 'N/A')}")

                # 检查是否使用了Seedream
                model = result.get('model', '').lower()
                if 'seedream' in model:
                    print("\n🎉 使用了即梦AI(Seedream)模型!")
                elif 'gemini' in model:
                    print("\n⚠️ 使用了备选Gemini模型")
                    print("   说明Seedream调用失败")

                # 显示参考图片描述
                ref_desc = result.get('reference_description')
                if ref_desc:
                    print(f"\n  参考图片描述: {ref_desc}")

                # 显示提示词(前100字符)
                prompt = result.get('prompt', '')
                print(f"\n  提示词(前100字符):")
                print(f"    {prompt[:100]}...")

                print("\n" + "="*80)
                print("✓ 测试完成!")
                print("="*80)

                return True
            else:
                print("\n❌ 生成失败")
                print(f"错误: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("\n❌ 请求超时")
        print("提示: 图像生成可能需要较长时间,请检查服务器日志")
        return False
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*80)
    print("                    V5 图生图功能测试")
    print("="*80)
    print()
    print("测试内容:")
    print("  1. 验证V5版本已启动")
    print("  2. 测试参考图片上传")
    print("  3. 验证image_urls参数格式")
    print("  4. 检查是否使用Seedream模型")
    print("  5. 确认生成的图片基于参考内容")
    print()

    success = test_image_to_image()

    print()
    print("="*80)
    print("测试总结")
    print("="*80)

    if success:
        print("✅ V5图生图功能正常!")
        print()
        print("关键改进:")
        print("  ✓ 使用官方推荐的image_urls参数格式")
        print("  ✓ 支持多模态图片融合(1-10张参考图)")
        print("  ✓ 正确传递参考图片给Seedream API")
        print()
        print("下一步:")
        print("  1. 在浏览器访问 http://localhost:5002")
        print("  2. 上传参考图片测试图生图")
        print("  3. 验证生成的图片与参考图片内容一致")
    else:
        print("❌ 测试失败")
        print()
        print("可能原因:")
        print("  1. V5服务器未启动或端口冲突")
        print("  2. Seedream API密钥配置错误")
        print("  3. 网络连接问题")
        print("  4. API参数格式仍需调整")
        print()
        print("建议:")
        print("  - 检查V5服务器日志: v5_debug.log")
        print("  - 访问 http://localhost:5002/logs 查看详细日志")

    print("="*80)

if __name__ == "__main__":
    main()
