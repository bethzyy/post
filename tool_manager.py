#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Post工具管理器 - Web版本
支持按功能分类的工具管理和快速启动
"""

import os
import subprocess
import time
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from datetime import datetime
import tempfile

# 导入工具详细配置
from tool_details_config import get_tool_details

app = Flask(__name__)

# 使用频率记录文件路径
USAGE_FREQUENCY_FILE = Path(__file__).parent / 'tool_usage_frequency.json'

def load_usage_frequency():
    """加载使用频率数据"""
    if USAGE_FREQUENCY_FILE.exists():
        try:
            with open(USAGE_FREQUENCY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_usage_frequency(frequency_data):
    """保存使用频率数据"""
    with open(USAGE_FREQUENCY_FILE, 'w', encoding='utf-8') as f:
        json.dump(frequency_data, f, ensure_ascii=False, indent=2)

def record_tool_usage(tool_filename):
    """记录工具使用（增加使用计数）"""
    frequency_data = load_usage_frequency()
    if tool_filename in frequency_data:
        frequency_data[tool_filename] += 1
    else:
        frequency_data[tool_filename] = 1
    save_usage_frequency(frequency_data)
    return frequency_data.get(tool_filename, 0)

# 禁用模板缓存
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 添加请求后钩子，禁用浏览器缓存
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

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
        "standalone_image_generator_v9.py": {
            "description": "🎨 AI图像生成器 V9.1 (主题/参考图片+7种画图风格)⭐⭐⭐",
            "is_web_service": True,
            "port": 5009,
            "url": "http://localhost:5009"
        },
        "generate_festival_images.py": "生成器 - 节日主题图像生成器 (支持自定义主题,使用DALL-E3+Flux+Seedream对比)",
        "advanced_watermark_remover.py": "工具 - 高级去水印 (NS高质量算法,油猴脚本智能检测,推荐使用)⭐⭐",
    },
    "article/": {
        "toutiao_web_app.py": {
            "description": "📝 今日头条文章生成器 Web版 (独立Web应用，支持主题生成+草稿完善+智能配图)⭐⭐⭐",
            "is_web_service": True,
            "port": 5010,
            "url": "http://localhost:5010"
        },
        "toutiao_article_generator.py": {
            "description": "生成器 - 今日头条文章生成器 v3.1 (命令行版)",
            "needs_input": True,
            "input_fields": [
                {"name": "mode", "label": "生成模式", "type": "select", "options": [
                    {"value": "1", "label": "主题生成 (AI从零开始)"},
                    {"value": "2", "label": "草稿完善 (AI优化您的草稿)"}
                ], "default": "1"},
                {"name": "theme", "label": "文章主题 (模式1)", "type": "text", "placeholder": "如: 过年回老家", "required": False},
                {"name": "draft", "label": "草稿文件路径 (模式2)", "type": "text", "placeholder": "如: article/draft.txt 或 C:\\path\\to\\draft.txt", "required": False},
                {"name": "length", "label": "文章长度", "type": "select", "options": [
                    {"value": "800", "label": "800字 (短视频文案)"},
                    {"value": "1200", "label": "1200字 (轻量阅读)"},
                    {"value": "1500", "label": "1500字 (快速阅读)"},
                    {"value": "2000", "label": "2000字 (标准长度)"},
                    {"value": "2500", "label": "2500字 (深度文章)"},
                    {"value": "3000", "label": "3000字 (长文深度)"},
                    {"value": "4000", "label": "4000字 (专题报道)"}
                ], "default": "2000"},
                {"name": "style", "label": "文风描述", "type": "select", "options": [
                    {"value": "", "label": "默认 (标准新闻体)"},
                    {"value": "wangzengqi", "label": "汪曾祺风格 (平淡质朴)"},
                    {"value": "luxun", "label": "鲁迅杂文风 (犀利批判)"},
                    {"value": "humor", "label": "幽默风趣 (轻松调侃)"},
                    {"value": "emotional", "label": "情感共鸣 (温暖治愈)"},
                    {"value": "professional", "label": "专业严谨 (学术分析)"},
                    {"value": "storytelling", "label": "故事叙述 (引人入胜)"},
                    {"value": "internet", "label": "网感十足 (年轻化表达)"}
                ], "default": ""},
                {"name": "generate_images", "label": "生成配图", "type": "select", "options": [
                    {"value": "n", "label": "不配图"},
                    {"value": "y", "label": "3张配图"},
                    {"value": "5", "label": "5张配图"},
                    {"value": "7", "label": "7张配图"}
                ], "default": "y"},
                {"name": "image_style", "label": "配图风格", "type": "select", "options": [
                    {"value": "auto", "label": "自动 (AI智能选择)"},
                    {"value": "realistic", "label": "真实照片"},
                    {"value": "artistic", "label": "艺术创作"},
                    {"value": "cartoon", "label": "卡通插画"},
                    {"value": "watercolor", "label": "水彩画风"},
                    {"value": "ink", "label": "中国水墨画"},
                    {"value": "technical", "label": "技术图表"},
                    {"value": "minimalist", "label": "极简风格"}
                ], "default": "auto"},
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
        "ai_trends_unified.py": "分析 - 2026年AI趋势分析工具 (多维度分析)",
        "ai_trends_with_websearch.py": "分析 - AI趋势分析工具 (支持网络搜索)",
    },
    "test/": {
        "test_antigravity_models.py": "测试 - Anti-gravity多模型测试 (测试DALL-E/Gemini等模型)",
        "test_gemini_pro_image.py": "测试 - Gemini Pro Image 3测试 (测试gemini-3-pro-image-2K模型生成图像能力)",
    },
    "docs/": {
        "二十四节气与中国传统色彩.html": {
            "description": "📚 二十四节气与中国传统色彩 (384种传统色按节气分类解读)",
            "is_document": True,
            "category": "article/二十四节气色彩"
        },
        "二十四节气配图文档索引.html": {
            "description": "🖼️ 二十四节气配图文档索引 (AI生成配图版)",
            "is_document": True,
            "category": "article/二十四节气色彩",
            "readme_file": "article/二十四节气色彩/配图文档生成说明.md"
        },
        "他山之石.html": {
            "description": "💎 他山之石 (技术概念科普文档：埋点、域名、RPA等)",
            "is_document": True,
            "category": "article/他山之石"
        }
    }
}

def get_file_info(file_path):
    """获取文件信息"""
    stat = file_path.stat()
    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
    size = stat.st_size
    return modified, size

def get_all_tools():
    """获取所有分类的工具（按使用频率排序）"""
    tools = {}

    # 加载使用频率数据
    frequency_data = load_usage_frequency()

    # 定义工具分类
    categories = {
        "bird": "鸟类绘画工具",
        "picture": "节日图像生成",
        "article": "文章生成工具",
        "video": "视频工具(下载/生成)",
        "hotspot": "AI热点研究",
        "test": "测试工具",
        "docs": "文档库"
    }

    for cat_dir, cat_name in categories.items():
        cat_path = BASE_DIR / cat_dir
        if not cat_path.exists():
            continue

        tools_list = []

        # 处理docs目录（文档库）- 特殊处理HTML文件
        if cat_dir == "docs":
            for doc_key, doc_config in TOOL_DESCRIPTIONS.get("docs/", {}).items():
                if isinstance(doc_config, dict) and doc_config.get('is_document'):
                    doc_category = doc_config.get('category', '')
                    doc_path = BASE_DIR / doc_category / doc_key
                    if doc_path.exists():
                        stat = doc_path.stat()
                        modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                        size = stat.st_size
                        tools_list.append({
                            'filename': f"docs/{doc_key}",
                            'description': doc_config.get('description', doc_key),
                            'modified': modified,
                            'size': size,
                            'needs_input': False,
                            'input_fields': [],
                            'details': doc_config.get('details'),
                            'readme_file': doc_config.get('readme_file'),
                            'usage_count': 0,
                            'is_document': True,
                            'document_path': f"{doc_category}/{doc_key}"
                        })
            if tools_list:
                tools[cat_name] = tools_list
            continue

        # 只查找Python文件,不包含HTML文件
        for py_file in sorted(cat_path.glob("*.py")):
            modified, size = get_file_info(py_file)

            # 获取工具描述
            rel_path = py_file.relative_to(BASE_DIR)
            sub_dir = str(rel_path.parent).replace('\\', '/') + '/'
            filename = py_file.name
            tool_rel_path = str(rel_path).replace('\\', '/')

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
                # 获取readme_file配置
                readme_file = tool_config.get('readme_file')
            else:
                description = tool_config if tool_config else f"{cat_name} - {filename}"
                needs_input = False
                input_fields = []
                # 从tool_details_config.py获取详情
                details = get_tool_details(str(rel_path))
                readme_file = None

            # 获取使用频率
            usage_count = frequency_data.get(tool_rel_path, 0)

            tools_list.append({
                'filename': tool_rel_path,
                'description': description,
                'modified': modified,
                'size': size,
                'needs_input': needs_input,
                'input_fields': input_fields,
                'details': details,  # 添加详细说明
                'readme_file': readme_file,  # 添加readme文件路径
                'usage_count': usage_count  # 添加使用频率
            })

        # 按使用频率排序（高频在前），频率相同的按文件名排序
        tools_list.sort(key=lambda x: (-x['usage_count'], x['filename']))

        if tools_list:
            tools[cat_name] = tools_list

    # 确保文档库排在最后
    docs_category = "文档库"
    if docs_category in tools:
        docs_data = tools.pop(docs_category)
        # 使用OrderedDict确保顺序
        from collections import OrderedDict
        ordered_tools = OrderedDict()
        for k, v in tools.items():
            ordered_tools[k] = v
        ordered_tools[docs_category] = docs_data
        return dict(ordered_tools)

    return tools

@app.route('/')
def index():
    """主页面"""
    tools = get_all_tools()
    return render_template('tool_manager.html', tools=tools, running_processes=running_processes)

@app.route('/view/article/<filename>')
def view_article(filename):
    """查看生成的文章HTML文件"""
    article_dir = BASE_DIR / 'article'
    response = send_from_directory(article_dir, filename)
    response.headers['Content-Disposition'] = 'inline'
    return response

@app.route('/view/document/<path:doc_path>')
def view_document(doc_path):
    """查看文档库中的HTML/MHTML文件"""
    from flask import Response
    # doc_path格式如: article/二十四节气色彩/二十四节气与中国传统色彩.html
    full_path = BASE_DIR / doc_path
    if not full_path.exists():
        return jsonify({'success': False, 'error': f'文档不存在: {doc_path}'}), 404

    # 获取文件所在目录和文件名
    parent_dir = full_path.parent
    filename = full_path.name

    # 根据文件扩展名设置MIME类型
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    mime_types = {
        'html': 'text/html',
        'htm': 'text/html',
        'mhtml': 'application/x-mimearchive',
        'mht': 'application/x-mimearchive',
        'css': 'text/css',
        'js': 'application/javascript',
        'json': 'application/json',
        'xml': 'application/xml',
        'txt': 'text/plain',
        'md': 'text/markdown'
    }
    mimetype = mime_types.get(ext, 'application/octet-stream')

    response = send_from_directory(parent_dir, filename, mimetype=mimetype)
    # 设置Content-Disposition为inline，确保浏览器打开而不是下载
    response.headers['Content-Disposition'] = 'inline'
    return response

@app.route('/view/readme/<path:doc_path>')
def view_readme(doc_path):
    """查看README.md文件，以HTML格式显示"""
    import re

    full_path = BASE_DIR / doc_path
    if not full_path.exists():
        return f'<html><body><h1>文件不存在</h1><p>{doc_path}</p></body></html>', 404

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f'<html><body><h1>读取失败</h1><p>{str(e)}</p></body></html>', 500

    # 简单的Markdown转HTML
    html_content = content
    # 转义HTML特殊字符
    html_content = html_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # 标题
    html_content = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    # 粗体
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    # 代码块
    html_content = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="\1">\2</code></pre>', html_content, flags=re.DOTALL)
    # 行内代码
    html_content = re.sub(r'`([^`]+)`', r'<code style="background:#f0f0f0;padding:2px 6px;border-radius:4px;">\1</code>', html_content)
    # 列表
    html_content = re.sub(r'^- (.*)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\d+\. (.*)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    # 链接
    html_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_content)
    # 换行
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = html_content.replace('\n', '<br>')

    # 构建完整HTML页面
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>README - {full_path.stem}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            line-height: 1.8;
            color: #333;
            background: #fafafa;
        }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        h3 {{ color: #7f8c8d; }}
        code {{
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Consolas, Monaco, monospace;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        li {{ margin: 5px 0; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div style="background:white;padding:30px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <p>{html_content}</p>
    </div>
</body>
</html>'''

    return html

@app.route('/api/document-info')
def api_document_info():
    """API: 获取文档的说明信息"""
    doc_path = request.args.get('path', '')
    if not doc_path:
        return jsonify({'success': False, 'error': '缺少文档路径'})

    # 获取文档所在目录的README.md
    full_path = BASE_DIR / doc_path
    if not full_path.exists():
        return jsonify({'success': False, 'error': f'文档不存在: {doc_path}'})

    # 查找README.md
    doc_dir = full_path.parent
    readme_path = doc_dir / 'README.md'

    doc_info = {
        'name': full_path.stem,
        'path': doc_path,
        'readme': None
    }

    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                doc_info['readme'] = f.read()
        except Exception as e:
            doc_info['readme'] = f'无法读取README: {str(e)}'

    return jsonify({'success': True, 'info': doc_info})

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

    # 记录工具使用
    record_tool_usage(filename)

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
            # 设置UTF-8编码，避免中文乱码
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'

            # Web服务类型工具 - 后台启动并自动打开浏览器
            tool_config = TOOL_DESCRIPTIONS.get(filename.replace('picture/', 'picture/').replace('article/', 'article/').replace('video/', 'video/').replace('bird/', 'bird/').replace('hotspot/', 'hotspot/').replace('test/', 'test/'), None)

            # 查找工具配置（需要遍历所有分类）
            tool_info = None
            for cat, tools in TOOL_DESCRIPTIONS.items():
                if filename.startswith(cat):
                    tool_name = filename.replace(cat, '')
                    if tool_name in tools:
                        tool_info = tools[tool_name]
                        break

            if tool_info and isinstance(tool_info, dict) and tool_info.get('is_web_service'):
                # Web服务类型工具
                port = tool_info.get('port', 5000)
                url = tool_info.get('url', f'http://localhost:{port}')

                # 后台启动服务
                process = subprocess.Popen(
                    ['python', str(tool_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=BASE_DIR,
                    env=env
                )

                # 延迟打开浏览器（等待服务启动）
                import threading
                import webbrowser

                def open_browser():
                    time.sleep(2)  # 等待2秒让服务启动
                    webbrowser.open(url)

                threading.Thread(target=open_browser, daemon=True).start()

                running_processes[process_id] = {
                    'process': process,
                    'filename': filename,
                    'start_time': time.time(),
                    'output': f'Web服务已启动: {url}\n请在浏览器中使用...',
                    'status': 'running',
                    'tool_path': tool_path
                }

                return jsonify({
                    'success': True,
                    'message': f'Web服务已启动，正在打开浏览器: {url}',
                    'process_id': process_id,
                    'filename': filename,
                    'url': url
                })

            # 今日头条文章生成器 - 支持模式选择、主题/草稿、字数、配图参数
            if filename == 'article/toutiao_article_generator.py':
                params = data.get('params', {})
                mode = params.get('mode', '1')
                theme = params.get('theme', '')
                draft = params.get('draft', '')
                length = params.get('length', '2000')
                generate_images = params.get('generate_images', 'y')
                image_style = params.get('image_style', 'realistic')
                style = params.get('style', 'standard')

                # 验证参数
                if mode == '1' and not theme:
                    return jsonify({'success': False, 'error': '模式1需要输入文章主题'})
                if mode == '2' and not draft:
                    return jsonify({'success': False, 'error': '模式2需要输入草稿文件路径'})

                # 使用JSON文件传递参数,避免stdin编码问题
                params_dict = {
                    'mode': mode,
                    'theme': theme,
                    'draft': draft,
                    'length': int(length),
                    'generate_images': generate_images,
                    'image_style': image_style,
                    'style': style,
                }

                # 创建JSON参数文件
                with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as f:
                    json.dump(params_dict, f, ensure_ascii=False, indent=2)
                    params_file = f.name

                print(f"[DEBUG] JSON参数文件: {params_file}")
                print(f"[DEBUG] ========== 文章生成参数 ==========")
                print(f"[DEBUG] 模式(mode): {mode}")
                print(f"[DEBUG] 主题(theme): {theme}")
                print(f"[DEBUG] 草稿(draft): {draft}")
                print(f"[DEBUG] 字数(length): {length}")
                print(f"[DEBUG] 生成配图(generate_images): {generate_images}")
                print(f"[DEBUG] 配图风格(image_style): {image_style}")
                print(f"[DEBUG] 文章风格(style): {style}")
                print(f"[DEBUG] 参数字典完整内容: {params_dict}")
                print(f"[DEBUG] ===================================")

                # 设置环境变量传递参数文件路径
                env['ARTICLE_PARAMS_JSON'] = params_file

                # 读取刚创建的JSON文件内容用于调试
                with open(params_file, 'r', encoding='utf-8') as debug_f:
                    json_content = debug_f.read()

                print(f"[DEBUG] ========== 创建的JSON文件内容 ==========")
                print(f"[DEBUG] 文件路径: {params_file}")
                print(f"[DEBUG] 文件存在: {os.path.exists(params_file)}")
                print(f"[DEBUG] JSON内容:\\n{json_content}")
                print(f"[DEBUG] ========================================\\n")

                print(f"[DEBUG] ========== 子进程环境 ==========")
                print(f"[DEBUG] 命令: python {tool_path}")
                print(f"[DEBUG] 工作目录: {BASE_DIR}")
                print(f"[DEBUG] ARTICLE_PARAMS_JSON: {env.get('ARTICLE_PARAMS_JSON')}")
                print(f"[DEBUG] ====================================\\n")

                process = subprocess.Popen(
                    ['python', str(tool_path)],
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

                # 使用命令行参数和环境变量传递参数,避免stdin编码问题
                cmd = ['python', str(tool_path)]

                # 添加命令行参数
                if mode == '1':
                    # 主题生成模式
                    cmd.extend(['--mode', 'theme', '--theme', theme])
                else:
                    # 草稿完善模式
                    cmd.extend(['--mode', 'draft', '--draft', draft])

                cmd.extend(['--length', length])
                cmd.extend(['--images', generate_images])
                cmd.extend(['--image-style', image_style])

                # 设置环境变量传递参数(作为备用)
                env['ARTICLE_MODE'] = mode
                env['ARTICLE_THEME'] = theme if mode == '1' else ''
                env['ARTICLE_DRAFT'] = draft if mode == '2' else ''
                env['ARTICLE_LENGTH'] = length
                env['ARTICLE_IMAGES'] = generate_images
                env['ARTICLE_IMAGE_STYLE'] = image_style

                process = subprocess.Popen(
                    cmd,
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

                # 使用命令行参数和环境变量传递参数,避免stdin编码问题
                cmd = ['python', str(tool_path)]

                # 添加命令行参数
                if mode == '1':
                    # 主题生成模式
                    cmd.extend(['--mode', 'theme', '--theme', theme])
                else:
                    # 草稿完善模式
                    cmd.extend(['--mode', 'draft', '--draft', draft])

                cmd.extend(['--length', length])
                cmd.extend(['--images', generate_images])
                cmd.extend(['--image-style', image_style])

                # 设置环境变量传递参数(作为备用)
                env['ARTICLE_MODE'] = mode
                env['ARTICLE_THEME'] = theme if mode == '1' else ''
                env['ARTICLE_DRAFT'] = draft if mode == '2' else ''
                env['ARTICLE_LENGTH'] = length
                env['ARTICLE_IMAGES'] = generate_images
                env['ARTICLE_IMAGE_STYLE'] = image_style

                process = subprocess.Popen(
                    cmd,
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
            'status': 'running',
            'tool_path': tool_path  # 保存工具路径用于文件检查
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
        # Windows下尝试非阻塞读取
        try:
            # 使用线程超时方式读取
            import threading
            output_data = {'stdout': '', 'stderr': ''}

            def read_stdout():
                try:
                    output_data['stdout'] = process.stdout.read()
                except:
                    pass

            def read_stderr():
                try:
                    output_data['stderr'] = process.stderr.read()
                except:
                    pass

            t1 = threading.Thread(target=read_stdout)
            t2 = threading.Thread(target=read_stderr)
            t1.start()
            t2.start()
            t1.join(timeout=0.1)
            t2.join(timeout=0.1)

            if output_data['stdout']:
                proc_info['output'] += output_data['stdout'].decode('utf-8', errors='ignore')
            if output_data['stderr']:
                proc_info['output'] += '\n[stderr] ' + output_data['stderr'].decode('utf-8', errors='ignore')
        except:
            pass

        elapsed_time = time.time() - proc_info['start_time']

        # 对于头条文章生成器,检查是否生成了HTML文件
        tool_path = proc_info.get('tool_path')
        if tool_path and 'toutiao_article_generator' in str(tool_path):
            # 检查article目录下最近生成的HTML文件 (支持多种命名模式)
            article_dir = tool_path.parent
            # 支持新的文件名模式
            html_patterns = ['DraftImproved_*.html', 'Article_*.html', '今日头条文章_*.html', '文章草稿完善_*.html']
            html_files = []
            for pattern in html_patterns:
                html_files.extend(article_dir.glob(pattern))

            if html_files:
                # 获取最新的HTML文件
                latest_html = max(html_files, key=lambda p: p.stat().st_mtime)
                file_age = time.time() - latest_html.stat().st_mtime

                # 如果文件在进程启动后生成,且超过5秒前创建的,认为已完成
                if file_age > 5 and file_age < elapsed_time:
                    proc_info['status'] = 'completed'
                    html_path = str(latest_html.absolute())
                    html_url = f'file:///{html_path.replace(chr(92), "/")}'
                    proc_info['output'] += f'\n[OUTPUT] HTML: {latest_html.name}'
                    proc_info['output'] += f'\n[文章链接] {html_url}'

                    # 自动用Chrome打开生成的HTML文件
                    try:
                        chrome_paths = [
                            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                        ]
                        chrome_exe = None
                        for cp in chrome_paths:
                            if os.path.exists(cp):
                                chrome_exe = cp
                                break

                        if chrome_exe:
                            subprocess.Popen([chrome_exe, html_path], shell=False)
                            proc_info['output'] += f'\n[浏览器] 已在Chrome中打开HTML文件'
                        else:
                            os.startfile(html_path)
                            proc_info['output'] += f'\n[浏览器] 已在默认浏览器中打开HTML文件'
                    except Exception as e:
                        proc_info['output'] += f'\n[提示] HTML文件: {latest_html.name}'

                    return jsonify({
                        'success': True,
                        'filename': proc_info['filename'],
                        'status': 'completed',
                        'elapsed_time': round(elapsed_time, 1),
                        'output': proc_info['output'],
                        'returncode': 0
                    })

        # 检查是否已在输出中标记为完成(用于长时间运行的任务)
        output_so_far = proc_info.get('output', '')
        if '生成完成!' in output_so_far or '[成功] HTML文件已保存' in output_so_far or '[SUCCESS] Article generation completed!' in output_so_far or '[OUTPUT] HTML:' in output_so_far:
            # 虽然进程还在运行(可能在等待浏览器打开等),但主要工作已完成
            # 尝试打开生成的HTML文件
            if tool_path and 'toutiao_article_generator' in str(tool_path):
                article_dir = tool_path.parent
                html_patterns = ['DraftImproved_*.html', 'Article_*.html', '今日头条文章_*.html', '文章草稿完善_*.html']
                html_files = []
                for pattern in html_patterns:
                    html_files.extend(article_dir.glob(pattern))

                if html_files:
                    # 获取进程启动后生成的最新HTML文件
                    start_time = proc_info['start_time']
                    recent_files = [f for f in html_files if f.stat().st_mtime > start_time]
                    if recent_files:
                        latest_html = max(recent_files, key=lambda p: p.stat().st_mtime)
                        html_path = str(latest_html.absolute())
                        html_url = f'file:///{html_path.replace(chr(92), "/")}'
                        output_so_far += f'\n[文章链接] {html_url}'

                        try:
                            chrome_paths = [
                                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                            ]
                            chrome_exe = None
                            for cp in chrome_paths:
                                if os.path.exists(cp):
                                    chrome_exe = cp
                                    break

                            if chrome_exe:
                                subprocess.Popen([chrome_exe, html_path], shell=False)
                                output_so_far += f'\n[浏览器] 已在Chrome中打开HTML文件'
                            else:
                                os.startfile(html_path)
                                output_so_far += f'\n[浏览器] 已在默认浏览器中打开HTML文件'
                        except Exception as e:
                            output_so_far += f'\n[提示] HTML文件: {latest_html.name}'

            return jsonify({
                'success': True,
                'filename': proc_info['filename'],
                'status': 'completed',
                'elapsed_time': round(elapsed_time, 1),
                'output': output_so_far,
                'returncode': 0
            })

        # 检查是否超时(5分钟) - 如果超时且输出中有成功标记,视为完成
        if elapsed_time > 300:  # 5分钟超时
            if 'HTML文件已保存' in output_so_far or '生成完成' in output_so_far or '[SUCCESS]' in output_so_far or '[OUTPUT] HTML:' in output_so_far:
                return jsonify({
                    'success': True,
                    'filename': proc_info['filename'],
                    'status': 'completed',
                    'elapsed_time': round(elapsed_time, 1),
                    'output': output_so_far + '\n[提示] 任务已完成(超时检测)',
                    'returncode': 0
                })

        return jsonify({
            'success': True,
            'filename': proc_info['filename'],
            'status': 'running',
            'elapsed_time': round(elapsed_time, 1),
            'output': output_so_far if output_so_far else '正在运行...',
            'returncode': None
        })
    else:
        # 进程已结束 - 使用communicate()获取剩余输出
        try:
            stdout, stderr = process.communicate(timeout=5)
            output = stdout.decode('utf-8', errors='ignore')
            error = stderr.decode('utf-8', errors='ignore')

            if error:
                output += f'\n[stderr]\n{error}'

            # 追加到之前的输出
            if proc_info.get('output'):
                output = proc_info['output'] + output
        except:
            # communicate()超时或失败,使用已缓存的输出
            output = proc_info.get('output', '输出读取失败')

        # 对于头条文章生成器,检测生成的HTML文件
        tool_path = proc_info.get('tool_path')
        if tool_path and 'toutiao_article_generator' in str(tool_path) and return_code == 0:
            article_dir = tool_path.parent
            html_patterns = ['DraftImproved_*.html', 'Article_*.html', '今日头条文章_*.html', '文章草稿完善_*.html']
            html_files = []
            for pattern in html_patterns:
                html_files.extend(article_dir.glob(pattern))

            if html_files:
                # 获取进程启动后生成的最新HTML文件
                start_time = proc_info['start_time']
                recent_files = [f for f in html_files if f.stat().st_mtime > start_time]
                if recent_files:
                    latest_html = max(recent_files, key=lambda p: p.stat().st_mtime)
                    html_path = str(latest_html.absolute())
                    html_url = f'file:///{html_path.replace(chr(92), "/")}'
                    output += f'\n[OUTPUT] HTML: {latest_html.name}'
                    output += f'\n[文章链接] {html_url}'

                    # 自动用Chrome打开生成的HTML文件
                    try:
                        import subprocess
                        # 使用Chrome打开HTML文件
                        chrome_paths = [
                            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                        ]
                        chrome_exe = None
                        for cp in chrome_paths:
                            if os.path.exists(cp):
                                chrome_exe = cp
                                break

                        if chrome_exe:
                            subprocess.Popen([chrome_exe, html_path], shell=False)
                            output += f'\n[浏览器] 已在Chrome中打开HTML文件'
                        else:
                            # 如果找不到Chrome，使用默认浏览器
                            os.startfile(html_path)
                            output += f'\n[浏览器] 已在默认浏览器中打开HTML文件'
                    except Exception as e:
                        output += f'\n[提示] HTML文件: {latest_html.name}'

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
    print("启动Web服务器: http://localhost:5001")
    print("=" * 80)
    print()

    # 启动Flask服务器(关闭debug模式,避免运行时修改文件导致重启)
    app.run(host='0.0.0.0', port=5001, debug=False)

if __name__ == '__main__':
    main()
