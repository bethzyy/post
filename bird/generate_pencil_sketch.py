# -*- coding: utf-8 -*-
"""
为bird.jpg生成铅笔起稿图
使用Volcano/Seedream模型
"""

import sys
import os
from pathlib import Path
import requests
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config import get_volcano_client


def generate_pencil_sketch():
    """生成铅笔起稿图"""

    print("="*80)
    print("鸟儿铅笔起稿图生成器")
    print("="*80)

    # 获取客户端
    client = get_volcano_client()

    if not client:
        print("\n[错误] 无法获取Volcano客户端")
        return False

    # 详细的prompt，强调构图匹配
    prompt = """
Step 1 of 6: Pencil sketch of bird perched on branch.

CRITICAL REQUIREMENTS:
- Reference image: bird.jpg (C:\D\CAIE_tool\MyAIProduct\draw\bird.jpg)
- You MUST study the reference image carefully first
- Bird's POSTURE and SILHOUETTE must be IDENTICAL to reference
- Branch position and angle must match reference exactly
- Leaves arrangement must match reference exactly
- Overall COMPOSITION must be identical to reference

Style Details:
- Light pencil outlines on white paper
- NO color
- NO shading
- Simple, clean lines
- Teaching demonstration style
- Size: 2K resolution

IMPORTANT: This is step 1 of a 6-step watercolor painting tutorial.
The bird should be in the SAME POSITION and POSTURE as the reference,
but rendered only as light pencil outlines without color or shading.
"""

    print(f"\n[信息] 模型: doubao-seedream-4-5-251128")
    print(f"[信息] 分辨率: 2K")
    print(f"[参考图] bird.jpg")
    print(f"\n[提示] 正在生成铅笔起稿图...")

    try:
        # 调用API
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt.strip(),
            size="2K",
            response_format="url",
            extra_body={
                "watermark": True,
            },
        )

        # 检查响应
        if hasattr(response, 'data') and len(response.data) > 0:
            image_url = response.data[0].url

            print(f"\n[成功] 图片生成成功！")

            # 下载图片
            print(f"[下载] 正在下载图片...")
            img_response = requests.get(image_url, timeout=60)

            if img_response.status_code == 200:
                # 保存图片
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = Path(__file__).parent / f"bird_pencil_sketch_{timestamp}.jpg"

                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content) / (1024 * 1024)

                print(f"[保存] {filename}")
                print(f"[大小] {file_size:.2f} MB")

                # 显示图片信息
                print(f"\n[信息] 图片详情:")
                print(f"  步骤: 第1步 - 铅笔起稿")
                print(f"  模型: doubao-seedream-4-5-251128")
                print(f"  分辨率: 2K")
                print(f"  风格: 铅笔线条素描")
                print(f"  要求: 构图与参考图严格匹配")

                return True, filename
            else:
                print(f"\n[错误] 下载图片失败")
                return False, None
        else:
            print(f"\n[错误] 未返回图片数据")
            return False, None

    except Exception as e:
        error_msg = str(e)

        print(f"\n[错误] API调用失败")
        print(f"[详情] {error_msg[:500]}")

        # 错误分类
        if "401" in error_msg:
            print(f"\n[类型] 认证失败 (401)")
            print(f"[说明] API Key可能无效")
        elif "429" in error_msg:
            print(f"\n[类型] 配额限制 (429)")
            print(f"[说明] 已达到速率限制")
        elif "500" in error_msg or "503" in error_msg:
            print(f"\n[类型] 服务器错误 (500/503)")
            print(f"[说明] 服务器暂时不可用")

        return False, None


def main():
    """主函数"""

    print("\n" + "="*80)
    print("Volcano/Seedream 铅笔起稿图生成程序")
    print("参考图: bird.jpg")
    print("="*80)

    # 生成图片
    success, filename = generate_pencil_sketch()

    print("\n" + "="*80)
    if success:
        print("生成成功！")
        print(f"\n图片文件: {filename}")
        print("\n[提示] 这是第1步：铅笔起稿")
        print("[说明] 构图与参考图bird.jpg严格匹配")
        print("[风格] 铅笔线条，无颜色，无阴影")
    else:
        print("生成失败，请查看上面的错误信息")
    print("="*80)


if __name__ == "__main__":
    main()
