#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI图像生成器 - 独立Web版 V2
支持主题输入或参考图片,多种画图风格选择
使用即梦AI(Seedream)模型生成图像

V2改进: 支持真正的图生图(Image-to-Image)功能
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import base64
import requests
from io import BytesIO
import tempfile
from flask import Flask, render_template, request, jsonify, send_from_directory

# 设置控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_volcano_client, get_antigravity_client

app = Flask(__name__)
BASE_DIR = Path(__file__).parent.parent

# 画图风格定义
IMAGE_STYLES = {
    "guofeng_gongbi": {
        "name": "国风工笔",
        "description": "中国传统工笔画风格,线条精细,色彩淡雅",
        "prompt_template": "{theme},中国传统工笔画风格,精细线条,淡雅色彩,高质量,杰作"
    },
    "guofeng_shuimo": {
        "name": "国风水墨",
        "description": "中国水墨画风格,意境深远,水墨淋漓",
        "prompt_template": "{theme},中国水墨画风格,传统笔墨,意境深远,留白艺术,高质量"
    },
    "shuica": {
        "name": "水彩画",
        "description": "水彩画风格,色彩通透,轻盈自然",
        "prompt_template": "{theme},水彩画风格,色彩通透,水彩质感,艺术绘画,高质量"
    },
    "youhua": {
        "name": "油画",
        "description": "油画风格,色彩丰富,笔触明显",
        "prompt_template": "{theme},油画风格,丰富色彩,明显笔触,古典油画质感,高质量"
    },
    "manhua": {
        "name": "动漫插画",
        "description": "日式动漫插画风格,色彩鲜明",
        "prompt_template": "{theme},动漫插画风格,日系动漫,色彩鲜明,精美插画,高质量"
    },
    "shisu": {
        "name": "写实摄影",
        "description": "真实照片风格,细节丰富",
        "prompt_template": "{theme},专业摄影,写实风格,高分辨率,细节丰富,8K画质"
    },
    "cartoon": {
        "name": "卡通插画",
        "description": "可爱卡通风格,色彩明快",
        "prompt_template": "{theme},卡通插画,可爱风格,色彩明快,儿童绘本风格,高质量"
    }
}


def generate_with_seedream_i2i(prompt, output_path, reference_image_path=None):
    """使用即梦AI(Seedream)生成图像 - 支持图生图

    Args:
        prompt: 文本提示词
        output_path: 输出文件路径
        reference_image_path: 参考图片路径(可选,用于图生图)

    Returns:
        (success, message)
    """
    try:
        client = get_volcano_client()
        if not client:
            return False, "Volcano客户端未配置,请检查.env中的VOLCANO_API_KEY"

        print(f"[即梦AI] 正在生成图像...")

        # 构建请求参数
        generate_params = {
            "model": "doubao-seedream-4-5-251128",
            "prompt": prompt,
            "size": "2K",
            "response_format": "url",
            "extra_body": {
                "watermark": False,
            }
        }

        # 如果有参考图片,使用图生图功能
        if reference_image_path and Path(reference_image_path).exists():
            print(f"[参考图片] {reference_image_path}")
            print(f"[图生图] 将基于参考图片生成,应用{prompt}")

            try:
                # 读取并编码参考图片为base64
                with open(reference_image_path, 'rb') as f:
                    image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')

                # 添加image参数到请求体(即梦AI支持图生图)
                generate_params["extra_body"]["image"] = base64_image
                print(f"[✓] 参考图片已编码({len(base64_image)} chars)")

            except Exception as e:
                print(f"[警告] 读取参考图片失败: {e},将使用文本生成")

        print(f"[提示词] {prompt}")

        # 发送生成请求
        response = client.images.generate(**generate_params)

        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"[图片URL] {image_url}")

            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                return True, f"成功生成: {output_path}"
            else:
                return False, f"下载图像失败: HTTP {img_response.status_code}"
        else:
            return False, "即梦AI返回空响应"

    except Exception as e:
        error_msg = str(e)
        # 检查是否是图生图不支持的错误
        if "invalid_request" in error_msg or "not supported" in error_msg:
            print(f"[警告] 即梦AI可能不支持图生图参数: {error_msg}")
        return False, f"生成失败: {error_msg}"


def generate_with_gemini(prompt, output_path):
    """使用Gemini生成图像(备选方案)"""
    try:
        client = get_antigravity_client()
        if not client:
            return False, "Anti-gravity客户端未配置"

        print("[Gemini] 正在生成图像...")
        print(f"[提示词] {prompt}")

        response = client.images.generate(
            model="gemini-3-pro-image-2k",
            prompt=prompt,
            size="2K"
        )

        if response.data and len(response.data) > 0 and response.data[0].url:
            image_url = response.data[0].url
            print(f"[图片URL] {image_url}")

            img_response = requests.get(image_url, timeout=60)
            if img_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                return True, f"成功生成: {output_path}"
            else:
                return False, f"下载图像失败: HTTP {img_response.status_code}"
        else:
            return False, "Gemini返回空响应"

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return False, "Gemini配额耗尽,请稍后再试"
        return False, f"生成失败: {error_msg}"


def encode_image_to_base64(image_path):
    """将图像文件编码为base64"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        print(f"[错误] 编码图像失败: {e}")
        return None


@app.route('/')
def index():
    """主页面"""
    return send_from_directory(Path(__file__).parent, 'web_image_generator.html')


@app.route('/api/generate-image', methods=['POST'])
def api_generate_image():
    """API: 生成图像 - 支持图生图"""
    reference_image_path = None

    try:
        data = request.json
        mode = data.get('mode', 'theme')
        theme = data.get('theme', '')
        reference_image = data.get('reference_image', '')
        style = data.get('style', 'guofeng_gongbi')

        # 验证参数
        if mode == 'theme' and not theme:
            return jsonify({'success': False, 'error': '主题模式需要输入主题描述'})
        if mode == 'reference' and not reference_image:
            return jsonify({'success': False, 'error': '参考图片模式需要上传参考图片'})

        # 获取风格配置
        style_config = IMAGE_STYLES.get(style, IMAGE_STYLES['guofeng_gongbi'])

        print(f"\n" + "="*80)
        print(f"[生成请求]")
        print(f"  模式: {mode}")
        print(f"  风格: {style_config['name']}")
        print(f"  主题: {theme if mode == 'theme' else '(参考图片)'}")

        # 构建提示词和处理参考图片
        if mode == 'theme':
            # 主题模式:直接使用主题描述
            prompt = style_config['prompt_template'].format(theme=theme)
            print(f"[提示词] {prompt}\n")
        else:
            # 参考图片模式:
            # 1. 保存base64图片为临时文件
            try:
                image_data = base64.b64decode(reference_image)

                # 创建临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                    temp_file.write(image_data)
                    reference_image_path = temp_file.name

                print(f"[参考图片] 已保存到: {reference_image_path} ({len(image_data)} bytes)")

                # 2. 构建提示词 - 让AI根据参考图片用指定风格重绘
                prompt = f"请仔细观察参考图片的画面内容、构图和细节,然后用{style_config['name']}风格重新绘制这张图片。要求:保持原有的画面主体和布局,将艺术风格转换为{style_config['description']},确保细节完整,线条流畅,色彩和谐。{style_config['prompt_template'].format(theme='')}"

                print(f"[提示词] {prompt}\n")

            except Exception as e:
                print(f"[错误] 处理参考图片失败: {e}")
                return jsonify({'success': False, 'error': f'处理参考图片失败: {str(e)}'})

        # 创建输出目录
        output_dir = Path(__file__).parent / "generated_images" / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"generated_{style}_{timestamp}.png"
        output_path = output_dir / output_filename

        # 优先使用即梦AI(Seedream)图生图
        print("[开始生成] 使用即梦AI(Seedream)...")
        success, message = generate_with_seedream_i2i(prompt, str(output_path), reference_image_path)

        # 清理临时文件
        if reference_image_path and Path(reference_image_path).exists():
            try:
                Path(reference_image_path).unlink()
                print(f"[清理] 已删除临时文件\n")
            except:
                pass

        if not success:
            print(f"[警告] Seedream生成失败: {message}")
            print("[备选] 尝试使用Gemini生成...")
            success, message = generate_with_gemini(prompt, str(output_path))

        if success:
            # 将生成的图像编码为base64
            image_base64 = encode_image_to_base64(str(output_path))

            result = {
                'success': True,
                'message': '图像生成成功',
                'model': 'seedream' if 'seedream' in message.lower() else 'gemini',
                'style': style_config['name'],
                'mode': mode,
                'prompt': prompt,
                'image_path': str(output_path),
                'image_filename': output_filename,
                'image_base64': image_base64,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            print(f"\n[✓] 生成成功!")
            print(f"  模型: {result['model'].upper()}")
            print(f"  风格: {result['style']}")
            print(f"  文件: {output_path}")
            print("="*80 + "\n")

            return jsonify(result)
        else:
            print(f"\n[✗] 生成失败: {message}")
            print("="*80 + "\n")
            return jsonify({'success': False, 'error': message})

    except Exception as e:
        # 清理临时文件
        if reference_image_path and Path(reference_image_path).exists():
            try:
                Path(reference_image_path).unlink()
            except:
                pass

        import traceback
        error_details = traceback.format_exc()
        print(f"\n[✗] 请求失败: {str(e)}")
        print(f"[详细错误]\n{error_details}")
        print("="*80 + "\n")
        return jsonify({'success': False, 'error': f'请求失败: {str(e)}'})


def main():
    """主函数"""
    print("\n" + "="*80)
    print("                    AI图像生成器 - Web版 V2")
    print("="*80)
    print()
    print("启动Web服务器: http://localhost:5001")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  ✨ 支持主题描述生成")
    print("  🖼️  支持参考图片生成(图生图)")
    print("  🎨 多种画图风格选择")
    print("  🤖 使用即梦AI(Seedream)模型")
    print()
    print("V2改进:")
    print("  ✅ 参考图片模式真正基于图片内容生成")
    print("  ✅ 支持图生图(Image-to-Image)功能")
    print("="*80)
    print()

    app.run(host='0.0.0.0', port=5001, debug=False)


if __name__ == "__main__":
    main()
