"""Agent核心 - 规划器"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import re
from datetime import datetime, timedelta

from models.schemas import (
    SceneType, VenueType, Location, Restaurant, Attraction,
    PlanItem, ActivityPlan, UserProfile, BookingInfo
)
from tools import RestaurantTool, AttractionTool, BookingTool, LocationTool, PlanningTool


@dataclass
class UserIntent:
    """用户意图"""
    scene_type: SceneType
    people_count: int
    time_range: Tuple[str, str]  # (start_time, end_time)
    duration_hours: float
    special_needs: List[str] = field(default_factory=list)
    family_info: Optional[Dict] = None
    friend_info: Optional[Dict] = None
    preferences: List[str] = field(default_factory=list)


class IntentParser:
    """意图解析器 - 解析自然语言输入"""
    
    def __init__(self):
        self.scene_keywords = {
            "family": ["老婆", "孩子", "家人", "亲子", "儿子", "女儿", "小孩"],
            "friends": ["朋友", "闺蜜", "哥们", "一起玩", "聚会", "几个朋友"]
        }
        
        self.time_keywords = {
            "上午": (9, 12),
            "中午": (11, 14),
            "下午": (14, 18),
            "傍晚": (17, 20),
            "晚上": (18, 22)
        }
    
    def parse(self, text: str) -> UserIntent:
        """解析用户输入"""
        # 场景类型
        scene_type = self._detect_scene(text)
        
        # 人数
        people_count = self._detect_people_count(text, scene_type)
        
        # 时间
        time_range, duration = self._detect_time(text)
        
        # 特殊需求
        special_needs = self._detect_special_needs(text)
        
        # 家庭信息
        family_info = self._detect_family_info(text) if scene_type == SceneType.FAMILY else None
        
        # 朋友信息
        friend_info = self._detect_friend_info(text) if scene_type == SceneType.FRIENDS else None
        
        return UserIntent(
            scene_type=scene_type,
            people_count=people_count,
            time_range=time_range,
            duration_hours=duration,
            special_needs=special_needs,
            family_info=family_info,
            friend_info=friend_info
        )
    
    def _detect_scene(self, text: str) -> SceneType:
        """检测场景类型"""
        for keyword in self.scene_keywords["family"]:
            if keyword in text:
                return SceneType.FAMILY
        for keyword in self.scene_keywords["friends"]:
            if keyword in text:
                return SceneType.FRIENDS
        return SceneType.FAMILY  # 默认家庭场景
    
    def _detect_people_count(self, text: str, scene_type: SceneType) -> int:
        """检测人数"""
        # 提取数字
        numbers = re.findall(r'(\d+)[个人]|[全]家(\d+)|(\d+)个', text)
        
        for nums in numbers:
            for n in nums:
                if n:
                    return int(n)
        
        # 默认人数
        if scene_type == SceneType.FAMILY:
            return 3  # 小明+老婆+孩子
        else:
            return 4  # 4个朋友
    
    def _detect_time(self, text: str) -> Tuple[Tuple[str, str], float]:
        """检测时间范围"""
        text_lower = text.lower()
        
        # 检测时间关键词
        if "下午" in text or "午后" in text:
            # 提取具体时间
            hours = re.findall(r'(\d+)[点时]', text)
            if hours:
                start_hour = int(hours[0])
                if start_hour < 12:
                    start_hour += 12  # 转换为24小时制
                end_hour = min(start_hour + 4, 21)
                return (f"{start_hour}:00", f"{end_hour}:00"), 4.0
        
        # 默认下午2点到6点
        return ("14:00", "18:00"), 4.0
    
    def _detect_special_needs(self, text: str) -> List[str]:
        """检测特殊需求"""
        needs = []
        
        if "减肥" in text:
            needs.append("减肥")
        if "孩子" in text or "小孩" in text or "亲子" in text:
            needs.append("亲子")
        if "老人" in text:
            needs.append("老人")
        if "生日" in text:
            needs.append("生日")
        if "纪念日" in text:
            needs.append("纪念日")
        
        return needs
    
    def _detect_family_info(self, text: str) -> Dict:
        """检测家庭信息"""
        info = {}
        
        # 孩子年龄
        age_match = re.search(r'孩子?(\d+)岁', text)
        if age_match:
            info["child_age"] = int(age_match.group(1))
        else:
            info["child_age"] = 5  # 默认5岁
        
        # 配偶需求
        if "减肥" in text:
            info["spouse_diet"] = "减肥"
        
        return info
    
    def _detect_friend_info(self, text: str) -> Dict:
        """检测朋友信息"""
        info = {"total": 4}
        
        # 提取男女数量
        male_match = re.search(r'(\d+)个?男', text)
        female_match = re.search(r'(\d+)个?女', text)
        
        if male_match:
            info["male"] = int(male_match.group(1))
        if female_match:
            info["female"] = int(female_match.group(1))
        
        return info


class ActivityPlanner:
    """活动规划器 - 核心规划逻辑"""
    
    def __init__(self):
        self.restaurant_tool = RestaurantTool()
        self.attraction_tool = AttractionTool()
        self.booking_tool = BookingTool()
        self.location_tool = LocationTool()
        self.planning_tool = PlanningTool()
    
    def plan(self, intent: UserIntent, user_name: str = "小明") -> ActivityPlan:
        """生成活动计划"""
        # 1. 获取用户位置
        home_location = self._get_home_location()
        
        # 2. 规划活动组合
        activities = self._plan_activities(intent, home_location)
        
        # 3. 分配时间
        allocated = self._allocate_time(activities, intent.time_range)
        
        # 4. 检查冲突
        conflicts = self.planning_tool.check_conflicts(allocated)
        if conflicts:
            allocated = self._resolve_conflicts(allocated, conflicts)
        
        # 5. 生成计划
        plan = self._build_plan(
            intent, allocated, home_location, user_name
        )
        
        return plan
    
    def _get_home_location(self) -> Location:
        """获取用户位置"""
        loc = self.location_tool.get_current_location()
        return Location(
            name=loc["name"],
            address=loc["address"],
            latitude=loc["latitude"],
            longitude=loc["longitude"]
        )
    
    def _plan_activities(
        self,
        intent: UserIntent,
        home_location: Location
    ) -> List[Dict[str, Any]]:
        """规划活动组合"""
        activities = []
        
        # 根据场景类型规划
        if intent.scene_type == SceneType.FAMILY:
            activities = self._plan_family_activities(intent, home_location)
        else:
            activities = self._plan_friends_activities(intent, home_location)
        
        return activities
    
    def _plan_family_activities(
        self,
        intent: UserIntent,
        home_location: Location
    ) -> List[Dict[str, Any]]:
        """规划家庭活动"""
        activities = []
        child_age = intent.family_info.get("child_age", 5) if intent.family_info else 5
        spouse_diet = intent.family_info.get("spouse_diet") if intent.family_info else None
        
        # 1. 选择亲子活动
        attractions = self.attraction_tool.search(
            attraction_type="亲子乐园",
            duration_max=150,
            limit=3
        )
        
        if attractions:
            # 选择适合年龄的
            suitable = None
            for a in attractions:
                if "适合5-10岁" in a.get("features", []) or child_age >= 3:
                    suitable = a
                    break
            
            if suitable:
                activities.append({
                    "type": "attraction",
                    "id": suitable["id"],
                    "name": suitable["name"],
                    "duration_minutes": suitable["duration_minutes"],
                    "price": suitable["price"],
                    "address": suitable["address"],
                    "distance_km": suitable["distance_km"],
                    "features": suitable["features"],
                    "booking_required": suitable["booking_required"],
                    "available_slots": suitable.get("available_slots", [])
                })
        
        # 2. 选择餐厅
        features = ["亲子友好"]
        if spouse_diet == "减肥":
            features.append("低卡轻食")

        restaurants = self.restaurant_tool.search(
            scene_type="family",
            features=features,
            limit=5
        )

        if restaurants:
            if spouse_diet == "减肥":
                both = [r for r in restaurants if r.get("children_facilities") and "低卡轻食" in r.get("features", [])]
                if both:
                    best = both[0]
                else:
                    diet = [r for r in restaurants if "低卡轻食" in r.get("features", [])]
                    best = diet[0] if diet else restaurants[0]
            else:
                best = next((r for r in restaurants if r.get("children_facilities")), restaurants[0])

            meal_type = "dinner" if int(intent.time_range[0].split(":")[0]) >= 15 else "lunch"

            activities.append({
                "type": "restaurant",
                "id": best["id"],
                "name": best["name"],
                "duration_minutes": 90,
                "price": best["price_per_person"],
                "address": best["address"],
                "distance_km": best["distance_km"],
                "features": best["features"],
                "available_times": best["available_times"],
                "cuisine_type": best["cuisine_type"],
                "meal_type": meal_type
            })
        
        return activities
    
    def _plan_friends_activities(
        self,
        intent: UserIntent,
        home_location: Location
    ) -> List[Dict[str, Any]]:
        """规划朋友活动"""
        activities = []
        
        # 1. 选择活动（展览/CityWalk/密室）
        attractions = self.attraction_tool.search(
            features=["打卡拍照", "团队协作"],
            duration_max=120,
            limit=5
        )
        
        if attractions:
            # 优先选择互动性强的
            interactive = [a for a in attractions if "密室" in a.get("type", "") or "展览" in a.get("type", "")]
            if interactive:
                activities.append({
                    "type": "attraction",
                    "id": interactive[0]["id"],
                    "name": interactive[0]["name"],
                    "duration_minutes": interactive[0]["duration_minutes"],
                    "price": interactive[0]["price"],
                    "address": interactive[0]["address"],
                    "distance_km": interactive[0]["distance_km"],
                    "features": interactive[0]["features"],
                    "booking_required": interactive[0]["booking_required"],
                    "available_slots": interactive[0].get("available_slots", [])
                })
            elif attractions:
                activities.append({
                    "type": "attraction",
                    "id": attractions[0]["id"],
                    "name": attractions[0]["name"],
                    "duration_minutes": attractions[0]["duration_minutes"],
                    "price": attractions[0]["price"],
                    "address": attractions[0]["address"],
                    "distance_km": attractions[0]["distance_km"],
                    "features": attractions[0]["features"],
                    "booking_required": attractions[0]["booking_required"],
                    "available_slots": attractions[0].get("available_slots", [])
                })
        
        # 2. 选择餐厅
        restaurants = self.restaurant_tool.search(
            scene_type="friends",
            features=["聚会推荐"],
            limit=3
        )
        
        if restaurants:
            best = restaurants[0]
            activities.append({
                "type": "restaurant",
                "id": best["id"],
                "name": best["name"],
                "duration_minutes": 90,
                "price": best["price_per_person"],
                "address": best["address"],
                "distance_km": best["distance_km"],
                "features": best["features"],
                "available_times": best["available_times"],
                "cuisine_type": best["cuisine_type"],
                "meal_type": "dinner"
            })
        
        return activities
    
    def _allocate_time(
        self,
        activities: List[Dict[str, Any]],
        time_range: Tuple[str, str]
    ) -> List[Dict[str, Any]]:
        """分配时间"""
        return self.planning_tool.allocate_time(
            time_range[0], time_range[1], activities
        )
    
    def _resolve_conflicts(
        self,
        activities: List[Dict[str, Any]],
        conflicts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """解决时间冲突"""
        # 简化处理：压缩时间
        for conflict in conflicts:
            # 找到冲突的活动并压缩
            for a in activities:
                if a.get("name") == conflict.get("activity1"):
                    a["duration_minutes"] = int(a.get("duration_minutes", 60) * 0.8)
        
        # 重新分配时间
        return activities
    
    def _build_plan(
        self,
        intent: UserIntent,
        activities: List[Dict[str, Any]],
        home_location: Location,
        user_name: str
    ) -> ActivityPlan:
        """构建活动计划"""
        plan = ActivityPlan(
            user_name=user_name,
            scene_type=intent.scene_type,
            people_count=intent.people_count,
            home_location=home_location,
            start_time=intent.time_range[0],
            end_time=intent.time_range[1]
        )
        
        total_budget = 0
        
        for activity in activities:
            venue_type = VenueType.RESTAURANT if activity["type"] == "restaurant" else VenueType.ATTRACTION
            
            # 创建场所对象
            if venue_type == VenueType.RESTAURANT:
                venue = Restaurant(
                    id=activity["id"],
                    name=activity["name"],
                    location=Location(
                        name=activity["name"],
                        address=activity["address"],
                        latitude=0, longitude=0,
                        distance_km=activity.get("distance_km")
                    ),
                    rating=4.5,
                    price_per_person=activity["price"],
                    cuisine_type=activity.get("cuisine_type", ""),
                    features=activity.get("features", []),
                    available_times=activity.get("available_times", []),
                    queue_length=0
                )
            else:
                venue = Attraction(
                    id=activity["id"],
                    name=activity["name"],
                    location=Location(
                        name=activity["name"],
                        address=activity["address"],
                        latitude=0, longitude=0,
                        distance_km=activity.get("distance_km")
                    ),
                    type=activity.get("type", "activity"),
                    rating=4.5,
                    price=activity["price"],
                    duration_minutes=activity["duration_minutes"],
                    features=activity.get("features", []),
                    opening_hours="",
                    booking_required=activity.get("booking_required", False),
                    available_slots=activity.get("available_slots", [])
                )
            
            # 计算花费
            if venue_type == VenueType.RESTAURANT:
                cost = activity["price"] * intent.people_count
            else:
                cost = activity["price"] * intent.people_count
            total_budget += cost
            
            # 创建计划项
            item = PlanItem(
                venue_type=venue_type,
                venue=venue,
                start_time=activity.get("start_time", ""),
                end_time=activity.get("end_time", ""),
                action="预订" if activity.get("booking_required") or venue_type == VenueType.RESTAURANT else "到店"
            )
            
            plan.items.append(item)
        
        plan.total_budget = total_budget
        
        # 添加备注
        if intent.scene_type == SceneType.FAMILY:
            plan.notes = "家庭亲子活动，已考虑儿童设施和健康饮食"
        else:
            plan.notes = "朋友聚会活动，已选择互动性强的项目"
        
        return plan


class PlanExecutor:
    """计划执行器 - 执行预订操作"""

    def __init__(self):
        self.restaurant_tool = RestaurantTool()
        self.attraction_tool = AttractionTool()
        self.booking_tool = BookingTool()

    def execute(
        self,
        plan: ActivityPlan,
        user_phone: str = "138****8888"
    ) -> ActivityPlan:
        """执行计划中的预订操作"""
        for item in plan.items:
            try:
                if item.venue_type == VenueType.RESTAURANT:
                    result = self._book_restaurant(item, plan, user_phone)
                else:
                    result = self._book_attraction(item, plan, user_phone)

                if result.get("success"):
                    if result.get("booking_id"):
                        item.status = "booked"
                    else:
                        item.status = "confirmed"
                    item.booking_info = BookingInfo(
                        venue_id=item.venue.id,
                        venue_name=item.venue.name,
                        venue_type=item.venue_type,
                        time=item.start_time,
                        people_count=plan.people_count,
                        status="confirmed" if result.get("booking_id") else "walk_in",
                        booking_id=result.get("booking_id"),
                        notes=result.get("message", "")
                    )
                else:
                    item.status = "failed"

            except Exception as e:
                item.status = "failed"
                print(f"预订失败: {e}")

        return plan

    def _book_restaurant(
        self,
        item: PlanItem,
        plan: ActivityPlan,
        phone: str
    ) -> Dict[str, Any]:
        """预订餐厅 - 失败时自动尝试其他时段/备选餐厅"""
        result = self.restaurant_tool.book(
            restaurant_id=item.venue.id,
            time_slot=item.start_time,
            people_count=plan.people_count,
            user_name=plan.user_name,
            phone=phone
        )
        if result.get("success"):
            return result

        available = getattr(item.venue, 'available_times', [])
        for alt_time in available:
            if alt_time != item.start_time:
                result = self.restaurant_tool.book(
                    restaurant_id=item.venue.id,
                    time_slot=alt_time,
                    people_count=plan.people_count,
                    user_name=plan.user_name,
                    phone=phone
                )
                if result.get("success"):
                    start_dt = datetime.strptime(alt_time, "%H:%M")
                    item.start_time = alt_time
                    item.end_time = (start_dt + timedelta(minutes=90)).strftime("%H:%M")
                    return result

        return self._try_alternative_restaurant(item, plan, phone)

    def _try_alternative_restaurant(
        self,
        item: PlanItem,
        plan: ActivityPlan,
        phone: str
    ) -> Dict[str, Any]:
        """尝试预订备选餐厅"""
        features = getattr(item.venue, 'features', [])
        alternatives = self.restaurant_tool.search(features=features, limit=5)

        for alt in alternatives:
            if alt["id"] == item.venue.id:
                continue
            for time_slot in alt.get("available_times", []):
                result = self.restaurant_tool.book(
                    restaurant_id=alt["id"],
                    time_slot=time_slot,
                    people_count=plan.people_count,
                    user_name=plan.user_name,
                    phone=phone
                )
                if result.get("success"):
                    item.venue.id = alt["id"]
                    item.venue.name = alt["name"]
                    item.venue.location.address = alt["address"]
                    start_dt = datetime.strptime(time_slot, "%H:%M")
                    item.start_time = time_slot
                    item.end_time = (start_dt + timedelta(minutes=90)).strftime("%H:%M")
                    return result

        return {"success": False, "message": "所有备选餐厅均无法预订"}

    def _book_attraction(
        self,
        item: PlanItem,
        plan: ActivityPlan,
        phone: str
    ) -> Dict[str, Any]:
        """预订景点"""
        if not getattr(item.venue, 'booking_required', False):
            return {"success": True, "booking_id": None, "message": "无需预订，直接到店"}

        return self.attraction_tool.book(
            attraction_id=item.venue.id,
            time_slot=item.start_time,
            people_count=plan.people_count,
            user_name=plan.user_name,
            phone=phone
        )

    def confirm_plan(self, plan: ActivityPlan) -> Dict[str, Any]:
        """确认计划（一键执行所有预订）"""
        results = {
            "total": len(plan.items),
            "success": 0,
            "failed": 0,
            "bookings": []
        }

        for item in plan.items:
            if item.status in ("booked", "confirmed") and item.booking_info:
                results["success"] += 1
                results["bookings"].append({
                    "name": item.venue.name,
                    "time": item.start_time,
                    "booking_id": item.booking_info.booking_id
                })
            elif item.status == "failed":
                results["failed"] += 1

        return results
