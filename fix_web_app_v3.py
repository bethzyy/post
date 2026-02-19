#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 toutiao_web_app.py - 文风描述单独一行"""

file_path = 'article/toutiao_web_app.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修改布局 - 将文风描述从 options-row 中移出，单独放一行
old_options = '''            <!-- 选项 -->
            <div class="options-row">
                <div class="form-group">
                    <label>文章长度</label>
                    <select id="length-select">
                        <option value="1500">1500字 (快速阅读)</option>
                        <option value="2000" selected>2000字 (标准长度)</option>
                        <option value="2500">2500字 (深度文章)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>文风描述 <small style="color: #a0aec0; font-weight: normal;">(可选，描述您期望的文章风格)</small></label>
                    <textarea id="style-input" placeholder="例如：
- 汪曾祺风格：简洁平淡，朴实有趣，形散神聚
- 幽默风趣：轻松幽默，适当使用网络流行语
- 严谨学术：专业术语准确，逻辑严密
- 温柔婉约：语言优美，情感细腻

也可以直接描述您想要的风格特点..."
                        style="min-height: 100px; resize: vertical;"></textarea>
                </div>

                <div class="form-group">
                    <label>配图风格</label>
                    <select id="image-style-select">
                        <option value="auto">自动 (AI智能选择)</option>
                        <option value="realistic" selected>真实照片</option>
                        <option value="artistic">艺术创作</option>
                        <option value="cartoon">卡通插画</option>
                        <option value="technical">技术图表</option>
                    </select>
                </div>
            </div>'''

new_options = '''            <!-- 选项 -->
            <div class="options-row">
                <div class="form-group">
                    <label>文章长度</label>
                    <select id="length-select">
                        <option value="1500">1500字 (快速阅读)</option>
                        <option value="2000" selected>2000字 (标准长度)</option>
                        <option value="2500">2500字 (深度文章)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>配图风格</label>
                    <select id="image-style-select">
                        <option value="auto">自动 (AI智能选择)</option>
                        <option value="realistic" selected>真实照片</option>
                        <option value="artistic">艺术创作</option>
                        <option value="cartoon">卡通插画</option>
                        <option value="technical">技术图表</option>
                    </select>
                </div>
            </div>

            <!-- 文风描述 - 单独一行 -->
            <div class="form-group">
                <label>文风描述 <small style="color: #a0aec0; font-weight: normal;">(可选，描述您期望的文章风格)</small></label>
                <textarea id="style-input" placeholder="例如：
- 汪曾祺风格：简洁平淡，朴实有趣，形散神聚，漫不经心中见真意
- 幽默风趣：轻松幽默，适当使用网络流行语，接地气
- 严谨学术：专业术语准确，逻辑严密，引用权威资料
- 温柔婉约：语言优美，情感细腻，如沐春风
- 鲁迅杂文风：犀利辛辣，针砭时弊，一针见血

也可以直接描述您想要的风格特点，越详细越好..."
                    style="min-height: 120px; resize: vertical; width: 100%;"></textarea>
            </div>'''

content = content.replace(old_options, new_options)

# 保存文件
with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("SUCCESS")
