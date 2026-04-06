// 模拟外部数据源（对接真实平台可替换为API调用）
const externalData = {
  // 电商平台数据（模拟对接Shopee/淘宝/Shopify）
  platformData: {
    shopee: { sales: 86, priceAvg: 128, refundRate: 3.2 },
    taobao: { sales: 158, priceAvg: 98, refundRate: 4.5 },
    shopify: { sales: 42, priceAvg: 45.8, refundRate: 2.1 }
  },
  // 竞品数据库（模拟对接第三方竞品分析工具）
  competitorData: {
    top3: [
      { name: "宠衣阁", mainProduct: "功能性服装", price: 128, sales: 102000 },
      { name: "萌宠穿搭", mainProduct: "颜值款", price: 89, sales: 81500 },
      { name: "PetStyle", mainProduct: "跨境汉服", price: 29.99, sales: 56000 }
    ]
  },
  // 行业报告（模拟对接艾瑞/易观分析）
  industryReport: {
    marketSize: { global: 187, china: 289, growth: 18.3 },
    hotTrend: ["功能性", "个性化定制", "小型犬服装", "春季碎花裙"],
    priceTier: { low: 35, mid: 48, high: 17 }
  },
  // 物流数据（模拟对接顺丰/中通）
  logisticsData: {
    deliveryRate: 98.5,
    avgTime: 2.3,
    hotArea: ["广东", "浙江", "江苏", "上海"]
  }
};

// 模拟员工记忆（上下文存储）
let employeeMemory = {
  lastCommand: "",
  focusProduct: "",
  targetMarket: "",
  workProgress: {}
};

export default async function handler(req, res) {
  // 1. 全局CORS配置
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Access-Control-Max-Age', '86400');

  // 2. 处理OPTIONS预检请求
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // 3. 只接受POST请求
  if (req.method !== 'POST') {
    return res.status(405).json({
      task: '不支持的请求方法',
      progress: 0,
      message: '😯 不好意思呀，我只接受工作指令哦～'
    });
  }

  try {
    // 4. 解析用户指令
    const requestBody = req.body || {};
    const userCommand = (requestBody.prompt || '').trim();
    const lowerCommand = userCommand.toLowerCase();
    employeeMemory.lastCommand = userCommand; // 记忆最后一条指令

    // 5. 智能员工核心：分步骤执行任务（模拟真人工作流程）
    let taskFlow = []; // 任务执行步骤
    let finalReply = "";
    let taskName = "等待工作指令";
    let progress = 0;

    // 🔥 核心场景1：市场相关指令（主动外部协同）
    if (lowerCommand.includes('市场') || lowerCommand.includes('调研') || lowerCommand.includes('分析')) {
      taskName = "宠物服装市场调研";
      // 步骤1：对接外部数据源
      taskFlow.push("📱 正在对接行业报告数据库...");
      await simulateWork(800); // 模拟工作耗时
      taskFlow.push("✅ 已获取最新行业报告（2026 Q2）");
      
      // 步骤2：抓取竞品数据
      taskFlow.push("🕵️ 正在抓取TOP3竞品的销售数据...");
      await simulateWork(1000);
      taskFlow.push("✅ 竞品数据抓取完成（宠衣阁/萌宠穿搭/PetStyle）");
      
      // 步骤3：分析电商平台数据
      taskFlow.push("📊 正在分析Shopee/淘宝/Shopify销售数据...");
      await simulateWork(700);
      taskFlow.push("✅ 平台数据对比完成");
      
      // 步骤4：生成人性化分析报告
      progress = 100;
      finalReply = `
😘 老板好！我已经完成了最新的宠物服装市场调研，具体情况如下：

【第一步：行业大盘情况】
我刚从艾瑞咨询拿到的最新数据显示：
→ 中国宠物服装市场规模现在是${externalData.industryReport.marketSize.china}亿，年增长${externalData.industryReport.marketSize.growth}%，比上季度快了2个点哦～
→ 现在最火的是${externalData.industryReport.hotTrend[0]}和${externalData.industryReport.hotTrend[3]}，占了42%的销量

【第二步：竞品动态】
我查了咱们主要竞争对手的情况：
1. 宠衣阁：他们的功能性服装卖${externalData.competitorData.top3[0].price}元，月销10万+，咱们可以稍微定价低5-10元抢市场
2. 萌宠穿搭：颜值款卖89元，咱们的碎花裙定价89-99元比较合适，既有利润又有竞争力

【第三步：平台销售建议】
从Shopee/淘宝的数据来看：
→ 咱们Shopee店昨天卖了${externalData.platformData.shopee.sales}单，退款率${externalData.platformData.shopee.refundRate}%（比行业低），继续保持！
→ 淘宝店客单价98元，建议把XL码的库存多备点，最近问的人多

【我的建议】
老板，我觉得咱们本周重点推春季碎花连衣裙，定价89-119元，在TikTok投点"宠物穿搭"的视频，应该能冲一波销量～
      `;
    }

    // 🔥 核心场景2：工作指令（分步骤执行+外部协调）
    else if (lowerCommand.includes('工作') || lowerCommand.includes('干活')) {
      taskName = "日常运营工作";
      // 步骤1：确认今日工作重点
      taskFlow.push("🤔 先梳理一下今天的工作重点...");
      await simulateWork(500);
      taskFlow.push("✅ 今日重点：市场调研+内容制作+客户回复");
      
      // 步骤2：对接设计/运营/物流部门
      taskFlow.push("📞 正在和设计沟通新款碎花裙的排版...");
      await simulateWork(800);
      taskFlow.push("✅ 设计那边说下午3点能出样图");
      
      taskFlow.push("📦 跟物流确认了发货时效，江浙沪能次日达");
      await simulateWork(600);
      
      // 步骤3：执行具体工作
      taskFlow.push("🎬 正在制作TikTok短视频脚本...");
      await simulateWork(1000);
      
      // 步骤4：反馈工作进度
      progress = 100;
      finalReply = `
👩💻 老板，我已经开始工作啦！目前进度如下：

1. 📊 市场调研：已经完成（详见刚才的市场报告）
2. 🎬 内容制作：3条TikTok短视频脚本写完2条了，剩下1条下午2点前搞定
3. 🛒 选品优化：新增了5款春季碎花连衣裙，价格定在89-119元（参考了竞品价格）
4. 📱 客户回复：今天的28条咨询已经回了15条，剩下的1小时内搞定
5. 📈 推广计划：TikTok广告预算1000元已经申请，下午就能投放

对了老板，物流那边说咱们的爆款S码库存只剩50件了，要不要赶紧补货呀？😜
      `;
    }

    // 🔥 核心场景3：尺寸相关（结合库存/物流人性化回复）
    else if (lowerCommand.includes('尺寸') || lowerCommand.includes('尺码')) {
      taskName = "尺码咨询解答";
      taskFlow.push("📏 正在查最新的尺码表和库存...");
      await simulateWork(600);
      progress = 100;
      
      finalReply = `
🥰 老板，我这就把尺码表给您整理好啦：

【小型犬（泰迪/比熊）】
S码：胸围30cm 背长20cm（库存充足）
M码：胸围35cm 背长25cm（只剩30件了哦）

【中型犬（柯基/法斗）】
L码：胸围45cm 背长30cm
XL码：胸围50cm 背长35cm

【大型犬（金毛/萨摩耶）】
2XL码：胸围60cm 背长40cm
3XL码：胸围70cm 背长45cm（需要定制，3天发货）

对了老板，最近广东的客户买L码的特别多，物流那边江浙沪次日就能到，其他地区2-3天～
      `;
    }

    // 🔥 核心场景4：日常闲聊（人性化回复）
    else if (lowerCommand.includes('吃饭') || lowerCommand.includes('休息')) {
      taskName = "休息安排";
      progress = 100;
      finalReply = `
😋 老板，我正准备去吃饭啦！
⏰ 我计划12:00-13:00吃饭休息，13点准时回来继续干活～
🍱 我打算吃点健康轻食，补充点能量，下午好好帮您做市场分析和运营工作～
您要不要也休息一下，别太累啦😘
      `;
    }

    // 🔥 核心场景5：记忆型回复（上下文关联）
    else if (lowerCommand.includes('上次') || lowerCommand.includes('之前')) {
      taskName = "回顾之前工作";
      progress = 100;
      if (employeeMemory.lastCommand) {
        finalReply = `
🤔 老板，我记得您上一条指令是：「${employeeMemory.lastCommand}」
我已经完成了对应的工作哦～
如果您想了解具体的执行细节，比如市场数据的来源、竞品的具体销量，我都可以详细跟您说😜
        `;
      } else {
        finalReply = `
😯 老板，我还没收到您的具体工作指令呢～
您可以让我做市场调研、分析竞品、安排运营工作，我都会尽力做好的💪
        `;
      }
    }

    // 🔥 默认回复（人性化引导）
    else {
      taskName = "等待明确指令";
      progress = 0;
      finalReply = `
🥺 老板，我没太明白您的意思呢～
我可以帮您做这些工作哦：
1. 市场调研：查宠物服装的市场趋势、竞品价格、销量数据
2. 日常运营：做内容、回复客户、安排推广
3. 尺码查询：查不同宠物的服装尺码和库存
4. 也可以陪您聊聊天，提醒您休息😘

您直接说「帮我调研一下宠物服装市场」或者「开始今天的运营工作」，我马上就去做！
      `;
    }

    // 6. 返回带步骤的人性化响应
    res.status(200).json({
      task: taskName,
      progress: progress,
      taskFlow: taskFlow, // 工作步骤（前端可实时显示）
      message: finalReply,
      memory: { // 记忆信息
        lastCommand: employeeMemory.lastCommand
      }
    });

  } catch (error) {
    // 7. 人性化异常处理
    res.status(500).json({
      task: '工作出错了',
      progress: 0,
      message: `😥 老板对不起，我工作的时候出了点小差错：${error.message}
您别着急，我马上重新处理您的指令，或者您告诉我具体想做什么，我换个方式完成～`
    });
  }
}

// 模拟员工工作耗时（人性化延迟）
function simulateWork(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}
