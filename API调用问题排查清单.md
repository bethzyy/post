# API调用问题排查清单

## 遇到429错误时的排查步骤

### 第一步：确认是哪个API返回的429

**情况A：WebSearch工具返回429**
```
错误信息：The API concurrent usage limit has been exceeded
错误来源：Pollinations.ai后端
解决方案：
1. 降低并发请求数量
2. 等待一段时间后重试
3. 分批执行搜索查询
```

**情况B：ZhipuAI API返回429**
```
错误信息：资源不足，请充值 (Error 1113)
错误代码：429
排查步骤：
1. ✅ 确认使用的是Anthropic兼容API接口
2. ✅ 检查配置文件中的端点是否正确
3. ✅ 验证API Key格式是否正确（id.secret）
```

### 第二步：ZhipuAI 429错误的正确处理

**✅ 正确配置（已验证可用）**：

```python
# .env文件配置
ZHIPU_API_KEY=your-zhipuai-api-key-here
ZHIPU_ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic

# config.py中的函数
def get_zhipu_anthropic_client():
    from anthropic import Anthropic
    return Anthropic(
        base_url=Config.ZHIPU_ANTHROPIC_BASE_URL,
        api_key=Config.ZHIPU_API_KEY
    )

# 使用方法
client = get_zhipu_anthropic_client()
response = client.messages.create(
    model="glm-4.6",
    max_tokens=4000,
    messages=[...]
)
```

**❌ 错误配置（会导致429）**：

```python
# 错误1：使用ZhipuAI原生SDK
from zhipuai import ZhipuAI
client = ZhipuAI(api_key=Config.ZHIPU_API_KEY)
# 可能返回：资源不足，请充值 (Error 1113)

# 错误2：使用错误的端点
from openai import OpenAI
client = OpenAI(
    base_url="https://open.bigmodel.cn/api/paas/v4/",  # ❌ 错误端点
    api_key=Config.ZHIPU_API_KEY
)
# 可能返回：429

# 错误3：通过anti-gravity代理
client = get_antigravity_client()
# anti-gravity服务配额已用尽，返回429
```

### 第三步：验证ZhipuAI配置是否正确

**测试脚本**：`test_zhipu_anthropic.py`

```python
from config import get_zhipu_anthropic_client

client = get_zhipu_anthropic_client()
response = client.messages.create(
    model="glm-4.6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "请用一句话介绍2026年AI趋势"}
    ]
)

# 如果成功，会返回正常响应
# 如果失败，检查上述配置
```

**预期成功结果**：
```
[成功] API调用成功!
响应内容: **2026年AI领域最重要的趋势是：从"云端大模型"向"端侧智能"和"具身智能"的全栈式突破...**
使用Token数: 73
```

## 关键要点

### 1. 区分不同API的429错误

| API类型 | 端点 | 库 | 429原因 | 解决方案 |
|---------|------|-----|---------|----------|
| **WebSearch工具** | Pollinations.ai后端 | 内置工具 | 并发限制 | 降低并发，分批执行 |
| **ZhipuAI Anthropic兼容** | https://open.bigmodel.cn/api/anthropic | anthropic | 余额/配置问题 | 检查端点和API Key |
| **ZhipuAI 原生SDK** | https://open.bigmodel.cn/api/paas/v4/ | zhipuai | 余额问题 | 充值或使用Anthropic兼容 |
| **Anti-gravity代理** | http://127.0.0.1:8045/v1 | openai | 配额用尽 | 无法使用 |

### 2. ZhipuAI调用原则

**✅ 正确做法**：
1. 使用Anthropic兼容API接口
2. 使用`anthropic`库而非`zhipuai`库
3. 端点：`https://open.bigmodel.cn/api/anthropic`
4. 模型名：`glm-4.6`

**❌ 错误做法**：
1. 使用ZhipuAI原生SDK (`zhipuai`库)
2. 使用错误的端点
3. 通过anti-gravity代理调用ZhipuAI
4. 使用不存在的模型名

### 3. 每次遇到429时的自查清单

```
□ 1. 确认是哪个API返回的429
   ├─ WebSearch工具？→ 降低并发，分批执行
   └─ ZhipuAI API？→ 继续下一步检查

□ 2. 检查ZhipuAI配置（如果使用的是ZhipuAI）
   ├─ 是否使用Anthropic兼容接口？
   ├─ 端点是否为 https://open.bigmodel.cn/api/anthropic？
   ├─ 是否使用 anthropic 库？
   └─ API Key格式是否正确（id.secret）？

□ 3. 运行测试脚本验证
   └─ python test_zhipu_anthropic.py

□ 4. 如果测试通过但主程序失败
   └─ 检查主程序中的API调用代码是否使用了正确的配置
```

## 实际案例记录

### 案例1：2026年1月28日 - WebSearch工具429错误

**错误**：
```
Error 429: The API concurrent usage limit has been exceeded
```

**原因**：
- WebSearch工具（Pollinations.ai后端）并发限制
- 短时间内执行了多次搜索

**解决**：
- 分批执行搜索，降低并发数
- 每批之间添加延迟

### 案例2：ZhipuAI配置成功

**测试**：
```bash
python test_zhipu_anthropic.py
```

**结果**：
```
✅ 成功
响应内容: 2026年AI领域最重要的趋势是...
使用Token数: 73
```

**配置**：
- 端点：`https://open.bigmodel.cn/api/anthropic`
- 库：`anthropic`
- 模型：`glm-4.6`

## 文档更新记录

**2026-01-28**:
- 创建此文档
- 记录WebSearch工具的429错误
- 验证ZhipuAI Anthropic兼容API配置正确
- 添加自查清单

---

**重要提醒**：
每次遇到429错误时，首先确认是哪个API返回的错误，然后根据上述清单进行排查。对于ZhipuAI，一定要确保使用Anthropic兼容接口。
