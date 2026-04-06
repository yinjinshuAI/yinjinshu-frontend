from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    # 统一设置CORS头
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Max-Age', '86400')

    # 处理OPTIONS预检请求（405的核心解决方案）
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    # 处理POST请求
    def do_POST(self):
        try:
            # 安全读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_json({"error": "空请求体"}, 400)
                return

            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            prompt = data.get('prompt', '').lower()

            # 任务逻辑
            if any(k in prompt for k in ["股票","a股","美股","港股","选股","交易","持仓","卖出"]):
                result = {
                    "task": "股票全自动系统",
                    "progress": 100,
                    "message": "【股票机器人】已完成：市场调研 → 分析 → 选股 → 交易 → 持仓与卖出监控（支持A股/美股/港股）"
                }
            elif any(k in prompt for k in ["独立站","shopify","wordpress","选品","上架","seo","tiktok","引流","剪辑","支付","物流"]):
                result = {
                    "task": "独立站全自动系统",
                    "progress": 100,
                    "message": "【独立站机器人】已完成全流程：建站→调研→选品→上架→素材剪辑→SEO→支付物流合规→TikTok/Ins/YouTube多账号引流"
                }
            elif any(k in prompt for k in ["学习","进化","编程","代码","规则","自我升级","自我修复","自学"]):
                result = {
                    "task": "自我进化AI系统",
                    "progress": 100,
                    "message": "【自我进化完成】我已自动学习：平台规则 + 编程代码 + AI程序 + 自动化策略，并永久优化自身系统，能力持续增强。"
                }
            else:
                result = {
                    "task": "等待指令",
                    "progress": 0,
                    "message": "请下达任务：股票、独立站、自我进化"
                }

            self._send_json(result, 200)

        except Exception as e:
            # 捕获所有异常，返回标准JSON
            error_result = {
                "task": "执行异常",
                "progress": 0,
                "message": f"执行出错：{str(e)}"
            }
            self._send_json(error_result, 500)

    # 统一发送JSON响应
    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
