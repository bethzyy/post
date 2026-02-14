#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试AI图像生成器
测试主题描述和参考图片两种模式
"""

import sys
from pathlib import Path
import json
import requests
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_theme_mode():
    """测试主题描述模式"""
    print("\n" + "="*80)
    print("测试1: 主题描述模式 - 东北粘火烧")
    print("="*80 + "\n")

    params = {
        "mode": "theme",
        "theme": "东北粘火烧外皮金黄酥脆,内里软糯拉丝。黄米面做皮,红豆做馅,香甜不腻,也是寓意生活'粘'粘乎乎,甜甜蜜蜜",
        "style": "guofeng_gongbi"
    }

    print(f"[参数]")
    print(f"  模式: {params['mode']}")
    print(f"  主题: {params['theme']}")
    print(f"  风格: 国风工笔")
    print()

    try:
        response = requests.post(
            'http://localhost:5001/api/generate-image',
            json=params,
            timeout=120
        )

        result = response.json()

        if result.get('success'):
            print(f"[✓] 生成成功!")
            print(f"  模型: {result['model'].upper()}")
            print(f"  风格: {result['style']}")
            print(f"  时间: {result['timestamp']}")
            print(f"  文件: {result['image_filename']}")
            print(f"  路径: {result['image_path']}")
            print(f"  提示词: {result['prompt']}")
            print()

            # 保存base64图片
            if result.get('image_base64'):
                import base64
                img_data = base64.b64decode(result['image_base64'])
                test_output = Path(__file__).parent / "test_output_theme.png"
                with open(test_output, 'wb') as f:
                    f.write(img_data)
                print(f"[✓] 测试图片已保存: {test_output}")

            return True
        else:
            print(f"[✗] 生成失败: {result.get('error')}")
            return False

    except Exception as e:
        print(f"[✗] 请求失败: {str(e)}")
        return False


def test_reference_mode():
    """测试参考图片模式"""
    print("\n" + "="*80)
    print("测试2: 参考图片模式")
    print("="*80 + "\n")

    # 创建一个简单的测试图片(base64编码)
    import base64
    from PIL import Image, ImageDraw

    # 创建一个简单的测试图片
    img = Image.new('RGB', (200, 200), color='lightblue')
    draw = ImageDraw.Draw(img)
    draw.text((50, 90), "Test Image", fill='white')

    # 转换为base64
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    params = {
        "mode": "reference",
        "reference_image": img_base64,
        "style": "shuica"
    }

    print(f"[参数]")
    print(f"  模式: {params['mode']}")
    print(f"  参考: 测试图片(200x200)")
    print(f"  风格: 水彩画")
    print()

    try:
        response = requests.post(
            'http://localhost:5001/api/generate-image',
            json=params,
            timeout=120
        )

        result = response.json()

        if result.get('success'):
            print(f"[✓] 生成成功!")
            print(f"  模型: {result['model'].upper()}")
            print(f"  风格: {result['style']}")
            print(f"  时间: {result['timestamp']}")
            print(f"  文件: {result['image_filename']}")
            print(f"  路径: {result['image_path']}")
            print()

            # 保存base64图片
            if result.get('image_base64'):
                img_data = base64.b64decode(result['image_base64'])
                test_output = Path(__file__).parent / "test_output_reference.png"
                with open(test_output, 'wb') as f:
                    f.write(img_data)
                print(f"[✓] 测试图片已保存: {test_output}")

            return True
        else:
            print(f"[✗] 生成失败: {result.get('error')}")
            return False

    except Exception as e:
        print(f"[✗] 请求失败: {str(e)}")
        return False


def test_different_styles():
    """测试不同风格"""
    print("\n" + "="*80)
    print("测试3: 不同风格快速测试")
    print("="*80 + "\n")

    styles = [
        ("guofeng_gongbi", "国风工笔"),
        ("guofeng_shuimo", "国风水墨"),
        ("shuica", "水彩画"),
        ("cartoon", "卡通插画")
    ]

    for style_code, style_name in styles:
        print(f"[测试] {style_name}...")

        params = {
            "mode": "theme",
            "theme": "一只可爱的小猫咪",
            "style": style_code
        }

        try:
            response = requests.post(
                'http://localhost:5001/api/generate-image',
                json=params,
                timeout=120
            )

            result = response.json()
            if result.get('success'):
                print(f"  ✓ {style_name}: {result['model'].upper()}")
            else:
                print(f"  ✗ {style_name}: {result.get('error')}")

        except Exception as e:
            print(f"  ✗ {style_name}: {str(e)}")

        print()


def main():
    """主测试函数"""
    print("\n" + "="*80)
    print("                    AI图像生成器 - 功能测试")
    print("="*80)

    # 检查服务器是否运行
    try:
        response = requests.get('http://localhost:5001', timeout=5)
        print("[✓] 服务器运行正常")
    except:
        print("[✗] 无法连接到服务器,请先运行: python standalone_image_generator.py")
        return

    # 运行测试
    test_theme_mode()

    time.sleep(2)

    test_reference_mode()

    time.sleep(2)

    test_different_styles()

    print("\n" + "="*80)
    print("测试完成!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
