# -*- coding: utf-8 -*-
"""
配置管理模块
从.env文件加载API密钥和配置
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent


def load_env():
    """加载.env文件"""
    env_file = BASE_DIR / ".env"

    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if not line or line.startswith('#'):
                    continue
                # 解析KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


# 自动加载环境变量
load_env()


class Config:
    """配置类"""

    # anti-gravity配置
    ANTIGRAVITY_BASE_URL = os.environ.get('ANTIGRAVITY_BASE_URL', 'http://127.0.0.1:8045/v1')
    ANTIGRAVITY_API_KEY = os.environ.get('ANTIGRAVITY_API_KEY', '')

    # ZhipuAI配置
    ZHIPU_API_KEY = os.environ.get('ZHIPU_API_KEY', '')
    ZHIPU_ANTHROPIC_BASE_URL = os.environ.get('ZHIPU_ANTHROPIC_BASE_URL', 'https://open.bigmodel.cn/api/anthropic')

    # OpenAI配置
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

    # Anthropic官方配置
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

    # Google Gemini配置
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')

    # Volcano/Seedream配置
    VOLCANO_BASE_URL = os.environ.get('VOLCANO_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3')
    VOLCANO_API_KEY = os.environ.get('VOLCANO_API_KEY', '')

    # 图像生成默认配置
    IMAGE_DEFAULT_SIZE = os.environ.get('IMAGE_DEFAULT_SIZE', '1024x1024')
    IMAGE_QUALITY = os.environ.get('IMAGE_QUALITY', 'standard')

    @classmethod
    def display(cls):
        """显示当前配置（隐藏敏感信息）"""
        print("="*80)
        print("当前配置 (Config)")
        print("="*80)
        print(f"anti-gravity Base URL: {cls.ANTIGRAVITY_BASE_URL}")
        print(f"anti-gravity API Key: {cls.ANTIGRAVITY_API_KEY[:20]}...")
        print(f"ZhipuAI API Key: {'已设置' if cls.ZHIPU_API_KEY else '未设置'}")
        print(f"OpenAI API Key: {'已设置' if cls.OPENAI_API_KEY else '未设置'}")
        print(f"Volcano API Key: {'已设置' if cls.VOLCANO_API_KEY else '未设置'}")
        print(f"默认图像尺寸: {cls.IMAGE_DEFAULT_SIZE}")
        print(f"默认图像质量: {cls.IMAGE_QUALITY}")
        print("="*80)


def get_antigravity_client():
    """获取anti-gravity客户端"""
    try:
        from openai import OpenAI
        return OpenAI(
            base_url=Config.ANTIGRAVITY_BASE_URL,
            api_key=Config.ANTIGRAVITY_API_KEY
        )
    except ImportError:
        print("错误: 需要安装 openai 库")
        print("请运行: pip install openai")
        return None


def get_zhipuai_client():
    """获取ZhipuAI客户端(使用原生SDK)"""
    try:
        from zhipuai import ZhipuAI
        if not Config.ZHIPU_API_KEY:
            print("警告: ZHIPU_API_KEY未设置")
            return None
        return ZhipuAI(api_key=Config.ZHIPU_API_KEY)
    except ImportError:
        print("错误: 需要安装 zhipuai 库")
        print("请运行: pip install zhipuai")
        return None


def get_zhipu_anthropic_client():
    """获取ZhipuAI Anthropic兼容客户端"""
    try:
        from anthropic import Anthropic
        if not Config.ZHIPU_API_KEY:
            print("警告: ZHIPU_API_KEY未设置")
            return None
        return Anthropic(
            base_url=Config.ZHIPU_ANTHROPIC_BASE_URL,
            api_key=Config.ZHIPU_API_KEY
        )
    except ImportError:
        print("错误: 需要安装 anthropic 库")
        print("请运行: pip install anthropic")
        return None


def get_volcano_client():
    """获取Volcano/Seedream客户端"""
    try:
        from openai import OpenAI
        if not Config.VOLCANO_API_KEY:
            print("警告: VOLCANO_API_KEY未设置")
            return None
        return OpenAI(
            base_url=Config.VOLCANO_BASE_URL,
            api_key=Config.VOLCANO_API_KEY
        )
    except ImportError:
        print("错误: 需要安装 openai 库")
        print("请运行: pip install openai")
        return None


def get_openai_client():
    """获取OpenAI官方客户端"""
    try:
        from openai import OpenAI
        if not Config.OPENAI_API_KEY:
            print("警告: OPENAI_API_KEY未设置")
            return None
        return OpenAI(api_key=Config.OPENAI_API_KEY)
    except ImportError:
        print("错误: 需要安装 openai 库")
        print("请运行: pip install openai")
        return None


def get_anthropic_client():
    """获取Anthropic官方客户端"""
    try:
        from anthropic import Anthropic
        if not Config.ANTHROPIC_API_KEY:
            print("警告: ANTHROPIC_API_KEY未设置")
            return None
        return Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    except ImportError:
        print("错误: 需要安装 anthropic 库")
        print("请运行: pip install anthropic")
        return None


def get_gemini_client():
    """获取Google Gemini客户端"""
    try:
        import google.generativeai as genai
        if not Config.GOOGLE_API_KEY:
            print("警告: GOOGLE_API_KEY未设置")
            return None
        genai.configure(api_key=Config.GOOGLE_API_KEY)

        # 创建一个包装类，使其接口与其他客户端一致
        class GeminiClientWrapper:
            def __init__(self, model_name):
                self.model = genai.GenerativeModel(model_name)

            class messages:
                @staticmethod
                def create(model, messages, max_tokens=4000):
                    # Gemini的接口不同，需要适配
                    prompt = messages[0]['content']
                    response = model.model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            max_output_tokens=max_tokens,
                            temperature=0.7,
                        )
                    )

                    # 创建一个响应对象来模拟Anthropic/OpenAI的响应格式
                    class Content:
                        def __init__(self, text):
                            self.text = text

                    class Response:
                        def __init__(self, text):
                            self.content = [Content(text)]

                    return Response(response.text)

        return GeminiClientWrapper("gemini-2.0-flash-exp")
    except ImportError:
        print("错误: 需要安装 google-generativeai 库")
        print("请运行: pip install google-generativeai")
        return None


if __name__ == "__main__":
    # 测试配置加载
    Config.display()
