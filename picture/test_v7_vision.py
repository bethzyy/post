#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试V7版本的视觉分析功能
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入V7的analyze_reference_image函数
from standalone_image_generator_v7 import analyze_reference_image

def test_vision():
    """测试视觉分析"""
    print("="*80)
    print("V7视觉分析测试")
    print("="*80)

    # 测试图片路径
    reference_image = Path(__file__).parent / "cat_reference.png"

    if not reference_image.exists():
        print(f"[错误] 测试图片不存在: {reference_image}")
        return

    print(f"[测试图片] {reference_image}")
    print(f"[文件大小] {reference_image.stat().st_size} bytes")
    print()

    print("[步骤] 开始视觉分析...")
    description = analyze_reference_image(str(reference_image))

    if description:
        print()
        print("="*80)
        print("[✓] 视觉分析成功!")
        print(f"[描述] {description}")
        print("="*80)

        # 检查描述是否包含猫相关信息
        cat_keywords = ["猫", "猫咪", "cat", "猫科", "动物"]
        has_cat = any(keyword in description.lower() for keyword in cat_keywords)

        if has_cat:
            print()
            print("[✓] 测试通过: 成功识别出图片中的猫!")
        else:
            print()
            print("[⚠] 测试警告: 描述中可能没有明确识别出猫")
            print(f"     描述内容: {description}")
    else:
        print()
        print("="*80)
        print("[✗] 视觉分析失败")
        print("="*80)

if __name__ == "__main__":
    test_vision()
