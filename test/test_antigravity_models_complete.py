# -*- coding: utf-8 -*-
"""
测试anti-gravity支持的所有模型（文本+图像）
完整版 - 包含所有26个模型
生成HTML报告并自动打开
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_antigravity_client


def get_quota_recovery_info():
    """获取配额恢复时间信息"""

    now = datetime.now()
    today = now.date()

    # 计算明天上午8点
    tomorrow = now + timedelta(days=1)
    tomorrow_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
    hours_until_tomorrow_8am = int((tomorrow_8am - now).total_seconds() / 3600)

    # 计算明天凌晨0点
    tomorrow_midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    hours_until_midnight = int((tomorrow_midnight - now).total_seconds() / 3600)

    # 计算下月1日
    if today.month == 12:
        next_month = now.replace(year=today.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        next_month = now.replace(month=today.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
    days_until_next_month = (next_month - now).days

    # 计算下周一
    days_until_monday = (0 - now.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = now + timedelta(days=days_until_monday)
    next_monday_str = next_monday.strftime('%m-%d')

    quota_info = {
        "Gemini系列": {
            "恢复时间": f"明天上午8点 ({hours_until_tomorrow_8am}小时后)",
            "说明": "每日UTC 00:00重置,北京时间上午8点",
            "可靠性": "中",
            "颜色": "#ffa500"
        },
        "GLM系列": {
            "恢复时间": f"明天凌晨0点 ({hours_until_midnight}小时后)",
            "说明": "每日重置",
            "可靠性": "中",
            "颜色": "#ffa500"
        },
        "GPT-4系列": {
            "恢复时间": f"下月1日 ({days_until_next_month}天后) 或充值后",
            "说明": "按月计算或需购买付费额度",
            "可靠性": "低",
            "颜色": "#dc3545"
        },
        "Claude系列": {
            "恢复时间": f"下月1日 ({days_until_next_month}天后)",
            "说明": "按月重置,每月1日恢复",
            "可靠性": "低",
            "颜色": "#dc3545"
        },
        "DALL-E系列": {
            "恢复时间": f"下月1日 ({days_until_next_month}天后) 或充值后",
            "说明": "免费层按月计算,建议充值",
            "可靠性": "低",
            "颜色": "#dc3545"
        },
        "Flux/SD系列": {
            "恢复时间": f"下周一 ({next_monday_str}) 或明天",
            "说明": "可能每周或每日重置",
            "可靠性": "中",
            "颜色": "#ffa000"
        },
        "Gemini图像系列": {
            "恢复时间": f"明天上午8点 ({hours_until_tomorrow_8am}小时后)",
            "说明": "与Gemini文本配额可能独立",
            "可靠性": "中",
            "颜色": "#ffa500"
        }
    }

    return quota_info


def test_text_models(client):
    """测试文本生成模型"""
    text_models = [
        # Gemini系列
        ("gemini-2.0-flash-exp", "Gemini", "最新Flash实验版"),
        ("gemini-2.5-pro", "Gemini", "2.5 Pro版本"),
        ("gemini-pro", "Gemini", "标准版"),
        ("gemini-1.5-pro", "Gemini", "1.5 Pro版本"),
        ("gemini-1.5-flash", "Gemini", "1.5 Flash版本"),

        # GPT系列
        ("gpt-4-turbo", "GPT", "GPT-4 Turbo"),
        ("gpt-4o", "GPT", "GPT-4 Omni"),
        ("gpt-4", "GPT", "GPT-4标准版"),
        ("gpt-3.5-turbo", "GPT", "GPT-3.5 Turbo"),

        # Claude系列
        ("claude-sonnet-4-5-20250514", "Claude", "Sonnet 4.5最新版"),
        ("claude-3-5-sonnet-20241022", "Claude", "Sonnet 3.5"),
        ("claude-3-opus-20240229", "Claude", "Opus 3"),

        # GLM系列
        ("glm-4.6", "GLM", "智谱GLM-4.6"),
        ("glm-4", "GLM", "智谱GLM-4"),
    ]

    results = []

    for model_id, series, description in text_models:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": "你好"}],
                max_tokens=10
            )
            content = response.choices[0].message.content if response.choices else "无响应"
            results.append({
                "model_id": model_id,
                "series": series,
                "description": description,
                "type": "text",
                "status": "available",
                "message": "可用",
                "response": content[:50] if content else "无响应"
            })
        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "NOT_FOUND" in error_str:
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "text",
                    "status": "not_found",
                    "message": "模型未找到 (404)",
                    "response": None
                })
            elif "429" in error_str or "quota" in error_str.lower():
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "text",
                    "status": "quota_exceeded",
                    "message": "配额已用尽 (429)",
                    "response": None
                })
            else:
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "text",
                    "status": "error",
                    "message": f"错误: {error_str[:100]}",
                    "response": None
                })

    return results


def test_image_models(client):
    """测试图像生成模型"""
    image_models = [
        # DALL-E系列
        ("dall-e-3", "DALL-E", "OpenAI最新图像模型"),
        ("dall-e-2", "DALL-E", "OpenAI经典图像模型"),

        # Flux系列
        ("flux-1.1-pro", "Flux", "Black Forest Labs 1.1 Pro"),
        ("flux-schnell", "Flux", "Schnell快速版"),
        ("flux-dev", "Flux", "Dev开发版"),

        # Stable Diffusion系列
        ("sd-3", "Stable Diffusion", "SD 3 (stable-diffusion-3)"),
        ("sd-xl-lightning", "Stable Diffusion", "SDXL Lightning"),
        ("sdxl-lightning", "Stable Diffusion", "SDXL Lightning (别名)"),
        ("sdxl-turbo", "Stable Diffusion", "SDXL Turbo"),

        # Gemini图像系列
        ("gemini-3-pro-image-4k", "Gemini Image", "3 Pro Image 4K最高分辨率"),
        ("gemini-3-pro-image-2k", "Gemini Image", "3 Pro Image 2K高分辨率"),
        ("gemini-3-flash-image", "Gemini Image", "3 Flash Image快速版"),
        ("gemini-2-pro-image", "Gemini Image", "2 Pro Image第二代专业版"),
        ("gemini-2-flash-image", "Gemini Image", "2 Flash Image第二代快速版"),
    ]

    results = []

    for model_id, series, description in image_models:
        try:
            response = client.images.generate(
                model=model_id,
                prompt="a cat",
                size="1024x1024"
            )
            results.append({
                "model_id": model_id,
                "series": series,
                "description": description,
                "type": "image",
                "status": "available",
                "message": "可用",
                "response": "图像生成成功"
            })
        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "NOT_FOUND" in error_str:
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "image",
                    "status": "not_found",
                    "message": "模型未找到 (404)",
                    "response": None
                })
            elif "429" in error_str or "quota" in error_str.lower():
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "image",
                    "status": "quota_exceeded",
                    "message": "配额已用尽 (429)",
                    "response": None
                })
            else:
                results.append({
                    "model_id": model_id,
                    "series": series,
                    "description": description,
                    "type": "image",
                    "status": "error",
                    "message": f"错误: {error_str[:100]}",
                    "response": None
                })

    return results


def generate_html_report(text_results, image_results):
    """生成HTML报告"""

    # 统计数据
    text_total = len(text_results)
    text_available = sum(1 for r in text_results if r["status"] == "available")
    text_quota = sum(1 for r in text_results if r["status"] == "quota_exceeded")
    text_not_found = sum(1 for r in text_results if r["status"] == "not_found")
    text_error = sum(1 for r in text_results if r["status"] == "error")

    image_total = len(image_results)
    image_available = sum(1 for r in image_results if r["status"] == "available")
    image_quota = sum(1 for r in image_results if r["status"] == "quota_exceeded")
    image_not_found = sum(1 for r in image_results if r["status"] == "not_found")
    image_error = sum(1 for r in image_results if r["status"] == "error")

    total_models = text_total + image_total
    total_available = text_available + image_available
    total_quota = text_quota + image_quota

    # 获取配额恢复信息
    quota_info = get_quota_recovery_info()

    # 生成HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antigravity完整模型测试报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .meta {{
            opacity: 0.9;
            font-size: 0.9em;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}

        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .summary-card h3 {{
            font-size: 2em;
            margin-bottom: 5px;
            color: #667eea;
        }}

        .summary-card p {{
            color: #666;
            font-size: 0.9em;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 50px;
        }}

        .section h2 {{
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 0.9em;
        }}

        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .status-available {{
            color: #28a745;
            font-weight: 600;
        }}

        .status-quota_exceeded {{
            color: #ffc107;
            font-weight: 600;
        }}

        .status-not_found {{
            color: #dc3545;
            font-weight: 600;
        }}

        .status-error {{
            color: #dc3545;
            font-weight: 600;
        }}

        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
        }}

        .badge-text {{
            background: #e3f2fd;
            color: #1976d2;
        }}

        .badge-image {{
            background: #fff3e0;
            color: #f57c00;
        }}

        .response {{
            font-family: monospace;
            background: #f8f9fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #666;
        }}

        .stats-detail {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }}

        .stats-detail h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}

        .stats-detail ul {{
            list-style: none;
            padding-left: 0;
        }}

        .stats-detail li {{
            padding: 5px 0;
        }}

        .quota-section {{
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            border-left: 5px solid #ff9800;
            padding: 30px;
            margin: 30px 0;
            border-radius: 12px;
        }}

        .quota-section h2 {{
            color: #e65100;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}

        .quota-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .quota-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #ff9800;
        }}

        .quota-card h3 {{
            color: #e65100;
            margin-bottom: 10px;
            font-size: 1.2em;
        }}

        .quota-card .time {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }}

        .quota-card .desc {{
            color: #666;
            font-size: 0.9em;
            line-height: 1.5;
        }}

        .quota-card .reliability {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Antigravity 完整模型测试报告</h1>
            <p class="meta">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p class="meta" style="font-size: 0.85em; margin-top: 10px;">测试范围: 文本模型(14个) + 图像模型(14个) = 总计28个模型</p>
        </div>

        <div class="summary">
            <div class="summary-card">
                <h3>{total_models}</h3>
                <p>总模型数</p>
            </div>
            <div class="summary-card">
                <h3>{total_available}</h3>
                <p>当前可用</p>
            </div>
            <div class="summary-card">
                <h3>{total_quota}</h3>
                <p>配额耗尽</p>
            </div>
            <div class="summary-card">
                <h3>{text_total}</h3>
                <p>文本模型</p>
            </div>
            <div class="summary-card">
                <h3>{image_total}</h3>
                <p>图像模型</p>
            </div>
        </div>

        <!-- 配额恢复时间预测 -->
        <div class="quota-section" id="quota-recovery">
            <h2>⏰ 配额恢复时间预测</h2>
            <p style="color: #666; margin-bottom: 20px;">基于当前时间({datetime.now().strftime('%Y-%m-%d %H:%M')})的智能预测</p>

            <div class="quota-grid">
"""

    # 为每个系列添加配额卡片
    for series_name, info in quota_info.items():
        reliability_emoji = {
            "高": "🟢",
            "中": "🟡",
            "低": "🔴"
        }.get(info["可靠性"], "⚪")

        html += f"""
                <div class="quota-card">
                    <h3>{series_name}</h3>
                    <div class="time" style="color: {info['颜色']};">{info['恢复时间']}</div>
                    <div class="desc">{info['说明']}</div>
                    <div class="reliability" style="background: {info['颜色']}; color: white;">
                        {reliability_emoji} 可靠性: {info['可靠性']}
                    </div>
                </div>
"""

    html += """
            </div>

            <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #4caf50;">
                <h3 style="color: #2e7d32; margin-bottom: 10px;">💡 立即可用的方案</h3>
                <ul style="color: #666; line-height: 1.8;">
                    <li><strong>继续使用</strong>: gpt-3.5-turbo (当前可用)</li>
                    <li><strong>明天上午8点</strong>: Gemini系列可能恢复</li>
                    <li><strong>购买额度</strong>: 需要持续使用时考虑充值</li>
                    <li><strong>免费替代</strong>: Groq、Hugging Face、本地模型</li>
                </ul>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2>📝 文本生成模型 ({text_total}个)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>模型ID</th>
                            <th>系列</th>
                            <th>描述</th>
                            <th>状态</th>
                            <th>响应示例</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for r in text_results:
        status_class = f"status-{r['status']}"
        status_text = {
            'available': '✅ 可用',
            'quota_exceeded': '⚠️ 配额耗尽',
            'not_found': '❌ 未找到',
            'error': '❌ 错误'
        }.get(r['status'], r['message'])

        response_html = f'<span class="response">{r["response"]}</span>' if r["response"] else '-'

        html += f"""
                        <tr>
                            <td><code>{r['model_id']}</code></td>
                            <td>{r['series']}</td>
                            <td>{r['description']}</td>
                            <td class="{status_class}">{status_text}</td>
                            <td>{response_html}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>

                <div class="stats-detail">
                    <h3>文本模型统计</h3>
                    <ul>
                        <li>✅ 可用: """ + str(text_available) + """个</li>
                        <li>⚠️ 配额耗尽: """ + str(text_quota) + """个</li>
                        <li>❌ 未找到: """ + str(text_not_found) + """个</li>
                        <li>❌ 其他错误: """ + str(text_error) + """个</li>
                    </ul>
                </div>
            </div>

            <div class="section">
                <h2>🎨 图像生成模型 (""" + str(image_total) + """个)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>模型ID</th>
                            <th>系列</th>
                            <th>描述</th>
                            <th>状态</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    for r in image_results:
        status_class = f"status-{r['status']}"
        status_text = {
            'available': '✅ 可用',
            'quota_exceeded': '⚠️ 配额耗尽',
            'not_found': '❌ 未找到',
            'error': '❌ 错误'
        }.get(r['status'], r['message'])

        html += f"""
                        <tr>
                            <td><code>{r['model_id']}</code></td>
                            <td>{r['series']}</td>
                            <td>{r['description']}</td>
                            <td class="{status_class}">{status_text}</td>
                        </tr>
"""

    html += f"""
                    </tbody>
                </table>

                <div class="stats-detail">
                    <h3>图像模型统计</h3>
                    <ul>
                        <li>✅ 可用: {image_available}个</li>
                        <li>⚠️ 配额耗尽: {image_quota}个</li>
                        <li>❌ 未找到: {image_not_found}个</li>
                        <li>❌ 其他错误: {image_error}个</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html


def main():
    """主函数"""
    print("="*80)
    print("Antigravity 完整模型测试 (文本26个 + 图像12个)")
    print("="*80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 获取客户端
    client = get_antigravity_client()
    if not client:
        print("[错误] 无法获取anti-gravity客户端")
        return

    print("[1/3] 测试文本生成模型 (14个)...")
    text_results = test_text_models(client)
    print(f"  完成: {len(text_results)}个模型")
    print()

    print("[2/3] 测试图像生成模型 (12个)...")
    image_results = test_image_models(client)
    print(f"  完成: {len(image_results)}个模型")
    print()

    print("[3/3] 生成HTML报告...")
    html_content = generate_html_report(text_results, image_results)

    # 保存HTML文件
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"antigravity_complete_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  报告已保存: {output_file}")
    print()

    print("="*80)
    print("测试完成!")
    print("="*80)
    print(f"总模型数: {len(text_results) + len(image_results)}")
    print(f"文本模型: {len(text_results)}")
    print(f"图像模型: {len(image_results)}")
    print()

    # 打开HTML文件
    import os
    os.startfile(str(output_file))
    print(f"报告已在浏览器中打开")


if __name__ == "__main__":
    main()
