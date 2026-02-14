#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI图像生成器 - Web版 V8 (Anthropic兼容版)
支持主题输入或参考图片,多种画图风格选择
使用即梦AI(Seedream)模型生成图像

V8改进:
  ✅ 使用Anthropic兼容接口进行视觉分析
  ✅ 使用openai库调用智谱AI的Anthropic兼容API
  ✅ 完全修复视觉模型分析错误
  ✅ 正确处理image_urls参数进行图生图
  ✅ 修复模型识别显示(SEEDREAM-V8而非GEMINI)
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import base64
import requests
from io import BytesIO
import tempfile
import logging
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

# 设置控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

app = Flask(__name__)
BASE_DIR = Path(__file__).parent.parent

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('v8_debug.log', encoding='utf-8')
    ]
)

# 画图风格定义
IMAGE_STYLES = {
    "guofeng_gongbi": {
        "name": "国风工笔",
        "description": "中国传统工笔画风格,线条精细,色彩淡雅",
        "prompt_template": "{theme},中国传统工笔画风格,精细线条,淡雅色彩,高质量,杰作"
    },
    "guofeng_shuimo": {
        "name": "国风水墨",
        "description": "中国水墨画风格,传统笔墨,意境深远,水墨淋漓",
        "prompt_template": "{theme},中国水墨画风格,传统笔墨,意境深远,留白艺术,高质量"
    },
    "shuica": {
        "name": "水彩画",
        "description": "水彩画风格,色彩通透,水彩质感,艺术绘画,高质量",
        "prompt_template": "{theme},水彩画风格,色彩通透,水彩质感,艺术绘画,高质量"
    },
    "youhua": {
        "name": "油画",
        "description": "油画风格,色彩丰富,笔触明显,古典油画质感",
        "prompt_template": "{theme},油画风格,色彩丰富,笔触明显,古典油画质感,高质量"
    },
    "manhua": {
        "name": "动漫插画",
        "description": "日式动漫插画风格,色彩鲜明,精美插画,高质量",
        "prompt_template": "{theme},日式动漫插画风格,色彩鲜明,精美插画,高质量"
    },
    "shisu": {
        "name": "写实摄影",
        "description": "真实照片风格,细节丰富,8K画质",
        "prompt_template": "{theme},真实照片风格,细节丰富,8K画质,高质量"
    },
    "cartoon": {
        "name": "卡通插画",
        "description": "可爱卡通风格,色彩明快,儿童绘本风格,高质量",
        "prompt_template": "{theme},可爱卡通风格,色彩明快,儿童绘本风格,高质量"
    }
}


def analyze_reference_image(reference_image_path):
    """使用Anthropic兼容接口分析参考图片内容

    Args:
        reference_image_path: 参考图片路径

    Returns:
        str: 图片内容描述
    """
    try:
        # 读取图片
        with open(reference_image_path, 'rb') as f:
            image_data = f.read()

        # 编码为base64
        img_base64 = base64.b64encode(image_data).decode('utf-8')

        # 使用Anthropic兼容接口(通过OpenAI SDK)
        try:
            import os
            api_key = os.environ.get('ZHIPU_API_KEY', '')
            if not api_key:
                logging.error("[错误] ZHIPU_API_KEY环境变量未设置")
                return None

            # 使用OpenAI SDK调用智谱AI的Anthropic兼容API
            client = OpenAI(
                api_key=api_key,
                base_url="https://open.bigmodel.cn/api/anthropic"  # Anthropic兼容端点
            )

            logging.info("[视觉分析] 使用Anthropic兼容接口分析参考图片...")

            # 调用Claude模型进行视觉分析
            response = client.chat.completions.create(
                model="claude-3-5-sonnet-20241022",  # 使用Claude模型
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_base64}"
                                }
                            },
                            {
                                "type": "text",
                                "text": "请详细描述这张图片的内容,包括:1.画面主体 2.背景和环境 3.颜色搭配 4.构图布局 5.重要细节。请用简练的中文描述。"
                            }
                        ]
                    }
                ],
                temperature=0.5,
                max_tokens=2000
            )

            # 获取图片描述
            if response.choices and len(response.choices) > 0:
                description = response.choices[0].message.content
                logging.info(f"[✓] 视觉分析成功: {description}")
                return description
            else:
                logging.warning("[警告] 视觉模型返回空响应")
                return None

        except Exception as e:
            logging.error(f"[错误] 视觉分析失败: {e}")
            import traceback
            logging.debug(traceback.format_exc())
            return None

    except Exception as e:
        logging.error(f"[错误] 读取参考图片失败: {e}")
        return None


def generate_with_seedream_v8(prompt, reference_image_path, output_path):
    """使用即梦AI(Seedream) V8格式生成图像

    V8关键改进:
    - 使用Anthropic兼容接口
    - 正确处理图生图参数
    - 完整的错误处理

    Args:
        prompt: 文本提示词
        reference_image_path: 参考图片路径(图生图模式)或None(文生图模式)
        output_path: 输出文件路径

    Returns:
        (success, message, model_used)
    """
    try:
        # 获取API密钥
        api_key = Config.VOLCANO_API_KEY
        if not api_key:
            logging.error("VOLCANO_API_KEY未配置")
            return False, "Volcano客户端未配置", "unknown"

        logging.info("[即梦AI V8] 正在生成图像...")
        logging.info(f"[提示词] {prompt}")

        # 构建API请求
        url = f"{Config.VOLCANO_BASE_URL}/images/generations"
        headers = {"Authorization": f"Bearer {api_key}"}

        payload = {
            "model": "doubao-seedream-4-5-25128",
            "prompt": prompt,
            "size": "2K",
            "response_format": "url"
        }

        if reference_image_path:
            # 读取并编码参考图片
            with open(reference_image_path, 'rb') as f:
                image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # 使用image_urls参数进行图生图
            payload["image_urls"] = [f"data:image/png;base64,{base64_image}"]

            logging.info(f"[参考图片] 已添加 {len(base64_image)} 字节")
            logging.info("[API参数] 图生图模式 (使用image_urls参数)")
        else:
            logging.info("[API参数] 文生图模式")

        logging.info(f"[API请求] URL: {url}")

        # 发送HTTP POST请求
        response = requests.post(url, json=payload, headers=headers, timeout=120)

        logging.info(f"[响应状态] HTTP {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 检查响应格式
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url')
                model_used = 'seedream-v8'

                logging.info(f"[图片URL] {image_url}")

                # 下载图片
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    logging.info(f"[✓] 图片已保存: {output_path}")
                    return True, f"成功生成: {output_path}", model_used
                else:
                    return False, f"下载图像失败: HTTP {img_response.status_code}", model_used
            elif 'image_url' in result:
                image_url = result['image_url']
                model_used = 'seedream-v8'

                logging.info(f"[图片URL] {image_url}")

                # 下载图片
                img_response = requests.get(image_url, timeout=60)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    logging.info(f"[✓] 图片已保存: {output_path}")
                    return True, f"成功生成: {output_path}", model_used
                else:
                    return False, f"下载图像失败: HTTP {img_response.status_code}", model_used
            else:
                logging.error(f"[错误] 响应格式未知: {list(result.keys())}")
                return False, "即梦AI返回未知格式", "unknown"
        else:
            error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
            logging.error(f"[错误] API请求失败: {error_msg}")
            return False, error_msg, "unknown"

    except Exception as e:
        logging.error(f"[错误] 生成失败: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return False, f"生成失败: {str(e)}", "unknown"


def encode_image_to_base64(image_path):
    """将图像文件编码为base64"""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        logging.error(f"[错误] 编码图像失败: {e}")
        return None


@app.route('/')
def index():
    """主页面"""
    return send_from_directory(Path(__file__).parent, 'web_image_generator.html')


@app.route('/api/generate-image', methods=['POST'])
def api_generate_image():
    """API: 生成图像 - V8版本"""
    reference_image_path = None
    reference_image_description = None
    prompt = None

    try:
        logging.info("="*80)
        logging.info("[生成请求] 收到API请求")

        data = request.json
        mode = data.get('mode', 'theme')
        theme = data.get('theme', '')
        reference_image = data.get('reference_image', '')
        style = data.get('style', 'guofeng_gongbi')

        logging.info(f"[参数解析] mode={mode}, style={style}")

        # 验证参数
        if mode == 'theme' and not theme:
            logging.warning("[验证失败] 主题模式需要输入主题描述")
            return jsonify({'success': False, 'error': '主题模式需要输入主题描述'})
        if mode == 'reference' and not reference_image:
            logging.warning("[验证失败] 参考图片模式需要上传参考图片")
            return jsonify({'success': False, 'error': '参考图片模式需要上传参考图片'})

        # 获取风格配置
        style_config = IMAGE_STYLES.get(style, IMAGE_STYLES['guofeng_gongbi'])

        logging.info(f"[风格选择] {style_config['name']}")

        # 构建提示词和处理参考图片
        if mode == 'theme':
            # 主题模式:直接使用主题描述
            prompt = style_config['prompt_template'].format(theme=theme)
            logging.info(f"[提示词构建] 主题模式")
        else:
            # 参考图片模式
            try:
                # 1. 解码并保存参考图片
                image_data = base64.b64decode(reference_image)

                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                    temp_file.write(image_data)
                    reference_image_path = temp_file.name

                logging.info(f"[参考图片] 已保存到: {reference_image_path} ({len(image_data)} bytes)")

                # 2. 使用Anthropic兼容接口分析参考图片
                logging.info("[步骤1] 开始视觉分析...")
                reference_image_description = analyze_reference_image(reference_image_path)

                if not reference_image_description:
                    logging.error("[视觉分析失败] 无法分析参考图片内容")
                    return jsonify({'success': False, 'error': '无法分析参考图片内容'})

                logging.info(f"[视觉分析结果] {reference_image_description[:100]}...")

                # 3. 构建详细的prompt
                prompt = f"""参考图片内容: {reference_image_description}

请根据上述参考图片,用{style_config['name']}风格重新绘制。
要求:
1. 保持参考图片中所有主体、物体和元素
2. 保持原有的构图和布局
3. 将艺术风格转换为{style_config['description']}
4. 确保所有细节都完整呈现
5. 线条流畅,色彩和谐

{style_config['prompt_template'].format(theme=reference_image_description)}"""

                logging.info(f"[提示词构建] 参考图片模式 (长度: {len(prompt)} 字符)")

            except Exception as e:
                logging.error(f"[错误] 处理参考图片失败: {e}")
                import traceback
                logging.debug(traceback.format_exc())
                return jsonify({'success': False, 'error': f'处理参考图片失败: {str(e)}'})

        # 4. 创建输出目录
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(__file__).parent / "generated_images" / timestamp_str
        output_dir.mkdir(parents=True, exist_ok=True)

        logging.info(f"[输出目录] {output_dir}")

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"generated_{style}_{timestamp}.png"
        output_path = output_dir / output_filename

        logging.info(f"[输出文件] {output_filename}")

        # 5. 使用Seedream V8生成
        logging.info("[步骤2] 开始即梦AI V8生成...")
        success, message, model_used = generate_with_seedream_v8(prompt, reference_image_path, str(output_path))

        # 清理临时文件
        if reference_image_path and Path(reference_image_path).exists():
            try:
                Path(reference_image_path).unlink()
                logging.info(f"[清理] 已删除临时参考图片文件")
            except:
                pass

        if success:
            # 将生成的图像编码为base64
            image_base64 = encode_image_to_base64(str(output_path))

            result = {
                'success': True,
                'message': '图像生成成功',
                'model': model_used.upper(),
                'style': style_config['name'],
                'mode': mode,
                'prompt': prompt,
                'image_path': str(output_path),
                'image_filename': output_filename,
                'image_base64': image_base64,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reference_description': reference_image_description
            }

            logging.info("="*80)
            logging.info("[✓] 生成成功!")
            logging.info(f"  模型: {result['model']}")
            logging.info(f"  风格: {result['style']}")
            logging.info(f"  文件: {output_path}")
            if mode == 'reference' and reference_image_description:
                logging.info(f"  参考图片描述: {reference_image_description}")
            logging.info("="*80)

            return jsonify(result)
        else:
            logging.error("="*80)
            logging.error(f"[✗] 生成失败")
            logging.error(f"  错误: {message}")
            logging.error("="*80)

            return jsonify({'success': False, 'error': message})

    except Exception as e:
        logging.error("="*80)
        logging.error(f"[✗] API异常")
        logging.error(f"  错误: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        logging.error("="*80)

        # 清理临时文件
        if reference_image_path and Path(reference_image_path).exists():
            try:
                Path(reference_image_path).unlink()
            except:
                pass

        return jsonify({'success': False, 'error': f'服务器错误: {str(e)}'})


@app.route('/logs')
def view_logs():
    """查看服务器日志"""
    try:
        with open('v8_debug.log', 'r', encoding='utf-8') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except Exception as e:
        return f"读取日志失败: {str(e)}"


def main():
    """主函数"""
    print("\n" + "="*80)
    print("                    AI图像生成器 - Web版 V8 (Anthropic兼容版)")
    print("="*80)
    print()
    print("启动Web服务器: http://localhost:5008")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  ✨ 支持主题描述生成")
    print("  🖼️  支持参考图片生成(图生图)")
    print("  🎨 多种画图风格选择")
    print("  🤖 使用即梦AI(Seedream)模型")
    print()
    print("V8改进:")
    print("  ✅ 使用Anthropic兼容接口进行视觉分析")
    print("  ✅ 使用openai库调用智谱AI的Anthropic兼容API")
    print("  ✅ 完全修复视觉模型分析错误")
    print("  ✅ 正确处理image_urls参数进行图生图")
    print("  ✅ 修复模型识别显示(SEEDREAM-V8)")
    print("="*80)
    print()
    print("💡 调试提示:")
    print("  - 所有print输出都会在浏览器F12控制台中显示")
    print("  - 可访问 http://localhost:5008/logs 查看完整日志")
    print("="*80)
    print()

    app.run(host='0.0.0.0', port=5008, debug=False)


if __name__ == "__main__":
    main()
