#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修改 toutiao_web_app.py - 草稿模式改为文件路径输入"""

file_path = 'article/toutiao_web_app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改草稿模式的描述
old_desc = '''                <div class="mode-tab" data-mode="draft" onclick="selectMode('draft')">
                    <h3>✏️ 草稿完善</h3>
                    <p>粘贴草稿，AI润色优化</p>
                </div>'''

new_desc = '''                <div class="mode-tab" data-mode="draft" onclick="selectMode('draft')">
                    <h3>✏️ 草稿完善</h3>
                    <p>选择草稿文件，AI润色优化</p>
                </div>'''

content = content.replace(old_desc, new_desc)

# 2. 修改草稿输入区域 - 从textarea改为文件路径输入
old_draft = '''            <!-- 草稿输入 -->
            <div id="draft-section" class="form-group hidden">
                <label>草稿内容</label>
                <textarea id="draft-input" placeholder="在此粘贴您的草稿内容..."></textarea>
            </div>'''

new_draft = '''            <!-- 草稿文件路径 -->
            <div id="draft-section" class="form-group hidden">
                <label>草稿文件路径</label>
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="draft-input" placeholder="例如: article/draft.txt 或 C:\\path\\to\\draft.txt" style="flex: 1;">
                    <button type="button" onclick="selectDraftFile()" style="padding: 12px 20px; background: #e2e8f0; border: none; border-radius: 8px; cursor: pointer;">📁 浏览</button>
                </div>
                <small style="color: #718096; margin-top: 5px; display: block;">支持 .txt 和 .md 格式的草稿文件</small>
            </div>'''

content = content.replace(old_draft, new_draft)

# 3. 修改验证提示
old_validate = '''            if (currentMode === 'draft' && !draft) {
                alert('请输入草稿内容');
                return;
            }'''

new_validate = '''            if (currentMode === 'draft' && !draft) {
                alert('请输入草稿文件路径');
                return;
            }'''

content = content.replace(old_validate, new_validate)

# 4. 添加文件选择函数
old_script_start = '''    <script>
        let currentMode = 'theme';
        let generatedFiles = {};

        function selectMode(mode) {'''

new_script_start = '''    <script>
        let currentMode = 'theme';
        let generatedFiles = {};

        function selectDraftFile() {
            // 由于浏览器安全限制，无法直接访问文件系统
            // 提示用户输入文件路径
            const path = prompt('请输入草稿文件的完整路径:\\n\\n例如: C:\\\\Users\\\\xxx\\\\Documents\\\\draft.txt\\n或者: article/draft.txt (相对路径)');
            if (path) {
                document.getElementById('draft-input').value = path;
            }
        }

        function selectMode(mode) {'''

content = content.replace(old_script_start, new_script_start)

# 5. 修改API调用 - draft字段改为文件路径
old_api = '''                    body: JSON.stringify({
                        mode: currentMode === 'theme' ? '1' : '2',
                        theme: theme,
                        draft: draft,
                        length: parseInt(length),
                        style: style || 'standard',
                        generate_images: generateImages,
                        image_style: imageStyle
                    })'''

new_api = '''                    body: JSON.stringify({
                        mode: currentMode === 'theme' ? '1' : '2',
                        theme: theme,
                        draft_path: draft,
                        length: parseInt(length),
                        style: style || 'standard',
                        generate_images: generateImages,
                        image_style: imageStyle
                    })'''

content = content.replace(old_api, new_api)

# 保存文件
with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("SUCCESS")
