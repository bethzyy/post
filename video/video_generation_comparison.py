#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
视频生成对比工具
支持多个视频生成模型,对同一主题生成视频并AI点评排序
"""

import sys
import os
from pathlib import Path
import json
import requests
from datetime import datetime
import subprocess
import tempfile

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_zhipuai_client


# 视频生成模型配置(仅包含真正支持视频生成的模型)
VIDEO_GENERATION_MODELS = {
    'dalle-animation': {
        'name': 'DALL-E 3 + FFmpeg动画',
        'description': '使用DALL-E生成图片,FFmpeg创建缩放动画效果',
        'provider': 'OpenAI + FFmpeg',
        'type': 'img-to-video',
        'enabled': True  # 可用,等待API配额恢复
    },
    'seedance': {
        'name': 'Seedance 1.5 Pro (火山引擎)',
        'description': '火山引擎豆包最新视频生成模型,支持文字转视频+音频',
        'provider': 'Volcano Engine',
        'type': 'text-to-video',
        'enabled': True  # 已开通,使用VOLCANO_API_KEY
    },
    'gemini-veo': {
        'name': 'Gemini Veo 3.1 (Google)',
        'description': 'Google最新视频生成模型,支持8秒高清视频生成',
        'provider': 'Google',
        'type': 'text-to-video',
        'enabled': False  # 需要Google Cloud API key
    }
}


def generate_with_pollinations(prompt, output_path):
    """使用Pollinations.ai生成图片(注意:实际返回图片而非视频)"""

    try:
        print(f"[Pollinations Image] 正在生成图片...")
        print(f"  提示词: {prompt[:100]}...")

        # 编码提示词
        encoded_prompt = requests.utils.quote(prompt)

        # Pollinations图片API
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=123&nologo=true&enh=true"

        # 请求图片
        response = requests.get(image_url, timeout=120)

        if response.status_code == 200:
            # 保存文件
            with open(output_path, 'wb') as f:
                f.write(response.content)

            file_size = len(response.content)

            # 检查文件类型
            file_type = "unknown"

            # 检查JPEG
            if response.content[:2] == b'\xff\xd8':
                file_type = "jpeg"
            # 检查PNG
            elif b'PNG' in response.content[:100]:
                file_type = "png"
            # 检查GIF
            elif response.content[:6] in [b'GIF87a', b'GIF89a']:
                file_type = "gif"
            # 检查MP4
            elif b'ftypmp42' in response.content[:100] or b'ftypisom' in response.content[:100]:
                file_type = "mp4"

            print(f"[成功] 文件已保存: {output_path}")
            print(f"  大小: {file_size} bytes")
            print(f"  类型: {file_type}")

            return {
                'success': True,
                'file_path': str(output_path),
                'file_size': file_size,
                'file_type': file_type,
                'message': f"成功生成 {file_type.upper()} 文件"
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}",
                'message': f"请求失败: {response.status_code}"
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'timeout',
            'message': '请求超时(120秒)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"生成失败: {str(e)[:100]}"
        }


def generate_video_with_dalle_first(prompt, output_path):
    """先生成DALL-E图片,然后转换为简单动画"""

    try:
        print(f"[DALL-E + 动画] 正在生成...")

        # 第一步: 生成图片
        from config import get_antigravity_client
        client = get_antigravity_client()

        if not client:
            return {
                'success': False,
                'error': 'no_client',
                'message': '无法获取anti-gravity客户端'
            }

        print(f"  [1/2] 生成基础图片...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        if not response.data or len(response.data) == 0:
            return {
                'success': False,
                'error': 'no_image',
                'message': 'DALL-E生成失败'
            }

        # 保存图片
        import base64
        image_data = response.data[0]

        if hasattr(image_data, 'b64_json') and image_data.b64_json:
            img_bytes = base64.b64decode(image_data.b64_json)
        elif hasattr(image_data, 'url') and image_data.url:
            img_response = requests.get(image_data.url)
            img_bytes = img_response.content
        else:
            return {
                'success': False,
                'error': 'no_data',
                'message': '无法获取图片数据'
            }

        temp_image = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_image.write(img_bytes)
        temp_image_path = temp_image.name
        temp_image.close()

        print(f"  [2/2] 创建视频动画...")

        # 第二步: 使用FFmpeg创建简单动画(缩放效果)
        try:
            # 创建5秒视频,图片缓慢放大
            ffmpeg_cmd = [
                'ffmpeg', '-y',
                '-loop', '1',
                '-i', temp_image_path,
                '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,zoompan=z=\'min(zoom+0.0015,1.5)\':d=700:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':fps=30',
                '-c:v', 'libx264',
                '-t', '5',
                '-pix_fmt', 'yuv420p',
                str(output_path)
            ]

            result = subprocess.run(
                ffmpeg_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            # 清理临时文件
            os.unlink(temp_image_path)

            if result.returncode == 0 and Path(output_path).exists():
                file_size = Path(output_path).stat().st_size
                print(f"[成功] 视频已生成: {output_path}")
                print(f"  大小: {file_size} bytes")

                return {
                    'success': True,
                    'file_path': str(output_path),
                    'file_size': file_size,
                    'file_type': 'mp4',
                    'message': 'DALL-E图片 + FFmpeg动画'
                }
            else:
                os.unlink(temp_image_path)
                return {
                    'success': False,
                    'error': 'ffmpeg_failed',
                    'message': 'FFmpeg视频创建失败'
                }

        except FileNotFoundError:
            os.unlink(temp_image_path)
            return {
                'success': False,
                'error': 'ffmpeg_not_found',
                'message': 'FFmpeg未安装,无法创建视频'
            }
        except Exception as e:
            os.unlink(temp_image_path)
            return {
                'success': False,
                'error': str(e),
                'message': f'视频创建失败: {str(e)[:100]}'
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"生成失败: {str(e)[:100]}"
        }


def generate_video_with_seedance(prompt, output_path):
    """使用Seedance 1.5 Pro(火山引擎)生成视频"""

    try:
        print(f"[Seedance 1.5 Pro] 正在生成视频...")
        print(f"  提示词: {prompt[:100]}...")

        import os
        volcano_api_key = os.environ.get('VOLCANO_API_KEY', '')

        if not volcano_api_key:
            return {
                'success': False,
                'error': 'no_api_key',
                'message': '未配置VOLCANO_API_KEY'
            }

        # 火山引擎Seedance视频生成API端点 (正确路径)
        api_url = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"

        headers = {
            'Authorization': f'Bearer {volcano_api_key}',
            'Content-Type': 'application/json'
        }

        # 构建请求payload (按照官方文档格式)
        payload = {
            "model": "doubao-seedance-1-5-pro-251215",  # Seedance 1.5 Pro最新模型
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ],
            "resolution": "720p",      # 分辨率: 480p/720p/1080p
            "ratio": "16:9",           # 宽高比: 16:9/4:3/1:1等
            "duration": 5,             # 视频时长(秒): 4-12秒
            "watermark": False,        # 不添加水印
            "generate_audio": True,    # 生成音频(Seedance 1.5 Pro新功能)
            "draft": False            # 非样片模式,生成正式视频
        }

        print(f"  [请求] 调用火山引擎Seedance 1.5 Pro API...")
        print(f"  [配置] 分辨率:720p, 时长:5秒, 带音频")
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)

        if response.status_code == 200:
            result = response.json()

            # 获取任务ID
            task_id = result.get('id')
            if not task_id:
                return {
                    'success': False,
                    'error': 'no_task_id',
                    'message': '未返回任务ID'
                }

            print(f"  [任务ID] {task_id}")
            print(f"  [轮询] 等待视频生成...")

            # 轮询检查状态
            max_attempts = 120  # 最多轮询120次(10分钟)
            import time

            for attempt in range(max_attempts):
                time.sleep(5)  # 等待5秒

                # 查询任务状态
                status_url = f"https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"
                status_response = requests.get(status_url, headers=headers, timeout=30)

                if status_response.status_code == 200:
                    status_result = status_response.json()
                    status = status_result.get('status', 'unknown')

                    if status == 'succeeded':
                        # 成功,获取视频URL
                        # 注意: video_url在content对象里面
                        content = status_result.get('content', {})
                        video_url = content.get('video_url')
                        if not video_url:
                            return {
                                'success': False,
                                'error': 'no_video_url',
                                'message': '任务成功但未返回视频URL'
                            }

                        print(f"  [下载] 正在下载视频...")
                        video_response = requests.get(video_url, timeout=120)

                        if video_response.status_code == 200:
                            with open(output_path, 'wb') as f:
                                f.write(video_response.content)

                            file_size = len(video_response.content)
                            print(f"[成功] 视频已保存: {output_path}")
                            print(f"  大小: {file_size} bytes")

                            return {
                                'success': True,
                                'file_path': str(output_path),
                                'file_size': file_size,
                                'file_type': 'mp4',
                                'message': 'Seedance 1.5 Pro视频生成成功(含音频)'
                            }
                        else:
                            return {
                                'success': False,
                                'error': 'download_failed',
                                'message': f'视频下载失败: {video_response.status_code}'
                            }

                    elif status == 'failed':
                        error_msg = status_result.get('error_message', '视频生成失败')
                        return {
                            'success': False,
                            'error': 'generation_failed',
                            'message': f'任务失败: {error_msg}'
                        }

                    elif status in ['queued', 'running']:
                        if (attempt + 1) % 6 == 0:  # 每30秒显示一次进度
                            print(f"  [轮询] {attempt+1}/{max_attempts} - 状态: {status}")
                    else:
                        print(f"  [轮询] {attempt+1}/{max_attempts} - 状态: {status}")
                else:
                    print(f"  [警告] 查询状态失败: {status_response.status_code}")

            return {
                'success': False,
                'error': 'timeout',
                'message': '视频生成超时(10分钟)'
            }
        else:
            # API返回错误
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', str(response.text))
            except:
                error_msg = str(response.text)[:200]

            return {
                'success': False,
                'error': f'api_error_{response.status_code}',
                'message': f'API错误({response.status_code}): {error_msg}'
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'timeout',
            'message': '请求超时'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"生成失败: {str(e)[:100]}"
        }


def generate_video_with_gemini_veo(prompt, output_path):
    """使用Gemini Veo 3.1生成视频"""

    try:
        print(f"[Gemini Veo 3.1] 正在生成视频...")
        print(f"  提示词: {prompt[:100]}...")

        # Gemini Veo需要Google Cloud API key
        # 不在antigravity下,需要直接使用Google API
        import os
        gemini_api_key = os.environ.get('GEMINI_API_KEY', '')

        if not gemini_api_key:
            return {
                'success': False,
                'error': 'no_api_key',
                'message': '未配置GEMINI_API_KEY (需要Google Cloud API key)'
            }

        # Gemini Veo API端点
        # 注意: Veo使用Google's generative-ai SDK
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=gemini_api_key)

            print(f"  [请求] 调用Gemini Veo 3.1 API...")
            print(f"  [提示] 视频生成是异步操作,可能需要几分钟...")

            # 创建视频生成操作
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                config=types.GenerateVideoConfig(
                    duration_seconds=8,  # 8秒视频
                    resolution="720p",   # 720p分辨率
                    aspect_ratio="16:9"
                )
            )

            # 轮询直到完成
            print(f"  [轮询] 等待视频生成...")
            max_attempts = 60  # 最多轮询60次(10分钟)
            import time

            for attempt in range(max_attempts):
                if operation.done:
                    break

                time.sleep(10)  # 等待10秒
                print(f"  [轮询] {attempt+1}/{max_attempts} - 生成中...")

            if not operation.done:
                return {
                    'success': False,
                    'error': 'timeout',
                    'message': '视频生成超时(10分钟)'
                }

            # 获取生成的视频
            if hasattr(operation.response, 'generated_videos') and len(operation.response.generated_videos) > 0:
                video = operation.response.generated_videos[0]

                # 下载视频
                if hasattr(video, 'video'):
                    client.files.download(file=video.video)
                    video.video.save(str(output_path))

                    file_size = Path(output_path).stat().st_size
                    print(f"[成功] 视频已保存: {output_path}")
                    print(f"  大小: {file_size} bytes")

                    return {
                        'success': True,
                        'file_path': str(output_path),
                        'file_size': file_size,
                        'file_type': 'mp4',
                        'message': 'Gemini Veo 3.1视频生成成功'
                    }

            return {
                'success': False,
                'error': 'no_video',
                'message': '未返回生成的视频'
            }

        except ImportError:
            return {
                'success': False,
                'error': 'no_sdk',
                'message': '需要安装google-generativeai SDK: pip install google-generativeai'
            }

    except Exception as e:
        error_str = str(e)
        # 检查是否是API key错误
        if 'API key' in error_str or 'auth' in error_str.lower():
            return {
                'success': False,
                'error': 'auth_failed',
                'message': 'Gemini API key验证失败'
            }
        else:
            return {
                'success': False,
                'error': str(e),
                'message': f"生成失败: {error_str[:100]}"
            }


# ==================== AI评价函数 ====================


def ai_evaluate_videos(prompt, video_results):
    """使用AI评价生成的视频"""

    try:
        print(f"\n[AI评价] 正在分析视频质量...")

        client = get_zhipuai_client()
        if not client:
            print("[警告] 无法获取ZhipuAI客户端,跳过AI评价")
            return None

        # 构建评价提示
        evaluation_prompt = f"""请评价以下视频生成结果,根据提示词质量和创意进行评分排序。

提示词: {prompt}

生成的视频结果:
"""

        for i, result in enumerate(video_results, 1):
            if result['success']:
                evaluation_prompt += f"\n{i}. {result['model_name']}\n"
                evaluation_prompt += f"   - 文件: {Path(result['file_path']).name}\n"
                evaluation_prompt += f"   - 大小: {result.get('file_size', 0)} bytes\n"
                evaluation_prompt += f"   - 类型: {result.get('file_type', 'unknown')}\n"
                evaluation_prompt += f"   - 说明: {result.get('message', '')}\n"

        evaluation_prompt += """

请根据以下标准评分(1-10分):
1. 技术质量(分辨率、流畅度)
2. 创意表现(是否符合提示词)
3. 视觉效果(色彩、构图)

请以JSON格式返回评价结果,格式如下:
{
  "rankings": [
    {
      "rank": 1,
      "model": "模型名称",
      "score": 85,
      "reasoning": "评价理由"
    }
  ],
  "summary": "总体评价"
}
"""

        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.7
        )

        # 解析AI响应
        ai_response = response.choices[0].message.content

        print(f"\n[AI评价结果]")
        print(ai_response)

        # 尝试提取JSON
        try:
            # 查找JSON代码块
            if '```json' in ai_response:
                json_start = ai_response.find('```json') + 7
                json_end = ai_response.find('```', json_start)
                json_str = ai_response[json_start:json_end].strip()
            elif '```' in ai_response:
                json_start = ai_response.find('```') + 3
                json_end = ai_response.find('```', json_start)
                json_str = ai_response[json_start:json_end].strip()
            else:
                # 尝试找到第一个{和最后一个}
                json_start = ai_response.find('{')
                json_end = ai_response.rfind('}') + 1
                json_str = ai_response[json_start:json_end]

            evaluation = json.loads(json_str)
            return evaluation

        except (json.JSONDecodeError, ValueError) as e:
            print(f"[警告] 无法解析AI响应为JSON: {e}")
            return {
                'summary': ai_response,
                'rankings': []
            }

    except Exception as e:
        print(f"[错误] AI评价失败: {e}")
        return None


def generate_html_report(prompt, video_results, ai_evaluation, output_path):
    """生成HTML对比报告"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视频生成模型对比 - {prompt[:50]}</title>
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
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}

        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}

        .prompt-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .prompt-text {{
            font-size: 1.1em;
            line-height: 1.6;
        }}

        .model-section {{
            margin-bottom: 40px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 25px;
            background: #f9f9f9;
        }}

        .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #ddd;
        }}

        .model-title {{
            font-size: 1.8em;
            color: #333;
            font-weight: bold;
        }}

        .model-meta {{
            color: #666;
            font-size: 0.9em;
        }}

        .video-container {{
            position: relative;
            background: black;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }}

        .video-container video,
        .video-container img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .rank-badge {{
            position: absolute;
            top: 15px;
            left: 15px;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.2em;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }}

        .rank-1 {{ background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); }}
        .rank-2 {{ background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%); }}
        .rank-3 {{ background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); }}

        .video-info {{
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}

        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}

        .info-row:last-child {{
            border-bottom: none;
        }}

        .info-label {{
            font-weight: bold;
            color: #555;
        }}

        .info-value {{
            color: #333;
        }}

        .status-success {{
            color: #4caf50;
            font-weight: bold;
        }}

        .status-error {{
            color: #f44336;
            font-weight: bold;
        }}

        .ai-evaluation {{
            background: #e8f5e9;
            border-left: 5px solid #4caf50;
            padding: 20px;
            margin-top: 30px;
            border-radius: 10px;
        }}

        .ai-evaluation h2 {{
            color: #2e7d32;
            margin-bottom: 15px;
        }}

        .ranking-item {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
        }}

        .ranking-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .ranking-model {{
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
        }}

        .ranking-score {{
            background: #4caf50;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}

        .ranking-reason {{
            color: #666;
            line-height: 1.6;
        }}

        footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 视频生成模型对比测试</h1>
        <p class="subtitle">生成时间: {timestamp}</p>

        <div class="prompt-section">
            <h2>📝 提示词</h2>
            <p class="prompt-text">{prompt}</p>
        </div>
"""

    # 添加AI评价(如果有)
    if ai_evaluation and 'rankings' in ai_evaluation:
        html_content += """
        <div class="ai-evaluation">
            <h2>🤖 AI评价与排名</h2>
"""

        # 创建排名映射
        rank_map = {}
        for ranking in ai_evaluation['rankings']:
            rank_map[ranking['model']] = ranking

        for ranking in ai_evaluation['rankings']:
            html_content += f"""
            <div class="ranking-item">
                <div class="ranking-header">
                    <span class="ranking-model">#{ranking['rank']} {ranking['model']}</span>
                    <span class="ranking-score">{ranking.get('score', 'N/A')}分</span>
                </div>
                <div class="ranking-reason">{ranking.get('reasoning', '')}</div>
            </div>
"""

        if 'summary' in ai_evaluation:
            html_content += f"""
            <p style="margin-top: 15px; color: #2e7d32; font-style: italic;">
                <strong>总结:</strong> {ai_evaluation['summary']}
            </p>
"""

        html_content += """
        </div>
"""

    # 添加视频结果
    for result in video_results:
        model_name = result['model_name']

        # 确定排名
        rank_badge = ""
        if ai_evaluation and 'rankings' in ai_evaluation:
            for ranking in ai_evaluation['rankings']:
                if ranking['model'] == model_name:
                    rank_class = f"rank-{ranking['rank']}" if ranking['rank'] <= 3 else "rank-other"
                    rank_badge = f'<div class="rank-badge {rank_class}">#{ranking["rank"]}</div>'
                    break

        html_content += f"""
        <div class="model-section">
            <div class="model-header">
                <div class="model-title">{model_name}</div>
                <div class="model-meta">
                    提供商: {result['provider']} |
                    类型: {result['type']}
                </div>
            </div>
"""

        if result['success']:
            file_ext = Path(result['file_path']).suffix.lower()
            is_video = file_ext in ['.mp4', '.webm', '.mov']
            is_gif = file_ext == '.gif'
            is_image = file_ext in ['.png', '.jpg', '.jpeg']

            html_content += f"""
            <div class="video-container" style="position: relative;">
                {rank_badge}
"""

            if is_video:
                html_content += f"""
                <video controls>
                    <source src="{Path(result['file_path']).name}" type="video/mp4">
                    您的浏览器不支持视频播放
                </video>
"""
            elif is_gif:
                html_content += f"""
                <img src="{Path(result['file_path']).name}" alt="{model_name}">
"""
            elif is_image:
                html_content += f"""
                <img src="{Path(result['file_path']).name}" alt="{model_name}">
                <p style="position: absolute; bottom: 10px; left: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.9em;">
                    ⚠️ 图片格式(非视频)
                </p>
"""
            else:
                html_content += f"""
                <p style="padding: 40px; text-align: center; color: white;">
                    文件格式: {file_ext.upper()}
                </p>
"""

            html_content += """
            </div>
            <div class="video-info">
"""

            # 添加文件信息
            html_content += f"""
                <div class="info-row">
                    <span class="info-label">状态:</span>
                    <span class="info-value status-success">✓ 成功</span>
                </div>
                <div class="info-row">
                    <span class="info-label">文件:</span>
                    <span class="info-value">{Path(result['file_path']).name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">大小:</span>
                    <span class="info-value">{result.get('file_size', 0):,} bytes</span>
                </div>
                <div class="info-row">
                    <span class="info-label">类型:</span>
                    <span class="info-value">{result.get('file_type', 'unknown').upper()}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">说明:</span>
                    <span class="info-value">{result.get('message', '')}</span>
                </div>
"""

            html_content += """
            </div>
        """
        else:
            html_content += f"""
            <div class="video-info">
                <div class="info-row">
                    <span class="info-label">状态:</span>
                    <span class="info-value status-error">✗ 失败</span>
                </div>
                <div class="info-row">
                    <span class="info-label">错误:</span>
                    <span class="info-value">{result.get('message', '未知错误')}</span>
                </div>
            </div>
        """

        html_content += """
        </div>
"""

    # 页脚
    html_content += f"""
        <footer>
            <p>测试完成时间: {timestamp}</p>
            <p>视频生成对比工具 | 支持多种视频生成模型</p>
        </footer>
    </div>
</body>
</html>
"""

    # 保存HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path


def load_progress(output_dir):
    """加载之前的进度"""
    progress_file = output_dir / "video_generation_progress.json"

    if progress_file.exists():
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
                return progress
        except:
            pass

    return None


def save_progress(output_dir, prompt, completed_models):
    """保存进度"""
    progress_file = output_dir / "video_generation_progress.json"

    progress = {
        'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'prompt': prompt,
        'completed_models': completed_models
    }

    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""

    print("="*80)
    print("视频生成模型对比工具")
    print("="*80)
    print()

    # 获取用户输入
    prompt = input("请输入视频生成主题/提示词: ").strip()

    if not prompt:
        print("[错误] 提示词不能为空")
        return

    print()
    print(f"[提示词] {prompt}")
    print()

    # 创建输出目录
    script_dir = Path(__file__).parent
    output_dir = script_dir / "video_comparison_output"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"[输出目录] {output_dir}")
    print()

    # 准备模型列表
    enabled_models = []
    for model_id, config in VIDEO_GENERATION_MODELS.items():
        if config['enabled']:
            enabled_models.append({
                'id': model_id,
                'name': config['name'],
                'provider': config['provider'],
                'type': config['type']
            })

    print(f"[信息] 将测试 {len(enabled_models)} 个视频生成模型")
    for i, model in enumerate(enabled_models, 1):
        print(f"  {i}. {model['name']} ({model['provider']})")
    print()

    # 加载之前的进度
    previous_progress = load_progress(output_dir)
    completed_models = set()

    if previous_progress:
        print(f"[断点续传] 找到之前的进度")
        print(f"  提示词: {previous_progress.get('prompt', '')[:50]}...")
        print(f"  时间: {previous_progress.get('timestamp', '')}")
        print(f"  已完成: {len(previous_progress.get('completed_models', []))} 个模型")
        print()

        # 检查提示词是否相同
        if previous_progress.get('prompt') == prompt:
            completed_models = set(previous_progress.get('completed_models', []))
            print(f"[断点续传] 将跳过已完成的 {len(completed_models)} 个模型")
        else:
            print(f"[新任务] 提示词已更改,重新开始")
            completed_models = set()
    else:
        print(f"[新任务] 未找到之前的进度")
    print()

    # 生成视频
    print("="*80)
    print("开始生成视频...")
    print("="*80)
    print()

    results = []
    completed_count = 0
    skipped_count = 0

    for i, model in enumerate(enabled_models, 1):
        model_id = model['id']
        model_name = model['name']

        # 断点续传: 跳过已完成的模型
        if model_id in completed_models:
            print(f"[{i}/{len(enabled_models)}] {model_name}")
            print(f"  [跳过] 已生成,跳过")
            print()

            # 尝试加载之前的结果
            safe_name = model_name.replace(' ', '_').replace('(', '').replace(')', '')

            # 查找已生成的文件
            existing_files = list(output_dir.glob(f"{safe_name}_*.*"))
            if existing_files:
                latest_file = max(existing_files, key=lambda p: p.stat().st_mtime)
                file_size = latest_file.stat().st_size

                # 确定文件类型
                file_ext = latest_file.suffix.lower()
                file_type = file_ext[1:] if file_ext else 'unknown'

                result = {
                    'success': True,
                    'file_path': str(latest_file),
                    'file_size': file_size,
                    'file_type': file_type,
                    'message': f'使用已生成的 {file_type.upper()} 文件'
                }
                skipped_count += 1
            else:
                result = {
                    'success': False,
                    'error': 'file_not_found',
                    'message': '之前生成的文件未找到,需要重新生成'
                }
                # 从completed集合中移除,以便重新生成
                completed_models.discard(model_id)

            result['model_id'] = model_id
            result['model_name'] = model_name
            result['provider'] = model['provider']
            result['type'] = model['type']

            results.append(result)
            continue

        print(f"[{i}/{len(enabled_models)}] {model_name}")
        print(f"  提供商: {model['provider']}")
        print(f"  类型: {model['type']}")

        # 生成输出文件名
        safe_name = model_name.replace(' ', '_').replace('(', '').replace(')', '')
        output_path = output_dir / f"{safe_name}_{timestamp}.mp4"

        # 调用对应的生成函数
        if model_id == 'dalle-animation':
            result = generate_video_with_dalle_first(prompt, output_path)
        elif model_id == 'seedance':
            result = generate_video_with_seedance(prompt, output_path)
        elif model_id == 'gemini-veo':
            result = generate_video_with_gemini_veo(prompt, output_path)
        else:
            result = {
                'success': False,
                'error': 'not_implemented',
                'message': f'{model_name} 暂未实现(视频生成功能开发中)'
            }

        # 添加模型信息
        result['model_id'] = model_id
        result['model_name'] = model_name
        result['provider'] = model['provider']
        result['type'] = model['type']

        results.append(result)

        status = "[OK] 成功" if result['success'] else "[FAIL] 失败"
        print(f"  {status} {result.get('message', '')}")
        print()

        # 如果成功,添加到已完成列表
        if result['success']:
            completed_models.add(model_id)
            completed_count += 1

    # 保存进度
    save_progress(output_dir, prompt, list(completed_models))

    # AI评价
    successful_results = [r for r in results if r['success']]

    if successful_results:
        print("="*80)
        print("AI评价视频质量...")
        print("="*80)

        ai_evaluation = ai_evaluate_videos(prompt, successful_results)
    else:
        ai_evaluation = None

    # 生成HTML报告
    print()
    print("[生成] HTML对比报告...")

    html_path = output_dir / f"video_comparison_{timestamp}.html"
    generate_html_report(prompt, results, ai_evaluation, html_path)

    print(f"[完成] HTML报告: {html_path}")

    # 统计
    print()
    print("="*80)
    print("测试统计")
    print("="*80)
    print(f"总模型数: {len(enabled_models)}")
    print(f"本次新生成: {completed_count}")
    print(f"跳过已完成: {skipped_count}")
    print(f"成功生成: {len(successful_results)}")
    print(f"失败: {len(enabled_models) - len(successful_results)}")
    print()

    # 自动打开HTML报告
    try:
        import subprocess
        subprocess.Popen(['start', '', str(html_path)], shell=True)
        print(f"[信息] 已在浏览器中打开HTML报告")
    except:
        print(f"[提示] 请手动打开: {html_path}")

    print()
    print("="*80)
    print("完成!")
    print("="*80)


if __name__ == "__main__":
    main()
