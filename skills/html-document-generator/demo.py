#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实战示例：使用 html-document-generator Skill
演示如何生成一篇关于"区块链技术"的文档
"""

import sqlite3
import os
from datetime import datetime

# ==================== 使用Skill的方式 ====================

# 方式1: 直接使用template.py中的类
# ================================================

print("="*60)
print("示例：使用 html-document-generator Skill")
print("="*60)

# 1. 导入Skill中的类
import sys
# 添加当前目录到路径，以便导入template
sys.path.insert(0, os.path.dirname(__file__))

# 直接从template文件导入
from template import WikipediaMCP, SQLiteMCP, FilesystemMCP

# 2. 初始化MCP服务器
print("\n[步骤1] 初始化MCP服务器...")
wiki_mcp = WikipediaMCP()
sqlite_mcp = SQLiteMCP('blockchain_article.db')
fs_mcp = FilesystemMCP()

# 3. 连接数据库
print("[步骤2] 连接数据库...")
sqlite_mcp.connect()
sqlite_mcp.create_tables()

# 4. 准备文档内容
print("[步骤3] 准备文档内容...")

sections = []

# Wikipedia MCP - 提供知识
print("  - 添加Wikipedia知识...")
sections.append({
    'mcp_type': 'wikipedia',
    'label': 'Wikipedia MCP - 知识来源',
    'content': '''
        <h2>什么是区块链？</h2>
        <p><strong>区块链（Blockchain）</strong>是一种分布式账本技术，通过密码学方法产生和存储数据块，并按时间顺序连接成链。</p>

        <h3>核心特点</h3>
        <ul>
            <li><strong>去中心化</strong>：没有中央控制机构</li>
            <li><strong>不可篡改</strong>：一旦记录无法修改</li>
            <li><strong>透明公开</strong>：所有交易公开可查</li>
            <li><strong>匿名性</strong>：保护用户隐私</li>
        </ul>

        <h3>技术原理</h3>
        <p>区块链通过哈希算法将数据块连接，每个区块包含：</p>
        <ul>
            <li>前一个区块的哈希值</li>
            <li>当前区块的交易数据</li>
            <li>时间戳</li>
            <li>随机数（用于挖矿）</li>
        </ul>
    '''
})

# Filesystem MCP - 生成应用场景
print("  - 添加应用场景...")
sections.append({
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP - 内容生成',
    'content': '''
        <h2>区块链的应用场景</h2>

        <h3>1. 金融领域</h3>
        <ul>
            <li><strong>数字货币</strong>：比特币、以太坊等</li>
            <li><strong>跨境支付</strong>：快速、低成本的转账</li>
            <li><strong>智能合约</strong>：自动执行的合约协议</li>
            <li><strong>DeFi</strong>：去中心化金融服务</li>
        </ul>

        <h3>2. 供应链管理</h3>
        <ul>
            <li>产品溯源：追踪商品从生产到销售的全过程</li>
            <li>防伪验证：验证商品真伪</li>
            <li>物流跟踪：实时监控物流状态</li>
        </ul>

        <h3>3. 数字身份</h3>
        <ul>
            <li>身份认证：去中心化身份系统</li>
            <li>学历认证：防止学历造假</li>
            <li>投票系统：透明、不可篡改的投票</li>
        </ul>

        <h3>4. 版权保护</h3>
        <ul>
            <li>数字版权：保护创作者权益</li>
            <li>知识产权：防止盗版和侵权</li>
            <li>内容分发：直接面向消费者</li>
        </ul>
    '''
})

# Filesystem MCP - 生成发展历程
print("  - 添加发展历程...")
sections.append({
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP - 内容生成',
    'content': '''
        <h2>区块链发展历程</h2>

        <h3>第一阶段：萌芽期（2008-2013）</h3>
        <ul>
            <li>2008年：中本聪发布比特币白皮书</li>
            <li>2009年：比特币网络诞生</li>
            <li>2010年：第一个比特币交易（披萨交易）</li>
            <li>2011年：其他加密货币出现</li>
        </ul>

        <h3>第二阶段：探索期（2014-2017）</h3>
        <ul>
            <li>2014年：以太坊智能合约平台</li>
            <li>2015年：区块链技术受到关注</li>
            <li>2016年：ICO热潮开始</li>
            <li>2017年：比特币价格突破1万美元</li>
        </ul>

        <h3>第三阶段：应用期（2018-至今）</h3>
        <ul>
            <li>2018年：企业级区块链应用</li>
            <li>2019年：央行数字货币（CBDC）研究</li>
            <li>2020年：DeFi生态爆发</li>
            <li>2021年：NFT市场火热</li>
            <li>2022-2026年：Web3和元宇宙概念兴起</li>
        </ul>
    '''
})

# SQLite MCP - 添加数据统计
print("  - 添加数据统计...")
sections.append({
    'mcp_type': 'sqlite',
    'label': 'SQLite MCP - 数据管理',
    'content': f'''
        <h2>文档数据统计</h2>

        <table style="width:100%; border-collapse: collapse; margin-top: 20px;">
            <tr style="background: #667eea; color: white;">
                <th style="padding: 12px; text-align: left;">指标</th>
                <th style="padding: 12px; text-align: left;">数值</th>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">文章标题</td>
                <td style="padding: 10px;">区块链技术深度解析</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">章节数量</td>
                <td style="padding: 10px;">4个</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">MCP服务器</td>
                <td style="padding: 10px;">3个（Wikipedia、SQLite、Filesystem）</td>
            </tr>
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px;">生成时间</td>
                <td style="padding: 10px;">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td>
            </tr>
            <tr>
                <td style="padding: 10px;">数据存储</td>
                <td style="padding: 10px;">SQLite数据库（blockchain_article.db）</td>
            </tr>
        </table>

        <h3 style="margin-top: 30px;">MCP服务器贡献</h3>
        <ul>
            <li>🔵 <strong>Wikipedia MCP</strong>：提供区块链的基础知识</li>
            <li>🟣 <strong>SQLite MCP</strong>：管理文章数据和统计信息</li>
            <li>🟢 <strong>Filesystem MCP</strong>：生成应用场景和发展历程内容</li>
        </ul>
    '''
})

# Filesystem MCP - 添加总结
print("  - 添加总结...")
sections.append({
    'mcp_type': 'filesystem',
    'label': 'Filesystem MCP - 结论',
    'content': '''
        <h2>总结与展望</h2>

        <h3>技术挑战</h3>
        <ul>
            <li><strong>可扩展性</strong>：交易速度和吞吐量限制</li>
            <li><strong>能耗问题</strong>：PoW共识机制能源消耗大</li>
            <li><strong>监管合规</strong>：法律法规尚不完善</li>
            <li><strong>用户友好</strong>：技术门槛较高</li>
        </ul>

        <h3>未来趋势</h3>
        <ul>
            <li><strong>Layer 2解决方案</strong>：提高交易速度（如闪电网络）</li>
            <li><strong>跨链技术</strong>：实现不同区块链的互操作</li>
            <li><strong>监管科技</strong>：满足合规要求的解决方案</li>
            <li><strong>Web3集成</strong>：去中心化网络基础设施</li>
        </ul>

        <h3>对个人和企业的影响</h3>
        <p><strong>个人层面</strong>：</p>
        <ul>
            <li>数字资产管理：自主控制资产</li>
            <li>隐私保护：更好的数据控制权</li>
            <li>新的投资机会：参与加密经济</li>
        </ul>

        <p><strong>企业层面</strong>：</p>
        <ul>
            <li>降低成本：去除中间商，提高效率</li>
            <li>增强透明度：建立信任机制</li>
            <li>创新商业模式：智能合约应用</li>
        </ul>

        <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin-top: 30px;">
            <h3 style="color: #1976d2; margin-top: 0;">结论</h3>
            <p>区块链技术正在重塑数字化时代的基础设施。从金融到供应链，从身份认证到版权保护，区块链的应用场景不断扩展。</p>
            <p>虽然面临技术挑战和监管不确定性，但区块链的去中心化、透明、不可篡改的特性，使其成为构建未来信任社会的重要技术。</p>
            <p><strong>学习和拥抱区块链技术</strong>，将帮助我们在数字化浪潮中把握机遇。</p>
        </div>
    '''
})

# 5. 生成HTML文档
print("[步骤4] 生成HTML文档...")
output_path = os.path.join('output', '区块链技术解析.html')
os.makedirs('output', exist_ok=True)

html_content = fs_mcp.generate_html(
    title='区块链技术深度解析',
    sections=sections,
    output_path=output_path
)

print(f"[OK] HTML文档已生成: {output_path}")
print(f"    文件大小: {len(html_content)} 字符")

# 6. 保存到数据库
print("[步骤5] 保存到数据库...")
article_id = sqlite_mcp.insert_article('区块链技术深度解析', html_content)
print(f"[OK] 文章已保存到数据库，ID: {article_id}")

# 7. 添加引用
print("[步骤6] 添加Wikipedia引用...")
refs = [
    ('Blockchain', 'https://en.wikipedia.org/wiki/Blockchain'),
    ('Bitcoin', 'https://en.wikipedia.org/wiki/Bitcoin'),
    ('Ethereum', 'https://en.wikipedia.org/wiki/Ethereum'),
    ('Smart contract', 'https://en.wikipedia.org/wiki/Smart_contract')
]

for title, url in refs:
    sqlite_mcp.insert_ref(article_id, title, url)

print(f"[OK] 已添加{len(refs)}条Wikipedia引用")

# 8. 关闭数据库
print("[步骤7] 清理资源...")
sqlite_mcp.close()

# 9. 打开生成的文档
print("[步骤8] 打开生成的文档...")
os.startfile(output_path)

print("\n" + "="*60)
print("✅ 示例完成！")
print("="*60)
print(f"📄 生成的文档: {output_path}")
print(f"🗄️ 数据库文件: blockchain_article.db")
print(f"📊 文章ID: {article_id}")
print("="*60)
