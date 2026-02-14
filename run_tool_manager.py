#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动工具管理器 - 确保使用最新配置
"""
import sys
import importlib

# 清除模块缓存
if 'tool_manager' in sys.modules:
    del sys.modules['tool_manager']

# 现在导入
import tool_manager

# 启动服务器
if __name__ == '__main__':
    tool_manager.app.run(host='0.0.0.0', port=5000, debug=False)
