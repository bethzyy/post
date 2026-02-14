#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试升级后的豆包去水印工具
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from picture.remove_doubao_watermark import DoubaoWatermarkRemover

def quick_test():
    """快速测试"""
    print("="*80)
    print("测试升级后的豆包去水印工具（油猴脚本智能检测）")
    print("="*80)
    print()

    remover = DoubaoWatermarkRemover()

    # 测试图片
    images = [
        (Path("picture/荸荠饼.png"), "荸荠饼"),
        (Path("picture/酒酿.png"), "酒酿")
    ]

    for img_path, name in images:
        print(f"\n{'='*60}")
        print(f"测试图片: {name}")
        print(f"{'='*60}")

        if not img_path.exists():
            print(f"❌ 图片不存在: {img_path}")
            continue

        # 输出路径
        output_path = img_path.parent / f"{img_path.stem}_smart_no_watermark{img_path.suffix}"

        try:
            # 测试检测
            print("\n[步骤1] 检测水印区域...")
            regions = remover.detect_text_regions(img_path)
            print(f"检测到 {len(regions)} 个区域")

            # 测试去除
            print("\n[步骤2] 去除水印...")
            success = remover.remove_watermark_inpainting(img_path, output_path, regions)

            if success:
                print(f"\n✅ 成功!")
                print(f"   输出: {output_path.name}")
                print(f"   路径: {output_path}")
            else:
                print(f"\n❌ 失败")

        except Exception as e:
            print(f"\n❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("测试完成!")
    print("="*80)

if __name__ == '__main__':
    quick_test()
