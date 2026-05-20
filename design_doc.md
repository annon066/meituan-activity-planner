# 美团活动规划Agent设计文档

## 1. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户交互层 (CLI/Web)                    │
│                     main.py / ActivityAgentCLI               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Agent 核心层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │IntentParser │→ │ActivityPlanner│→ │PlanExecutor│         │
│  │ (意图解析)   │  │ (方案规划)    │  │ (执行预订)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      工具层 (Tools)                          │
│  RestaurantTool │ AttractionTool │ BookingTool │ LocationTool│
│     (餐厅)      │     (景点)      │    (预订)   │    (位置)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Mock API 层                               │
│  MockRestaurantAPI │ MockAttractionAPI │ MockBookingAPI     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Planning 策略

### 2.1 意图解析策略
采用**规则+关键词匹配**的方式解析自然语言输入：

| 信息类型 | 解析方法 | 示例 |
|---------|---------|------|
| 场景类型 | 关键词匹配 | "老婆孩子"→家庭, "朋友"→聚会 |
| 人数 | 正则提取数字+默认推断 | "4个人"→4, 家庭场景默认3人 |
| 时间 | 时间词识别+默认值 | "下午"→14:00-18:00 |
| 特殊需求 | 关键词识别 | "减肥"→低卡饮食需求 |

### 2.2 活动规划策略
采用**场景驱动+约束优化**的多阶段规划：

```
1. 场景识别 → 确定活动类型偏好
   - 家庭场景: 亲子活动 + 家庭友好餐厅
   - 朋友场景: 互动活动 + 聚会餐厅

2. 约束过滤 → 筛选符合条件的场所
   - 距离约束: 优先10km内
   - 特色约束: 匹配特殊需求（减肥→轻食餐厅）
   - 时间约束: 活动时长适配可用时间

3. 时间分配 → 合理安排活动顺序
   - 规则: 活动 → 用餐 → 活动
   - 自动计算时长，分配具体时间段

4. 冲突检测 → 验证时间合理性
   - 检测时间重叠
   - 自动调整压缩时长
```

### 2.3 方案生成优先级
```
家庭场景优先级:
  1. 儿童设施 (children_facilities=True)
  2. 距离近 (distance_km 最小)
  3. 评分高 (rating ≥ 4.5)

朋友场景优先级:
  1. 互动性 (密室/展览优先)
  2. 聚会氛围 (聚会推荐标签)
  3. 可预订性 (booking_required)
```

## 3. 工具调用链路

### 3.1 核心调用流程
```
用户输入
    │
    ▼
IntentParser.parse()
    │ 输出: UserIntent
    ▼
ActivityPlanner.plan()
    │
    ├─→ LocationTool.get_current_location()  # 获取位置
    ├─→ AttractionTool.search()              # 搜索活动
    ├─→ RestaurantTool.search()              # 搜索餐厅
    ├─→ PlanningTool.allocate_time()         # 分配时间
    └─→ PlanningTool.check_conflicts()       # 检查冲突
    │ 输出: ActivityPlan
    ▼
PlanExecutor.execute()
    │
    ├─→ RestaurantTool.book()                # 预订餐厅
    └─→ AttractionTool.book()                # 预订景点
    │ 输出: ActivityPlan (含预订结果)
    ▼
用户确认 → 一键执行所有预订
```

### 3.2 工具接口设计
所有工具遵循统一的接口规范：

```python
class ToolInterface:
    def search(self, **filters) -> List[Dict]
        """搜索资源"""
    
    def check_availability(self, id, time_slot) -> Dict
        """检查可用性"""
    
    def book(self, id, time_slot, people_count, user_info) -> Dict
        """执行预订"""
```

## 4. 异常处理机制

### 4.1 异常分类与处理
| 异常类型 | 场景 | 处理策略 |
|---------|------|---------|
| 解析失败 | 无法识别场景/时间 | 使用默认值，提示用户确认 |
| 资源不足 | 无符合条件的场所 | 扩大搜索范围/降低筛选条件 |
| 时段冲突 | 预订时段不可用 | 推荐替代时段/自动调整 |
| 预订失败 | API调用异常 | 标记失败状态，提供手动处理建议 |

### 4.2 容错机制
```python
# 1. 降级策略
if not attractions:
    # 扩大搜索范围或使用默认推荐
    attractions = get_default_recommendations(scene_type)

# 2. 重试机制
def book_with_retry(booking_func, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = booking_func()
            if result["success"]:
                return result
        except Exception as e:
            log_error(e)
    return {"success": False, "message": "预订失败"}

# 3. 部分成功处理
results = {"success": 0, "failed": 0}
for item in plan.items:
    try:
        book(item)
        results["success"] += 1
    except:
        results["failed"] += 1
        # 继续处理其他项目，不中断整体流程
```

## 5. 扩展性设计

### 5.1 新增场景
在 `IntentParser.scene_keywords` 添加关键词，在 `ActivityPlanner._plan_xxx_activities()` 实现规划逻辑。

### 5.2 新增工具
实现 `ToolInterface` 接口，在 `ActivityPlanner` 中集成调用。

### 5.3 接入真实API
Mock API 可替换为真实美团API调用，工具层无需修改。

## 6. 性能指标

- 意图解析: < 100ms
- 方案生成: < 2s (含搜索)
- 预订执行: < 5s (并行调用)

---

**项目结构:**
```
meituan/
├── main.py              # CLI入口
├── agent/
│   └── planner.py       # Agent核心逻辑
├── tools/               # 工具层
├── mock_api/            # Mock API
├── models/              # 数据模型
└── utils/               # 工具函数
```
