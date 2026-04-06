#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 tool_manager.html"""

import os
import time

# 等待文件稳定
time.sleep(0.5)

file_path = 'templates/tool_manager.html'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """                if (data.success) {
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
                }

            } catch (error) {
                addLog('error', `请求失败: ${error.message}`);
                btn.disabled = false;
                btn.textContent = '▶ 运行';
                btn.classList.remove('running');
            }
        }

        // 检查运行状态(直接运行版本)"""

new_code = """                if (data.success) {
                    currentProcessId = data.process_id;

                    // 检查是否是Web服务类型
                    if (data.url) {
                        // Web服务类型 - 显示URL并打开
                        addLog('success', `Web服务已启动: \${data.url}`);
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
                    addLog('error', `启动失败: \${data.error}`);
                    btn.disabled = false;
                    btn.textContent = '▶ 运行';
                    btn.classList.remove('running');
                }

            } catch (error) {
                addLog('error', `请求失败: \${error.message}`);
                btn.disabled = false;
                btn.textContent = '▶ 运行';
                btn.classList.remove('running');
            }
        }

        // 检查运行状态(直接运行版本)"""

if old_code in content:
    new_content = content.replace(old_code, new_code)
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("NOT_FOUND")
    # 调试：打印找到的代码
    import re
    match = re.search(r"if \(data\.success\) \{[\s\S]{0,500}checkStatusDirect", content)
    if match:
        print("Found similar code block")
