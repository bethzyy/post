#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Post工具管理器 - Web版本
支持按功能分类的工具管理和快速启动
"""

import os
import subprocess
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import tempfile

# 导入工具详细配置
from tool_details_config import get_tool_details

app = Flask(__name__)

# 全局变量存储运行中的进程
running_processes = {}

BASE_DIR = Path(__file__).parent

# 工具描述配置
TOOL_DESCRIPTIONS = {
    "bird/": {
        "bird_painting_optimized.py": "测试 - 鸟类绘画优化生成器 (Gemini+Pollinations+Volcano多模型对比)",
        "bird_painting_self_correction.py": "测试 - 鸟类绘画自纠错系统 (智能修正和优化绘画结果)",
        "bird_painting_steps_generator.py": "测试 - 鸟类绘画步骤生成器 (生成详细的绘画教学步骤)",
        "bird_painting_steps_teaching.py": "测试 - 鸟类绘画教学工具 (交互式绘画教学)",
        "bird_painting_tutorial_final.html": "展示 - 鸟类绘画教程最终版 (完整的绘画教程展示页面)",
        "bird_painting_volcano.py": "测试 - 鸟类绘画Volcano版 (使用Volcano API生成)",
        "bird_painting_with_verification.py": "测试 - 鸟类绘画验证版 (带质量验证功能)",
        "bird_pollinations_simple.py": "测试 - Pollinations简单版鸟类绘画",
        "create_final_teaching_page.py": "工具 - 创建最终教学页面",
        "create_simple_tutorial.py": "工具 - 创建简单教程",
        "generate_bird_gallery.py": "工具 - 生成鸟类绘画画廊",
        "generate_pencil_sketch.py": "工具 - 生成铅笔素描效果",
    },
    "picture/": {
        "generate_festival_images.py": "生成器 - 节日主题图像生成器 (支持自定义主题,使用DALL-E3+Flux+Seedream对比)",
    },
    "article/": {
        "toutiao_article_generator.py": {
            "description": "生成器 - 今日头条文章生成器 v3.1 (支持主题生成+草稿完善+智能配图)",
            "needs_input": True,
            "input_fields": [
                {"name": "mode", "label": "生成模式", "type": "select", "options": [
                    {"value": "1", "label": "主题生成 (AI从零开始)"},
                    {"value": "2", "label": "草稿完善 (AI优化您的草稿)"}
                ], "default": "1"},
                {"name": "theme", "label": "文章主题 (模式1)", "type": "text", "placeholder": "如: 过年回老家", "required": False},
                {"name": "draft", "label": "文章草稿 (模式2)", "type": "textarea", "placeholder": "请输入您的文章草稿内容...", "required": False},
                {"name": "length", "label": "文章长度", "type": "select", "options": [
                    {"value": "1500", "label": "1500字 (快速阅读)"},
                    {"value": "2000", "label": "2000字 (标准长度)"},
                    {"value": "2500", "label": "2500字 (深度文章)"}
                ], "default": "2000"},
                {"name": "generate_images", "label": "生成配图", "type": "select", "options": [
                    {"value": "y", "label": "是 (生成3张配图)"},
                    {"value": "n", "label": "否 (仅生成文章)"}
                ], "default": "y"},
                {"name": "image_style", "label": "配图风格", "type": "select", "options": [
                    {"value": "realistic", "label": "真实照片"},
                    {"value": "artistic", "label": "艺术创作"},
                    {"value": "cartoon", "label": "卡通插画"}
                ], "default": "realistic"}
            ]
        },
        "article_review_and_revision.py": "工具 - 文章审校和修订工具 (AI辅助文章优化)",
        "article_review_and_revision_local.py": "工具 - 本地版文章审校工具",
        "generate_article_images.py": "生成器 - 文章配图生成器 (自动为文章生成配套图片)",
        "generate_food_article_images.py": "生成器 - 美食文章配图生成器 (美食主题文章+图片)",
        "generate_food_article_pollinations.py": "测试 - Pollinations版美食文章生成",
        "generate_food_article_seedream.py": "测试 - Seedream版美食文章生成",
        "generate_tea_article_images.py": "生成器 - 饮茶文章配图生成器 (冬日饮茶养生主题)",
    },
    "video/": {
        "baidu_video_downloader.py": {
            "description": "下载器 - 百度视频下载工具 v2.0 (Selenium增强版,支持绕过安全验证)",
            "needs_input": True,
            "input_fields": [
                {"name": "url", "label": "视频URL", "type": "text", "placeholder": "如: https://mbd.baidu.com/newspaper/data/videolanding?nid=...", "required": True},
                {"name": "output_filename", "label": "输出文件名", "type": "text", "placeholder": "如: video.mp4 (留空自动生成)", "required": False}
            ]
        },
        "video_generation_comparison.py": {
            "description": "🎬 视频生成对比工具 - 多模型AI视频生成与对比分析"
        },
    },
    "hotspot/": {
        "ai_trends_2026_comparison.py": "分析 - 2026年AI趋势对比分析工具 (多维度对比分析)",
    },
    "test/": {
        "test_antigravity_models.py": "测试 - Anti-gravity多模型测试 (测试DALL-E/Gemini等模型)",
        "test_gemini_pro_image.py": "测试 - Gemini Pro Image 3测试 (测试gemini-3-pro-image-2K模型生成图像能力)",
    }
}

def get_file_info(file_path):
    """获取文件信息"""
    stat = file_path.stat()
    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
    size = stat.st_size
    return modified, size

def get_all_tools():
    """获取所有分类的工具"""
    tools = {}

    # 定义工具分类
    categories = {
        "bird": "鸟类绘画工具",
        "picture": "节日图像生成",
        "article": "文章生成工具",
        "video": "视频工具(下载/生成)",
        "hotspot": "AI热点研究",
        "test": "测试工具"
    }

    for cat_dir, cat_name in categories.items():
        cat_path = BASE_DIR / cat_dir
        if not cat_path.exists():
            continue

        tools_list = []
        # 只查找Python文件,不包含HTML文件
        for py_file in sorted(cat_path.glob("*.py")):
            modified, size = get_file_info(py_file)

            # 获取工具描述
            rel_path = py_file.relative_to(BASE_DIR)
            sub_dir = str(rel_path.parent).replace('\\', '/') + '/'
            filename = py_file.name

            tool_config = TOOL_DESCRIPTIONS.get(sub_dir, {}).get(filename)

            # 处理新旧两种格式
            if isinstance(tool_config, dict):
                description = tool_config.get('description', f"{cat_name} - {filename}")
                needs_input = tool_config.get('needs_input', False)
                input_fields = tool_config.get('input_fields', [])
                # 优先使用tool_config中的details，如果没有则从tool_details_config.py获取
                details = tool_config.get('details')
                if not details:
                    details = get_tool_details(str(rel_path))
            else:
                description = tool_config if tool_config else f"{cat_name} - {filename}"
                needs_input = False
                input_fields = []
                # 从tool_details_config.py获取详情
                details = get_tool_details(str(rel_path))

            tools_list.append({
                'filename': str(rel_path).replace('\\', '/'),
                'description': description,
                'modified': modified,
                'size': size,
                'needs_input': needs_input,
                'input_fields': input_fields,
                'details': details  # 添加详细说明
            })

        if tools_list:
            tools[cat_name] = tools_list

    return tools

@app.route('/')
def index():
    """主页面"""
    tools = get_all_tools()
    return render_template('tool_manager.html', tools=tools, running_processes=running_processes)

@app.route('/api/tools')
def api_tools():
    """API: 获取所有工具列表"""
    tools = get_all_tools()
    return jsonify({'success': True, 'tools': tools})

@app.route('/api/documentation')
def api_documentation():
    """API: 获取工具文档"""
    doc_file = BASE_DIR / 'tool_documentation.json'
    if doc_file.exists():
        import json
        with open(doc_file, 'r', encoding='utf-8') as f:
            return jsonify({'success': True, 'documentation': json.load(f)})
    return jsonify({'success': False, 'error': '文档文件不存在'})

@app.route('/api/update-documentation', methods=['POST'])
def api_update_documentation():
    """API: 重新生成工具文档"""
    try:
        import subprocess
        import sys

        # 运行文档生成脚本
        script_path = BASE_DIR / 'generate_tool_docs.py'
        if not script_path.exists():
            return jsonify({'success': False, 'error': '文档生成脚本不存在'})

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': '文档已成功更新',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'error': f'文档生成失败: {result.stderr}'
            })

    except Exception as e:
        return jsonify({'success': False, 'error': f'更新失败: {str(e)}'})

@app.route('/api/run', methods=['POST'])
def api_run():
    """API: 运行指定工具"""
    data = request.json
    filename = data.get('filename')

    if not filename:
        return jsonify({'success': False, 'error': '未指定文件名'})

    tool_path = BASE_DIR / filename

    if not tool_path.exists():
        return jsonify({'success': False, 'error': f'工具不存在: {filename}'})

    # 生成唯一的进程ID（将文件名中的斜杠替换为下划线，避免URL路由问题）
    safe_filename = filename.replace('/', '_').replace('\\', '_')
    process_id = f"{safe_filename}_{int(time.time())}"

    try:
        if tool_path.suffix == '.py':
            # Python脚本 - 设置环境变量以包含BASE_DIR到Python路径
            import sys
            import os

            # 创建环境变量，添加BASE_DIR到Python路径
            env = os.environ.copy()
            pythonpath = env.get('PYTHONPATH', '')
            env['PYTHONPATH'] = str(BASE_DIR) + os.pathsep + pythonpath

            # 今日头条文章生成器 - 支持模式选择、主题/草稿、字数、配图参数
            if filename == 'article/toutiao_article_generator.py':
                params = data.get('params', {})
                mode = params.get('mode', '1')
                theme = params.get('theme', '')
                draft = params.get('draft', '')
                length = params.get('length', '2000')
                generate_images = params.get('generate_images', 'y')
                image_style = params.get('image_style', 'realistic')

                # 验证参数
                if mode == '1' and not theme:
                    return jsonify({'success': False, 'error': '模式1需要输入文章主题'})
                if mode == '2' and not draft:
                    return jsonify({'success': False, 'error': '模式2需要输入文章草稿'})

                # 创建临时输入文件
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
                    # 写入模式选择
                    f.write(mode + '\n')

                    # 根据模式写入不同内容
                    if mode == '1':
                        # 主题生成模式
                        f.write(theme + '\n')
                    else:
                        # 草稿完善模式 - 写入END标记结束
                        if draft:
                            f.write(draft + '\n')
                        f.write('END\n')

                    # 写入通用参数
                    f.write(length + '\n')
                    f.write(generate_images + '\n')
                    f.write(image_style + '\n')
                    temp_file = f.name

                process = subprocess.Popen(
                    ['python', str(tool_path)],
                    stdin=open(temp_file, 'r', encoding='utf-8'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env=env
                )
            # 百度视频下载器 - 支持URL和输出文件名参数
            elif filename == 'video/baidu_video_downloader.py':
                params = data.get('params', {})
                url = params.get('url', '')
                output_filename = params.get('output_filename', '')

                if not url:
                    return jsonify({'success': False, 'error': '视频URL不能为空'})

                # 创建临时输入文件
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
                    f.write(url + '\n')
                    f.write(output_filename + '\n')
                    temp_file = f.name

                process = subprocess.Popen(
                    ['python', str(tool_path)],
                    stdin=open(temp_file, 'r', encoding='utf-8'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env=env
                )
            # 视频生成对比工具 - 支持提示词参数
            elif filename == 'video/video_generation_comparison.py':
                params = data.get('params', {})
                prompt = params.get('prompt', '')

                # 创建临时输入文件传递提示词
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
                    f.write(prompt + '\n')
                    temp_file = f.name

                process = subprocess.Popen(
                    ['python', str(tool_path)],
                    stdin=open(temp_file, 'r', encoding='utf-8'),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env=env
                )
            # 节日图像生成器 - 支持主题参数
            elif filename == 'picture/generate_festival_images.py':
                theme = data.get('params', {}).get('theme', '')
                if theme:
                    # 创建临时文件传递主题
                    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as f:
                        f.write(theme + '\n')
                        temp_file = f.name

                    process = subprocess.Popen(
                        ['python', str(tool_path)],
                        stdin=open(temp_file, 'r', encoding='utf-8'),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=BASE_DIR,
                        env=env
                    )
                else:
                    process = subprocess.Popen(
                        ['python', str(tool_path)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=BASE_DIR,
                        env=env
                    )
            else:
                process = subprocess.Popen(
                    ['python', str(tool_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env=env
                )
        elif tool_path.suffix == '.html':
            # HTML文件 - 在浏览器中打开
            import webbrowser
            webbrowser.open(f'file://{tool_path.absolute()}')
            return jsonify({
                'success': True,
                'message': f'已在浏览器中打开: {tool_path.name}',
                'process_id': process_id,
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'error': f'不支持的文件类型: {tool_path.suffix}'})

        running_processes[process_id] = {
            'process': process,
            'filename': filename,
            'start_time': time.time(),
            'output': '',
            'status': 'running'
        }

        return jsonify({
            'success': True,
            'message': f'工具已启动: {filename}',
            'process_id': process_id,
            'filename': filename
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/status/<process_id>')
def api_status(process_id):
    """API: 获取运行状态"""
    if process_id not in running_processes:
        return jsonify({
            'success': False,
            'error': '进程不存在'
        })

    proc_info = running_processes[process_id]
    process = proc_info['process']

    # 检查进程状态
    return_code = process.poll()

    if return_code is None:
        # 进程仍在运行
        # 尝试读取已产生的输出(非阻塞)
        try:
            # Unix/Linux系统使用fcntl设置非阻塞模式
            import fcntl
            import errno

            # 设置非阻塞模式
            fd = process.stdout.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

            try:
                output = process.stdout.read()
                if output:
                    proc_info['output'] += output.decode('utf-8', errors='ignore')
            except (IOError, OSError) as e:
                # 非阻塞读取时没有数据可读是正常的
                if e.errno != errno.EAGAIN:
                    pass
        except (ImportError, AttributeError):
            # Windows不支持fcntl,跳过
            pass
        except:
            # 其他错误,忽略
            pass

        elapsed_time = time.time() - proc_info['start_time']
        return jsonify({
            'success': True,
            'filename': proc_info['filename'],
            'status': 'running',
            'elapsed_time': round(elapsed_time, 1),
            'output': proc_info.get('output', '正在运行...'),
            'returncode': None
        })
    else:
        # 进程已结束 - 使用communicate()获取剩余输出
        try:
            stdout, stderr = process.communicate(timeout=5)
            output = stdout.decode('utf-8', errors='ignore')
            error = stderr.decode('utf-8', errors='ignore')

            if error:
                output += f'\n[错误输出]\n{error}'

            # 追加到之前的输出
            if proc_info.get('output'):
                output = proc_info['output'] + output
        except:
            # communicate()超时或失败,使用已缓存的输出
            output = proc_info.get('output', '输出读取失败')

        proc_info['status'] = 'completed' if return_code == 0 else 'failed'
        proc_info['output'] = output
        proc_info['return_code'] = return_code

        elapsed_time = time.time() - proc_info['start_time']

        return jsonify({
            'success': True,
            'filename': proc_info['filename'],
            'status': proc_info['status'],
            'elapsed_time': round(elapsed_time, 1),
            'output': output,
            'returncode': return_code
        })

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """API: 停止运行中的工具"""
    data = request.json
    process_id = data.get('process_id')

    if process_id not in running_processes:
        return jsonify({'success': False, 'error': '进程不存在'})

    try:
        process = running_processes[process_id]['process']
        process.terminate()
        time.sleep(0.5)

        if process.poll() is None:
            process.kill()

        running_processes[process_id]['status'] = 'stopped'

        return jsonify({
            'success': True,
            'message': '工具已停止'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/delete', methods=['POST'])
def api_delete():
    """API: 删除工具文件"""
    data = request.json
    filename = data.get('filename')

    if not filename:
        return jsonify({'success': False, 'error': '未指定文件名'})

    tool_path = BASE_DIR / filename

    # 安全检查：确保文件在BASE_DIR内
    try:
        tool_path.resolve().relative_to(BASE_DIR.resolve())
    except ValueError:
        return jsonify({'success': False, 'error': '非法的文件路径'})

    if not tool_path.exists():
        return jsonify({'success': False, 'error': f'文件不存在: {filename}'})

    try:
        # 删除文件
        if tool_path.is_file():
            tool_path.unlink()
        elif tool_path.is_dir():
            import shutil
            shutil.rmtree(tool_path)

        return jsonify({
            'success': True,
            'message': f'文件已删除: {filename}'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': f'删除失败: {str(e)}'})

def main():
    """主函数"""
    print("=" * 80)
    print("                         [AI发文工具管理器 - Web版]")
    print("=" * 80)
    print()
    print("当前目录:", BASE_DIR)
    print("启动Web服务器: http://localhost:5000")
    print("=" * 80)
    print()

    # 启动Flask服务器
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
