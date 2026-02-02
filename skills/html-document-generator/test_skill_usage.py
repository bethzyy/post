#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 html-document-generator Skill 的正确使用方式
演示如何作为Python包导入并使用
"""

import sys
import os

# ==================== 方式1: 添加到路径后导入 ====================
print("="*60)
print("测试: html-document-generator Skill 复用")
print("="*60)

# 获取Skill目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = current_dir

print(f"\n[步骤1] Skill目录: {skill_dir}")

# 添加到Python路径
sys.path.insert(0, skill_dir)
print("[OK] Skill目录已添加到Python路径")

# ==================== 导入Skill ====================
print("\n[步骤2] 导入Skill...")

try:
    # 方式A: 从包导入（推荐）
    from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP
    print("[OK] 成功导入: from html_document_generator import ...")

except ImportError as e:
    print(f"[ERROR] 导入失败: {e}")
    print("\n尝试直接导入...")
    # 方式B: 直接导入（备用）
    from template import FilesystemMCP, SQLiteMCP, WikipediaMCP
    print("[OK] 成功导入: from template import ...")

# ==================== 使用Skill生成文档 ====================
print("\n[步骤3] 初始化MCP服务器...")

sqlite_mcp = SQLiteMCP('skill_test.db')
sqlite_mcp.connect()
sqlite_mcp.create_tables()
print("[OK] 数据库已初始化")

print("\n[步骤4] 准备文档内容...")

sections = [
    {
        'mcp_type': 'wikipedia',
        'label': 'Wikipedia MCP - 知识来源',
        'content': '''
            <h2>什么是云计算？</h2>
            <p><strong>云计算（Cloud Computing）</strong>是一种通过互联网按需提供计算服务的模式。</p>

            <h3>核心特点</h3>
            <ul>
                <li><strong>按需自助服务</strong>：用户可以随时获取资源</li>
                <li><strong>广泛的网络访问</strong>：通过网络随时随地访问</li>
                <li><strong>资源池化</strong>：多用户共享计算资源</li>
                <li><strong>快速弹性</strong>：快速扩展或收缩资源</li>
                <li><strong>可计量服务</strong>：按使用量计费</li>
            </ul>

            <h3>服务模式</h3>
            <ul>
                <li><strong>IaaS</strong>：基础设施即服务（如AWS EC2）</li>
                <li><strong>PaaS</strong>：平台即服务（如Google App Engine）</li>
                <li><strong>SaaS</strong>：软件即服务（如Google Docs）</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 应用场景',
        'content': '''
            <h2>云计算的应用场景</h2>

            <h3>1. 企业应用</h3>
            <ul>
                <li>企业资源规划（ERP）</li>
                <li>客户关系管理（CRM）</li>
                <li>办公协作（Office 365, Google Workspace）</li>
            </ul>

            <h3>2. 开发测试</h3>
            <ul>
                <li>开发环境搭建</li>
                <li>自动化测试</li>
                <li>持续集成/持续部署（CI/CD）</li>
            </ul>

            <h3>3. 数据存储</h3>
            <ul>
                <li>云数据库（RDS, DynamoDB）</li>
                <li>对象存储（S3, Azure Blob）</li>
                <li>文件存储（EFS, Azure Files）</li>
            </ul>

            <h3>4. 大数据分析</h3>
            <ul>
                <li>数据仓库（Redshift, Snowflake）</li>
                <li>流处理（Kinesis, Spark Streaming）</li>
                <li>机器学习平台（SageMaker, MLflow）</li>
            </ul>
        '''
    },
    {
        'mcp_type': 'filesystem',
        'label': 'Filesystem MCP - 优势与挑战',
        'content': '''
            <h2>云计算的优势与挑战</h2>

            <h3>优势</h3>
            <ul>
                <li><strong>成本节约</strong>：无需购买硬件，按需付费</li>
                <li><strong>弹性扩展</strong>：根据负载自动调整资源</li>
                <li><strong>高可用性</strong>：多地域部署，自动故障转移</li>
                <li><strong>快速部署</strong>：分钟内启动服务</li>
                <li><strong>自动更新</strong>：软件自动升级维护</li>
            </ul>

            <h3>挑战</h3>
            <ul>
                <li><strong>数据安全</strong>：数据存储在第三方</li>
                <li><strong>合规性</strong>：满足行业监管要求</li>
                <li><strong> vendor lock-in</strong>：迁移成本高</li>
                <li><strong>网络依赖</strong>：需要稳定的网络连接</li>
                <li><strong>成本控制</strong>：使用不当可能导致费用超支</li>
            </ul>

            <div style="background: #e8f5e9; padding: 20px; border-radius: 8px; margin-top: 30px;">
                <h3 style="color: #388e3c; margin-top: 0;">最佳实践</h3>
                <ul>
                    <li>实施云成本管理策略</li>
                    <li>使用多云策略避免vendor lock-in</li>
                    <li>加强身份和访问管理</li>
                    <li>定期审计云资源使用</li>
                    <li>建立云治理框架</li>
                </ul>
            </div>
        '''
    },
    {
        'mcp_type': 'sqlite',
        'label': 'SQLite MCP - 文档元数据',
        'content': '''
            <h2>本文档说明</h2>

            <table style="width:100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="background: #7b1fa2; color: white;">
                    <th style="padding: 12px; text-align: left;">属性</th>
                    <th style="padding: 12px; text-align: left;">值</th>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">文档标题</td>
                    <td style="padding: 10px;">云计算技术深度解析</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">使用的Skill</td>
                    <td style="padding: 10px;">html-document-generator v1.0.0</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">MCP服务器</td>
                    <td style="padding: 10px;">
                        🔵 Wikipedia MCP<br>
                        🟢 Filesystem MCP<br>
                        🟣 SQLite MCP
                    </td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px;">章节数量</td>
                    <td style="padding: 10px;">4个</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">生成时间</td>
                    <td style="padding: 10px;">2026-02-01</td>
                </tr>
            </table>

            <h3 style="margin-top: 30px;">Skill复用说明</h3>
            <p>本文档展示了如何复用 <code>html-document-generator</code> Skill：</p>
            <ol>
                <li><strong>导入Skill</strong>: <code>from html_document_generator import FilesystemMCP, SQLiteMCP, WikipediaMCP</code></li>
                <li><strong>初始化MCP</strong>: 创建MCP服务器实例</li>
                <li><strong>准备内容</strong>: 定义sections数组</li>
                <li><strong>生成文档</strong>: 调用<code>generate_html()</code>方法</li>
                <li><strong>保存数据</strong>: 存储到SQLite数据库</li>
            </ol>
        '''
    }
]

print(f"[OK] 已准备 {len(sections)} 个章节")

# ==================== 生成HTML ====================
print("\n[步骤5] 生成HTML文档...")

fs_mcp = FilesystemMCP()
output_path = os.path.join('output', '云计算技术解析.html')
os.makedirs('output', exist_ok=True)

html_content = fs_mcp.generate_html(
    title='云计算技术深度解析',
    sections=sections,
    output_path=output_path
)

print(f"[OK] HTML文档已生成: {output_path}")
print(f"    文件大小: {len(html_content)} 字符")

# ==================== 保存到数据库 ====================
print("\n[步骤6] 保存到数据库...")

article_id = sqlite_mcp.insert_article('云计算技术深度解析', html_content)
print(f"[OK] 文章已保存，ID: {article_id}")

# 添加引用
refs = [
    ('Cloud computing', 'https://en.wikipedia.org/wiki/Cloud_computing'),
    ('Infrastructure as a service', 'https://en.wikipedia.org/wiki/Infrastructure_as_a_service'),
    ('Platform as a service', 'https://en.wikipedia.org/wiki/Platform_as_a_service'),
    ('Software as a service', 'https://en.wikipedia.org/wiki/Software_as_a_service')
]

for title, url in refs:
    sqlite_mcp.insert_ref(article_id, title, url)

print(f"[OK] 已添加 {len(refs)} 条Wikipedia引用")

# ==================== 关闭并打开 ====================
print("\n[步骤7] 清理资源...")
sqlite_mcp.close()

print("\n[步骤8] 打开生成的文档...")
os.startfile(output_path)

# ==================== 总结 ====================
print("\n" + "="*60)
print("✅ Skill复用测试成功！")
print("="*60)
print(f"\n📊 统计信息:")
print(f"  - Skill名称: html-document-generator")
print(f"  - 导入方式: from html_document_generator import ...")
print(f"  - 生成文档: {output_path}")
print(f"  - 数据库: skill_test.db")
print(f"  - 文章ID: {article_id}")
print(f"  - 文件大小: {len(html_content)} 字符")

print(f"\n🎯 关键代码:")
print(f"  from html_document_generator import FilesystemMCP, SQLiteMCP")
print(f"  fs = FilesystemMCP()")
print(f"  fs.generate_html(title, sections, output_path)")

print("\n" + "="*60)
print("这就是Skill的正确复用方式！")
print("="*60)
