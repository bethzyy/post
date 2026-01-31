#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中国山水画生成测试 - 使用Volcano/Seedream模型
生成一张中国传统山水画
"""

import sys
import os
from pathlib import Path
import requests
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_volcano_client


def generate_chinese_landscape():
    """生成中国山水画"""

    print("=" * 80)
    print("中国山水画生成测试 - Volcano/Seedream")
    print("=" * 80)
    print()

    # 获取客户端
    client = get_volcano_client()

    if not client:
        print("[ERROR] 无法获取Volcano客户端")
        print("请检查config.py中的API密钥配置")
        return False

    print("[OK] Volcano客户端初始化成功")
    print()

    # 中国山水画提示词
    prompt = """
中国传统山水画，水墨画风格。

画面内容：
- 远山如黛，层峦叠嶂，云雾缭绕
- 近景有苍松翠柏，枝干遒劲
- 山间有小溪潺潺流淌，水波粼粼
- 水墨晕染，墨色浓淡相宜
- 构图开阔，意境深远
- 留白得当，富有诗意

艺术风格：
- 中国传统水墨画技法
- 笔墨苍劲，气韵生动
- 淡雅脱俗，富有禅意
- 继承宋代山水画传统
- 1024x1024分辨率
"""

    print(f"Prompt: {prompt.strip()}")
    print()
    print("-" * 80)
    print()

    # 创建输出目录
    output_dir = "landscape_test"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        print("正在生成图像...")

        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt.strip(),
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,  # 不加水印
            },
        )

        print("[OK] API调用成功")
        print()

        # 检查响应
        if hasattr(response, 'data') and len(response.data) > 0:
            image_url = response.data[0].url

            print(f"[OK] 图片URL: {image_url}")
            print()

            # 下载图片
            print("正在下载图片...")
            img_response = requests.get(image_url, timeout=60)

            if img_response.status_code == 200:
                # 保存图片
                filename = Path(__file__).parent / f"{output_dir}/chinese_landscape_seedream_{timestamp}.jpg"

                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                file_size = len(img_response.content)

                print(f"[OK] 图片已保存: {filename}")
                print(f"[OK] 文件大小: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
                print()

                # 保存测试结果
                import json
                result = {
                    'model': 'doubao-seedream-4-5-251128',
                    'model_name': 'Volcano/Seedream 豆包图灵',
                    'prompt': prompt.strip(),
                    'filename': str(filename),
                    'size': file_size,
                    'resolution': '2K',
                    'url': image_url,
                    'timestamp': timestamp,
                    'status': 'success'
                }

                result_file = Path(__file__).parent / f"{output_dir}/test_result_{timestamp}.json"
                with open(result_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

                print(f"[OK] 测试结果已保存: {result_file}")
                print()

                # 生成HTML展示页面
                html_file = generate_html_display(result, output_dir, timestamp)
                print(f"[OK] HTML展示页面已生成: {html_file}")
                print()

                print("=" * 80)
                print("测试成功完成!")
                print("=" * 80)
                print()

                # 自动打开图片和HTML
                try:
                    import webbrowser
                    # 打开HTML文件
                    webbrowser.open(f'file:///{os.path.abspath(html_file)}'.replace('\\', '/'))
                    print("[OK] 已在浏览器中打开展示页面")
                except:
                    print("[INFO] 请手动打开HTML文件查看结果")

                return True
            else:
                print(f"[ERROR] 下载图片失败")
                print(f"[状态码] {img_response.status_code}")
                return False
        else:
            print("[ERROR] 未返回图片数据")
            return False

    except Exception as e:
        print(f"[ERROR] 生成失败: {str(e)}")
        print()
        print("错误分析:")
        error_msg = str(e)

        if "401" in error_msg or "Unauthorized" in error_msg:
            print("  类型: 认证失败 (401)")
            print("  说明: API Key可能无效或已过期")
        elif "429" in error_msg or "quota" in error_msg.lower():
            print("  类型: 配额限制 (429)")
            print("  说明: 已达到速率限制或配额耗尽")
        elif "500" in error_msg or "503" in error_msg:
            print("  类型: 服务器错误 (500/503)")
            print("  说明: 服务器暂时不可用")
        else:
            print(f"  详情: {error_msg[:300]}")

        return False


def generate_html_display(result, output_dir, timestamp):
    """生成HTML展示页面"""

    html_filename = Path(__file__).parent / f"{output_dir}/chinese_landscape_display_{timestamp}.html"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>中国山水画生成展示 - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .container {{
            max-width: 900px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .content {{
            padding: 40px;
        }}

        .image-container {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .image-container img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .info-section {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }}

        .info-item {{
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}

        .info-item:last-child {{
            border-bottom: none;
        }}

        .info-label {{
            font-weight: bold;
            color: #5a67d8;
            width: 150px;
            flex-shrink: 0;
        }}

        .info-value {{
            color: #4a5568;
            flex-grow: 1;
        }}

        .prompt-box {{
            background: #edf2f7;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            white-space: pre-wrap;
            font-style: italic;
            color: #2d3748;
            line-height: 1.6;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            background: #48bb78;
            color: white;
        }}

        .footer {{
            background: #2d3748;
            color: white;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 中国山水画生成展示</h1>
            <p>使用Volcano/Seedream豆包图灵模型</p>
        </div>

        <div class="content">
            <div class="image-container">
                <img src="{result['filename']}" alt="中国山水画">
            </div>

            <div style="text-align: center; margin-bottom: 20px;">
                <span class="badge">生成成功</span>
            </div>

            <div class="info-section">
                <div class="info-item">
                    <div class="info-label">模型名称:</div>
                    <div class="info-value">{result['model_name']}</div>
                </div>

                <div class="info-item">
                    <div class="info-label">模型ID:</div>
                    <div class="info-value">{result['model']}</div>
                </div>

                <div class="info-item">
                    <div class="info-label">分辨率:</div>
                    <div class="info-value">{result['resolution']}</div>
                </div>

                <div class="info-item">
                    <div class="info-label">文件大小:</div>
                    <div class="info-value">{result['size']:,} bytes ({result['size']/1024/1024:.2f} MB)</div>
                </div>

                <div class="info-item">
                    <div class="info-label">文件名:</div>
                    <div class="info-value">{result['filename']}</div>
                </div>

                <div class="prompt-box">
                    <strong>生成提示词:</strong>
                    {result['prompt']}
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Generated by AI发文工具管理器</p>
            <p>测试时间: {timestamp}</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return str(html_filename)


if __name__ == '__main__':
    try:
        generate_chinese_landscape()
    except KeyboardInterrupt:
        print("\n\n[WARNING] 测试被用户中断")
    except Exception as e:
        print(f"\n\n[ERROR] 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
