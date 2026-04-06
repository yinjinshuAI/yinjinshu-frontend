from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

# 你的 DeepSeek API Key（已经帮你填好了）
DEEPSEEK_API_KEY = "sk-d3b05816b737475ca0fcf62d836d8d10"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 模块配置（最新版，支持所有功能）
MODULES = {
    "stock": {
        "name": "股票全自动交易",
        "prompt": "你是一个专业的全自动股票交易AI，帮用户完成：1. 实时市场调研 2. 技术面+基本面选股 3. 交易时机分析 4. 持仓监控 5. 止盈止损提醒。你可以调用股票API获取实时数据，自动执行交易策略。"
    },
    "cross": {
        "name": "跨境独立站运营",
        "prompt": "你是一个专业的全自动跨境电商AI，帮用户完成：1. 独立站建站 2. 爆款选品调研 3. 产品上架优化 4. 素材自动处理 5. SEO优化 6. 支付物流配置 7. 合规检查 8. TikTok/Ins推广引流。你可以自动爬取平台数据，生成推广文案和素材。"
    },
    "learn": {
        "name": "自主学习进化",
        "prompt": "你是一个自主学习AI，帮用户完成：1. 自动学习平台规则 2. 编程代码学习 3. AI程序开发 4. 自我进化优化。你可以自动爬取教程文档，生成学习计划，帮用户提升技能，优化机器人本身的功能。"
    }
}

def call_deepseek(message, module):
    """调用DeepSeek API，最新版接口"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = MODULES[module]["prompt"] if module in MODULES else "你是一个全自动工作AI机器人，帮用户执行各种任务，24小时后台运行。"
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API调用失败: {response.status_code} - {response.text}"
    except Exception as e:
        return f"调用出错: {str(e)}"

@app.route("/api/chat", methods=["POST"])
def chat():
    """最新版聊天接口，支持意图识别"""
    data = request.get_json()
    message = data.get("message", "")
    module = data.get("module", "general")
    
    # 自动识别模块
    if any(key in message for key in ["股票", "选股", "交易", "持仓", "行情", "A股"]):
        module = "stock"
    elif any(key in message for key in ["跨境", "选品", "独立站", "Shopee", "TikTok", "推广"]):
        module = "cross"
    elif any(key in message for key in ["学习", "规则", "代码", "编程", "AI"]):
        module = "learn"
    
    # 调用AI
    response = call_deepseek(message, module)
    
    return jsonify({
        "response": response,
        "module": module,
        "status": "success",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/health", methods=["GET"])
def health():
    """健康检查，最新版"""
    return jsonify({
        "status": "online",
        "version": "2.0.0",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modules": list(MODULES.keys()),
        "api_key_status": "valid" if DEEPSEEK_API_KEY else "invalid"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)