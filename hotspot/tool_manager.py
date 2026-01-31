# -*- coding: utf-8 -*-
"""
Post工具管理器 - Web应用
提供可视化界面管理和运行post目录下的所有Python工具
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import subprocess
import os
import threading
import time
from pathlib import Path
from datetime import datetime
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 工具目录
TOOLS_DIR = Path(__file__).parent

# 工具分类
TOOL_CATEGORIES = {
    "AI趋势分析": [
        "multi_model_api_call.py",
        "check_quota_status.py",
        "test_antigravity_models.py",
        "deep_research_ai_trends_2026.py",
        "deep_research_ai_trends_2026_realtime.py",
        "complete_multi_model_realtime_search.py",
        "complete_multi_model_report.py",
        "create_ai_trends_final.py",
        "ai_trends_2026_comparison.py"
    ],
    "图像生成 - 节日": [
        "generate_festival_images.py"
    ],
    "图像生成 - 鸟类": [
        "bird_painting_self_correction.py",
        "bird_painting_steps_generator.py",
        "bird_painting_steps_teaching.py",
        "bird_painting_with_verification.py",
        "bird_painting_volcano.py",
        "bird_painting_optimized.py",
        "bird_pollinations_simple.py",
        "generate_bird_gallery.py"
    ],
    "图像生成 - 文章插图": [
        "generate_article_images.py",
        "generate_food_article_images.py",
        "generate_food_article_pollinations.py",
        "generate_food_article_seedream.py",
        "generate_tea_article_images.py"
    ],
    "文章处理": [
        "article_review_and_revision.py",
        "article_review_and_revision_local.py",
        "create_final_teaching_page.py",
        "create_simple_tutorial.py"
    ],
    "其他工具": [
        "config.py",
        "generate_pencil_sketch.py"
    ]
}

# 运行中的进程
running_processes = {}


def get_tool_description(filename):
    """从文件或描述文件中提取工具描述"""
    try:
        # 尝试从描述文件加载
        desc_file = TOOLS_DIR / 'tool_descriptions.json'
        if desc_file.exists():
            with open(desc_file, 'r', encoding='utf-8') as f:
                descriptions = json.load(f)
                for category, tools in descriptions.items():
                    if filename in tools:
                        return tools[filename]

        # 如果没有找到，从文件中提取
        filepath = TOOLS_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            # 读取前20行
            lines = [f.readline() for _ in range(20)]
            for line in lines:
                line = line.strip()
                # 查找文档字符串
                if line.startswith('"""') or line.startswith("'''"):
                    desc = line[3:].strip()
                    if desc:
                        return desc
                # 查找注释
                if line.startswith('#'):
                    desc = line[1:].strip()
                    if desc and not desc.startswith('#!'):
                        return desc
    except Exception as e:
        pass
    return f"{filename} - Python工具"


def get_all_tools():
    """获取所有工具及其分类"""
    all_files = list(TOOLS_DIR.glob("*.py"))

    tools = {}
    for category, file_list in TOOL_CATEGORIES.items():
        tools[category] = []
        for filename in file_list:
            filepath = TOOLS_DIR / filename
            if filepath.exists():
                tools[category].append({
                    'filename': filename,
                    'description': get_tool_description(filename),
                    'size': filepath.stat().st_size,
                    'modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                })

    # 添加未分类的工具
    categorized_files = set()
    for file_list in TOOL_CATEGORIES.values():
        categorized_files.update(file_list)

    uncategorized = []
    for filepath in all_files:
        if filepath.name not in categorized_files and filepath.name != 'tool_manager.py':
            uncategorized.append({
                'filename': filepath.name,
                'description': get_tool_description(filepath.name),
                'size': filepath.stat().st_size,
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

    if uncategorized:
        tools['未分类'] = uncategorized

    return tools


def run_tool(filename, process_id, params=None):
    """在后台运行工具"""
    if params is None:
        params = {}

    try:
        filepath = TOOLS_DIR / filename

        # 记录开始时间
        start_time = time.time()

        # 如果有参数且是节日图像生成器，创建输入文件
        if filename == 'generate_festival_images.py' and 'theme' in params:
            # 创建临时输入文件来传递主题
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(params['theme'] + '\n')
                input_file = f.name

            # 使用输入文件运行
            process = subprocess.Popen(
                ['python', str(filepath)],
                cwd=str(TOOLS_DIR),
                stdin=open(input_file, 'r'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # 删除临时文件
            import os
            try:
                os.unlink(input_file)
            except:
                pass
        else:
            # 运行Python脚本
            process = subprocess.Popen(
                ['python', str(filepath)],
                cwd=str(TOOLS_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

        running_processes[process_id] = {
            'process': process,
            'filename': filename,
            'start_time': start_time,
            'status': 'running',
            'output': []
        }

        # 等待进程完成
        stdout, stderr = process.communicate()

        # 更新状态
        running_processes[process_id]['status'] = 'completed' if process.returncode == 0 else 'failed'
        running_processes[process_id]['returncode'] = process.returncode

        # 保存输出
        if stdout:
            running_processes[process_id]['output'].append(f"STDOUT:\n{stdout}")
        if stderr:
            running_processes[process_id]['output'].append(f"STDERR:\n{stderr}")

    except Exception as e:
        running_processes[process_id]['status'] = 'failed'
        running_processes[process_id]['output'].append(f"错误: {str(e)}")


@app.route('/')
def index():
    """首页"""
    tools = get_all_tools()
    return render_template('tool_manager.html', tools=tools, running_processes=running_processes)


@app.route('/api/tools')
def api_tools():
    """获取所有工具列表"""
    tools = get_all_tools()
    return jsonify(tools)


@app.route('/api/run', methods=['POST'])
def api_run():
    """运行工具"""
    data = request.json
    filename = data.get('filename')
    params = data.get('params', {})  # 新增：支持传入参数

    if not filename:
        return jsonify({'success': False, 'error': '未指定文件名'}), 400

    filepath = TOOLS_DIR / filename
    if not filepath.exists():
        return jsonify({'success': False, 'error': f'文件不存在: {filename}'}), 404

    # 生成进程ID
    process_id = f"{filename}_{int(time.time())}"

    # 在后台线程中运行
    thread = threading.Thread(target=run_tool, args=(filename, process_id, params))
    thread.start()

    return jsonify({
        'success': True,
        'process_id': process_id,
        'message': f'正在运行 {filename}...'
    })


@app.route('/api/status/<process_id>')
def api_status(process_id):
    """获取运行状态"""
    if process_id not in running_processes:
        return jsonify({'success': False, 'error': '进程不存在'}), 404

    proc_info = running_processes[process_id]

    # 计算运行时间
    elapsed = time.time() - proc_info['start_time']

    return jsonify({
        'success': True,
        'filename': proc_info['filename'],
        'status': proc_info['status'],
        'elapsed_time': elapsed,
        'output': '\n'.join(proc_info['output']),
        'returncode': proc_info.get('returncode')
    })


@app.route('/api/stop', methods=['POST'])
def api_stop():
    """停止运行中的进程"""
    data = request.json
    process_id = data.get('process_id')

    if not process_id:
        return jsonify({'success': False, 'error': '未指定进程ID'}), 400

    if process_id not in running_processes:
        return jsonify({'success': False, 'error': '进程不存在'}), 404

    proc_info = running_processes[process_id]

    try:
        if proc_info['status'] == 'running':
            proc_info['process'].terminate()
            proc_info['status'] = 'stopped'
            return jsonify({'success': True, 'message': '进程已停止'})
        else:
            return jsonify({'success': False, 'error': '进程未在运行'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/view_output/<filename>')
def view_output(filename):
    """查看输出文件"""
    # 查找相关的输出文件
    output_files = list(TOOLS_DIR.glob(f"*{filename.stem}*.html")) + \
                   list(TOOLS_DIR.glob(f"*{filename.stem}*.txt")) + \
                   list(TOOLS_DIR.glob(f"*{filename.stem}*.md"))

    return render_template('view_output.html',
                          filename=filename,
                          output_files=output_files)


if __name__ == '__main__':
    print("="*80)
    print("Post工具管理器")
    print("="*80)
    print(f"工具目录: {TOOLS_DIR}")
    print(f"启动Web服务器: http://localhost:5000")
    print("="*80)

    app.run(host='0.0.0.0', port=5000, debug=True)
