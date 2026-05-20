"""数据模型定义"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime, time


class SceneType(Enum):
    """场景类型"""
    FAMILY = "family"  # 家庭场景
    FRIENDS = "friends"  # 朋友场景


class VenueType(Enum):
    """场所类型"""
    RESTAURANT = "restaurant"
    ATTRACTION = "attraction"
    ACTIVITY = "activity"
    SHOPPING = "shopping"


@dataclass
class Location:
    """位置信息"""
    name: str
    address: str
    latitude: float
    longitude: float
    distance_km: Optional[float] = None


@dataclass
class Restaurant:
    """餐厅信息"""
    id: str
    name: str
    location: Location
    rating: float
    price_per_person: int
    cuisine_type: str
    features: List[str]  # 如: ["亲子友好", "低卡轻食"]
    available_times: List[str]  # 可预约时段
    queue_length: int  # 当前排队人数
    has_private_room: bool = False
    children_facilities: bool = False


@dataclass
class Attraction:
    """景点/活动信息"""
    id: str
    name: str
    location: Location
    type: str  # 亲子乐园, 展览, citywalk, 电影等
    rating: float
    price: int
    duration_minutes: int
    features: List[str]
    opening_hours: str
    booking_required: bool = False
    available_slots: List[str] = field(default_factory=list)


@dataclass
class BookingInfo:
    """预订信息"""
    venue_id: str
    venue_name: str
    venue_type: VenueType
    time: str
    people_count: int
    status: str  # pending, confirmed, failed
    booking_id: Optional[str] = None
    notes: str = ""


@dataclass
class PlanItem:
    """计划项"""
    venue_type: VenueType
    venue: Any  # Restaurant or Attraction
    start_time: str
    end_time: str
    action: str  # 预订/购票/到店
    status: str = "planned"  # planned, booked, failed
    booking_info: Optional[BookingInfo] = None


@dataclass
class ActivityPlan:
    """完整活动计划"""
    user_name: str
    scene_type: SceneType
    people_count: int
    home_location: Location
    start_time: str
    end_time: str
    items: List[PlanItem] = field(default_factory=list)
    total_budget: int = 0
    notes: str = ""
    
    def to_summary(self) -> str:
        """生成计划摘要"""
        lines = [
            f"📋 下午活动方案（{self.start_time} - {self.end_time}）",
            f"📍 出发地：{self.home_location.name}",
            ""
        ]
        
        for i, item in enumerate(self.items, 1):
            emoji = "🍽️" if item.venue_type == VenueType.RESTAURANT else "🎯"
            lines.append(
                f"{i}. {emoji} {item.start_time}-{item.end_time} | "
                f"{item.venue.name} | {item.action}"
            )
            if item.booking_info and item.booking_info.booking_id:
                lines.append(f"   ✅ 已{item.action}（{item.booking_info.booking_id}）")
            elif item.status in ("confirmed", "booked") and not (item.booking_info and item.booking_info.booking_id):
                lines.append(f"   ✅ 直接到店")
        
        lines.extend([
            "",
            f"💰 预计花费：¥{self.total_budget}",
            f"👥 人数：{self.people_count}人",
        ])
        
        if self.notes:
            lines.extend(["", f"📝 备注：{self.notes}"])
        
        return "\n".join(lines)


@dataclass
class UserProfile:
    """用户画像"""
    name: str
    home_location: Location
    scene_type: SceneType
    family_info: Optional[Dict] = None  # {child_age: 5, spouse_diet: "减肥"}
    friend_info: Optional[Dict] = None  # {total: 4, male: 2, female: 2}
    preferences: List[str] = field(default_factory=list)
