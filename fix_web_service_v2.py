#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复 tool_manager.html 以支持 Web 服务类型工具自动启动 - V2"""

file_path = 'templates/tool_manager.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要修改的行号
found_line = -1
for i, line in enumerate(lines):
    if "addLog('success', `工具已启动`);" in line:
        found_line = i
        break

if found_line == -1:
    print("ERROR: Cannot find target line")
    exit(1)

# 构建新的代码块
new_lines = []
for i, line in enumerate(lines):
    if i == found_line - 1 and "currentProcessId = data.process_id;" in lines[i]:
        # 替换从这里开始
        new_lines.append(lines[i])  # currentProcessId = data.process_id;
        new_lines.append('\n')
        new_lines.append('                    // 检查是否是Web服务类型\n')
        new_lines.append('                    if (data.url) {\n')
        new_lines.append('                        // Web服务类型 - 显示URL并打开\n')
        new_lines.append("                        addLog('success', `Web服务已启动: ${data.url}`);\n")
        new_lines.append("                        addLogWithLink('info', `🔗 点击打开: `, data.url, data.url);\n")
        new_lines.append('\n')
        new_lines.append('                        // 更新按钮状态\n')
        new_lines.append("                        element.classList.add('running');\n")
        new_lines.append("                        btn.textContent = '🌐';\n")
        new_lines.append("                        btn.style.background = '#4299e1';\n")
        new_lines.append('\n')
        new_lines.append('                        // 不需要轮询状态，Web服务会持续运行\n')
        new_lines.append('                    } else {\n')
        new_lines.append('                        // 普通工具 - 开始检查状态\n')
        new_lines.append("                        addLog('success', `工具已启动`);\n")
        new_lines.append('\n')
        new_lines.append('                        // 更新树节点状态\n')
        new_lines.append("                        element.classList.add('running');\n")
        new_lines.append("                        btn.textContent = '🔄';\n")
        new_lines.append('\n')
        new_lines.append('                        // 开始检查状态\n')
        new_lines.append('                        checkStatusDirect(tool, element, btn);\n')
        new_lines.append('                    }\n')
        # 跳过原来的行直到 checkStatusDirect 调用
        skip_until = found_line + 6  # 跳过到 checkStatusDirect 之后的 }
        continue
    elif found_line != -1 and i >= found_line and i <= found_line + 6:
        # 跳过原来的代码块
        continue
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("SUCCESS: File updated with Web service handling")
