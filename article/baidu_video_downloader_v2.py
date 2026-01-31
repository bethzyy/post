# -*- coding: utf-8 -*-
"""
百度视频下载工具 v2.0 - Selenium增强版
使用Selenium绕过百度安全验证,支持下载百度新闻、百家号等平台的视频
"""

import sys
import os
from pathlib import Path
import re
import time
import requests
from urllib.parse import urljoin, urlparse

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 尝试导入Selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[警告] 未安装Selenium,将使用基础模式")
    print("[提示] 安装Selenium: pip install selenium")


class BaiduVideoDownloader:
    """百度视频下载器 v2.0 - Selenium增强版"""

    def __init__(self, use_selenium=True):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE

    def get_video_info_with_selenium(self, url):
        """使用Selenium获取视频信息"""

        print(f"\n[Selenium] 正在启动浏览器...")
        print(f"[URL] {url}\n")

        driver = None
        try:
            # 配置Chrome选项
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 无头模式
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')

            # 启动浏览器
            service = Service()
            driver = webdriver.Chrome(service=service, options=chrome_options)

            print("[Selenium] 浏览器已启动")

            # 访问页面
            print("[Selenium] 正在加载页面...")
            driver.get(url)

            # 等待页面加载
            print("[Selenium] 等待页面加载完成...")
            time.sleep(5)  # 等待JavaScript执行

            # 尝试等待视频元素加载
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                print("[Selenium] 检测到视频元素")
            except:
                print("[Selenium] 未检测到video标签,尝试其他方法...")

            # 获取页面HTML
            html = driver.page_source

            # 保存HTML用于调试
            debug_file = 'baidu_page_selenium_debug.html'
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[调试] 页面HTML已保存到: {debug_file}")

            # 方法1: 查找video标签的src属性
            video_urls = re.findall(r'<video[^>]*src=["\']([^"\']+)["\']', html)
            if video_urls:
                print(f"[成功] 从video标签找到 {len(video_urls)} 个URL")
                return video_urls[0]

            # 方法2: 查找所有http/https URL
            all_urls = re.findall(r'https?://[^\s"\'<>]+', html)
            print(f"[调试] 找到 {len(all_urls)} 个URL")

            # 过滤出视频相关的URL
            video_keywords = ['mp4', 'video', 'm3u8', 'flv', 'media']
            video_urls = []
            for url in all_urls:
                url_lower = url.lower()
                if any(keyword in url_lower for keyword in video_keywords):
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

                if video_urls:
                    print(f"\n[选择] 使用第一个视频URL")
                    return video_urls[0]

            # 方法3: 检查网络请求
            print("\n[调试] 尝试从网络请求获取...")
            try:
                # 获取所有网络请求的日志
                logs = driver.get_log('performance')

                for log in logs:
                    message = log['message']
                    if 'Network.response' in message and 'mp4' in message:
                        # 解析JSON获取URL
                        import json
                        data = json.loads(message)
                        try:
                            url = data['message']['params']['response']['url']
                            if '.mp4' in url:
                                print(f"[成功] 从网络请求找到: {url}")
                                return url
                        except:
                            pass
            except Exception as e:
                print(f"[调试] 无法获取网络日志: {e}")

            print("\n[失败] 未找到视频URL")
            print("[提示] 请检查调试HTML文件: baidu_page_selenium_debug.html")
            return None

        except Exception as e:
            print(f"[错误] Selenium执行失败: {e}")
            import traceback
            traceback.print_exc()
            return None

        finally:
            if driver:
                try:
                    driver.quit()
                    print("\n[Selenium] 浏览器已关闭")
                except:
                    pass

    def get_video_info_basic(self, url):
        """基础模式获取视频信息"""

        print(f"\n[基础模式] 正在解析视频页面...")
        print(f"[URL] {url}\n")

        try:
            # 请求页面
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'

            html = response.text

            # 保存HTML用于调试
            debug_file = 'baidu_page_basic_debug.html'
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"[调试] 页面HTML已保存到: {debug_file}")

            # 检查是否是安全验证页面
            if '百度安全验证' in html or '安全验证' in html:
                print("[失败] 遇到百度安全验证")
                print("[提示] 请使用Selenium模式或手动提供Cookie")
                return None

            # 查找所有http/https URL
            all_urls = re.findall(r'https?://[^\s"\'<>]+', html)
            print(f"[调试] 找到 {len(all_urls)} 个URL")

            # 过滤出视频相关的URL
            video_keywords = ['mp4', 'video', 'm3u8', 'flv', 'media']
            video_urls = []
            for url in all_urls:
                url_lower = url.lower()
                if any(keyword in url_lower for keyword in video_keywords):
                    url = url.rstrip('\'"')
                    if url not in video_urls:
                        video_urls.append(url)

            if video_urls:
                print(f"\n[成功] 找到 {len(video_urls)} 个可能视频URL:\n")
                for i, video_url in enumerate(video_urls, 1):
                    print(f"  {i}. {video_url[:150]}")

                for url in video_urls:
                    if '.mp4' in url.lower():
                        print(f"\n[选择] 使用MP4格式视频")
                        return url

                if video_urls:
                    print(f"\n[选择] 使用第一个视频URL")
                    return video_urls[0]

            print("\n[失败] 未找到视频URL")
            return None

        except requests.RequestException as e:
            print(f"[错误] 网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"[错误] 解析页面失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_video_info(self, url):
        """获取视频信息 - 自动选择模式"""

        if self.use_selenium:
            return self.get_video_info_with_selenium(url)
        else:
            return self.get_video_info_basic(url)

    def download_video(self, video_url, output_filename=None):
        """下载视频文件"""

        if not output_filename:
            parsed_url = urlparse(video_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"baidu_video_{int(time.time())}.mp4"
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
        print("百度视频下载工具 v2.0 - Selenium增强版")
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


def main():
    """主函数"""

    print("\n" + "=" * 80)
    print("百度视频下载工具 v2.0 - Selenium增强版")
    print("支持下载百度新闻、百家号等平台的视频")
    print("=" * 80)

    # 检查Selenium是否可用
    if not SELENIUM_AVAILABLE:
        print("\n[提示] Selenium未安装,将使用基础模式")
        print("[提示] 要使用Selenium模式,请运行: pip install selenium")
        print("[提示] 并安装ChromeDriver: https://chromedriver.chromium.org/")
        print()

        choice = input("是否继续使用基础模式? (y/n): ").strip().lower()
        if choice not in ['y', 'yes', '是']:
            print("\n[退出] 请先安装Selenium")
            return

        use_selenium = False
    else:
        print("\n[成功] 检测到Selenium,将使用Selenium模式")
        use_selenium = True

    # 获取URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_filename = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("\n请输入百度视频URL")
        print()

        url = input("URL: ").strip()
        if not url:
            print("\n[退出] 未输入URL")
            return

        output_filename = input("输出文件名 (留空自动生成): ").strip()
        if not output_filename:
            output_filename = None

    # 创建下载器
    downloader = BaiduVideoDownloader(use_selenium=use_selenium)

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
