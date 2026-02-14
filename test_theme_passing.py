# -*- coding: utf-8 -*-
"""
测试主题传递
"""
import subprocess
import sys
from pathlib import Path

# 模拟工具管理器调用toutiao_article_generator
tool_dir = Path(__file__).parent / "article"
script_path = tool_dir / "toutiao_article_generator.py"

# 准备输入数据
input_data = "1\n投资人Jason Calacanis警告OpenAI API风险\n2000\nn\n"
input_data = input_data.encode('utf-8')

print("准备调用脚本...")
print(f"脚本路径: {script_path}")
print(f"输入数据: {input_data.decode('utf-8')}")

# 调用脚本
result = subprocess.run(
    [sys.executable, str(script_path)],
    cwd=str(tool_dir),
    input=input_data,
    capture_output=True,
    text=True,
    encoding='utf-8',
    timeout=120
)

print("\n" + "="*80)
print("标准输出:")
print("="*80)
print(result.stdout)

if result.stderr:
    print("\n" + "="*80)
    print("标准错误:")
    print("="*80)
    print(result.stderr)

print("\n" + "="*80)
print("返回码:", result.returncode)
print("="*80)
