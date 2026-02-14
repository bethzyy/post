#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI图像生成器 - Web版
支持主题输入或参考图片,多种画图风格选择
使用即梦AI(Seedream)模型生成图像
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import base64
import requests
from io import BytesIO

# 设置控制台输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_volcano_client, get_antigravity_client


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


def generate_with_seedream(prompt, output_path):
    """使用即梦AI(Seedream)生成图像"""
    try:
        client = get_volcano_client()
        if not client:
            return False, "Volcano客户端未配置,请检查.env中的VOLCANO_API_KEY"

        print("[即梦AI] 正在生成图像...")
        print(f"[提示词] {prompt}")

        # 清理prompt编码
        try:
            prompt = prompt.encode('utf-8', errors='replace').decode('utf-8')
        except:
            pass

        # 使用即梦AI(Seedream)生成图像
        response = client.images.generate(
            model="doubao-seedream-4-5-251128",
            prompt=prompt,
            size="2K",
            response_format="url",
            extra_body={
                "watermark": False,  # 关闭AI水印
            }
        )

        # 检查返回结果
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url

            # 下载图像
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
        return False, f"生成失败: {str(e)}"


def generate_with_gemini(prompt, output_path):
    """使用Gemini生成图像(备选方案)"""
    try:
        client = get_antigravity_client()
        if not client:
            return False, "Anti-gravity客户端未配置"

        print("[Gemini] 正在生成图像...")

        # 使用Gemini图像生成模型
        response = client.images.generate(
            model="gemini-3-pro-image-2k",
            prompt=prompt,
            size="2K"
        )

        # 检查返回结果
        if response.data and len(response.data) > 0 and response.data[0].url:
            image_url = response.data[0].url
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


def main():
    """主函数 - 从标准输入读取JSON参数"""

    print("\n" + "="*80)
    print("AI图像生成器 - Web版")
    print("="*80 + "\n")

    # 读取标准输入
    input_data = sys.stdin.read()

    if not input_data:
        print("[错误] 未接收到输入数据")
        result = {
            'success': False,
            'error': '未接收到输入数据'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        # 解析JSON输入
        params = json.loads(input_data)

        mode = params.get('mode', 'theme')  # 'theme' 或 'reference'
        theme = params.get('theme', '')
        reference_image = params.get('reference_image', '')  # base64编码的图片
        style = params.get('style', 'guofeng_gongbi')

        # 验证参数
        if mode == 'theme' and not theme:
            result = {
                'success': False,
                'error': '主题模式需要输入主题描述'
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        if mode == 'reference' and not reference_image:
            result = {
                'success': False,
                'error': '参考图片模式需要上传参考图片'
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return

        # 获取风格配置
        style_config = IMAGE_STYLES.get(style, IMAGE_STYLES['guofeng_gongbi'])

        print(f"[模式] {'主题描述' if mode == 'theme' else '参考图片'}")
        print(f"[风格] {style_config['name']}")
        print(f"[风格描述] {style_config['description']}")

        # 构建提示词
        if mode == 'theme':
            # 主题模式:直接使用用户输入的主题
            prompt = style_config['prompt_template'].format(theme=theme)
            print(f"[主题] {theme}")
        else:
            # 参考图片模式:需要图片分析(这里简化处理,假设主题从图片内容推断)
            # 实际应用中可以使用视觉模型分析参考图片
            prompt = style_config['prompt_template'].format(theme="根据参考图片生成相同风格的艺术作品")
            print(f"[参考图片] 已上传({len(reference_image)} bytes)")

        print(f"[最终提示词] {prompt}\n")

        # 创建输出目录
        output_dir = Path(__file__).parent / "generated_images" / datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"generated_{style}_{timestamp}.png"
        output_path = output_dir / output_filename

        # 优先使用即梦AI(Seedream),失败则使用Gemini
        success, message = generate_with_seedream(prompt, str(output_path))

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
                'prompt': prompt,
                'image_path': str(output_path),
                'image_filename': output_filename,
                'image_base64': image_base64,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            print(f"\n[✓] {message}")
            print(f"[输出] {output_path}")
            print(f"[模型] {result['model'].upper()}")
            print(f"[风格] {style_config['name']}\n")
        else:
            result = {
                'success': False,
                'error': message
            }
            print(f"\n[✗] {message}\n")

        # 输出JSON结果
        print("="*80)
        print("生成完成!")
        print("="*80)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except json.JSONDecodeError as e:
        result = {
            'success': False,
            'error': f'JSON解析错误: {str(e)}'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        result = {
            'success': False,
            'error': f'未知错误: {str(e)}'
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
