import json
import os
import requests

def handler(request):
    # 1. 配置完整跨域头，覆盖所有浏览器校验要求
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "86400"
    }

    # 2. 优先处理OPTIONS预检请求（浏览器跨域请求前必发）
    if request.method == "OPTIONS":
        return ("", 204, headers)

    # 3. 仅允许POST请求，拦截非法方法
    if request.method != "POST":
        return (json.dumps({"error": "Method Not Allowed"}), 405, headers)

    try:
        # 4. 从环境变量读取DeepSeek密钥，增加空值校验
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if not deepseek_key:
            return (json.dumps({"error": "未配置DeepSeek API密钥，请在Vercel环境变量中添加DEEPSEEK_API_KEY"}), 401, headers)

        # 5. 解析前端请求体，兼容空消息兜底
        body = request.json or {}
        user_message = body.get("message", "你好")

        # 6. 调用DeepSeek API，增加超时与异常捕获
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

        # 7. 正常返回AI响应给前端
        return (json.dumps(api_response.json()), 200, headers)

    except Exception as e:
        # 8. 捕获所有异常，返回友好提示
        return (json.dumps({"error": f"服务器异常: {str(e)}"}), 500, headers)
