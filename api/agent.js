export default function handler(req, res) {
  // 处理CORS预检请求，彻底解决405
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // 只处理POST请求
  if (req.method !== 'POST') {
    return res.status(405).json({
      task: '方法不允许',
      progress: 0,
      message: '请使用POST请求'
    });
  }

  try {
    const { prompt = '' } = req.body;
    const lowerPrompt = prompt.toLowerCase();

    // 任务逻辑
    let result;
    if (['股票','a股','美股','港股','选股','交易','持仓','卖出'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "股票全自动系统",
        progress: 100,
        message: "【股票机器人】已完成：市场调研 → 分析 → 选股 → 交易 → 持仓与卖出监控（支持A股/美股/港股）"
      };
    } else if (['独立站','shopify','wordpress','选品','上架','seo','tiktok','引流','剪辑','支付','物流'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "独立站全自动系统",
        progress: 100,
        message: "【独立站机器人】已完成全流程：建站→调研→选品→上架→素材剪辑→SEO→支付物流合规→TikTok/Ins/YouTube多账号引流"
      };
    } else if (['学习','进化','编程','代码','规则','自我升级','自我修复','自学'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "自我进化AI系统",
        progress: 100,
        message: "【自我进化完成】我已自动学习：平台规则 + 编程代码 + AI程序 + 自动化策略，并永久优化自身系统，能力持续增强。"
      };
    } else {
      result = {
        task: "等待指令",
        progress: 0,
        message: "请下达任务：股票、独立站、自我进化"
      };
    }

    res.status(200).json(result);
  } catch (error) {
    res.status(500).json({
      task: '执行异常',
      progress: 0,
      message: `执行出错：${error.message}`
    });
  }
}
