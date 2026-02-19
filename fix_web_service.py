#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 tool_manager.html 以支持 Web 服务类型工具自动启动"""

import re

file_path = 'templates/tool_manager.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''                if (data.success) {
                    currentProcessId = data.process_id;
                    addLog('success', `工具已启动`);

                    // 更新树节点状态
                    element.classList.add('running');
                    btn.textContent = '🔄';

                    // 开始检查状态
                    checkStatusDirect(tool, element, btn);

                } else {
                    addLog('error', `启动失败: ${data.error}`);
                    btn.disabled = false;
                    btn.textContent = '▶ 运行';
                    btn.classList.remove('running');
                }'''

new_code = '''                if (data.success) {
                    currentProcessId = data.process_id;

                    // 检查是否是Web服务类型
                    if (data.url) {
                        // Web服务类型 - 显示URL并打开
                        addLog('success', `Web服务已启动: ${data.url}`);
                        addLogWithLink('info', `🔗 点击打开: `, data.url, data.url);

                        // 更新按钮状态
                        element.classList.add('running');
                        btn.textContent = '🌐';
                        btn.style.background = '#4299e1';

                        // 不需要轮询状态，Web服务会持续运行
                    } else {
                        // 普通工具 - 开始检查状态
                        addLog('success', `工具已启动`);

                        // 更新树节点状态
                        element.classList.add('running');
                        btn.textContent = '🔄';

                        // 开始检查状态
                        checkStatusDirect(tool, element, btn);
                    }

                } else {
                    addLog('error', `启动失败: ${data.error}`);
                    btn.disabled = false;
                    btn.textContent = '▶ 运行';
                    btn.classList.remove('running');
                }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("修复成功！已添加 Web 服务类型工具的自动启动支持。")
else:
    print("未找到需要替换的代码块，可能已经修改过了。")
    # 检查是否已经包含新代码
    if 'data.url' in content:
        print("检测到文件已包含 Web 服务处理逻辑。")
    else:
        print("警告：文件结构可能已变化，请手动检查。")
