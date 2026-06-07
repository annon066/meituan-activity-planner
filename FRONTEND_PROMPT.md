# 前端改造 Prompt

## 你的任务

基于下面提供的现有 HTML 文件，补全所有交互功能，使其成为一个完整可用的 C 端产品页面。输出一个完整的、自包含的 HTML 文件（所有 CSS 和 JS 都内联），可以直接替换 `web/templates/index.html` 使用。

## 后端 API 接口

Flask 后端提供以下接口，前端需要调用：

### GET /api/status
返回 LLM 是否可用：
```json
{"llm_enabled": true/false}
```

### POST /api/chat （当 llm_enabled=true 时使用）
请求：`{"messages": [{"role": "user", "content": "..."}]}`
返回：`{"content": "回复文本", "role": "assistant"}`
- 如果回复中包含 `<!--PLAN_JSON-->{ ... }<!--/PLAN_JSON-->`，表示生成了方案，需要解析并渲染为方案卡片

### POST /api/parse （当 llm_enabled=false 时，fallback）
请求：`{"input": "用户输入文本"}`
返回：
```json
{
  "scene_type": "family/friends",
  "people_count": 3,
  "time_range": ["14:00", "18:00"],
  "duration_hours": 4.0,
  "special_needs": ["减肥", "亲子"],
  "family_info": {"child_age": 5, "spouse_diet": "减肥"},
  "friend_info": null
}
```

### POST /api/plan
请求：`{"intent": { ... 上面 parse 的返回 }}`
返回：
```json
{
  "scene_type": "family",
  "people_count": 3,
  "start_time": "14:00",
  "end_time": "18:00",
  "total_budget": 384,
  "home_location": {"name": "望京西园四区", "address": "朝阳区望京西园四区"},
  "items": [
    {"name": "朝阳公园儿童乐园", "venue_type": "attraction", "start_time": "14:00", "end_time": "16:00", "address": "朝阳区朝阳公园南路1号", "price": 50, "action": "到店"},
    {"name": "鹿港小镇(朝阳大悦城店)", "venue_type": "restaurant", "start_time": "17:00", "end_time": "18:30", "address": "朝阳区朝阳北路101号", "price": 78, "action": "预订"}
  ],
  "notes": "家庭亲子活动，已考虑儿童设施和健康饮食"
}
```

### POST /api/execute
请求：`{"plan": { ... 上面 plan 的返回 }}`
返回：
```json
{
  "success": true,
  "bookings": [
    {"name": "朝阳公园儿童乐园", "success": true, "booking_id": "BK123456"},
    {"name": "鹿港小镇", "success": false, "booking_id": null}
  ],
  "message": "搞定了！下午 14:00 出发..."
}
```

## 需要补全的功能

### 1. 侧边栏 - 对话历史管理
- **新建对话**按钮：点击后清空聊天区域，重置状态，开始新对话
- **对话列表项可点击**：点击切换到该对话（用 localStorage 保存多个对话的 messages 历史）
- **当前对话自动保存**：每次对话后自动保存到 localStorage，侧边栏动态更新
- **对话标题自动生成**：取用户第一条消息前 15 字作为标题
- **删除对话**：长按或右键显示删除选项
- 移动端下侧边栏可以通过汉堡菜单打开/关闭

### 2. 右上角头像 - 设置面板
点击右上角的"团"头像，弹出一个设置抽屉/弹窗，包含：
- **API 配置区域**：
  - LLM Base URL 输入框（默认显示当前值或 placeholder）
  - API Key 输入框（密码类型，可切换显示）
  - 模型名称输入框
  - "保存并测试连接"按钮 → 调用 POST /api/config 保存（如果后端没有这个接口，就保存到 localStorage 并通过 URL 参数传递）
  - 连接状态指示灯（绿色=已连接，灰色=未配置）
- **用户信息**：
  - 昵称设置（保存到 localStorage，用于头像显示和预订时的姓名）
  - 默认手机号（用于预订）
  - 家庭地址/常用出发地
- "关于"信息：版本号、Powered by 美团 Agent

### 3. 聊天功能完善
- 消息中的 XSS 防护：用户输入需要 HTML 转义
- 空状态优化：如果没有历史对话，显示一个更大的欢迎引导页
- 方案卡片增加"导出分享"按钮（已有 showShareModal 函数可复用）
- 方案卡片增加"复制文字版"按钮
- 输入框支持 Shift+Enter 换行（用 textarea 替代 input）
- 正在加载时禁用发送按钮

### 4. 移动端适配
- 屏幕 < 768px 时隐藏侧边栏，显示汉堡菜单按钮
- 聊天区域 padding 缩小
- 方案卡片全宽
- 底部输入区域贴底

### 5. 主题和体验
- 保留现有的设计系统变量（--primary, --canvas 等全部保留）
- 消息发送时有轻微的动画反馈
- 加载状态时输入框显示 disabled 状态
- 方案卡片的确认按钮执行后不可重复点击

## 现有代码

以下是当前的完整 HTML 文件，在此基础上修改：

```html
<!DOCTYPE html><html lang="zh-CN"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>美团本地规划 Agent</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">

[... 保留现有的所有 CSS 变量和样式 ...]
[... 保留现有的 HTML 结构 ...]
[... JS 部分需要重写以支持上述所有功能 ...]
```

## 输出要求

1. 输出**一个完整的 HTML 文件**，所有 CSS 和 JS 内联
2. 保留现有的视觉设计风格不变（颜色、圆角、字体、间距）
3. JS 代码要有合理的模块化结构（可以用 class 或模块模式）
4. localStorage 的 key 统一用 `meituan_agent_` 前缀
5. 所有功能必须实际可用，不能只是 UI 壳子
6. 文件开头注释标注版本和日期
