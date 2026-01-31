# AI趋势分析工具 - 技术文档

## 📋 工具概述

本工具用于生成"2026年AI五大热点"分析报告,使用GLM-4.6 API生成内容,并提供真实的技术来源链接。

## 🎯 核心功能

### 1. 多模型分析
- 支持4个AI模型: GLM-4.6, Claude, ChatGPT, Gemini
- 每个模型独立分析2026年AI热点
- 提示词要求每个模型收集100+热点,筛选出最重要的5个

### 2. 真实技术来源
- 预定义67个真实可点击的技术链接
- 覆盖13个国际技术社区/网站
- 按类别分组显示(GitHub, arXiv, TechCrunch等)

### 3. GLM-4.6 API集成
- 使用`glm-4-flash`模型
- API密钥从`../.env`文件读取
- 环境变量: `ZHIPU_API_KEY`

## 🔧 重要技术实现

### ⚠️ 关键功能1: URL自动转超链接

**位置**: `ai_trends_final.py` 第18-30行

```python
def convert_urls_to_links(text):
    """将文本中的URL转换为可点击的超链接"""
    # 匹配http/https URL
    url_pattern = r'https?://[^\s\)]+'

    def replace_url(match):
        url = match.group(0)
        # 清理URL末尾的标点符号
        clean_url = url.rstrip('.,;!?)')
        return f'<a href="{clean_url}" target="_blank" style="color: #1976d2; text-decoration: underline; font-weight: 500;">{clean_url}</a>'

    return re.sub(url_pattern, replace_url, text)
```

**⚠️ 注意事项:**
- **必须保留**: 此函数在生成HTML报告时被调用,将模型生成内容中的URL转换为可点击的超链接
- **调用位置**: `generate_html_report()` 函数中,对每个模型的content应用
- **删除后果**: 模型生成内容中的URL将显示为纯文本,无法点击

**示例效果:**
```
输入: "来源链接:https://news.ycombinator.com/item?id=31234"
输出: "来源链接:<a href="https://news.ycombinator.com/item?id=31234" target="_blank" style="...">https://news.ycombinator.com/item?id=31234</a>"
```

### ⚠️ 关键功能2: 数据来源可折叠

**位置**: `ai_trends_final.py` 第33-58行

**HTML结构:**
```html
<h3 class="sources-title" onclick="toggleSources(this)" style="cursor: pointer;">
    [数据来源] XX搜索来源 <span class="toggle-icon">▶</span>
</h3>
<div class="sources-list" style="display: none;">
    <!-- 来源链接列表 -->
</div>
```

**JavaScript实现:**
```javascript
function toggleSources(element) {
    const sourcesList = element.nextElementSibling;
    const icon = element.querySelector('.toggle-icon');

    if (sourcesList.style.display === 'none') {
        sourcesList.style.display = 'grid';
        icon.classList.add('expanded');
    } else {
        sourcesList.style.display = 'none';
        icon.classList.remove('expanded');
    }
}
```

**CSS样式:**
```css
.toggle-icon {
    transition: transform 0.3s ease;
    font-size: 0.8em;
}
.toggle-icon.expanded {
    transform: rotate(90deg);
}
.sources-list {
    display: grid;  /* 展开时 */
    /* display: none; 折叠时 */
}
```

**⚠️ 注意事项:**
- **默认状态**: `display: none` (折叠)
- **必须包含**: `<span class="toggle-icon">▶</span>`
- **onclick事件**: `onclick="toggleSources(this)"`
- **光标样式**: `cursor: pointer;` 提示可点击
- **删除后果**: 数据来源将始终展开显示,失去折叠功能

## 📁 文件说明

### 主要文件

| 文件名 | 说明 | 推荐使用 |
|--------|------|----------|
| `ai_trends_final.py` | **最终改进版** (URL转超链接 + 可折叠来源) | ✅ **推荐** |
| `ai_trends_with_manual_sources.py` | 手动来源版 (无URL转换,不可折叠) | ⚠️ 旧版本 |
| `ai_trends_ultimate.py` | 最初版本 (DuckDuckGo搜索失败) | ❌ 已废弃 |

### 生成的报告

| 文件名 | 说明 |
|--------|------|
| `2026年AI五大热点_最终改进版.html` | 包含所有新功能的完整报告 |
| `2026年AI五大热点_真实来源版.html` | 旧版本报告 |

## 🔑 配置说明

### API密钥配置

**位置**: `C:/D/CAIE_tool/MyAIProduct/post/.env`

```bash
ZHIPU_API_KEY=your-zhipuai-api-key-here
```

**格式**: `id.secret` (两部分组成,中间用点分隔)

### API调用限制

- **模型**: `glm-4-flash`
- **温度参数**: `0.7`
- **超时时间**: 默认(无特殊设置)
- **搜索工具**: `web_search` (但不返回来源信息)

## 🚀 运行方式

### 方法1: 直接运行Python脚本

```bash
cd C:/D/CAIE_tool/MyAIProduct/post/hotspot
python ai_trends_final.py
```

### 方法2: 修改代码后运行

1. 编辑`ai_trends_final.py`
2. 保存文件
3. 运行上述命令

**⚠️ 重要**: 修改代码后必须确保以下功能正常:
- ✅ `convert_urls_to_links()` 函数存在
- ✅ `toggleSources()` JavaScript函数存在
- ✅ 默认折叠状态 `display: none`
- ✅ 箭头图标 `<span class="toggle-icon">`

## 📊 数据来源列表

工具预定义了67个真实技术链接,分为13个类别:

1. **GitHub AI Projects** (8个)
2. **arXiv AI Papers** (8个)
3. **TechCrunch AI** (5个)
4. **MIT Technology Review** (5个)
5. **The Verge AI** (5个)
6. **Wired AI** (5个)
7. **Hacker News** (4个)
8. **OpenAI Blog** (5个)
9. **Google AI Blog** (5个)
10. **Meta AI Research** (5个)
11. **Microsoft Research** (4个)
12. **Anthropic Claude** (4个)
13. **NVIDIA AI** (4个)

**位置**: `get_real_ai_sources()` 函数 (第40-135行)

## ⚙️ 代码修改注意事项

### ✅ 可以修改的部分

1. **技术来源列表**: 在`get_real_ai_sources()`中添加/删除链接
2. **样式调整**: 修改CSS颜色、字体、间距等
3. **提示词优化**: 修改`generate_search_prompt()`中的内容
4. **模型数量**: 在`main()`函数中的`models`列表增删模型

### ❌ 不要修改的部分

1. **`convert_urls_to_links()`函数**: 核心URL转换逻辑
2. **`toggleSources()`JavaScript函数**: 折叠交互逻辑
3. **默认折叠状态**: `display: none` 必须保留
4. **箭头图标HTML**: `<span class="toggle-icon">▶</span>` 必须保留

### 🔧 修改后的测试清单

修改代码后,必须验证以下功能:

- [ ] 报告能成功生成
- [ ] 模型内容中的URL显示为蓝色下划线链接
- [ ] 点击URL能在新标签页打开
- [ ] 数据来源默认折叠
- [ ] 点击标题能展开/折叠
- [ ] 箭头图标有旋转动画
- [ ] 所有来源链接可点击

## 🐛 常见问题

### Q1: 报告生成了但URL不能点击?

**原因**: 可能删除了`convert_urls_to_links()`函数或忘记调用

**解决**: 确保在`generate_html_report()`中有此代码:
```python
content_with_links = convert_urls_to_links(content)
```

### Q2: 数据来源默认展开?

**原因**: 删除了`style="display: none;"`

**解决**: 在`format_sources_html()`中确保有:
```python
<div class="sources-list" style="display: none;">
```

### Q3: 点击标题无法折叠?

**原因**: 缺少`onclick`事件或JavaScript函数

**解决**: 确保HTML中有:
```html
<h3 class="sources-title" onclick="toggleSources(this)" style="cursor: pointer;">
```

### Q4: 箭头图标不旋转?

**原因**: 缺少CSS动画或`expanded`类

**解决**: 确保CSS中有:
```css
.toggle-icon.expanded {
    transform: rotate(90deg);
}
```

## 📝 版本历史

### v1.0 - 初始版本
- 文件: `ai_trends_ultimate.py`
- 功能: 基础API调用 + DuckDuckGo搜索
- 问题: DuckDuckGo返回0结果

### v2.0 - 手动来源版
- 文件: `ai_trends_with_manual_sources.py`
- 功能: 预定义67个真实链接
- 问题: URL不自动转超链接,来源不可折叠

### v3.0 - 最终改进版 ✅
- 文件: `ai_trends_final.py`
- 新增: URL自动转超链接
- 新增: 数据来源可折叠
- 状态: **推荐使用**

## 📞 技术支持

如有问题,检查:
1. API密钥是否正确配置
2. 网络连接是否正常
3. Python依赖是否安装 (`zhipuai`, `requests`)
4. 代码是否被意外修改

---

**最后更新**: 2026-01-31
**维护者**: Claude Code AI Assistant
**版本**: v3.0 (最终改进版)
