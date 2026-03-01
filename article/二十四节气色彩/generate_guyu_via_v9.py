# -*- coding: utf-8 -*-
"""
谷雨节气配图生成脚本 - 通过V9 Web API
调用本地运行的standalone_image_generator_v9.py服务生成横版配图
"""

import requests
import time
import base64
from pathlib import Path
from datetime import datetime

# V9 API地址
V9_API_URL = "http://localhost:5009/api/generate-image"
V9_SAVE_URL = "http://localhost:5009/api/save-image"

# 输出目录
OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_image_via_v9(theme, style="guofeng_gongbi", save_path=None):
    """通过V9 API生成图像

    Args:
        theme: 主题描述
        style: 风格代码 (guofeng_gongbi, shuica等)
        save_path: 保存路径（绝对路径）

    Returns:
        (success, message, filepath)
    """
    try:
        # 构建横版图片的主题（添加横向构图要求）
        enhanced_theme = f"{theme}, 横版构图16:9比例, 宽幅画卷效果"

        payload = {
            "mode": "theme",
            "theme": enhanced_theme,
            "style": style
        }

        print(f"  [请求] {theme[:50]}...")

        response = requests.post(V9_API_URL, json=payload, timeout=120)

        if response.status_code != 200:
            return False, f"HTTP {response.status_code}", None

        result = response.json()

        if not result.get('success'):
            return False, result.get('error', '未知错误'), None

        # 获取图片数据（base64）
        image_data = result.get('image')
        if not image_data:
            return False, "未返回图片数据", None

        # 保存图片
        if save_path:
            # 通过V9 API保存
            save_payload = {
                "image_data": image_data,
                "save_path": str(save_path)
            }
            save_response = requests.post(V9_SAVE_URL, json=save_payload, timeout=30)

            if save_response.status_code == 200:
                save_result = save_response.json()
                if save_result.get('success'):
                    return True, "保存成功", save_path
                else:
                    return False, save_result.get('error', '保存失败'), None
            else:
                # 直接保存
                image_bytes = base64.b64decode(image_data)
                with open(save_path, 'wb') as f:
                    f.write(image_bytes)
                return True, "直接保存成功", save_path

        return True, "生成成功（未保存）", None

    except requests.exceptions.Timeout:
        return False, "请求超时", None
    except Exception as e:
        return False, str(e), None


def main():
    """主函数"""
    print("=" * 60)
    print("谷雨节气配图生成器 - 通过V9 API")
    print("=" * 60)
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"API地址: {V9_API_URL}")

    # 检查V9服务是否运行
    try:
        response = requests.get("http://localhost:5009", timeout=5)
        print(f"V9服务状态: 运行中")
    except:
        print("错误: V9服务未运行，请先启动 standalone_image_generator_v9.py")
        return

    # 谷雨配图任务
    # 使用"中国风水彩画"风格，最符合节气色彩主题
    tasks = [
        # 第一组：昌荣、紫薄汗、茈藐、紫紶 - 浮萍初生，水面泛紫
        {
            "filename": "guyu_group1_duckweed.jpg",
            "theme": "暮春池塘浮萍初生，水面泛紫，荷叶初露，紫色与嫩绿的浮萍交织，晨雾笼罩古园池塘，紫色倒影映在平静水面",
            "style": "shuica"
        },
        # 第二组：苍葭、庭芜绿、翠微、翠虬 - 斑鸠拂羽，春意更浓
        {
            "filename": "guyu_group2_greenery.jpg",
            "theme": "斑鸠在桑树枝头梳羽，暮春草木葱茏，青苍芦苇在河边摇曳，庭院芜草翠绿，远山青翠淡绿，从近处庭草到远山层层绿意铺开",
            "style": "shuica"
        },
        # 第三组：碧落、挼蓝、青雀头黛、螺子黛 - 戴胜鸟青蓝色系羽冠
        {
            "filename": "guyu_group3_hoopoe.jpg",
            "theme": "戴胜鸟落在桑树上，头顶五彩羽冠，青碧天穹为背景，揉搓蓝草的青色，青雀羽毛的青黑，画眉用的螺子黛青黑颜料，绚丽蓝青色羽冠",
            "style": "shuica"
        },
        # 第四组：露褐、檀褐、緅絺、目童子 - 暮春褐色的过渡
        {
            "filename": "guyu_group4_transition.jpg",
            "theme": "暮春时节草木将老未老，露水浸染的褐色，檀木浅褐，红褐色葛布，深褐瞳孔，温暖的褐色调，金色黄昏光线，春天即将结束夏天即将到来的过渡",
            "style": "shuica"
        },
        # 节气总览图1：谷雨整体意境 - 雨水把庄稼喂饱
        {
            "filename": "guyu_overview_rain.jpg",
            "theme": "谷雨时节雨水滋润稻田和庄稼，细雨落在肥沃农田，幼苗吸饱雨水茁壮生长，颜色变得更浓郁深沉，紫色更深绿色更浓红色更艳，传统农耕景象",
            "style": "shuica"
        },
        # 节气总览图2：谷雨三候图
        {
            "filename": "guyu_overview_three_phases.jpg",
            "theme": "谷雨三候长卷：左侧池塘浮萍初生泛紫，中间斑鸠在葱茏园中梳羽，右侧戴胜鸟落在桑树上，紫绿青褐四色交织，从春天过渡到夏天",
            "style": "shuica"
        }
    ]

    # 生成图片
    generated_files = []
    for i, task in enumerate(tasks, 1):
        print(f"\n[{i}/{len(tasks)}] 生成: {task['filename']}")

        save_path = OUTPUT_DIR / task['filename']

        success, message, filepath = generate_image_via_v9(
            theme=task['theme'],
            style=task['style'],
            save_path=str(save_path)
        )

        if success:
            print(f"  [OK] {task['filename']}")
            generated_files.append({
                'filename': task['filename'],
                'filepath': filepath
            })
        else:
            print(f"  [FAIL] {message}")

        # 等待避免API压力
        if i < len(tasks):
            print("  等待5秒...")
            time.sleep(5)

    # 输出结果
    print("\n" + "=" * 60)
    print("生成完成!")
    print("=" * 60)
    print(f"\n成功生成 {len(generated_files)}/{len(tasks)} 张图片:")
    for f in generated_files:
        print(f"  - {f['filename']}")

    print(f"\n图片保存在: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
