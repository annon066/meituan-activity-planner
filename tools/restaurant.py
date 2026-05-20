"""工具层 - 餐厅工具"""
from typing import List, Dict, Any, Optional
from models.schemas import Restaurant, VenueType
from mock_api.restaurant_api import MockRestaurantAPI


class RestaurantTool:
    """餐厅查询与预订工具"""
    
    def __init__(self):
        self.api = MockRestaurantAPI()
        self.name = "restaurant_tool"
        self.description = """
        餐厅查询与预订工具。
        可根据场景类型、特色标签、距离、价格等条件搜索餐厅。
        支持检查可用性和预订餐厅。
        """
    
    def search(
        self,
        scene_type: str = None,
        features: List[str] = None,
        max_distance_km: float = 10.0,
        price_range: tuple = (0, 500),
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """搜索餐厅
        
        Args:
            scene_type: 场景类型 (family/friends)
            features: 特色标签，如 ["亲子友好", "低卡轻食", "聚会推荐"]
            max_distance_km: 最大距离(公里)
            price_range: 人均价格范围 (min, max)
            limit: 返回数量限制
        
        Returns:
            餐厅列表
        """
        # 根据场景类型推断特色
        inferred_features = list(features) if features else []
        
        if scene_type == "family":
            inferred_features.extend(["亲子友好"])
        elif scene_type == "friends":
            inferred_features.extend(["聚会推荐"])
        
        restaurants = self.api.search_restaurants(
            features=inferred_features if inferred_features else None,
            max_distance_km=max_distance_km,
            price_range=price_range,
            min_rating=4.0,
            limit=limit
        )
        
        return [
            {
                "id": r.id,
                "name": r.name,
                "address": r.location.address,
                "distance_km": r.location.distance_km,
                "rating": r.rating,
                "price_per_person": r.price_per_person,
                "cuisine_type": r.cuisine_type,
                "features": r.features,
                "available_times": r.available_times,
                "queue_length": r.queue_length,
                "has_private_room": r.has_private_room,
                "children_facilities": r.children_facilities
            }
            for r in restaurants
        ]
    
    def check_availability(
        self,
        restaurant_id: str,
        time_slot: str,
        people_count: int
    ) -> Dict[str, Any]:
        """检查餐厅可用性"""
        return self.api.check_availability(restaurant_id, time_slot, people_count)
    
    def book(
        self,
        restaurant_id: str,
        time_slot: str,
        people_count: int,
        user_name: str,
        phone: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """预订餐厅"""
        return self.api.book_restaurant(
            restaurant_id, time_slot, people_count, user_name, phone, notes
        )
    
    def get_recommendation(
        self,
        scene_type: str,
        special_needs: List[str] = None
    ) -> Dict[str, Any]:
        """获取餐厅推荐（简化版）"""
        features = []
        if scene_type == "family":
            features.append("亲子友好")
        if special_needs:
            if "减肥" in special_needs:
                features.append("低卡轻食")
        
        restaurants = self.search(scene_type=scene_type, features=features, limit=3)
        
        if not restaurants:
            return {"recommendation": None, "message": "未找到合适的餐厅"}
        
        best = restaurants[0]
        return {
            "recommendation": best,
            "message": f"推荐【{best['name']}】，评分{best['rating']}，人均¥{best['price_per_person']}，距离{best['distance_km']}km"
        }
