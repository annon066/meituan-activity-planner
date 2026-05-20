"""工具层 - 景点/活动工具"""
from typing import List, Dict, Any, Optional
from mock_api.attraction_api import MockAttractionAPI


class AttractionTool:
    """景点/活动查询与预订工具"""
    
    def __init__(self):
        self.api = MockAttractionAPI()
        self.name = "attraction_tool"
        self.description = """
        景点/活动查询与预订工具。
        支持搜索亲子乐园、展览、CityWalk、电影、话剧、健身、密室等活动。
        """
    
    def search(
        self,
        attraction_type: str = None,
        features: List[str] = None,
        max_distance_km: float = 10.0,
        price_range: tuple = (0, 500),
        duration_max: int = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索景点/活动
        
        Args:
            attraction_type: 类型 (亲子乐园/展览/citywalk/电影/话剧/健身/密室)
            features: 特色标签
            max_distance_km: 最大距离
            price_range: 价格范围
            duration_max: 最大时长(分钟)
            limit: 返回数量限制
        """
        attractions = self.api.search_attractions(
            attraction_type=attraction_type,
            features=features,
            max_distance_km=max_distance_km,
            price_range=price_range,
            duration_max=duration_max,
            min_rating=4.0,
            limit=limit
        )
        
        return [
            {
                "id": a.id,
                "name": a.name,
                "type": a.type,
                "address": a.location.address,
                "distance_km": a.location.distance_km,
                "rating": a.rating,
                "price": a.price,
                "duration_minutes": a.duration_minutes,
                "features": a.features,
                "opening_hours": a.opening_hours,
                "booking_required": a.booking_required,
                "available_slots": a.available_slots
            }
            for a in attractions
        ]
    
    def check_availability(self, attraction_id: str, time_slot: str) -> Dict[str, Any]:
        """检查景点可用性"""
        return self.api.check_availability(attraction_id, time_slot)
    
    def book(
        self,
        attraction_id: str,
        time_slot: str,
        people_count: int,
        user_name: str,
        phone: str
    ) -> Dict[str, Any]:
        """预订景点/活动"""
        return self.api.book_attraction(
            attraction_id, time_slot, people_count, user_name, phone
        )
    
    def get_for_scene(
        self,
        scene_type: str,
        time_available: int = 120,  # 可用时间(分钟)
        children_age: int = None
    ) -> Dict[str, Any]:
        """根据场景获取推荐活动"""
        if scene_type == "family":
            # 家庭场景：优先亲子乐园
            attractions = self.search(
                attraction_type="亲子乐园",
                duration_max=time_available,
                limit=3
            )
        elif scene_type == "friends":
            # 朋友场景：展览、CityWalk、密室等
            attractions = self.search(
                features=["打卡拍照", "团队协作"],
                duration_max=time_available,
                limit=5
            )
        else:
            attractions = self.search(duration_max=time_available, limit=3)
        
        if not attractions:
            return {"recommendations": [], "message": "未找到合适的活动"}
        
        return {
            "recommendations": attractions,
            "message": f"找到{len(attractions)}个活动，推荐【{attractions[0]['name']}】"
        }
