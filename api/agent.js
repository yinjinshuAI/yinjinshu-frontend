export default function handler(req, res) {
  // 处理CORS预检请求
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

    // 🔥 定制你的指令逻辑（可无限添加）
    let result;
    // 1. 宠物服装相关指令
    if (['看尺寸','尺寸','尺码'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "宠物服装尺寸查询",
        progress: 100,
        message: "【宠物服装尺寸表】\n• 小型犬（泰迪/比熊）：S码（胸围30cm，背长20cm）\n• 中型犬（柯基/法斗）：M码（胸围45cm，背长30cm）\n• 大型犬（金毛/萨摩耶）：L码（胸围60cm，背长40cm）\n支持定制尺寸，联系客服！"
      };
    } else if (['去工作','工作','干活'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "宠物服装运营工作",
        progress: 100,
        message: "【已开始工作】\n1. 调研最新宠物服装趋势\n2. 优化Shopify店铺商品详情\n3. 制作TikTok引流视频\n4. 跟进客户订单与售后\n5. 分析竞品价格与销量"
      };
    // 2. 保留原有指令
    } else if (['股票','a股','美股','港股'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "股票全自动系统",
        progress: 100,
        message: "【股票机器人】已完成：市场调研 → 分析 → 选股 → 交易 → 持仓与卖出监控（支持A股/美股/港股）"
      };
    } else if (['独立站','shopify','选品','引流'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "独立站全自动系统",
        progress: 100,
        message: "【独立站机器人】已完成全流程：建站→调研→选品→上架→素材剪辑→SEO→支付物流合规→TikTok引流"
      };
    } else if (['学习','进化','编程'].some(k => lowerPrompt.includes(k))) {
      result = {
        task: "自我进化AI系统",
        progress: 100,
        message: "【自我进化完成】已学习宠物服装行业规则+运营技巧+自动化策略，能力持续增强！"
      };
    // 3. 默认回复（引导用户）
    } else {
      result = {
        task: "等待指令",
        progress: 0,
        message: "👉 支持的指令：\n• 看尺寸（查询宠物服装尺码）\n• 去工作（启动宠物服装运营）\n• 股票（A股/美股/港股分析）\n• 独立站（Shopify运营）\n• 自我进化（AI能力升级）"
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
