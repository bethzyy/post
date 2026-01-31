#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接下载MP4工具 - 测试版
用于直接下载已知的视频URL
"""

import sys
import os
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

def download_direct_mp4(video_url, output_filename=None):
    """直接下载MP4视频"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.baidu.com/',
    }

    if not output_filename:
        parsed_url = urlparse(video_url)
        filename = os.path.basename(parsed_url.path)
        if not filename or '.' not in filename:
            filename = f"direct_video_{int(time.time())}.mp4"
        output_filename = filename

    # 保存到工具目录
    tool_dir = Path(__file__).parent
    output_path = str(tool_dir / output_filename)

    print(f"\n[直接下载] 开始下载视频...")
    print(f"[URL] {video_url}")
    print(f"[保存] {output_path}\n")

    try:
        # 流式下载
        response = requests.get(video_url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        mb_downloaded = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        print(f"\r[进度] {percent:.1f}% ({mb_downloaded:.1f}MB / {mb_total:.1f}MB)", end='')
                    else:
                        mb_downloaded = downloaded / (1024 * 1024)
                        print(f"\r[进度] {mb_downloaded:.1f}MB", end='')

        print(f"\n\n[成功] 视频下载完成: {output_path}")
        return output_path

    except requests.RequestException as e:
        print(f"\n[错误] 下载失败: {e}")
        return None
    except Exception as e:
        print(f"\n[错误] 保存文件失败: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("直接MP4下载工具 - 测试版")
    print("=" * 80)

    # 从参数或命令行获取URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("\n请输入视频URL (mp4/m3u8/flv等直链)")
        url = input("URL: ").strip()
        if not url:
            print("\n[退出] 未输入URL")
            sys.exit(1)

        output_filename = input("输出文件名 (留空自动生成): ").strip()
        if not output_filename:
            output_filename = None

    # 下载视频
    result = download_direct_mp4(url, output_filename)

    if result:
        print("\n" + "=" * 80)
        print("下载完成!")
        print("=" * 80)
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("下载失败!")
        print("=" * 80)
        sys.exit(1)
