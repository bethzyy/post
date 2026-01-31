#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试 you-get 工具"""

from you_get import common as you_get

url = "https://haokan.baidu.com/v?pd=wisenatural&vid=10279466881940791546"

try:
    print(f"[you-get] 正在获取视频信息: {url}")
    you_get.any_download(url=url, info_only=True)
except Exception as e:
    print(f"[错误] you-get执行失败: {e}")
    import traceback
    traceback.print_exc()
