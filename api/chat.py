import json
import os
import requests

def handler(request):
    # 配置跨域头，彻底解决前端请求问题
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # 处理OPTIONS预检请求
    if request.method == "OPTIONS":
        return ("", 204, headers)

    try:
        # 从环境变量读取密钥
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if not deepseek_key:
            return (json.dumps({"error": "未配置DeepSeek密钥"}), 401, headers)

        # 解析前端发来的消息
        body = request.json
        user_message = body.get("message", "你好")

        # 调用DeepSeek API
        api_response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {deepseek_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是银金舒高端宠物服装品牌的专属AI顾问，精通宠物服饰设计、面料工艺、穿搭搭配、品牌运营、跨境电商，为用户提供专业、高端、贴心的服务，24小时在线。"
                    },
                    {"role": "user", "content": user_message}
                ]
            },
            timeout=20
        )
        api_response.raise_for_status()

        # 返回AI结果给前端
        return (json.dumps(api_response.json()), 200, headers)

    except Exception as e:
        return (json.dumps({"error": str(e)}), 500, headers)
