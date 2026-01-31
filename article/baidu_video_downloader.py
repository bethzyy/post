# -*- coding: utf-8 -*-
"""
百度视频下载工具
支持下载百度新闻、百家号等平台的视频
"""

import sys
import os
from pathlib import Path
import re
import requests
from urllib.parse import urljoin, urlparse
import json

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class BaiduVideoDownloader:
    """百度视频下载器"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def get_video_info(self, url):
        """获取视频信息"""

        print(f"\n[分析] 正在解析视频页面...")
        print(f"[URL] {url}\n")

        try:
            # 请求页面
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'

            html = response.text

            # 保存HTML用于调试
            debug_file = 'baidu_page_debug.html'
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[调试] 页面HTML已保存到: {debug_file}")

            # 尝试多种方式提取视频URL

            # 方法1: 查找所有http/https URL
            all_urls = re.findall(r'https?://[^\s"\'<>]+', html)
            print(f"[调试] 找到 {len(all_urls)} 个URL")

            # 过滤出视频相关的URL
            video_keywords = ['mp4', 'video', 'm3u8', 'flv', 'media']
            video_urls = []
            for url in all_urls:
                url_lower = url.lower()
                if any(keyword in url_lower for keyword in video_keywords):
                    # 清理URL
                    url = url.rstrip('\'"')
                    if url not in video_urls:
                        video_urls.append(url)

            if video_urls:
                print(f"\n[成功] 找到 {len(video_urls)} 个可能视频URL:\n")
                for i, video_url in enumerate(video_urls, 1):
                    print(f"  {i}. {video_url[:150]}")

                # 返回第一个包含mp4的URL
                for url in video_urls:
                    if '.mp4' in url.lower():
                        print(f"\n[选择] 使用MP4格式视频")
                        return url

                # 如果没有mp4,返回第一个
                if video_urls:
                    print(f"\n[选择] 使用第一个视频URL")
                    return video_urls[0]

            print("\n[失败] 未找到视频URL")
            print("[提示] 请检查调试HTML文件: baidu_page_debug.html")
            return None

        except requests.RequestException as e:
            print(f"[错误] 网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"[错误] 解析页面失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _find_urls_in_json(self, data):
        """递归查找JSON中的视频URL"""
        urls = []

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and ('.mp4' in value or 'video' in value.lower()):
                    urls.append(value)
                elif isinstance(value, (dict, list)):
                    urls.extend(self._find_urls_in_json(value))
        elif isinstance(data, list):
            for item in data:
                urls.extend(self._find_urls_in_json(item))

        return urls

    def download_video(self, video_url, output_filename=None):
        """下载视频文件"""

        if not output_filename:
            # 从URL提取文件名
            parsed_url = urlparse(video_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"baidu_video_{os.path.randint(1000, 9999)}.mp4"
            output_filename = filename

        print(f"\n[下载] 开始下载视频...")
        print(f"[保存] {output_filename}\n")

        try:
            # 流式下载
            response = requests.get(video_url, headers=self.headers, stream=True, timeout=60)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            downloaded = 0

            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            print(f"\r[进度] {percent:.1f}% ({mb_downloaded:.1f}MB / {mb_total:.1f}MB)", end='')
                        else:
                            mb_downloaded = downloaded / (1024 * 1024)
                            print(f"\r[进度] {mb_downloaded:.1f}MB", end='')

            print(f"\n\n[成功] 视频下载完成: {output_filename}")
            return output_filename

        except requests.RequestException as e:
            print(f"\n[错误] 下载失败: {e}")
            return None
        except Exception as e:
            print(f"\n[错误] 保存文件失败: {e}")
            return None

    def download_from_url(self, url, output_filename=None):
        """从URL下载完整视频"""

        print("=" * 80)
        print("百度视频下载工具")
        print("=" * 80)

        # 获取视频URL
        video_url = self.get_video_info(url)

        if not video_url:
            print("\n[失败] 无法获取视频链接")
            return False

        # 下载视频
        result = self.download_video(video_url, output_filename)

        if result:
            print("\n" + "=" * 80)
            print("下载完成!")
            print("=" * 80)
            return True
        else:
            print("\n" + "=" * 80)
            print("下载失败!")
            print("=" * 80)
            return False


def get_user_url():
    """获取用户输入的URL"""

    print("\n请输入百度视频URL")
    print()
    print("支持的平台:")
    print("  - 百度新闻 (mbd.baidu.com)")
    print("  - 百家号 (baijiahao.baidu.com)")
    print()

    while True:
        try:
            url = input("\n请输入URL (输入 'q' 退出): ").strip()

            if url.lower() == 'q':
                return None

            if url:
                # 验证URL格式
                if 'baidu.com' in url:
                    return url
                else:
                    print("[提示] 请输入有效的百度视频URL")
            else:
                print("[提示] URL不能为空")

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return None


def get_output_filename():
    """获取输出文件名"""

    print()
    while True:
        try:
            filename = input("请输入输出文件名 (留空自动生成, 输入 'q' 退出): ").strip()

            if filename.lower() == 'q':
                return None

            if not filename:
                return None  # 自动生成

            # 添加.mp4扩展名
            if not filename.endswith('.mp4'):
                filename += '.mp4'

            return filename

        except KeyboardInterrupt:
            print("\n\n[提示] 用户取消输入")
            return None
        except Exception as e:
            print(f"[错误] 输入错误: {e}")
            return None


def main():
    """主函数"""

    print("\n" + "=" * 80)
    print("百度视频下载工具 v1.0")
    print("支持下载百度新闻、百家号等平台的视频")
    print("=" * 80)

    # 如果有命令行参数,直接使用
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # 交互式输入
        url = get_user_url()

        if not url:
            print("\n[退出] 未输入URL")
            return

        output_filename = get_output_filename()

        if output_filename is None:  # 用户输入了'q'
            print("\n[退出] 用户取消")
            return

    # 创建下载器
    downloader = BaiduVideoDownloader()

    # 下载视频
    success = downloader.download_from_url(url, output_filename)

    if success:
        print("\n[成功] 视频下载成功!")
    else:
        print("\n[失败] 视频下载失败!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[提示] 程序被用户中断")
    except Exception as e:
        print(f"\n\n[错误] 发生错误: {e}")
        import traceback
        traceback.print_exc()
