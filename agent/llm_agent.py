"""LLM Agent - 基于 OpenAI 兼容接口的活动规划 Agent（无第三方依赖）"""
import json
import logging
import ssl
import urllib.request
import config as cfg

logger = logging.getLogger(__name__)


def _get_ssl_ctx():
    if cfg.SSL_VERIFY:
        return ssl.create_default_context()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
from tools import RestaurantTool, AttractionTool, BookingTool, LocationTool

SYSTEM_PROMPT = """你是美团活动规划助手。用户告诉你需求后，你需要：
1. 理解用户意图（场景类型、人数、时间、特殊需求）
2. 调用 plan_search 工具一次性搜索所有需要的餐厅和景点
3. 根据搜索结果组合完整方案，合理安排时间并输出

方案编排规则：
- 活动和用餐必须交替安排，不能连续安排两个餐厅或连续安排两个景点
- 正确模式举例：景点→餐厅→景点，或 餐厅→景点→餐厅
- 一天最多安排1-2顿正餐（午餐和/或晚餐），不能连续吃两顿
- 根据时间段合理安排：下午一般先玩后吃，上午一般先吃后玩
- 每个活动之间留15-30分钟通勤/休息时间
- 家庭场景优先亲子友好的地方；朋友场景优先互动性强的活动

输出规则：
- 输出方案时，必须在回复末尾附上结构化数据（这是前端渲染卡片的依赖，绝对不能省略），格式为：
  <!--PLAN_JSON-->{"items":[{"name":"xxx","venue_type":"restaurant/attraction","start_time":"HH:MM","end_time":"HH:MM","address":"xxx","price":数字,"action":"预订/到店"}],"total_budget":数字,"scene_type":"family/friends","people_count":数字,"duration_hours":数字}<!--/PLAN_JSON-->
- 每次给出方案都必须附带上面的 PLAN_JSON 标记
- 普通对话不需要附 PLAN_JSON
- 回复简洁自然，像朋友聊天一样"""

TOOLS = [
    {"type": "function", "function": {"name": "plan_search", "description": "一次性搜索餐厅和景点，返回所有可选项", "parameters": {"type": "object", "properties": {"scene_type": {"type": "string", "enum": ["family", "friends"], "description": "场景类型"}, "features": {"type": "array", "items": {"type": "string"}, "description": "偏好特征，如亲子、减肥、浪漫等"}, "people_count": {"type": "integer", "description": "人数"}}, "required": ["scene_type"]}}},
    {"type": "function", "function": {"name": "book_restaurant", "description": "预订餐厅", "parameters": {"type": "object", "properties": {"restaurant_id": {"type": "string"}, "time_slot": {"type": "string"}, "people_count": {"type": "integer"}, "user_name": {"type": "string"}, "phone": {"type": "string"}}, "required": ["restaurant_id", "time_slot", "people_count", "user_name"]}}},
    {"type": "function", "function": {"name": "book_attraction", "description": "预订景点/活动", "parameters": {"type": "object", "properties": {"attraction_id": {"type": "string"}, "time_slot": {"type": "string"}, "people_count": {"type": "integer"}, "user_name": {"type": "string"}, "phone": {"type": "string"}}, "required": ["attraction_id", "time_slot", "people_count", "user_name"]}}}
]


class LLMAgent:
    def __init__(self):
        self.restaurant_tool = RestaurantTool()
        self.attraction_tool = AttractionTool()
        self.booking_tool = BookingTool()
        self.location_tool = LocationTool()

    def _call_api(self, messages, tools=None):
        body = {"model": cfg.LLM_MODEL, "messages": messages}
        if tools:
            body["tools"] = tools
            body["tool_choice"] = "auto"

        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"{cfg.LLM_BASE_URL}/chat/completions",
            data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {cfg.LLM_API_KEY}"}
        )
        try:
            with urllib.request.urlopen(req, timeout=90, context=_get_ssl_ctx()) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode() if e.fp else ''
            logger.error("API HTTP %d: %s", e.code, body[:200])
            raise Exception(f"API 返回 {e.code}: {body[:200]}")
        except urllib.error.URLError as e:
            logger.error("API 连接失败: %s", e.reason)
            raise Exception(f"无法连接到 API: {e.reason}")
        except TimeoutError:
            logger.error("API 请求超时")
            raise Exception("API 请求超时，请稍后重试")

    def chat(self, messages: list, user_context: str = None) -> dict:
        system_content = SYSTEM_PROMPT
        if user_context:
            system_content += f"\n\n{user_context}"
        full_messages = [{"role": "system", "content": system_content}] + messages

        for _ in range(5):
            result = self._call_api(full_messages, TOOLS)
            choice = result["choices"][0]["message"]

            if choice.get("tool_calls"):
                full_messages.append(choice)
                for tc in choice["tool_calls"]:
                    try:
                        args = json.loads(tc["function"]["arguments"]) if tc["function"]["arguments"] else {}
                    except json.JSONDecodeError:
                        args = {}
                    fn_result = self._dispatch_tool(tc["function"]["name"], args)
                    full_messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": json.dumps(fn_result, ensure_ascii=False)
                    })
            else:
                return {"content": choice.get("content", ""), "role": "assistant"}

        return {"content": "抱歉，处理超时了，请重试~", "role": "assistant"}

    def _dispatch_tool(self, name: str, args: dict):
        if name == "plan_search":
            location = self.location_tool.get_current_location()
            scene = args.get("scene_type", "family")
            restaurants = self.restaurant_tool.search(scene_type=scene, features=args.get("features", []), limit=3)
            # 按场景选择景点类型
            if scene == "family":
                attractions = self.attraction_tool.search(attraction_type="亲子乐园", limit=3)
            else:
                attractions = self.attraction_tool.search(limit=5)
            # 如果结果不够，补充其他类型
            if len(attractions) < 2:
                attractions += self.attraction_tool.search(limit=3)
            return {"location": location, "restaurants": restaurants, "attractions": attractions}
        elif name == "book_restaurant":
            args.setdefault("phone", "138****8888")
            return self.restaurant_tool.book(**args)
        elif name == "book_attraction":
            args.setdefault("phone", "138****8888")
            return self.attraction_tool.book(**args)
        return {"error": f"未知工具: {name}"}
