# -*- coding: utf-8 -*-
"""
批量生成二十四节气配图版MHTML文档
MHTML格式：将图片嵌入为Base64，单个文件包含所有内容
"""

import base64
from pathlib import Path
from datetime import datetime

# 节气数据
SOLAR_TERMS_DATA = {
    "立夏": {
        "colors": [
            ["青粲", "翠缥", "人籁", "水龙吟"],
            ["地籁", "大块", "养生主", "大云"],
            ["溶溶月", "绍衣", "石莲褐", "黑朱"],
            ["朱颜酡", "苕荣", "檎丹", "丹罽"]
        ],
        "hou": ["蝼蝈鸣", "蚯蚓出", "王瓜生"],
        "intro": "立夏来了，蝼蝈开始叫，蚯蚓钻出土，王瓜藤蔓攀爬。古人说立夏有三候：蝼蝈鸣，蚯蚓出，王瓜生。这十六种颜色，便从这三候里来。",
        "summary": "夏天不是突然来的。先是虫子叫了，然后蚯蚓出来了，再然后藤蔓爬上架子。颜色也跟着换，青的变翠了，白的变黄了，像是要把春天收起来，换上夏天的衣裳。",
        "end": "立夏这天，江南有称人的习俗。人往秤上一站，斤两报出来，夏天就正式开始了。颜色也有分量，青的轻，红的重，像是夏天比春天沉甸甸一些。",
        "end2": "颜色也懂得换季。春天的颜色收进箱底，夏天的颜色拿出来晾晒。青的晒得更翠，红的晒得更艳，黄的呢，晒得像麦穗一样饱满。",
        "color_desc": [
            ['"青粲"是青白相间的浅色，如初夏晨光，', '"翠缥"是翠绿与淡青交织的色泽，', '"人籁"取自《庄子》，是人间的声响之色，', '"水龙吟"是水波荡漾的深青之色。'],
            ['"地籁"是大地的声音之色，是土黄与青灰的交织，', '"大块"是天地间浑然一体的苍茫之色，', '"养生主"取自《庄子》，是自然生机的温润之色，', '"大云"是厚重云层的灰白之色。'],
            ['"溶溶月"是月光如水溶溶的淡黄色，', '"绍衣"是承袭的衣裳之色，浅黄中带着温润，', '"石莲褐"是石莲花瓣的褐黄色泽，', '"黑朱"是深红近黑的浓重之色。'],
            ['"朱颜酡"是酒后红润的面色，如石榴花般艳丽，', '"苕荣"是凌霄花的红色，鲜艳夺目，', '"檎丹"是林檎果的红色，是红果的统称，', '"丹罽"是红色毛织品的华贵之色。']
        ],
        "group_summary": [
            "从浅青到深青，是蝼蝈从沉默到鸣叫的声音变化，也是立夏时节清晨、水面、林间层层叠叠的青绿色彩。",
            "这一组土黄灰色系，是蚯蚓钻出土时翻动的泥土颜色，也是立夏时节大地从沉睡中苏醒的色彩。",
            "这一组黄褐色系，是王瓜从开花到结果的色彩变化，从淡黄的花到褐黄的果，再到深红的籽。",
            "从粉红到深红，是初夏石榴花、凌霄花竞相绽放的绚烂，也是立夏时节最热烈奔放的色彩。"
        ],
        "imagery": ["蝼蝈初鸣，夏声渐起", "蚯蚓出土，大地苏醒", "王瓜藤蔓攀爬，果实渐熟", "夏日花开，红艳热烈"],
        "image_files": ["lixia_group1_cicada.png", "lixia_group2_earthworm.png", "lixia_group3_melon.png", "lixia_group4_flowers.png", "lixia_summary_summer.png"],
        "prev": "谷雨_配图版.mhtml",
        "next": "小满_配图版.mhtml"
    }
}

def generate_mhtml(term_name, data, images_dir):
    """生成单个节气的MHTML文档"""
    colors = data["colors"]
    hou = data["hou"]
    color_desc = data.get("color_desc", [["" for _ in range(4)] for _ in range(4)])
    group_summary = data.get("group_summary", ["", "", "", ""])
    imagery = data.get("imagery", ["", "", "", ""])
    image_files = data["image_files"]

    # 读取图片并转换为base64
    images_b64 = {}
    for img_file in image_files:
        img_path = images_dir / img_file
        if img_path.exists():
            with open(img_path, 'rb') as f:
                images_b64[img_file] = base64.b64encode(f.read()).decode('utf-8')
        else:
            print(f"  警告: 图片不存在 {img_path}")
            images_b64[img_file] = ""

    # 生成HTML内容
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{term_name}节气与中国传统色彩</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.8;
            color: #333;
            background: #fff;
        }}
        h1 {{
            font-size: 1.6em;
            text-align: center;
            margin-bottom: 10px;
        }}
        .meta {{
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-bottom: 25px;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 15px;
            margin: 20px 0;
            color: #666;
            line-height: 2;
        }}
        p {{
            margin: 15px 0;
        }}
        h2 {{
            font-size: 1.3em;
            margin-top: 35px;
            margin-bottom: 15px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .nav {{
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .nav a {{
            color: #8B4513;
            text-decoration: none;
        }}
        .color-list {{
            margin: 15px 0;
            padding-left: 0;
            list-style: none;
        }}
        .color-list li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>

<h1>{term_name}节气与中国传统色彩</h1>
<p class="meta">{datetime.now().strftime("%Y-%m-%d")} · 二十四节气色彩</p>

<p>《中国传统色：故宫里的色彩美学》一书中为什么把下面这些颜色归入{term_name}节气？</p>

<blockquote>
{colors[0][0]}、{colors[0][1]}、{colors[0][2]}、{colors[0][3]}<br>
{colors[1][0]}、{colors[1][1]}、{colors[1][2]}、{colors[1][3]}<br>
{colors[2][0]}、{colors[2][1]}、{colors[2][2]}、{colors[2][3]}<br>
{colors[3][0]}、{colors[3][1]}、{colors[3][2]}、{colors[3][3]}
</blockquote>

<p>{data["intro"]}</p>

<p>{data["summary"]}</p>

<h2>第一组：{colors[0][0]}、{colors[0][1]}、{colors[0][2]}、{colors[0][3]}</h2>

<p>对应：{term_name}节气一候"{hou[0]}"的起、承、转、合四色。</p>

<p>色彩意象：{imagery[0]}。</p>

<ul class="color-list">
<li>{color_desc[0][0]}</li>
<li>{color_desc[0][1]}</li>
<li>{color_desc[0][2]}</li>
<li>{color_desc[0][3]}</li>
</ul>

<p>{group_summary[0]}</p>

<img src="cid:{image_files[0]}" alt="{imagery[0]}">

<h2>第二组：{colors[1][0]}、{colors[1][1]}、{colors[1][2]}、{colors[1][3]}</h2>

<p>对应：{term_name}节气二候"{hou[1]}"的起、承、转、合四色。</p>

<p>色彩意象：{imagery[1]}。</p>

<ul class="color-list">
<li>{color_desc[1][0]}</li>
<li>{color_desc[1][1]}</li>
<li>{color_desc[1][2]}</li>
<li>{color_desc[1][3]}</li>
</ul>

<p>{group_summary[1]}</p>

<img src="cid:{image_files[1]}" alt="{imagery[1]}">

<h2>第三组：{colors[2][0]}、{colors[2][1]}、{colors[2][2]}、{colors[2][3]}</h2>

<p>对应：{term_name}节气三候"{hou[2]}"的起、承、转、合四色（其一）。</p>

<p>色彩意象：{imagery[2]}。</p>

<ul class="color-list">
<li>{color_desc[2][0]}</li>
<li>{color_desc[2][1]}</li>
<li>{color_desc[2][2]}</li>
<li>{color_desc[2][3]}</li>
</ul>

<p>{group_summary[2]}</p>

<img src="cid:{image_files[2]}" alt="{imagery[2]}">

<h2>第四组：{colors[3][0]}、{colors[3][1]}、{colors[3][2]}、{colors[3][3]}</h2>

<p>对应：{term_name}节气三候"{hou[2]}"的起、承、转、合四色（其二）。</p>

<p>色彩意象：{imagery[3]}。</p>

<ul class="color-list">
<li>{color_desc[3][0]}</li>
<li>{color_desc[3][1]}</li>
<li>{color_desc[3][2]}</li>
<li>{color_desc[3][3]}</li>
</ul>

<p>{group_summary[3]}</p>

<img src="cid:{image_files[3]}" alt="{imagery[3]}">

<p>{data["end"]}</p>

<img src="cid:{image_files[4]}" alt="{term_name}时节">

<p>{data["end2"]}</p>

<p>（以上解读不代表原书观点）</p>

<div class="nav">
    <a href="{data["prev"]}">← 上一个</a>
    <a href="二十四节气与中国传统色彩.html">目录</a>
    <a href="{data["next"]}">下一个 →</a>
</div>

</body>
</html>'''

    # 构建MHTML内容
    boundary = "----=_NextPart_" + datetime.now().strftime("%Y%m%d%H%M%S")

    mhtml_parts = []
    mhtml_parts.append(f"From: <Saved by Claude Code>")
    mhtml_parts.append(f"Subject: {term_name}节气与中国传统色彩")
    mhtml_parts.append(f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S')}")
    mhtml_parts.append(f"MIME-Version: 1.0")
    mhtml_parts.append(f"Content-Type: multipart/related;")
    mhtml_parts.append(f"\ttype=\"text/html\";")
    mhtml_parts.append(f"\tboundary=\"{boundary}\"")
    mhtml_parts.append("")
    mhtml_parts.append(f"--{boundary}")
    mhtml_parts.append("Content-Type: text/html; charset=\"utf-8\"")
    mhtml_parts.append("Content-Transfer-Encoding: quoted-printable")
    mhtml_parts.append("")
    mhtml_parts.append(html_content)

    # 添加图片部分
    for img_file in image_files:
        if images_b64.get(img_file):
            mhtml_parts.append("")
            mhtml_parts.append(f"--{boundary}")
            mhtml_parts.append(f"Content-Type: image/png")
            mhtml_parts.append(f"Content-Transfer-Encoding: base64")
            mhtml_parts.append(f"Content-Location: cid:{img_file}")
            mhtml_parts.append("")
            # 将base64分成每行76字符
            b64_data = images_b64[img_file]
            b64_lines = [b64_data[i:i+76] for i in range(0, len(b64_data), 76)]
            mhtml_parts.append("\n".join(b64_lines))

    mhtml_parts.append("")
    mhtml_parts.append(f"--{boundary}--")

    return "\n".join(mhtml_parts)


def main():
    """主函数"""
    print("=" * 60)
    print("MHTML文档生成器")
    print("=" * 60)

    base_dir = Path(__file__).parent

    for term_name, data in SOLAR_TERMS_DATA.items():
        print(f"\n生成: {term_name}")

        # 获取图片目录
        term_pinyin = {
            "立夏": "lixia", "小满": "xiaoman", "芒种": "mangzhong",
            "夏至": "xiazhi", "小暑": "xiaoshu", "大暑": "dashu",
            "立秋": "liqiu", "处暑": "chushu", "白露": "bailu",
            "秋分": "qiufen", "寒露": "hanlu", "霜降": "shuangjiang",
            "立冬": "lidong", "小雪": "xiaoxue", "大雪": "daxue",
            "冬至": "dongzhi", "小寒": "xiaohan", "大寒": "dahan"
        }
        images_dir = base_dir / "images" / term_pinyin.get(term_name, term_name.lower())

        # 生成MHTML
        mhtml_content = generate_mhtml(term_name, data, images_dir)

        # 保存文件
        output_path = base_dir / f"{term_name}_配图版.mhtml"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mhtml_content)

        print(f"  保存: {output_path}")
        print(f"  大小: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
