#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用所有调试修复并重启服务器
"""
import os
import subprocess
import sys

os.chdir("C:/D/CAIE_tool/MyAIProduct/post")

print("="*80)
print("应用所有调试修复并重启服务器")
print("="*80)
print()

# 步骤1: 添加tool_manager.py调试
print("步骤1: 添加tool_manager.py调试信息")
print("-"*80)
result = subprocess.run([sys.executable, "add_tool_manager_debug.py"],
                       capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("[ERROR]", result.stderr)

# 步骤2: 清理Python缓存
print()
print("步骤2: 清理Python缓存")
print("-"*80)
subprocess.run([sys.executable, "kill_port_5000.py"], capture_output=True)
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))
    if '__pycache__' in dirs:
        import shutil
        shutil.rmtree(os.path.join(root, '__pycache__'))
print("[OK] 已清理所有.pyc和__pycache__")

# 步骤3: 验证语法
print()
print("步骤3: 验证Python语法")
print("-"*80)
result = subprocess.run([sys.executable, "-m", "py_compile", "article/toutiao_article_generator.py"],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("[OK] toutiao_article_generator.py 语法正确")
else:
    print("[ERROR] 语法错误:")
    print(result.stderr)

result = subprocess.run([sys.executable, "-m", "py_compile", "tool_manager.py"],
                       capture_output=True, text=True)
if result.returncode == 0:
    print("[OK] tool_manager.py 语法正确")
else:
    print("[ERROR] 语法错误:")
    print(result.stderr)

# 步骤4: 启动服务器
print()
print("步骤4: 启动Web服务器")
print("-"*80)
print("[INFO] 启动tool_manager.py在http://localhost:5000")
print("[INFO] 按Ctrl+C停止服务器")
print()

subprocess.run([sys.executable, "tool_manager.py"])
