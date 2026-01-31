#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速提取测试 - 在验证码加载前提取视频URL
"""

import sys
import os
from pathlib import Path
import re
import time

# 尝试导入Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[错误] 未安装Selenium")
    sys.exit(1)

# 尝试导入undetected-chromedriver
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False

def fast_extract_video_url(url):
    """快速提取 - 在验证码出现前获取视频URL"""

    print(f"\n[快速提取] 尝试在验证码前提取视频URL")
    print(f"[URL] {url}\n")

    driver = None
    try:
        # 使用undetected-chromedriver
        if UNDETECTED_AVAILABLE:
            print("[快速] 使用undetected-chromedriver")
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = uc.Chrome(options=options, version_main=144)
        else:
            print("[快速] 使用标准Selenium")
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=chrome_options)

        print("[快速] 浏览器已启动")

        # 访问页面
        print("[快速] 正在加载页面...")
        driver.get(url)

        # ✅ 关键：立即提取，不等待
        print("[快速] 立即提取页面内容 (等待1秒)...")
        time.sleep(1)  # 只等待1秒

        # 获取HTML
        html = driver.page_source

        # 检查是否有验证码
        if 'passMod' in html or '验证' in html:
            print("[警告] 验证码已出现，尝试更快的方法...")

        # 保存HTML
        debug_file = 'baidu_page_fast_debug.html'
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"[调试] HTML已保存: {debug_file}")

        # 方法1: 查找video标签
        video_urls = re.findall(r'<video[^>]*src=["\']([^"\']+)["\']', html)
        if video_urls:
            print(f"[成功] 从video标签找到URL: {video_urls[0]}")
            return video_urls[0]

        # 方法2: 查找所有http URL
        all_urls = re.findall(r'https://[^\s"\'<>]+', html)
        print(f"[调试] 找到 {len(all_urls)} 个URL")

        # 过滤视频URL
        video_keywords = ['mp4', 'video', 'm3u8', 'flv', 'media']
        video_urls = []
        for url in all_urls:
            url_lower = url.lower()
            if any(keyword in url_lower for keyword in video_keywords):
                url = url.rstrip('\'"')
                if url not in video_urls:
                    video_urls.append(url)

        if video_urls:
            print(f"\n[成功] 找到 {len(video_urls)} 个视频URL:")
            for i, vurl in enumerate(video_urls, 1):
                print(f"  {i}. {vurl[:150]}")

            # 返回第一个mp4
            for vurl in video_urls:
                if '.mp4' in vurl.lower():
                    print(f"\n[选择] 使用MP4格式")
                    return vurl

            if video_urls:
                print(f"\n[选择] 使用第一个视频URL")
                return video_urls[0]

        print("[失败] 未找到视频URL")
        return None

    except Exception as e:
        print(f"[错误] 快速提取失败: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        if driver:
            try:
                driver.quit()
                print("\n[快速] 浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    # 测试URL
    test_url = "https://haokan.baidu.com/v?vid=mda-rgtd15pn4bggw00h"

    print("=" * 80)
    print("快速视频URL提取测试")
    print("=" * 80)

    video_url = fast_extract_video_url(test_url)

    if video_url:
        print("\n" + "=" * 80)
        print(f"✅ 成功提取视频URL:")
        print(video_url)
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("❌ 提取失败")
        print("=" * 80)
