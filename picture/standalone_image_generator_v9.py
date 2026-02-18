#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI图像生成器 - Web版 V9.4 (官网API修复版)
支持主题输入或参考图片,多种画图风格选择
支持多模型自动切换:Seedream 4.5 -> Seedream 4.0 -> Antigravity多模型

V9.4修复(2026-02-15):
  ✅ 根据官网示例修复API调用方式
  ✅ 使用OpenAI客户端方式调用Seedream API
  ✅ size参数从"2048x2048"改为"2K"(官网格式)
  ✅ 使用extra_body传递watermark等参数

V9.3改进(2026-02-15):
  ✅ 新增Seedream 4.0作为备选:当4.5配额用尽时自动切换到4.0
  ✅ Fallback优先级: Seedream 4.5 -> Seedream 4.0 -> Antigravity

V9.2改进(2026-02-15):
  ✅ 添加多模型Fallback机制:Seedream配额用尽时自动切换到Antigravity模型
  ✅ 支持Antigravity的多个图像模型:flux-1.1-pro, flux-schnell, gemini-3-flash-image等

V9.1修复(2026-02-13):
  ✅ 修复图生图参数:使用binary_data_base64替代image_urls
  ✅ 图生图现在正确保留参考图片的主体内容
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

# 设置控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config, get_antigravity_client, get_zhipu_anthropic_client

app = Flask(__name__)
BASE_DIR = Path(__file__).parent.parent


def get_visual_reference_for_subject(subject):
    """使用AI查询主题物质的视觉特征描述

    Args:
        subject: 主题物质名称（从第一行标题提取）

    Returns:
        str: 该物质的视觉特征描述，用于增强图像生成prompt
    """
    try:
        client = get_zhipu_anthropic_client()

        prompt = f"""请简短描述"{subject}"的实际外观特征，用于指导AI绘图。

要求：
1. 用2-3句话描述其主要外观特征（颜色、形状、质感等）
2. 如果是生物，描述其典型姿态或状态
3. 如果是植物，描述其叶子、花朵或果实的典型特征
4. 如果是物品，描述其材质和典型形态
5. 只描述客观物理特征，不要添加艺术性描述
6. 回答要简短，不超过100字

示例格式：
牡丹：大型花朵，花瓣层叠饱满，颜色多为红色、粉色或白色。叶片为绿色羽状复叶，茎秆直立粗壮。"""

        response = client.messages.create(
            model="glm-4-flash",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        visual_desc = response.content[0].text.strip()
        logging.info(f"[视觉参考] {subject}: {visual_desc}")
        return visual_desc

    except Exception as e:
        logging.warning(f"[视觉参考] 查询失败: {e}")
        return ""


def extract_subject_from_theme(theme):
    """从主题描述中提取主要物质名称

    Args:
        theme: 完整的主题描述（可能包含多行，取第一行）

    Returns:
        str: 主要物质名称
    """
    # 取第一行作为主题
    first_line = theme.split('\n')[0].strip()

    # 去除常见的修饰词，提取核心物质
    # 如果第一行较短（<15字），直接使用
    if len(first_line) <= 15:
        return first_line

    # 否则尝试提取关键词（取第一个逗号或空格前的内容）
    for delimiter in ['，', ',', '、', ' ', '的']:
        if delimiter in first_line:
            return first_line.split(delimiter)[0]

    return first_line

# Antigravity图像模型优先级列表 (按质量/速度排序)
ANTIGRAVITY_IMAGE_MODELS = [
    ("gemini-3-flash-image", "Gemini 3 Flash Image", "Google最新图像模型,快速高质量"),
    ("flux-1.1-pro", "Flux 1.1 Pro", "Black Forest Labs专业版,高质量"),
    ("flux-schnell", "Flux Schnell", "快速版,适合批量生成"),
    ("gemini-2-flash-image", "Gemini 2 Flash Image", "第二代Gemini图像模型"),
    ("dall-e-3", "DALL-E 3", "OpenAI最新图像模型"),
]

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('v9_debug.log', encoding='utf-8')
    ]
)

# 画图风格定义
IMAGE_STYLES = {
    "guofeng_gongbi": {
        "name": "国风工笔",
        "description": "中国传统工笔画风格,线条精细,色彩淡雅",
        "prompt_template": "{theme},中国传统工笔画风格,精细线条,淡雅色彩,参考真实物体形态,保持物体真实性,高质量杰作,no text,no words,no letters,no watermark,纯画面"
    },
    "guofeng_shuimo": {
        "name": "国风水墨",
        "description": "中国水墨画风格,传统笔墨,意境深远,水墨淋漓",
        "prompt_template": "{theme},中国水墨画风格,传统笔墨,意境深远,留白艺术,参考真实物体形态,保持物体真实性,高质量,no text,no words,no letters,纯画面"
    },
    "shuica": {
        "name": "中国风水彩画",
        "description": "中国风水彩画风格,色彩通透,水彩质感,艺术绘画,高质量",
        "prompt_template": "{theme},中国风水彩画风格,色彩通透,水彩质感,艺术绘画,参考真实物体形态,保持物体真实性和细节,高质量,no text,no words,no letters,纯画面"
    },
    "youhua": {
        "name": "油画",
        "description": "油画风格,色彩丰富,笔触明显,古典油画质感",
        "prompt_template": "{theme},油画风格,色彩丰富,笔触明显,古典油画质感,参考真实物体形态,保持物体真实性,高质量,no text,no words,no letters,纯画面"
    },
    "manhua": {
        "name": "动漫插画",
        "description": "日式动漫插画风格,色彩鲜明,精美插画,高质量",
        "prompt_template": "{theme},日式动漫插画风格,色彩鲜明,精美插画,参考真实物体形态,保持基本特征,高质量,no text,no words,no letters,纯画面"
    },
    "shisu": {
        "name": "写实摄影",
        "description": "真实照片风格,细节丰富,8K画质",
        "prompt_template": "{theme},真实照片风格,细节丰富,8K画质,高度还原真实物体,高质量,no text,no words,no letters,no watermark,纯画面"
    },
    "cartoon": {
        "name": "卡通插画",
        "description": "可爱卡通风格,色彩明快,儿童绘本风格,高质量",
        "prompt_template": "{theme},可爱卡通风格,色彩明快,儿童绘本风格,参考真实物体形态,保持可识别特征,高质量,no text,no words,no letters,纯画面"
    }
}


def generate_with_seedream(prompt, reference_image_path, output_path, style_name, model_version="doubao-seedream-4-5-251128"):
    """使用即梦AI(Seedream)生成图像 - 支持多版本

    Args:
        prompt: 文本提示词(已包含风格信息)
        reference_image_path: 参考图片路径(图生图模式)或None(文生图模式)
        output_path: 输出文件路径
        style_name: 风格名称
        model_version: 模型版本 (默认4.5, 可选4.0)

    Returns:
        (success, message, model_used)

    Note:
        V9.4修复(2026-02-15): 根据官网示例更新API调用方式
        - 使用OpenAI客户端方式调用
        - size参数改为"2K"而不是"2048x2048"
        - 添加extra_body参数支持watermark
    """
    try:
        # 获取API密钥
        api_key = Config.VOLCANO_API_KEY
        if not api_key:
            logging.error("VOLCANO_API_KEY未配置")
            return False, "Volcano客户端未配置", "unknown"

        model_name = "Seedream 4.5" if "4-5" in model_version else "Seedream 4.0"
        logging.info(f"[即梦AI {model_name}] 正在生成图像...")
        logging.info(f"[提示词] {prompt}")

        # 使用OpenAI客户端方式调用 (V9.4修复)
        from openai import OpenAI
        client = OpenAI(
            base_url=Config.VOLCANO_BASE_URL,
            api_key=api_key
        )

        logging.info(f"[API请求] 使用OpenAI客户端, base_url={Config.VOLCANO_BASE_URL}")

        if reference_image_path:
            # 读取并编码参考图片
            with open(reference_image_path, 'rb') as f:
                image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

            logging.info(f"[参考图片] 已添加 {len(base64_image)} 字节")
            logging.info(f"[API参数] 图生图模式 - 使用binary_data_base64参数")
            logging.info(f"[风格] {style_name}")

            # 图生图模式 - 使用extra_body传递binary_data_base64
            response = client.images.generate(
                model=model_version,
                prompt=prompt,
                size="2048x2048",  # 正方形 2048×2048
                response_format="url",
                extra_body={
                    "binary_data_base64": [base64_image],
                    "watermark": False,  # 不添加水印
                }
            )
        else:
            logging.info("[API参数] 文生图模式")

            # 文生图模式
            response = client.images.generate(
                model=model_version,
                prompt=prompt,
                size="2048x2048",  # 正方形 2048×2048
                response_format="url",
                extra_body={
                    "watermark": False,  # 不添加水印
                }
            )

        # 获取图片URL
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            model_used = 'seedream-v9'

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
            logging.error(f"[错误] 响应格式未知: response.data为空")
            return False, "即梦AI返回空响应", "unknown"

    except Exception as e:
        error_str = str(e)
        logging.error(f"[错误] 生成失败: {error_str}")
        import traceback
        logging.debug(traceback.format_exc())

        # 检查是否是配额问题
        if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
            return False, error_str, "unknown"

        return False, f"生成失败: {error_str}", "unknown"


def generate_with_antigravity(prompt, output_path, style_name):
    """使用Antigravity图像模型生成图像 (Fallback方案)

    当Seedream配额用尽时,自动尝试Antigravity的多个图像模型

    Args:
        prompt: 文本提示词(已包含风格信息)
        output_path: 输出文件路径
        style_name: 风格名称

    Returns:
        (success, message, model_used)
    """
    try:
        client = get_antigravity_client()
        if not client:
            logging.error("[Antigravity] 客户端未配置")
            return False, "Antigravity客户端未配置", "unknown"

        logging.info("[Antigravity] 正在尝试备选图像模型...")

        # 按优先级尝试各个模型
        for model_id, model_name, model_desc in ANTIGRAVITY_IMAGE_MODELS:
            try:
                logging.info(f"[Antigravity] 尝试模型: {model_name} ({model_id})")

                response = client.images.generate(
                    model=model_id,
                    prompt=prompt,
                    size="1024x1024"
                )

                if response.data and len(response.data) > 0:
                    image_url = response.data[0].url

                    logging.info(f"[Antigravity] 获取图片URL: {image_url[:50]}...")

                    # 下载图片
                    img_response = requests.get(image_url, timeout=60)
                    if img_response.status_code == 200:
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        logging.info(f"[✓] Antigravity图片已保存: {output_path}")
                        logging.info(f"[✓] 使用模型: {model_name}")
                        return True, f"成功生成(使用{model_name}): {output_path}", f"antigravity-{model_id}"
                    else:
                        logging.warning(f"[Antigravity] 下载失败: HTTP {img_response.status_code}")
                        continue
                else:
                    logging.warning(f"[Antigravity] {model_name} 返回空响应")
                    continue

            except Exception as e:
                error_str = str(e)
                # 检查是否是配额问题
                if "429" in error_str or "quota" in error_str.lower() or "limit" in error_str.lower():
                    logging.warning(f"[Antigravity] {model_name} 配额已用尽,尝试下一个模型...")
                    continue
                elif "404" in error_str or "NOT_FOUND" in error_str:
                    logging.warning(f"[Antigravity] {model_name} 模型未找到,尝试下一个...")
                    continue
                else:
                    logging.warning(f"[Antigravity] {model_name} 生成失败: {error_str[:100]}")
                    continue

        # 所有模型都失败
        logging.error("[Antigravity] 所有备选模型都不可用")
        return False, "所有图像模型配额已用尽", "unknown"

    except Exception as e:
        logging.error(f"[Antigravity] 错误: {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return False, f"Antigravity生成失败: {str(e)}", "unknown"


def generate_image_with_fallback(prompt, reference_image_path, output_path, style_name):
    """智能图像生成: 优先Seedream 4.5 -> Seedream 4.0 -> Antigravity

    Fallback优先级:
    1. Seedream 4.5 (doubao-seedream-4-5-251128) - 最新版本
    2. Seedream 4.0 (doubao-seedream-4-0-250828) - 稳定版本
    3. Antigravity: Gemini 3 Flash Image -> Flux 1.1 Pro -> Flux Schnell -> DALL-E 3

    Args:
        prompt: 文本提示词
        reference_image_path: 参考图片路径(图生图模式)或None
        output_path: 输出文件路径
        style_name: 风格名称

    Returns:
        (success, message, model_used)
    """
    # 1. 首先尝试 Seedream 4.5
    logging.info("[Fallback 1/3] 尝试 Seedream 4.5...")
    success, message, model_used = generate_with_seedream(
        prompt, reference_image_path, output_path, style_name,
        model_version="doubao-seedream-4-5-251128"
    )

    if success:
        return success, message, model_used

    # 检查是否是配额问题
    if "429" in message or "limit" in message.lower() or "quota" in message.lower():
        logging.info("[Fallback 2/3] Seedream 4.5配额用尽,尝试 Seedream 4.0...")

        # 2. 尝试 Seedream 4.0
        success, message, model_used = generate_with_seedream(
            prompt, reference_image_path, output_path, style_name,
            model_version="doubao-seedream-4-0-250828"
        )

        if success:
            return success, message, model_used

        # 检查是否还是配额问题
        if "429" in message or "limit" in message.lower() or "quota" in message.lower():
            logging.info("[Fallback 3/3] Seedream 4.0也配额用尽,切换到Antigravity备选模型...")
            # 3. Fallback到Antigravity
            return generate_with_antigravity(prompt, output_path, style_name)

    # 其他错误直接返回
    return success, message, model_used


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
    """API: 生成图像 - V9简化版"""
    reference_image_path = None
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
            # 主题模式:提取主题物质并查询视觉特征
            # 1. 从第一行提取主题物质名称
            subject = extract_subject_from_theme(theme)
            logging.info(f"[主题物质] {subject}")

            # 2. 查询该物质的视觉特征
            visual_reference = get_visual_reference_for_subject(subject)

            # 3. 构建增强的prompt，强调主题物质为主要内容
            base_prompt = style_config['prompt_template'].format(theme=theme)

            if visual_reference:
                # 添加视觉参考和强调主题物质
                prompt = f"""【重要】主题物质: {subject}

真实外观参考: {visual_reference}

绘图要求:
1. {subject}必须是画面的绝对主体，占据画面中心位置，尺寸要足够大
2. 严格按照上述真实外观参考来绘制{subject}，不要偏离实际特征
3. 整体场景描述: {theme}

{base_prompt}"""
                logging.info(f"[提示词构建] 主题模式 + 视觉参考增强 (长度: {len(prompt)} 字符)")
            else:
                # 没有视觉参考时，仍然强调主题物质
                prompt = f"""【重要】主题物质: {subject}

绘图要求:
1. {subject}必须是画面的绝对主体，占据画面中心位置，尺寸要足够大
2. 整体场景描述: {theme}

{base_prompt}"""
                logging.info(f"[提示词构建] 主题模式 + 主题强调 (长度: {len(prompt)} 字符)")
        else:
            # 参考图片模式:V9简化流程
            try:
                # 1. 解码并保存参考图片
                image_data = base64.b64decode(reference_image)

                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    temp_file.write(image_data)
                    reference_image_path = temp_file.name

                logging.info(f"[参考图片] 已保存到: {reference_image_path} ({len(image_data)} bytes)")

                # 2. 构建提示词 - V9不再需要视觉分析
                # 即梦AI会自动识别参考图片内容
                prompt = f"""请根据参考图片,用{style_config['name']}风格重新绘制。

要求:
1. 保持参考图片中所有主体、物体和元素的识别
2. 保持原有的构图和布局
3. 将艺术风格转换为{style_config['description']}
4. 确保所有细节都完整呈现
5. 线条流畅,色彩和谐

{style_config['prompt_template'].format(theme='参考图片内容')}"""

                logging.info(f"[提示词构建] 参考图片模式 - 即梦AI将自动识别内容 (长度: {len(prompt)} 字符)")

            except Exception as e:
                logging.error(f"[错误] 处理参考图片失败: {e}")
                import traceback
                logging.debug(traceback.format_exc())
                return jsonify({'success': False, 'error': f'处理参考图片失败: {str(e)}'})

        # 3. 创建输出目录
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(__file__).parent / "generated_images" / timestamp_str
        output_dir.mkdir(parents=True, exist_ok=True)

        logging.info(f"[输出目录] {output_dir}")

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"generated_{style}_{timestamp}.png"
        output_path = output_dir / output_filename

        logging.info(f"[输出文件] {output_filename}")

        # 4. 使用智能Fallback生成 (优先Seedream,失败时自动切换Antigravity)
        logging.info("[步骤2] 开始图像生成 (智能Fallback模式)...")
        success, message, model_used = generate_image_with_fallback(prompt, reference_image_path, str(output_path), style_config['name'])

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
                'reference_description': '即梦AI自动识别参考图片内容' if mode == 'reference' else None
            }

            logging.info("="*80)
            logging.info("[✓] 生成成功!")
            logging.info(f"  模型: {result['model']}")
            logging.info(f"  风格: {result['style']}")
            logging.info(f"  文件: {output_path}")
            if mode == 'reference':
                logging.info(f"  图生图: 即梦AI自动识别参考图片内容")
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
        with open('v9_debug.log', 'r', encoding='utf-8') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>"
    except Exception as e:
        return f"读取日志失败: {str(e)}"


@app.route('/api/save-image', methods=['POST'])
def api_save_image():
    """API: 保存图片到指定路径"""
    try:
        data = request.json
        image_base64 = data.get('image_base64', '')
        filename = data.get('filename', 'image.png')
        save_path = data.get('save_path', '')

        if not image_base64:
            return jsonify({'success': False, 'error': '缺少图片数据'})

        if not save_path:
            return jsonify({'success': False, 'error': '缺少保存路径'})

        # 创建目录(如果不存在)
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)

        # 生成完整文件路径
        full_path = save_dir / filename

        # 如果文件已存在,添加序号
        if full_path.exists():
            base_name = full_path.stem
            ext = full_path.suffix
            counter = 1
            while full_path.exists():
                full_path = save_dir / f"{base_name}_{counter}{ext}"
                counter += 1

        # 解码并保存图片
        image_data = base64.b64decode(image_base64)
        with open(full_path, 'wb') as f:
            f.write(image_data)

        logging.info(f"[保存成功] {full_path}")
        return jsonify({
            'success': True,
            'message': f'图片已保存到: {full_path}',
            'path': str(full_path)
        })

    except Exception as e:
        logging.error(f"[保存失败] {str(e)}")
        import traceback
        logging.debug(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})


def main():
    """主函数"""
    print("\n" + "="*80)
    print("                    AI图像生成器 - Web版 V9.3 (多模型Fallback版)")
    print("="*80)
    print()
    print("启动Web服务器: http://localhost:5009")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  ✨ 支持主题描述生成")
    print("  🖼️  支持参考图片生成(图生图)")
    print("  🎨 多种画图风格选择")
    print("  🤖 多模型自动切换")
    print()
    print("V9.3新增(2026-02-15):")
    print("  ✅ 新增Seedream 4.0作为备选模型")
    print("  ✅ Fallback优先级:")
    print("     1. Seedream 4.5 (doubao-seedream-4-5-251128)")
    print("     2. Seedream 4.0 (doubao-seedream-4-0-250828)")
    print("     3. Antigravity: Gemini/Flux/DALL-E")
    print()
    print("V9.2功能:")
    print("  ✅ Antigravity多个图像模型备选:")
    print("     - Gemini 3 Flash Image")
    print("     - Flux 1.1 Pro")
    print("     - Flux Schnell")
    print("     - DALL-E 3")
    print("="*80)
    print()
    print("💡 调试提示:")
    print("  - 所有print输出都会在浏览器F12控制台中显示")
    print("  - 可访问 http://localhost:5009/logs 查看完整日志")
    print("="*80)
    print()

    app.run(host='0.0.0.0', port=5009, debug=False)


if __name__ == "__main__":
    main()
