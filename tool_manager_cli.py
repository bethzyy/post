#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI发文工具管理器 - 更新版
支持按功能分类的工具管理和快速启动
"""

import os
import subprocess
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

class ToolManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.port = 5000

    def print_header(self):
        """打印标题"""
        print("=" * 80)
        print("[AI发文工具管理器 - 分类整理版]".center(70))
        print("=" * 80)
        print()

    def print_categories(self):
        """显示所有工具分类"""
        print("[工具分类菜单]")
        print("-" * 80)
        print()

        print("[1] bird/      - 鸟类绘画工具 (35个文件)")
        print("    包含: 鸟类绘画生成器、画廊展示、多种模型测试工具")
        print()

        print("[2] picture/   - 节日图像生成 (24个文件)")
        print("    包含: 腊八节、小年图像生成和对比工具")
        print()

        print("[3] article/   - 文章生成工具 (30个文件)")
        print("    包含: 今日头条、美食、饮茶文章生成及配图工具")
        print()

        print("[4] hotspot/   - AI热点研究 (12个文件)")
        print("    包含: 2026 AI趋势分析、实时搜索工具")
        print()

        print("[5] test/      - 测试工具 (7个文件)")
        print("    包含: API测试、模型验证工具")
        print()

        print("[6] 系统工具")
        print("    config.py: API配置管理")
        print()

        print("=" * 80)
        print()

    def get_bird_tools(self):
        """获取鸟类绘画工具列表"""
        tools = []
        bird_dir = self.base_dir / "bird"

        # 查找Python脚本
        for py_file in bird_dir.glob("*.py"):
            tools.append({
                'name': py_file.stem,
                'path': py_file,
                'type': 'Python脚本'
            })

        # 查找HTML画廊
        for html_file in bird_dir.glob("*.html"):
            tools.append({
                'name': html_file.stem,
                'path': html_file,
                'type': 'HTML画廊'
            })

        return tools

    def get_picture_tools(self):
        """获取节日图像生成工具列表"""
        tools = []
        picture_dir = self.base_dir / "picture"

        # 查找Python脚本
        for py_file in picture_dir.glob("*.py"):
            tools.append({
                'name': py_file.stem,
                'path': py_file,
                'type': '节日图像生成'
            })

        return tools

    def get_article_tools(self):
        """获取文章生成工具列表"""
        tools = []
        article_dir = self.base_dir / "article"

        # 查找Python脚本
        for py_file in article_dir.glob("*.py"):
            tools.append({
                'name': py_file.stem,
                'path': py_file,
                'type': '文章生成工具'
            })

        return tools

    def get_hotspot_tools(self):
        """获取AI热点研究工具列表"""
        tools = []
        hotspot_dir = self.base_dir / "hotspot"

        # 查找Python脚本
        for py_file in hotspot_dir.glob("*.py"):
            tools.append({
                'name': py_file.stem,
                'path': py_file,
                'type': 'AI研究工具'
            })

        return tools

    def get_test_tools(self):
        """获取测试工具列表"""
        tools = []
        test_dir = self.base_dir / "test"

        # 查找Python脚本
        for py_file in test_dir.glob("*.py"):
            tools.append({
                'name': py_file.stem,
                'path': py_file,
                'type': '测试工具'
            })

        return tools

    def display_tools(self, category):
        """显示指定分类的工具"""
        if category == '1':
            tools = self.get_bird_tools()
            title = "[Image] 鸟类绘画工具"
        elif category == '2':
            tools = self.get_picture_tools()
            title = "[Festival] 节日图像生成工具"
        elif category == '3':
            tools = self.get_article_tools()
            title = "[Article] 文章生成工具"
        elif category == '4':
            tools = self.get_hotspot_tools()
            title = "[Hot] AI热点研究工具"
        elif category == '5':
            tools = self.get_test_tools()
            title = "[Test] 测试工具"
        else:
            print("[X] 无效的分类选择")
            return []

        print(f"\n{title}")
        print("-" * 80)

        if not tools:
            print("未找到工具")
            return []

        for idx, tool in enumerate(tools, 1):
            print(f"{idx:2d}. [{tool['type']}] {tool['name']}")
            print(f"    路径: {tool['path'].relative_to(self.base_dir)}")

        print()
        return tools

    def run_tool(self, tool_path):
        """运行指定的工具"""
        tool_path = Path(tool_path)

        if not tool_path.exists():
            print(f"[X] 工具不存在: {tool_path}")
            return False

        print(f"\n🚀 启动工具: {tool_path.name}")
        print("-" * 80)

        try:
            if tool_path.suffix == '.py':
                # Python脚本
                subprocess.run(['python', str(tool_path)], check=True)
            elif tool_path.suffix == '.html':
                # HTML文件，在浏览器中打开
                webbrowser.open(f'file://{tool_path.absolute()}')
                print(f"[OK] 已在浏览器中打开: {tool_path.name}")
            else:
                print(f"[X] 不支持的文件类型: {tool_path.suffix}")
                return False

            return True

        except subprocess.CalledProcessError as e:
            print(f"[X] 工具运行失败: {e}")
            return False
        except Exception as e:
            print(f"[X] 发生错误: {e}")
            return False

    def start_web_server(self):
        """启动简单的Web服务器"""
        server_dir = self.base_dir
        os.chdir(server_dir)

        server = HTTPServer(('localhost', self.port), SimpleHTTPRequestHandler)
        print(f"🌐 Web服务器已启动: http://localhost:{self.port}")
        print("📂 服务目录:", server_dir)
        print()

        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        return server

    def interactive_menu(self):
        """交互式菜单"""
        while True:
            self.print_header()
            self.print_categories()

            print("请选择操作:")
            print("  1-5: 查看对应分类的工具")
            print("  0:   退出")
            print("  web: 启动Web服务器")
            print()

            choice = input("请输入选择: ").strip().lower()

            if choice == '0':
                print("\n👋 再见！")
                break
            elif choice == 'web':
                server = self.start_web_server()
                webbrowser.open(f'http://localhost:{self.port}')
                input("\n按Enter停止Web服务器...")
                server.shutdown()
            elif choice in ['1', '2', '3', '4', '5']:
                tools = self.display_tools(choice)

                if tools:
                    print("\n请选择要运行的工具 (输入序号，或0返回):")
                    tool_choice = input("请输入: ").strip()

                    if tool_choice == '0':
                        continue

                    try:
                        tool_idx = int(tool_choice) - 1
                        if 0 <= tool_idx < len(tools):
                            self.run_tool(tools[tool_idx]['path'])
                            input("\n按Enter继续...")
                        else:
                            print("[X] 无效的选择")
                    except ValueError:
                        print("[X] 请输入有效的数字")
            else:
                print("[X] 无效的选择，请重试")
                time.sleep(1)

            # 清屏（可选）
            os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """主函数"""
    manager = ToolManager()

    # 如果命令行参数指定了工具，直接运行
    if len(__import__('sys').argv) > 1:
        tool_path = Path(__import__('sys').argv[1])
        manager.run_tool(tool_path)
    else:
        # 否则启动交互式菜单
        manager.interactive_menu()

if __name__ == '__main__':
    main()
