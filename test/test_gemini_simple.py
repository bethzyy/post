#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gemini模型简单测试 - 中国山水画
测试单个Gemini模型生成一张中国山水画
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_antigravity_client
from datetime import datetime
import base64
import json

# 测试配置
TEST_MODEL = 'gemini-3-pro-image-4k'
TEST_MODEL_NAME = 'Gemini 3 Pro Image 4K'

TEST_PROMPT = 'Traditional Chinese landscape painting, mountains and mist, ink wash style, serene atmosphere, elegant composition, masterpiece quality'

def generate_chinese_landscape():
    """生成中国山水画"""

    print("=" * 80)
    print("Gemini模型测试 - 中国山水画")
    print("=" * 80)
    print()

    # 获取客户端
    client = get_antigravity_client()

    if not client:
        print("[ERROR] 无法获取API客户端")
        print("请检查config.py中的API密钥配置")
        return

    print("[OK] API客户端初始化成功")
    print()

    # 创建输出目录
    output_dir = "gemini_simple_test"
    os.makedirs(output_dir, exist_ok=True)

    # 时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"测试模型: {TEST_MODEL_NAME}")
    print(f"模型ID: {TEST_MODEL}")
    print(f"输出目录: {output_dir}/")
    print()
    print(f"Prompt: {TEST_PROMPT}")
    print()
    print("-" * 80)
    print()

    # 生成图像
    print("正在生成图像...")

    try:
        response = client.images.generate(
            model=TEST_MODEL,
            prompt=TEST_PROMPT,
            size="1024x1024",
            n=1,
        )

        print("[OK] API调用成功")
        print()

        # 检查响应
        if hasattr(response, 'data') and len(response.data) > 0:
            image_data = response.data[0]
            b64_json = getattr(image_data, 'b64_json', None)

            if b64_json:
                # 保存base64图像
                image_bytes = base64.b64decode(b64_json)
                filename = f"{output_dir}/chinese_landscape_{timestamp}.png"

                with open(filename, 'wb') as f:
                    f.write(image_bytes)

                print(f"[OK] 图像已保存: {filename}")
                print(f"[OK] 文件大小: {len(image_bytes):,} bytes")
                print(f"[OK] 图像尺寸: 1024x1024")
                print()

                # 保存测试结果
                result = {
                    'model': TEST_MODEL,
                    'model_name': TEST_MODEL_NAME,
                    'prompt': TEST_PROMPT,
                    'filename': filename,
                    'size': len(image_bytes),
                    'resolution': '1024x1024',
                    'timestamp': timestamp,
                    'status': 'success'
                }

                result_file = f"{output_dir}/test_result_{timestamp}.json"
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

                # 自动打开HTML文件
                try:
                    import webbrowser
                    webbrowser.open(f'file:///{os.path.abspath(html_file)}'.replace('\\', '/'))
                    print("[OK] 已在浏览器中打开展示页面")
                except:
                    print("[INFO] 请手动打开HTML文件查看结果")

                print()

            else:
                print("[ERROR] 响应中没有找到base64图像数据")
                print("[INFO] 响应数据:", image_data)

        else:
            print("[ERROR] 响应格式异常")

    except Exception as e:
        print(f"[ERROR] 生成失败: {str(e)}")
        print()
        print("错误分析:")
        error_msg = str(e)

        if "429" in error_msg:
            print("  类型: 配额限制 (429 Too Many Requests)")
            print("  说明: 已达到速率限制，需要等待")
        elif "502" in error_msg:
            print("  类型: 网关错误 (502 Bad Gateway)")
            print("  说明: API服务暂时不可用")
        elif "503" in error_msg or "MODEL_CAPACITY_EXHAUSTED" in error_msg:
            print("  类型: 服务器容量耗尽 (503 Service Unavailable)")
            print("  说明: 服务器过载，请稍后重试")
        elif "401" in error_msg:
            print("  类型: 认证失败 (401 Unauthorized)")
            print("  说明: API key无效或过期")
        else:
            print(f"  详情: {error_msg[:300]}")

    print()

def generate_html_display(result, output_dir, timestamp):
    """生成HTML展示页面"""

    html_filename = f"{output_dir}/chinese_landscape_display_{timestamp}.html"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini中国山水画生成测试 - {timestamp}</title>
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
            max-width: 800px;
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

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
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
            <h1>🎨 Gemini中国山水画生成测试</h1>
            <p>测试时间: {timestamp}</p>
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
                    <div class="info-value">{result['size']:,} bytes</div>
                </div>

                <div class="info-item">
                    <div class="info-label">文件名:</div>
                    <div class="info-value">{result['filename']}</div>
                </div>

                <div class="prompt-box">
                    <strong>生成提示词:</strong><br>
                    {result['prompt']}
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Generated by AI发文工具管理器 - Gemini模型测试工具</p>
            <p>测试时间: {timestamp}</p>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML文件
    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_filename

if __name__ == '__main__':
    try:
        generate_chinese_landscape()
    except KeyboardInterrupt:
        print("\n\n[WARNING] 测试被用户中断")
    except Exception as e:
        print(f"\n\n[ERROR] 发生未预期的错误: {e}")
        import traceback
        traceback.print_exc()
