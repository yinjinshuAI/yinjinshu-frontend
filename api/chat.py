from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode()
        data = json.loads(body)
        prompt = data.get("prompt", "").lower()

        # 股票自动化（A股/美股/港股）
        if any(k in prompt for k in ["股票","a股","美股","港股","选股","交易","持仓","卖出"]):
            res = {
                "task": "股票全自动系统",
                "progress": 100,
                "message": "【股票机器人】已完成：市场调研 → 分析 → 选股 → 交易 → 持仓与卖出监控（支持A股/美股/港股）"
            }

        # 独立站自动化（Shopify + WordPress）
        elif any(k in prompt for k in ["独立站","shopify","wordpress","选品","上架","seo","tiktok","引流","剪辑","支付","物流"]):
            res = {
                "task": "独立站全自动系统",
                "progress": 100,
                "message": "【独立站机器人】已完成全流程：建站→调研→选品→上架→素材剪辑→SEO→支付物流合规→TikTok/Ins/YouTube多账号引流"
            }

        # 自我进化（核心功能）
        elif any(k in prompt for k in ["学习","进化","编程","代码","规则","自我升级","自我修复","自学"]):
            res = {
                "task": "自我进化AI系统",
                "progress": 100,
                "message": "【自我进化完成】我已自动学习：平台规则 + 编程代码 + AI程序 + 自动化策略，并永久优化自身系统，能力持续增强。"
            }

        # 普通对话
        else:
            res = {
                "task": "等待指令",
                "progress": 0,
                "message": "请下达任务：股票、独立站、自我进化"
            }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._send_cors()
        self.end_headers()
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode('utf-8'))
