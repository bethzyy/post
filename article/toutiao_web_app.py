# -*- coding: utf-8 -*-
"""
今日头条文章生成器 - Web版 V1.0
独立运行的Flask Web应用，提供友好的Web界面

功能:
  - 主题生成模式：输入主题，AI从零开始写文章
  - 草稿完善模式：上传或粘贴草稿，AI润色优化
  - 支持多种文章长度和文风
  - 可选自动配图功能
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import base64
import re
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 导入原有的生成器类
from article.toutiao_article_generator import ToutiaoArticleGenerator

app = Flask(__name__)
CORS(app)

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日头条文章生成器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 900px; margin: 0 auto; background: white;
            border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; text-align: center;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .main-content { padding: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; }
        .mode-tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .mode-tab {
            flex: 1; padding: 15px; border: 2px solid #e2e8f0; border-radius: 10px;
            cursor: pointer; text-align: center; transition: all 0.3s; background: #f7fafc;
        }
        .mode-tab:hover { border-color: #667eea; }
        .mode-tab.active {
            border-color: #667eea; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        }
        .mode-tab h3 { margin-bottom: 5px; }
        .mode-tab p { font-size: 0.85em; opacity: 0.8; }
        .mode-tab .badge {
            display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.7em;
            background: rgba(255,255,255,0.2); margin-top: 5px;
        }
        .mode-tab:not(.active) .badge { background: #e2e8f0; color: #4a5568; }
        input[type="text"], textarea, select {
            width: 100%; padding: 12px 15px; border: 2px solid #e2e8f0;
            border-radius: 8px; font-size: 1em; transition: border-color 0.3s;
        }
        input[type="text"]:focus, textarea:focus, select:focus { outline: none; border-color: #667eea; }
        textarea { min-height: 100px; resize: vertical; font-family: inherit; }
        .options-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .checkbox-group { display: flex; align-items: center; gap: 10px; }
        .checkbox-group input[type="checkbox"] { width: 20px; height: 20px; }
        .generate-btn {
            width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 10px; font-size: 1.2em;
            font-weight: 600; cursor: pointer; transition: transform 0.3s, box-shadow 0.3s;
        }
        .generate-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
        .generate-btn:disabled { background: #a0aec0; cursor: not-allowed; transform: none; }
        .progress-section { margin-top: 20px; padding: 20px; background: #f7fafc; border-radius: 10px; display: none; }
        .progress-section.active { display: block; }
        .progress-log {
            font-family: monospace; font-size: 0.9em; line-height: 1.6; max-height: 300px;
            overflow-y: auto; padding: 15px; background: #1a202c; color: #a0aec0; border-radius: 8px;
        }
        .progress-log .success { color: #48bb78; }
        .progress-log .error { color: #f56565; }
        .progress-log .info { color: #4299e1; }
        .result-section { margin-top: 20px; display: none; }
        .result-section.active { display: block; }
        .result-card { background: #f7fafc; border-radius: 10px; padding: 20px; margin-bottom: 15px; }
        .result-card h3 { margin-bottom: 15px; color: #667eea; }
        .article-preview { background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; line-height: 1.8; }
        .btn-group { display: flex; gap: 10px; margin-top: 15px; }
        .action-btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s; }
        .btn-primary { background: #667eea; color: white; }
        .btn-secondary { background: #e2e8f0; color: #4a5568; }
        .action-btn:hover { transform: translateY(-2px); }
        .hidden { display: none !important; }
        @media (max-width: 600px) {
            .container { border-radius: 0; }
            .main-content { padding: 15px; }
            .mode-tabs { flex-direction: column; }
            .options-row { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>今日头条文章生成器</h1>
            <p>AI智能写作 - 一键生成高质量文章</p>
        </div>
        <div class="main-content">
            <div class="mode-tabs">
                <div class="mode-tab active" data-mode="theme" onclick="selectMode('theme')">
                    <h3>主题生成</h3>
                    <p>输入主题，AI快速写作</p>
                </div>
                <div class="mode-tab" data-mode="collaborative" onclick="selectMode('collaborative')">
                    <h3>协作模式</h3>
                    <p>双作者审校，高质量文章</p>
                    <span class="badge">推荐</span>
                </div>
                <div class="mode-tab" data-mode="draft" onclick="selectMode('draft')">
                    <h3>草稿完善</h3>
                    <p>选择草稿文件，AI润色优化</p>
                </div>
            </div>

            <div id="collaborative-info" class="form-group hidden" style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 15px; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 20px;">
                <strong style="color: #667eea;">双作者协作模式说明：</strong><br>
                <span style="color: #4a5568; font-size: 0.9em;">
                作者1负责原创初稿，作者2（主编角色）从专业和读者角度审校，检查内容准确性、可读性和争议点。<br>
                如有问题，作者1根据意见修改，反复迭代直到双方满意。生成高质量文章。
                </span>
            </div>

            <div id="theme-section" class="form-group">
                <label>文章主题</label>
                <input type="text" id="theme-input" placeholder="例如：春季养生指南、AI改变生活、职场沟通技巧...">
            </div>

            <div id="draft-section" class="form-group hidden">
                <label>草稿文件路径</label>
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="draft-input" placeholder="例如: article/draft.txt 或 C:\path\to\draft.txt" style="flex: 1;">
                    <button type="button" onclick="selectDraftFile()" style="padding: 12px 20px; background: #e2e8f0; border: none; border-radius: 8px; cursor: pointer;">浏览</button>
                </div>
                <small style="color: #718096; margin-top: 5px; display: block;">支持 .txt 和 .md 格式的草稿文件</small>
            </div>

            <div class="options-row">
                <div class="form-group">
                    <label>文章长度</label>
                    <select id="length-select">
                        <option value="0" selected>自动 (AI根据需要决定)</option>
                        <option value="1500">1500字 (快速阅读)</option>
                        <option value="2000">2000字 (标准长度)</option>
                        <option value="2500">2500字 (深度文章)</option>
                        <option value="3000">3000字 (长文深度)</option>
                        <option value="4000">4000字 (专题长文)</option>
                    </select>
                </div>
                <div class="form-group" id="rounds-group">
                    <label>协作轮数 <small style="color: #a0aec0; font-weight: normal;">(仅协作模式)</small></label>
                    <select id="rounds-select">
                        <option value="2">2轮 (快速)</option>
                        <option value="3" selected>3轮 (标准)</option>
                        <option value="4">4轮 (深度打磨)</option>
                        <option value="5">5轮 (精雕细琢)</option>
                    </select>
                </div>
            </div>

            <div class="options-row">
                <div class="form-group">
                    <label>配图风格</label>
                    <select id="image-style-select">
                        <option value="auto">自动 (AI智能选择)</option>
                        <option value="realistic" selected>真实照片</option>
                        <option value="artistic">艺术创作</option>
                        <option value="cartoon">卡通插画</option>
                        <option value="watercolor">水彩画风</option>
                        <option value="ink">中国水墨画</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>生成配图 <small style="color: #a0aec0; font-weight: normal;">(0=不生成)</small></label>
                    <input type="number" id="image-count-input" value="3" min="0" max="10" step="1" placeholder="0-10">
                </div>
            </div>

            <div class="form-group">
                <label>文风描述 <small style="color: #a0aec0; font-weight: normal;">(可选，直接指导作者1和作者2的工作原则)</small></label>
                <textarea id="style-input" placeholder="例如：汪曾祺风格、幽默风趣、严谨学术、温柔婉约、鲁迅杂文风等，也可以直接描述您想要的风格特点..." style="min-height: 80px;"></textarea>
            </div>

            <button class="generate-btn" id="generate-btn" onclick="generateArticle()">开始生成</button>

            <div class="progress-section" id="progress-section">
                <h3>生成进度</h3>
                <div class="progress-log" id="progress-log"></div>
            </div>

            <div class="result-section" id="result-section">
                <div class="result-card">
                    <h3>生成结果</h3>
                    <div class="article-preview" id="article-preview"></div>
                    <div class="btn-group">
                        <button class="action-btn btn-primary" onclick="openHtmlFile()">打开HTML文件</button>
                        <button class="action-btn btn-secondary" onclick="copyContent()">复制内容</button>
                        <button class="action-btn btn-secondary" onclick="resetForm()">重新生成</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'theme';
        let generatedFiles = {};

        function selectDraftFile() {
            var path = prompt('请输入草稿文件的完整路径:\\n\\n例如: C:\\\\Users\\\\xxx\\\\Documents\\\\draft.txt\\n或者: article/draft.txt (相对路径)');
            if (path) {
                document.getElementById('draft-input').value = path;
            }
        }

        function selectMode(mode) {
            currentMode = mode;
            document.querySelectorAll('.mode-tab').forEach(function(tab) {
                if (tab.dataset.mode === mode) {
                    tab.classList.add('active');
                } else {
                    tab.classList.remove('active');
                }
            });

            // 主题输入区域：主题生成和协作模式都需要
            document.getElementById('theme-section').classList.toggle('hidden', mode === 'draft');
            // 草稿区域：只有草稿模式显示
            document.getElementById('draft-section').classList.toggle('hidden', mode !== 'draft');
            // 协作模式说明：只有协作模式显示
            document.getElementById('collaborative-info').classList.toggle('hidden', mode !== 'collaborative');
        }

        function addLog(type, message) {
            var logDiv = document.getElementById('progress-log');
            var timestamp = new Date().toLocaleTimeString();
            var span = document.createElement('span');
            span.className = type;
            span.textContent = '[' + timestamp + '] ' + message + '\\n';
            logDiv.appendChild(span);
            logDiv.scrollTop = logDiv.scrollHeight;
        }

        function generateArticle() {
            var btn = document.getElementById('generate-btn');
            var progressSection = document.getElementById('progress-section');
            var resultSection = document.getElementById('result-section');
            var progressLog = document.getElementById('progress-log');

            var theme = document.getElementById('theme-input').value.trim();
            var draft = document.getElementById('draft-input').value.trim();
            var length = document.getElementById('length-select').value;
            var styleInput = document.getElementById('style-input').value.trim();
            var imageStyle = document.getElementById('image-style-select').value;
            var imageCount = parseInt(document.getElementById('image-count-input').value) || 0;
            var rounds = document.getElementById('rounds-select').value;

            // 验证输入
            if ((currentMode === 'theme' || currentMode === 'collaborative') && !theme) {
                alert('请输入文章主题');
                return;
            }
            if (currentMode === 'draft' && !draft) {
                alert('请输入草稿文件路径');
                return;
            }
            if (imageCount < 0 || imageCount > 10) {
                alert('配图数量请在0-10之间');
                return;
            }

            btn.disabled = true;
            btn.textContent = currentMode === 'collaborative' ? '协作生成中...' : '生成中...';
            progressSection.classList.add('active');
            resultSection.classList.remove('active');
            progressLog.innerHTML = '';

            addLog('info', '正在启动生成任务...');

            // 构建请求参数
            var requestData = {
                mode: currentMode === 'draft' ? '2' : '1',
                theme: theme,
                draft_path: draft,
                length: parseInt(length),
                style: styleInput || 'standard',
                image_count: imageCount,
                image_style: imageStyle,
                collaborative: currentMode === 'collaborative' ? 'y' : 'n',
                max_rounds: parseInt(rounds)
            };

            fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            }).then(function(response) {
                var reader = response.body.getReader();
                var decoder = new TextDecoder();

                function read() {
                    return reader.read().then(function(result) {
                        if (result.done) {
                            btn.disabled = false;
                            btn.textContent = '开始生成';
                            return;
                        }
                        var text = decoder.decode(result.value);
                        var lines = text.split('\\n');
                        lines.forEach(function(line) {
                            if (line.startsWith('data: ')) {
                                try {
                                    var data = JSON.parse(line.slice(6));
                                    if (data.type === 'log') {
                                        addLog(data.level || 'info', data.message);
                                    } else if (data.type === 'complete') {
                                        generatedFiles = data.files || {};
                                        showResult(data);
                                    } else if (data.type === 'error') {
                                        addLog('error', data.message);
                                    }
                                } catch (e) {}
                            }
                        });
                        return read();
                    });
                }
                return read();
            }).catch(function(error) {
                addLog('error', '请求失败: ' + error.message);
                btn.disabled = false;
                btn.textContent = '开始生成';
            });
        }

        function showResult(data) {
            var resultSection = document.getElementById('result-section');
            var preview = document.getElementById('article-preview');
            preview.innerHTML = '<h2>' + (data.title || '文章标题') + '</h2>' +
                '<p><strong>字数:</strong> ' + (data.word_count || 0) + '字</p>' +
                '<hr style="margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;">' +
                '<div style="white-space: pre-wrap;">' + (data.content || '').substring(0, 500) + '...</div>';
            resultSection.classList.add('active');
            addLog('success', '文章生成完成！');
            if (data.html_file) {
                addLog('success', 'HTML文件: ' + data.html_file);
            }
            if (data.images && data.images.length > 0) {
                addLog('success', '生成配图: ' + data.images.length + '张');
            }
        }

        function openHtmlFile() {
            if (generatedFiles.html) {
                window.open(generatedFiles.html, '_blank');
            } else {
                alert('HTML文件路径不可用');
            }
        }

        function copyContent() {
            var preview = document.getElementById('article-preview');
            navigator.clipboard.writeText(preview.innerText).then(function() {
                alert('内容已复制到剪贴板');
            });
        }

        function resetForm() {
            document.getElementById('theme-input').value = '';
            document.getElementById('draft-input').value = '';
            document.getElementById('progress-log').innerHTML = '';
            document.getElementById('result-section').classList.remove('active');
            document.getElementById('progress-section').classList.remove('active');
            generatedFiles = {};
        }

        // 保存参数到localStorage
        function saveParams() {
            var params = {
                currentMode: currentMode,
                theme: document.getElementById('theme-input').value,
                draft: document.getElementById('draft-input').value,
                length: document.getElementById('length-select').value,
                style: document.getElementById('style-input').value,
                imageStyle: document.getElementById('image-style-select').value,
                imageCount: document.getElementById('image-count-input').value
            };
            localStorage.setItem('toutiao_params', JSON.stringify(params));
        }

        // 从localStorage加载参数
        function loadParams() {
            var saved = localStorage.getItem('toutiao_params');
            if (saved) {
                try {
                    var params = JSON.parse(saved);
                    if (params.currentMode) {
                        selectMode(params.currentMode);
                    }
                    if (params.theme) {
                        document.getElementById('theme-input').value = params.theme;
                    }
                    if (params.draft) {
                        document.getElementById('draft-input').value = params.draft;
                    }
                    if (params.length) {
                        document.getElementById('length-select').value = params.length;
                    }
                    if (params.style) {
                        document.getElementById('style-input').value = params.style;
                    }
                    if (params.imageStyle) {
                        document.getElementById('image-style-select').value = params.imageStyle;
                    }
                    if (params.imageCount !== undefined) {
                        document.getElementById('image-count-input').value = params.imageCount;
                    }
                } catch (e) {}
            }
        }

        // 页面加载时恢复参数
        window.onload = function() {
            loadParams();
        };

        // 页面关闭前保存参数
        window.onbeforeunload = function() {
            saveParams();
        };
    </script>
</body>
</html>'''


def stream_generator(gen, params):
    """生成器函数，流式返回进度"""
    import queue
    import threading

    output_queue = queue.Queue()

    # 重定向print输出到队列
    original_print = print

    def queued_print(*args, **kwargs):
        message = ' '.join(str(arg) for arg in args)
        output_queue.put(('log', 'info', message))
        original_print(*args, **kwargs)

    # 临时替换print
    import builtins
    builtins.print = queued_print

    def run_generation():
        try:
            # 获取文风描述 - 如果有自定义文风则使用，否则使用默认值
            style = params.get('style', '').strip()
            if not style:
                style = 'standard'

            # 检查是否使用协作模式
            use_collaborative = params.get('collaborative', 'n') == 'y'
            max_rounds = params.get('max_rounds', 3)

            if params['mode'] == '1':
                # 主题生成模式
                target_length = params['length']
                length_desc = "自动" if target_length == 0 else f"{target_length}字"

                if use_collaborative:
                    # 协作模式 - 双作者协作
                    output_queue.put(('log', 'info', f"开始协作生成文章，主题: {params['theme']}"))
                    output_queue.put(('log', 'info', f"模式: 双作者协作 (最多{max_rounds}轮)"))
                    output_queue.put(('log', 'info', f"目标长度: {length_desc}"))
                    if style != 'standard':
                        output_queue.put(('log', 'info', f"文风: {style[:50]}..."))
                    result = gen.generate_article_collaborative(
                        theme=params['theme'],
                        target_length=target_length,
                        style=style,
                        max_rounds=max_rounds
                    )
                else:
                    # 快速模式 - 单次生成
                    output_queue.put(('log', 'info', f"开始生成文章，主题: {params['theme']}"))
                    output_queue.put(('log', 'info', f"目标长度: {length_desc}"))
                    if style != 'standard':
                        output_queue.put(('log', 'info', f"文风: {style[:50]}..."))
                    result = gen.generate_article_with_ai(
                        theme=params['theme'],
                        target_length=target_length,
                        style=style
                    )
            else:
                # 草稿完善模式 - 从文件读取草稿内容
                draft_path = params.get('draft_path', '').strip()
                if not draft_path:
                    output_queue.put(('error', None, '草稿文件路径不能为空'))
                    return

                # 解析文件路径
                base_dir = Path(__file__).parent.parent
                if os.path.isabs(draft_path):
                    file_path = Path(draft_path)
                else:
                    # 相对路径，相对于post目录
                    file_path = base_dir / draft_path

                if not file_path.exists():
                    output_queue.put(('error', None, f'草稿文件不存在: {file_path}'))
                    return

                output_queue.put(('log', 'info', f'读取草稿文件: {file_path}'))
                with open(file_path, 'r', encoding='utf-8') as f:
                    draft_content = f.read()

                output_queue.put(('log', 'info', f'草稿内容: {len(draft_content)}字'))
                if style != 'standard':
                    output_queue.put(('log', 'info', f"文风: {style[:50]}..."))

                result = gen.improve_article_draft(
                    draft_content=draft_content,
                    target_length=params['length'],
                    style=style
                )

            if not result:
                output_queue.put(('error', None, '生成失败，请检查输入参数'))
                return

            output_queue.put(('log', 'success', f"文章生成完成，标题: {result['title']}"))
            output_queue.put(('log', 'info', f"字数: {result['word_count']}"))

            # 如果是协作模式，显示协作轮数
            if result.get('source') == 'collaborative':
                output_queue.put(('log', 'success', f"协作轮数: {result.get('rounds', 'N/A')}轮"))

            # 生成配图
            images = []
            image_count = params.get('image_count', 0)
            if image_count > 0:
                output_queue.put(('log', 'info', f'开始生成{image_count}张配图...'))
                images = gen.generate_article_images(
                    theme=params.get('theme', result['title']),
                    article_content=result['content'],
                    image_style=params.get('image_style', 'realistic'),
                    num_images=image_count
                )
                if images:
                    output_queue.put(('log', 'success', f'配图生成完成，共{len(images)}张'))

            # 保存HTML文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = "".join(c for c in result['title'] if c.isalnum() or c in (' ', '_', '-'))[:20]
            html_filename = f"Article_{safe_title}_{timestamp}.html"
            md_filename = f"Article_{safe_title}_{timestamp}.md"

            # 使用 create_article_html 生成HTML内容，然后保存到文件
            html_content = gen.create_article_html(
                title=result['title'],
                content=result['content'],
                theme=params.get('theme', result['title']),
                images=images
            )

            # 保存HTML文件到article目录
            article_dir = Path(__file__).parent
            html_path = article_dir / html_filename
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            output_queue.put(('log', 'success', f'HTML文件已保存: {html_filename}'))

            # 保存Markdown文件
            md_content = f"# {result['title']}\n\n{result['content']}"
            md_path = article_dir / md_filename
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            output_queue.put(('log', 'success', f'Markdown文件已保存: {md_filename}'))

            output_queue.put(('complete', {
                'title': result['title'],
                'content': result['content'],
                'word_count': result['word_count'],
                'html_file': html_filename,
                'md_file': md_filename,
                'images': images,
                'files': {
                    'html': f'/view/{html_filename}'
                }
            }))

        except Exception as e:
            import traceback
            output_queue.put(('error', None, f'生成错误: {str(e)}'))
            traceback.print_exc()
        finally:
            builtins.print = original_print

    # 启动生成线程
    thread = threading.Thread(target=run_generation)
    thread.start()

    # 流式返回
    while thread.is_alive() or not output_queue.empty():
        try:
            item = output_queue.get(timeout=0.5)
            if item[0] == 'log':
                yield f"data: {json.dumps({'type': 'log', 'level': item[1], 'message': item[2]})}\n\n"
            elif item[0] == 'complete':
                yield f"data: {json.dumps({'type': 'complete', **item[1]})}\n\n"
            elif item[0] == 'error':
                yield f"data: {json.dumps({'type': 'error', 'message': item[2]})}\n\n"
        except queue.Empty:
            continue


@app.route('/')
def index():
    """主页面"""
    response = make_response(render_template_string(HTML_TEMPLATE))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """API: 生成文章"""
    params = request.json

    # 验证参数
    if params.get('mode') == '1' and not params.get('theme'):
        return jsonify({'error': '主题不能为空'}), 400
    if params.get('mode') == '2' and not params.get('draft_path'):
        return jsonify({'error': '草稿文件路径不能为空'}), 400

    gen = ToutiaoArticleGenerator()

    from flask import Response
    return Response(
        stream_generator(gen, params),
        mimetype='text/event-stream'
    )


@app.route('/view/<filename>')
def view_article(filename):
    """查看生成的文章"""
    article_dir = Path(__file__).parent
    from flask import send_from_directory
    return send_from_directory(article_dir, filename)


def main():
    """主函数"""
    print("=" * 80)
    print("                    今日头条文章生成器 - Web版 V1.0")
    print("=" * 80)
    print()
    print("启动Web服务器: http://localhost:5010")
    print("请在浏览器中打开上述地址")
    print()
    print("功能特性:")
    print("  [1] 主题生成 - 输入主题，AI从零开始写作")
    print("  [2] 草稿完善 - 选择草稿文件，AI润色优化")
    print("  [3] 智能配图 - 自动生成3张配图")
    print("  [4] 多种格式 - 支持HTML和Markdown输出")
    print("=" * 80)
    print()

    app.run(host='0.0.0.0', port=5010, debug=False, threaded=True)


if __name__ == '__main__':
    main()
