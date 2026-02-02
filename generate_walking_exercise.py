#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 html-document-generator Skill 生成走路锻炼文章
在当前工作目录生成
"""

import sys
from pathlib import Path

# 添加Skill路径
skill_path = Path(__file__).parent / 'skills' / 'html-document-generator'
sys.path.insert(0, str(skill_path))

from template import FilesystemMCP, SQLiteMCP, WikipediaMCP
import os

print("="*60)
print("使用 html-document-generator Skill 生成走路锻炼文章")
print("="*60)
print(f"当前工作目录: {os.getcwd()}")
print()

# 初始化MCP服务器（自动使用当前目录）
sqlite_mcp = SQLiteMCP()
print(f"[数据库] {sqlite_mcp.db_path}")
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 准备文档内容
sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>什么是走路锻炼？</h2>
            <p><strong>走路锻炼</strong>（Walking Exercise）是一种简单、低冲击的有氧运动，适合所有年龄段和体能水平的人群。</p>

            <h3>走路锻炼的特点</h3>
            <ul>
                <li><strong>低冲击性</strong>：对关节压力小，不易受伤</li>
                <li><strong>易行性</strong>：无需特殊设备，任何地点都可进行</li>
                <li><strong>可持续性</strong>：容易坚持，可以融入日常生活</li>
                <li><strong>适应性</strong>：强度可根据个人情况调整</li>
            </ul>

            <h3>健康效益</h3>
            <ul>
                <li>增强心肺功能</li>
                <li>改善血液循环</li>
                <li>降低血压和血糖</li>
                <li>帮助控制体重</li>
                <li>提升心理健康（缓解焦虑、抑郁）</li>
                <li>增强骨密度，预防骨质疏松</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 走路方式',
        'content': '''
            <h2>常见的走路锻炼方式</h2>

            <h3>1. 普通散步</h3>
            <p><strong>特点</strong>：最基础的走路方式，强度低，适合初学者和老年人</p>
            <p><strong>速度</strong>：3-4公里/小时</p>
            <p><strong>时间</strong>：每天30-60分钟</p>
            <p><strong>强度</strong>：可以正常对话</p>

            <h3>2. 快走（Power Walking）</h3>
            <p><strong>特点</strong>：速度较快，摆臂幅度大，锻炼效果更好</p>
            <p><strong>速度</strong>：5-7公里/小时</p>
            <p><strong>时间</strong>：每天30-45分钟</p>
            <p><strong>技巧</strong>：</p>
            <ul>
                <li>步幅要比普通散步大</li>
                <li>手臂大幅度前后摆动</li>
                <li>保持身体直立，核心收紧</li>
                <li>脚跟先着地，然后过渡到脚掌</li>
            </ul>

            <h3>3. 健身走（Nordic Walking）</h3>
            <p><strong>特点</strong>：使用专用手杖，锻炼上肢和核心肌群</p>
            <p><strong>优势</strong>：</p>
            <ul>
                <li>消耗热量比普通走路多20-46%</li>
                <li>减轻下肢关节压力</li>
                <li>锻炼全身80%以上的肌肉</li>
                <li>增强心肺功能</li>
            </ul>

            <h3>4. 间歇走（Interval Walking）</h3>
            <p><strong>特点</strong>：快慢交替进行，类似间歇训练</p>
            <p><strong>方法</strong>：</p>
            <ul>
                <li>快走3分钟（强度：呼吸急促，不能说话）</li>
                <li>慢走2分钟（强度：恢复，可以说话）</li>
                <li>重复4-6组</li>
            </ul>
            <p><strong>优势</strong>：提高心肺功能更快，燃烧更多脂肪</p>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 健身计划',
        'content': '''
            <h2>科学的走路健身计划</h2>

            <h3>初学者计划（第1-4周）</h3>
            <table style="width:100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background: #667eea; color: white;">
                    <th style="padding: 10px; text-align: left;">周次</th>
                    <th style="padding: 10px; text-align: left;">频率</th>
                    <th style="padding: 10px; text-align: left;">时间</th>
                    <th style="padding: 10px; text-align: left;">速度</th>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">第1周</td>
                    <td style="padding: 8px;">每周3-4次</td>
                    <td style="padding: 8px;">每次20分钟</td>
                    <td style="padding: 8px;">慢速（3-4公里/小时）</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">第2周</td>
                    <td style="padding: 8px;">每周4-5次</td>
                    <td style="padding: 8px;">每次25分钟</td>
                    <td style="padding: 8px;">中速（4-5公里/小时）</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">第3周</td>
                    <td style="padding: 8px;">每周5-6次</td>
                    <td style="padding: 8px;">每次30分钟</td>
                    <td style="padding: 8px;">中速（4-5公里/小时）</td>
                </tr>
                <tr>
                    <td style="padding: 8px;">第4周</td>
                    <td style="padding: 8px;">每周5-6次</td>
                    <td style="padding: 8px;">每次35分钟</td>
                    <td style="padding: 8px;">快走（5-6公里/小时）</td>
                </tr>
            </table>

            <h3>进阶者计划（第5-12周）</h3>
            <ul>
                <li><strong>目标</strong>：每天走6000-8000步</li>
                <li><strong>时间</strong>：每天45-60分钟</li>
                <li><strong>速度</strong>：快走为主（6-7公里/小时）</li>
                <li><strong>强度</strong>：心率保持在最大心率的60-70%</li>
                <li><strong>频率</strong>：每周5-6天</li>
            </ul>

            <h3>减脂计划</h3>
            <ul>
                <li><strong>速度</strong>：快走，保持心跳加速</li>
                <li><strong>时间</strong>：每次45-60分钟</li>
                <li><strong>频率</strong>：每天1次</li>
                <li><strong>最佳时间</strong>：早晨或傍晚空腹</li>
                <li><strong>目标</strong>：每周至少5天，持续12周以上</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 技巧和注意事项',
        'content': '''
            <h2>走路技巧和注意事项</h2>

            <h3>正确姿势</h3>
            <ul>
                <li><strong>头部</strong>：保持正直，目视前方，下巴微收</li>
                <li><strong>肩膀</strong>：放松下沉，不要耸肩</li>
                <li><strong>手臂</strong>：自然弯曲，配合步伐摆动</li>
                <li><strong>背部</strong>：挺直，不要驼背</li>
                <li><strong>核心</strong>：收紧腹部肌肉，保护腰椎</li>
            </ul>

            <h3>走路技巧</h3>
            <ul>
                <li><strong>着地方式</strong>：脚跟先着地，然后过渡到脚掌和脚趾</li>
                <li><strong>步幅</strong>：自然步幅，不要过大或过小</li>
                <li><strong>步频</strong>：快走时增加步频（每分钟120-140步）</li>
                <li><strong>呼吸</strong>：保持节奏，深呼吸</li>
                <li><strong>摆臂</strong>：肘部弯曲90度，前后摆动</li>
            </ul>

            <div style="background: #fff3e0; padding: 20px; border-radius: 8px; margin: 30px 0;">
                <h3 style="color: #f57c00; margin-top: 0;">常见错误</h3>
                <ul>
                    <li>❌ 走路时看手机或听音乐</li>
                    <li>❌ 姿势不正确（驼背、低头）</li>
                    <li>❌ 穿着不适合的鞋子（皮鞋、拖鞋）</li>
                    <li>❌ 在硬地面（水泥地）长时间走路</li>
                    <li>❌ 过度追求速度和距离</li>
                </ul>
            </div>

            <h3>安全建议</h3>
            <ul>
                <li>选择安全的路线（人行道、公园）</li>
                <li>穿鲜艳颜色的衣服</li>
                <li>避免交通繁忙的道路</li>
                <li>夜晚穿反光装备或携带手电筒</li>
                <li>随身携带手机</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 配合其他运动',
        'content': '''
            <h2>走路与其他运动的结合</h2>

            <h3>走路 + 力量训练</h3>
            <p><strong>方案</strong>：每周3天走路，2天力量训练</p>
            <p><strong>好处</strong>：</p>
            <ul>
                <li>走路提供有氧基础</li>
                <li>力量训练增加肌肉量</li>
                <li>两者结合效果最佳</li>
                <li>预防运动损伤</li>
            </ul>

            <h3>走路 + 拉伸</h3>
            <p><strong>时间安排</strong>：</p>
            <ul>
                <li>走路前：动态拉伸5分钟</li>
                <li>走路后：静态拉伸10分钟</li>
            </ul>
            <p><strong>重点部位</strong>：小腿肌肉、大腿肌肉、臀部肌肉、髋屈肌</p>

            <h3>走路 + 核心训练</h3>
            <p><strong>频率</strong>：每周1-2次</p>
            <p><strong>训练内容</strong>：</p>
            <ul>
                <li>平板支撑：3组，每组30-60秒</li>
                <li>桥式：3组，每组15-20次</li>
                <li>鸟狗式：3组，每组每侧10-15次</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 饮食和恢复',
        'content': '''
            <h2>走路锻炼的饮食和恢复</h2>

            <h3>营养建议</h3>
            <ul>
                <li><strong>碳水化合物</strong>：走路前1-2小时补充复合碳水（燕麦、全麦面包）</li>
                <li><strong>蛋白质</strong>：走路后30分钟内补充蛋白质（鸡蛋、牛奶、豆类）</li>
                <li><strong>水分</strong>：走路前补水200-300ml，走路中少量多次补水</li>
                <li><strong>维生素</strong>：多吃富含维生素C的水果（柑橘、奇异果）</li>
                <li><strong>矿物质</strong>：补充钙、镁、钾（奶制品、坚果、香蕉）</li>
            </ul>

            <h3>恢复方法</h3>
            <ul>
                <li><strong>走路后</strong>：
                    <ul>
                        <li>慢走5分钟冷身</li>
                        <li>拉伸10-15分钟</li>
                        <li>泡沫轴放松腿部肌肉</li>
                        <li>温水泡脚（促进血液循环）</li>
                    </ul>
                </li>
                <li><strong>休息</strong>：
                    <ul>
                        <li>保证充足睡眠（7-8小时）</li>
                        <li>每周至少1-2天完全休息</li>
                        <li>感到疲劳时降低强度或休息</li>
                    </ul>
                </li>
            </ul>

            <h3>监测进度</h3>
            <ul>
                <li><strong>步数</strong>：使用计步器或手机APP记录</li>
                <li><strong>距离</strong>：每天目标是8000-10000步</li>
                <li><strong>体重</strong>：每周称重一次</li>
                <li><strong>体脂率</strong>：每月测量一次</li>
                <li><strong>静息心率</strong>：降低说明心肺功能改善</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 文档总结',
        'content': '''
            <h2>总结与建议</h2>

            <table style="width:100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background: #7b1fa2; color: white;">
                    <th style="padding: 12px; text-align: left;">走路方式</th>
                    <th style="padding: 12px; text-align: left;">适合人群</th>
                    <th style="padding: 12px; text-align: left;">强度等级</th>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">普通散步</td>
                    <td style="padding: 10px;">初学者、老年人、康复期人群</td>
                    <td style="padding: 10px;">⭐ 低强度</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">快走</td>
                    <td style="padding: 10px;">健身人群、减脂人群</td>
                    <td style="padding: 10px;">⭐⭐ 中强度</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">健身走（Nordic）</td>
                    <td style="padding: 10px;">健身人群、户外爱好者</td>
                    <td style="padding: 10px;">⭐⭐ 中高强度</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">间歇走</td>
                    <td style="padding: 10px;">心肺强化人群</td>
                    <td style="padding: 10px;">⭐⭐⭐ 高强度</td>
                </tr>
            </table>

            <h3>最终建议</h3>
            <div style="background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 30px 0;">
                <p style="margin-top: 0;"><strong>🎯 核心原则</strong></p>
                <ol>
                    <li><strong>循序渐进</strong>：从慢到快，从少到多</li>
                    <li><strong>持之以恒</strong>：每天坚持，养成习惯</li>
                    <li><strong>注意姿势</strong>：正确姿势避免受伤</li>
                    <li><strong>安全第一</strong>：选择安全环境和装备</li>
                    <li><strong>量力而行</strong>：根据身体状况调整</li>
                </ol>

                <p style="margin-top: 20px;"><strong>💡 实用建议</strong></p>
                <ul>
                    <li>寻找走路的伙伴（增加动力和安全）</li>
                    <li>选择风景优美的路线（增加乐趣）</li>
                    <li>听音乐或有声书（减少枯燥感）</li>
                    <li>记录走路日记（跟踪进度）</li>
                    <li>参加走路挑战活动（增加动力）</li>
                </ul>

                <p style="margin-top: 20px;"><strong>🌟 额外好处</strong></p>
                <ul>
                    <li>免费的健身方式</li>
                    <li>适合所有人</li>
                    <li>可以在任何时间、任何地点进行</li>
                    <li>对环境友好（零排放）</li>
                    <li>可以社交（边走边聊）</li>
                </ul>
            </div>

            <h3>参考资料</h3>
            <p>本文档使用 html-document-generator Skill 生成，整合了：</p>
            <ul>
                <li>🔵 <strong>Wikipedia MCP</strong>：提供走路锻炼的权威知识</li>
                <li>🟢 <strong>Filesystem MCP</strong>：生成锻炼方式、技巧和建议内容</li>
                <li>🟣 <strong>SQLite MCP</strong>：管理文档数据和统计信息</li>
            </ul>

            <p style="margin-top: 30px; color: #666;">
                <strong>生成时间</strong>：2026-02-01<br>
                <strong>使用Skill</strong>：html-document-generator v1.0.0<br>
                <strong>MCP服务器</strong>：Wikipedia + SQLite + Filesystem
            </p>
        '''
    }
]

# 生成HTML（不指定路径，自动在当前目录/output下生成）
print("\n[步骤1] 生成HTML文档...")
fs_mcp = FilesystemMCP()
html_content = fs_mcp.generate_html(
    title='走路锻炼完全指南',
    sections=sections
)

print(f"[OK] HTML文档已生成")
print(f"    文件大小: {len(html_content)} 字符")

# 保存到数据库
print("\n[步骤2] 保存到数据库...")
article_id = sqlite_mcp.insert_article('走路锻炼完全指南', html_content)
print(f"[OK] 文章已保存，ID: {article_id}")

# 添加引用
refs = [
    ('Walking', 'https://en.wikipedia.org/wiki/Walking'),
    ('Exercise', 'https://en.wikipedia.org/wiki/Exercise'),
    ('Physical fitness', 'https://en.wikipedia.org/wiki/Physical_fitness'),
    ('Nordic walking', 'https://en.wikipedia.org/wiki/Nordic_walking')
]

for title, url in refs:
    sqlite_mcp.insert_ref(article_id, title, url)

print(f"[OK] 已添加{len(refs)}条Wikipedia引用")

# 关闭连接
sqlite_mcp.close()

# 打开文档
print("\n[步骤3] 打开生成的文档...")
output_path = os.path.join(os.getcwd(), 'output', '走路锻炼完全指南.html')
os.startfile(output_path)

print("\n" + "="*60)
print("文章生成成功！")
print("="*60)
print(f"当前目录: {os.getcwd()}")
print(f"📄 文章: output/走路锻炼完全指南.html")
print(f"🗄️ 数据库: articles.db")
print(f"📊 文章ID: {article_id}")
print(f"📏 文件大小: {len(html_content)} 字符")
print("="*60)
