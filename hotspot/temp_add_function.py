
def create_evaluation_prompt(model_name, web_search_data):
    """创建评估提示词 - 让GLM-4.6模拟其他模型视角评估实时搜索数据"""
    
    # 格式化搜索数据
    search_summary = []
    if web_search_data:
        for item in web_search_data[:20]:  # 只使用前20条结果
            if isinstance(item, dict):
                title = item.get('title', 'N/A')
                source = item.get('source', 'N/A')
                points = item.get('points', item.get('upvotes', 0))
                search_summary.append(f"- [{title}] ({source}) - {points} points")
    
    search_context = "\n".join(search_summary) if search_summary else "未获取到实时搜索数据"
    
    # 根据模型特点定制提示词
    model_instructions = {
        "Claude": "你是Claude Anthropic,注重安全性、深度思考和伦理考量。请从你的视角分析这些AI热点。",
        "Gemini": "你是Google Gemini,注重多模态能力、技术创新和实用价值。请从你的视角分析这些AI热点。",
        "ChatGPT": "你是ChatGPT OpenAI,注重用户体验、应用场景和产业影响。请从你的视角分析这些AI热点。"
    }
    
    instruction = model_instructions.get(model_name, f"你是{model_name},请分析这些AI热点。")
    
    prompt = f"""{instruction}

以下是当前从GitHub Trending、HackerNews和Reddit获取到的实时AI热点数据:

{search_context}

请基于以上实时数据,以{model_name}的视角进行评估:

任务要求:
1. 仔细分析上述实时搜索数据中的热点
2. 结合{model_name}的特点和优势,筛选出五大AI热点
3. 对每个热点进行深度分析,包括技术特点、应用场景、发展前景
4. 保持{model_name}的分析风格和观点倾向
5. 确保分析基于上述真实数据,不要编造

输出格式:
一、[热点名称]
- 技术特点: [特点描述]
- 应用场景: [场景说明]
- 发展前景: [前景分析]
- 数据支撑: [引用上述实时数据中的具体项目/讨论]

(重复5次,列出5个热点)

注意:请以{model_name}的身份和视角进行分析,确保每个热点都能从上述实时搜索数据中找到依据。"""
    
    return prompt
