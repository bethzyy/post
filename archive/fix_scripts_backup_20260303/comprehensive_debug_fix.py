#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全面调试修复脚本
添加所有必要的调试信息以定位草稿完善问题
"""

import os
import re

def add_debug_to_toutiao_generator():
    """在toutiao_article_generator.py中添加全面的调试信息"""
    file_path = "C:/D/CAIE_tool/MyAIProduct/post/article/toutiao_article_generator.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 修复入口点 - 添加环境变量检测和调试输出
    old_entry = r"if __name__ == \"__main__\":\s+try:\s+main\(\)"

    new_entry = """if __name__ == "__main__":
    # 添加入口点调试
    print("\\n" + "="*80)
    print("[DEBUG] ========== 入口点调试 ==========")
    print(f"[DEBUG] 当前工作目录: {os.getcwd()}")
    print(f"[DEBUG] Python路径: {os.sys.path[0]}")
    print(f"[DEBUG] ARTICLE_PARAMS_JSON环境变量: {os.environ.get('ARTICLE_PARAMS_JSON', 'NOT SET')}")

    # 检测是否在Web模式下运行
    if os.environ.get("ARTICLE_PARAMS_JSON"):
        print("[DEBUG] 检测到Web模式 - 调用 main_web()")
        print("="*80 + "\\n")
        main_web()
    else:
        print("[DEBUG] 检测到CLI模式 - 调用 main()")
        print("="*80 + "\\n")
        main()"""

    if '[DEBUG] ========== 入口点调试 ==========' in content:
        print("[INFO] 入口点调试已存在,跳过")
    else:
        content = re.sub(old_entry, new_entry, content, flags=re.MULTILINE | re.DOTALL)
        print("[OK] 已添加入口点环境变量检测和调试输出")

    # 2. 在main_web函数开头添加更多调试信息
    old_main_web_start = r'def main_web\(\):\s+"""Web模式主函数'

    new_main_web_start = r'''def main_web():
    """Web模式主函数 - 从tool_manager.py调用"""
    print("\\n" + "="*80)
    print("[ENTER] ========== 进入 main_web() ==========")
    print("[ENTER] Web模式被调用!")
    print("="*80 + "\\n")

    # 立即打印环境变量
    import sys
    print(f"[DEBUG] sys.argv: {sys.argv}")
    print(f"[DEBUG] os.getcwd(): {os.getcwd()}")
    print(f"[DEBUG] ARTICLE_PARAMS_JSON: {os.environ.get('ARTICLE_PARAMS_JSON', 'NOT SET')}")
    print()
'''

    if '[ENTER] ========== 进入 main_web() ========' in content:
        print("[INFO] main_web入口调试已存在,跳过")
    else:
        content = re.sub(old_main_web_start, new_main_web_start, content, count=1)
        print("[OK] 已增强main_web入口调试")

    # 3. 在读取JSON文件后添加调试
    old_json_read = r'with open\(params_json_path, \'r\', encoding=\'utf-8\'\) as f:\s+params = json\.load\(f\)\s+print\(f"\[DEBUG\] 成功读取参数文件'

    new_json_read = r'''with open(params_json_path, 'r', encoding='utf-8') as f:
            params = json.load(f)

        print(f"[DEBUG] ========== JSON文件内容 ==========")
        print(f"[DEBUG] 参数文件路径: {params_json_path}")
        print(f"[DEBUG] JSON原始内容:\\n{json.dumps(params, ensure_ascii=False, indent=2)}")
        print(f"[DEBUG] =====================================\\n")
'''

    if '[DEBUG] ========== JSON文件内容 ==========' in content:
        print("[INFO] JSON读取调试已存在,跳过")
    else:
        content = re.sub(old_json_read, new_json_read, content)
        print("[OK] 已添加JSON文件内容打印")

    # 4. 在草稿文件读取后添加详细调试
    old_draft_read = r'with open\(draft, \'r\', encoding=\'utf-8\'\) as f:\s+draft = f\.read\(\)\s+print\(f"\[草稿完善\] 成功读取草稿文件'

    new_draft_read = r'''with open(draft, 'r', encoding='utf-8') as f:
                    draft = f.read()
                print(f"[草稿完善] ========== 草稿文件内容 ==========")
                print(f"[草稿完善] 文件路径: {draft_path}")
                print(f"[草稿完善] 文件长度: {len(draft)} 字符")
                print(f"[草稿完善] 前100字符预览: {draft[:100]}")
                print(f"[草稿完善] ======================================\\n")
'''

    # 需要先保存原始路径
    if 'draft_path = draft' not in content:
        # 在读取文件之前保存路径
        old_draft_check = r'if os\.path\.exists\(draft\):'
        new_draft_check = r'''if os.path.exists(draft):
                draft_path = draft  # 保存原始路径用于调试'''
        content = re.sub(old_draft_check, new_draft_check, content)

    if '[草稿完善] ========== 草稿文件内容 ==========' in content:
        print("[INFO] 草稿读取调试已存在,跳过")
    else:
        content = re.sub(old_draft_read, new_draft_read)
        print("[OK] 已添加草稿文件内容详细打印")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] toutiao_article_generator.py 调试增强完成")
    return True

def add_debug_to_tool_manager():
    """在tool_manager.py中添加全面的调试信息"""
    file_path = "C:/D/CAIE_tool/MyAIProduct/post/tool_manager.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 在run_tool函数开头添加请求调试
    old_run_tool_start = r'@app\.route\(\'/api/run\', methods=\[\'POST\'\]\)\s+def run_tool\(\):'

    new_run_tool_start = r'''@app.route('/api/run', methods=['POST'])
def run_tool():
    # 添加请求调试
    print("\\n" + "="*80)
    print("[REQUEST] ========== 收到Web请求 ==========")
    print(f"[REQUEST] 时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[REQUEST] Method: {request.method}")
    print(f"[REQUEST] Content-Type: {request.content_type}")
    print("="*80 + "\\n")
'''

    if '[REQUEST] ========== 收到Web请求 ==========' in content:
        print("[INFO] 请求调试已存在,跳过")
    else:
        content = re.sub(old_run_tool_start, new_run_tool_start, content)
        print("[OK] 已添加Web请求调试")

    # 2. 在创建JSON文件后添加文件内容打印
    old_json_create = r'json\.dump\(params_dict, f, ensure_ascii=False, indent=2\)\s+params_file = f\.name\s+print\(f"\[DEBUG\] JSON参数文件:'

    new_json_create = r'''json.dump(params_dict, f, ensure_ascii=False, indent=2)
                    params_file = f.name

                # 读取刚创建的JSON文件内容用于调试
                with open(params_file, 'r', encoding='utf-8') as debug_f:
                    json_content = debug_f.read()

                print(f"[DEBUG] ========== 创建的JSON参数文件 ==========")
                print(f"[DEBUG] 文件路径: {params_file}")
                print(f"[DEBUG] 文件存在: {os.path.exists(params_file)}")
                print(f"[DEBUG] JSON内容:\\n{json_content}")
                print(f"[DEBUG] =========================================\\n")
'''

    if '[DEBUG] ========== 创建的JSON参数文件 ==========' in content:
        print("[INFO] JSON文件创建调试已存在,跳过")
    else:
        content = re.sub(old_json_create, new_json_create)
        print("[OK] 已添加JSON文件内容详细打印")

    # 3. 在创建子进程前添加环境变量调试
    old_process_create = r"# 设置环境变量传递参数文件路径\s+env\['ARTICLE_PARAMS_JSON'\] = params_file\s+(process = subprocess\.Popen\(\['python', str\(tool_path\)\])"

    new_process_create = r"""# 设置环境变量传递参数文件路径
                env['ARTICLE_PARAMS_JSON'] = params_file

                print(f"[SUBPROCESS] ========== 创建子进程 ==========")
                print(f"[SUBPROCESS] 命令: python {tool_path}")
                print(f"[SUBPROCESS] 工作目录: {BASE_DIR}")
                print(f"[SUBPROCESS] 环境变量 ARTICLE_PARAMS_JSON: {env.get('ARTICLE_PARAMS_JSON')}")
                print(f"[SUBPROCESS] 完整环境变量数量: {len(env)}")
                print(f"[SUBPROCESS] ======================================\\n")

                process = subprocess.Popen(
                    ['python', str(tool_path)],"""

    if '[SUBPROCESS] ========== 创建子进程 ==========' in content:
        print("[INFO] 子进程创建调试已存在,跳过")
    else:
        content = re.sub(old_process_create, new_process_create)
        print("[OK] 已添加子进程创建调试")

    # 检查是否需要导入time
    if 'import time' not in content:
        # 在import区域添加
        import_section = re.search(r'(import os\\n)', content)
        if import_section:
            content = content.replace(import_section.group(1), import_section.group(1) + 'import time\\n')
            print("[OK] 已添加time模块导入")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] tool_manager.py 调试增强完成")
    return True

if __name__ == "__main__":
    print("="*80)
    print("全面调试修复脚本")
    print("="*80)
    print()

    try:
        print("步骤1: 修复 tool_manager.py")
        print("-"*80)
        add_debug_to_tool_manager()
        print()

        print("步骤2: 修复 toutiao_article_generator.py")
        print("-"*80)
        add_debug_to_toutiao_generator()
        print()

        print("="*80)
        print("[完成] 所有调试信息已添加!")
        print("[提示] 请重启服务器并测试草稿完善功能")
        print("[提示] 查看控制台输出以获取详细调试信息")
        print("="*80)

    except Exception as e:
        print(f"[ERROR] 修复失败: {e}")
        import traceback
        traceback.print_exc()
