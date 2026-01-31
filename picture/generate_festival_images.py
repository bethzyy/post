# -*- coding: utf-8 -*-
"""
节日主题图像生成器 - 整合版
支持用户自定义主题，使用多个模型生成图像并生成HTML对比页面
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess
import time
import os

# 设置控制台输出编码为UTF-8，避免Windows GBK编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))

from config import get_antigravity_client, get_volcano_client


def generate_with_antigravity(model_name, prompt, output_path):
    """使用anti-gravity生成图像"""
    try:
        client = get_antigravity_client()
        if not client:
            return None, "anti-gravity客户端未配置"

        print(f"[{model_name}] 正在生成图像...")

        # 清理prompt编码
        try:
            prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        except:
            pass

        # 使用DALL-E 3接口生成图像
        response = client.images.generate(
            model=model_name,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # 检查返回结果
        if response.data and len(response.data) > 0:
            image_data = response.data[0]

            # 优先使用base64数据（如果有）
            if hasattr(image_data, 'b64_json') and image_data.b64_json:
                import base64
                img_data = base64.b64decode(image_data.b64_json)

                with open(output_path, 'wb') as f:
                    f.write(img_data)

                return True, f"成功生成: {output_path}"

            # 其次使用URL（如果有）
            elif hasattr(image_data, 'url') and image_data.url:
                import requests
                img_data = requests.get(image_data.url).content

                with open(output_path, 'wb') as f:
                    f.write(img_data)

                return True, f"成功生成: {output_path}"

            else:
                return False, f"{model_name}图像模型暂时不可用（返回空数据）"
        else:
            return False, f"{model_name}图像模型返回空响应"

    except Exception as e:
        return False, str(e)


def generate_with_pollinations(prompt, output_path, model_name="flux"):
    """使用Pollinations.ai生成图像"""
    try:
        print(f"[Pollinations - {model_name}] 正在生成图像...")

        # 清理prompt编码
        try:
            prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        except:
            pass

        # Pollinations.ai使用URL方式
        import urllib.parse
        from PIL import Image
        import requests
        from io import BytesIO

        # 编码prompt
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        # 下载图像
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # 保存为PNG
        img.save(output_path)

        return True, f"成功生成: {output_path}"

    except Exception as e:
        return False, str(e)


def generate_with_volcano(prompt, output_path):
    """使用Volcano(Seedream)生成图像"""
    try:
        client = get_volcano_client()
        if not client:
            return None, "Volcano客户端未配置"

        print(f"[Volcano/Seedream] 正在生成图像...")

        # 清理prompt编码
        try:
            prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        except:
            pass

        # Volcano使用正确的模型名称
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt,
            size="2K",
            response_format="url",
            extra_body={
                "watermark": True,
            }
        )

        # 保存图像
        image_url = response.data[0].url
        import requests
        img_data = requests.get(image_url).content

        with open(output_path, 'wb') as f:
            f.write(img_data)

        return True, f"成功生成: {output_path}"

    except Exception as e:
        return False, str(e)


def generate_with_gemini(prompt, output_path):
    """使用Gemini图像模型生成图像"""
    try:
        client = get_antigravity_client()
        if not client:
            return None, "anti-gravity客户端未配置"

        print(f"[Gemini] 正在生成图像...")

        # 清理prompt编码
        try:
            prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        except:
            pass

        # 使用Gemini图像生成模型（注意：目前返回None）
        response = client.images.generate(
            model="gemini-3-pro-image-2k",
            prompt=prompt,
            size="2K"
        )

        # 检查返回结果
        if response.data and len(response.data) > 0 and response.data[0].url:
            # 保存图像
            image_url = response.data[0].url
            import requests
            img_data = requests.get(image_url).content

            with open(output_path, 'wb') as f:
                f.write(img_data)

            return True, f"成功生成: {output_path}"
        else:
            return False, "Gemini图像模型暂时不可用（返回空URL）"

    except Exception as e:
        return False, str(e)


def generate_html_report(theme, results, output_path):
    """生成HTML对比报告"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>节日主题图像生成对比 - {theme}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
        }}

        .header h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 15px;
        }}

        .theme-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            font-size: 1.2em;
            color: #333;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            text-align: center;
        }}

        .stat-card h3 {{
            color: #667eea;
            font-size: 2em;
            margin-bottom: 5px;
        }}

        .stat-card p {{
            color: #666;
            font-size: 0.9em;
        }}

        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
        }}

        .image-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}

        .image-card:hover {{
            transform: translateY(-5px);
        }}

        .image-header {{
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}

        .model-name {{
            color: #667eea;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .model-type {{
            color: #666;
            font-size: 0.9em;
        }}

        .image-container {{
            text-align: center;
            margin: 20px 0;
        }}

        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .status {{
            padding: 10px;
            border-radius: 8px;
            margin-top: 15px;
            font-weight: bold;
        }}

        .status.success {{
            background: #d4edda;
            color: #155724;
        }}

        .status.error {{
            background: #f8d7da;
            color: #721c24;
        }}

        .prompt-box {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 0.9em;
            color: #666;
        }}

        .footer {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin-top: 40px;
            text-align: center;
        }}

        .regenerate-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s;
        }}

        .regenerate-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 节日主题图像生成对比</h1>
            <div class="theme-box">
                <strong>生成主题：</strong> {theme}
            </div>
            <p style="color: #666; margin-top: 10px;">生成时间: {timestamp}</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <h3>{len(results)}</h3>
                <p>生成模型数</p>
            </div>
            <div class="stat-card">
                <h3>{sum(1 for r in results if r['success'])}</h3>
                <p>成功数量</p>
            </div>
            <div class="stat-card">
                <h3>{sum(1 for r in results if not r['success'])}</h3>
                <p>失败数量</p>
            </div>
        </div>

        <div class="image-grid">
"""

    # 添加每个模型的生成结果
    for result in results:
        status_class = "success" if result['success'] else "error"
        status_text = "✓ 生成成功" if result['success'] else f"✗ 生成失败: {result['message']}"

        image_html = ""
        if result['success'] and result['image_path']:
            # 相对路径
            rel_path = Path(result['image_path']).name
            image_html = f'<img src="{rel_path}" alt="{result["model_name"]}">'

        html_content += f"""
            <div class="image-card">
                <div class="image-header">
                    <div class="model-name">{result['model_name']}</div>
                    <div class="model-type">{result['model_type']}</div>
                </div>
                <div class="image-container">
                    {image_html}
                </div>
                <div class="status {status_class}">
                    {status_text}
                </div>
                <div class="prompt-box">
                    <strong>提示词：</strong><br>
                    {result['prompt']}
                </div>
            </div>
"""

    html_content += """
        </div>

        <div class="footer">
            <p style="color: #666; margin-bottom: 15px;">
                💡 提示：所有图像都保存在当前目录下的 images 文件夹中
            </p>
            <button class="regenerate-btn" onclick="window.location.reload()">
                🔄 重新生成
            </button>
        </div>
    </div>
</body>
</html>
"""

    # 保存HTML
    try:
        # 清理html_content中的无效字符
        html_content_clean = html_content.encode('utf-8', errors='replace').decode('utf-8')

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content_clean)

        return True, f"HTML报告已生成: {output_path}"
    except Exception as e:
        return False, f"保存HTML失败: {str(e)}"


def main():
    """主函数"""

    print("\n" + "="*80)
    print("节日主题图像生成器 - 整合版")
    print("="*80)

    # 获取用户输入
    print("\n请输入生成主题（例如：为春节生成中国风的水彩画）")
    print("或者直接按回车使用默认主题：春节主题 - 中国风水彩画")

    user_theme = input("\n主题: ").strip()

    # 清理可能的编码问题
    if user_theme:
        try:
            # 尝试编码检查，如果失败则使用默认
            user_theme.encode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            print("[警告] 输入包含不支持的字符，使用默认主题")
            user_theme = "春节主题 - 中国风水彩画"

    if not user_theme:
        user_theme = "春节主题 - 中国风水彩画"

    # 创建输出目录
    output_dir = Path(__file__).parent / "images" / f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[输出目录] {output_dir}")

    # 定义模型配置
    models_config = [
        {
            "name": "DALL-E 3 (Anti-gravity)",
            "type": "Anti-gravity / OpenAI",
            "func": generate_with_antigravity,
            "model": "dall-e-3",
            "enabled": True
        },
        {
            "name": "Gemini 3 Pro Image (Anti-gravity)",
            "type": "Anti-gravity / Google",
            "func": generate_with_gemini,
            "model": "gemini-3-pro-image",
            "enabled": True
        },
        {
            "name": "Flux (Pollinations)",
            "type": "Pollinations.ai",
            "func": generate_with_pollinations,
            "model": "flux",
            "enabled": True
        },
        {
            "name": "Seedream (Volcano)",
            "type": "火山引擎",
            "func": generate_with_volcano,
            "model": "seedream",
            "enabled": True
        }
    ]

    # 构建提示词
    base_prompt = f"{user_theme}，节日主题，高质量，1024x1024"

    print(f"\n[提示词] {base_prompt}")
    print("\n" + "="*80)
    print("开始生成图像...")
    print("="*80 + "\n")

    # 生成图像
    results = []

    for i, model_config in enumerate(models_config, 1):
        if not model_config['enabled']:
            continue

        model_name = model_config['name']
        model_type = model_config['type']

        print(f"\n[{i}/{len(models_config)}] {model_name}")

        # 生成文件名
        safe_name = model_name.replace(" ", "_").replace("(", "").replace(")", "")
        output_path = output_dir / f"{safe_name}.png"

        # 调用生成函数
        try:
            if model_config['func'] == generate_with_antigravity:
                success, message = model_config['func'](
                    model_config['model'],
                    base_prompt,
                    str(output_path)
                )
            elif model_config['func'] == generate_with_gemini:
                success, message = model_config['func'](
                    base_prompt,
                    str(output_path)
                )
            elif model_config['func'] == generate_with_pollinations:
                success, message = model_config['func'](
                    base_prompt,
                    str(output_path),
                    model_config['model']
                )
            elif model_config['func'] == generate_with_volcano:
                success, message = model_config['func'](
                    base_prompt,
                    str(output_path)
                )
            else:
                success, message = False, "未知的生成函数"

            result = {
                'model_name': model_name,
                'model_type': model_type,
                'success': success,
                'message': message,
                'prompt': base_prompt,
                'image_path': str(output_path) if success else None
            }

            print(f"{'[✓]' if success else '[✗]'} {message}")

        except Exception as e:
            result = {
                'model_name': model_name,
                'model_type': model_type,
                'success': False,
                'message': str(e),
                'prompt': base_prompt,
                'image_path': None
            }
            print(f"[✗] 错误: {str(e)}")

        results.append(result)
        time.sleep(1)  # 避免请求过快

    # 生成HTML报告
    print("\n" + "="*80)
    print("生成HTML报告...")
    print("="*80 + "\n")

    html_path = output_dir / "index.html"
    html_success, html_message = generate_html_report(user_theme, results, str(html_path))

    if html_success:
        print(f"[✓] {html_message}")
        print(f"\n[提示] 请在浏览器中打开: {html_path}")

        # 自动打开浏览器
        import webbrowser
        webbrowser.open(f"file:///{html_path}")
    else:
        print(f"[✗] {html_message}")

    print("\n" + "="*80)
    print("生成完成!")
    print("="*80)
    print(f"\n[统计] 总计: {len(results)} | 成功: {sum(1 for r in results if r['success'])} | 失败: {sum(1 for r in results if not r['success'])}")
    print(f"[目录] 所有文件保存在: {output_dir}\n")


if __name__ == "__main__":
    main()
