#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修改 toutiao_web_app.py - 文风描述改为大文本框"""

file_path = 'article/toutiao_web_app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改文风描述 - 从input改为textarea
old_style = '''                <div class="form-group">
                    <label>文风描述</label>
                    <input type="text" id="style-input" placeholder="例如：汪曾祺风格、幽默风趣、严谨学术...">
                </div>'''

new_style = '''                <div class="form-group">
                    <label>文风描述 <small style="color: #a0aec0; font-weight: normal;">(可选，描述您期望的文章风格)</small></label>
                    <textarea id="style-input" placeholder="例如：
- 汪曾祺风格：简洁平淡，朴实有趣，形散神聚
- 幽默风趣：轻松幽默，适当使用网络流行语
- 严谨学术：专业术语准确，逻辑严密
- 温柔婉约：语言优美，情感细腻

也可以直接描述您想要的风格特点..."
                        style="min-height: 100px; resize: vertical;"></textarea>
                </div>'''

content = content.replace(old_style, new_style)

# 2. 修改后端API - 支持 draft_path 参数并从文件读取
old_stream = '''def stream_generator(gen, params):
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
            if params['mode'] == '1':
                # 主题生成模式
                output_queue.put(('log', 'info', f"开始生成文章，主题: {params['theme']}"))
                result = gen.generate_article_with_ai(
                    theme=params['theme'],
                    target_length=params['length'],
                    style=params.get('style', 'standard')
                )
            else:
                # 草稿完善模式
                output_queue.put(('log', 'info', '开始完善草稿...'))
                result = gen.improve_article_draft(
                    draft_content=params['draft'],
                    target_length=params['length'],
                    style=params.get('style', 'standard')
                )'''

new_stream = '''def stream_generator(gen, params):
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

            if params['mode'] == '1':
                # 主题生成模式
                output_queue.put(('log', 'info', f"开始生成文章，主题: {params['theme']}"))
                if style != 'standard':
                    output_queue.put(('log', 'info', f"文风: {style[:50]}..."))
                result = gen.generate_article_with_ai(
                    theme=params['theme'],
                    target_length=params['length'],
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
                )'''

content = content.replace(old_stream, new_stream)

# 保存文件
with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("SUCCESS")
