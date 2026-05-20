"""Mock 餐厅 API"""
import random
from typing import List, Optional
from models.schemas import Restaurant, Location, VenueType


class MockRestaurantAPI:
    """Mock 餐厅查询 API"""
    
    def __init__(self):
        self._restaurants = self._init_restaurants()
    
    def _init_restaurants(self) -> List[Restaurant]:
        """初始化 Mock 餐厅数据"""
        return [
            # 亲子友好餐厅
            Restaurant(
                id="r001", name="西贝莜面村(朝阳大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.8, price_per_person=85, cuisine_type="西北菜",
                features=["亲子友好", "有儿童座椅", "环境宽敞"],
                available_times=["12:00", "12:30", "17:30", "18:00", "18:30"],
                queue_length=12, has_private_room=True, children_facilities=True
            ),
            Restaurant(
                id="r002", name="海底捞(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.7, price_per_person=120, cuisine_type="火锅",
                features=["亲子友好", "美甲服务", "儿童游乐区"],
                available_times=["11:00", "14:00", "17:00", "20:00"],
                queue_length=25, has_private_room=True, children_facilities=True
            ),
            # 轻食/减肥友好餐厅
            Restaurant(
                id="r003", name="Wagas(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=75, cuisine_type="西式轻食",
                features=["低卡轻食", "健康沙拉", "果汁饮品"],
                available_times=["11:30", "12:00", "18:00", "19:00"],
                queue_length=3, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r004", name="新元素(国贸店)",
                location=Location(name="国贸", address="朝阳区建国门外大街1号", latitude=39.91, longitude=116.46, distance_km=7.1),
                rating=4.6, price_per_person=95, cuisine_type="健康轻食",
                features=["低卡轻食", "有机食材", "适合减肥"],
                available_times=["11:00", "12:30", "18:30"],
                queue_length=5, has_private_room=False, children_facilities=False
            ),
            # 聚会餐厅
            Restaurant(
                id="r005", name="胡桃里音乐酒馆(工体店)",
                location=Location(name="工人体育场", address="朝阳区工体北路", latitude=39.93, longitude=116.45, distance_km=5.5),
                rating=4.4, price_per_person=150, cuisine_type="创意菜",
                features=["聚会推荐", "现场音乐", "氛围感强"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=8, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r006", name="局气(王府井店)",
                location=Location(name="王府井", address="东城区王府井大街", latitude=39.91, longitude=116.41, distance_km=8.5),
                rating=4.6, price_per_person=100, cuisine_type="北京菜",
                features=["聚会推荐", "老北京风味", "环境特色"],
                available_times=["11:30", "17:30", "18:30"],
                queue_length=15, has_private_room=True, children_facilities=False
            ),
            # 综合型餐厅
            Restaurant(
                id="r007", name="外婆家(大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.5, price_per_person=65, cuisine_type="杭帮菜",
                features=["性价比高", "亲子友好", "环境优雅"],
                available_times=["11:00", "12:00", "17:00", "18:00"],
                queue_length=20, has_private_room=True, children_facilities=True
            ),
            Restaurant(
                id="r008", name="绿茶餐厅(荟聚店)",
                location=Location(name="荟聚中心", address="大兴区欣雅街", latitude=39.79, longitude=116.33, distance_km=12.0),
                rating=4.4, price_per_person=60, cuisine_type="创意融合菜",
                features=["亲子友好", "装修有特色", "性价比高"],
                available_times=["11:30", "17:30", "18:00"],
                queue_length=18, has_private_room=False, children_facilities=True
            ),
            Restaurant(
                id="r009", name="鹿港小镇(朝阳大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.6, price_per_person=78, cuisine_type="台式简餐",
                features=["亲子友好", "低卡轻食", "有儿童座椅", "健康少油"],
                available_times=["11:30", "12:00", "17:00", "17:30", "18:00"],
                queue_length=6, has_private_room=True, children_facilities=True
            ),
        ]
    
    def search_restaurants(
        self,
        location: Optional[str] = None,
        cuisine_type: Optional[str] = None,
        features: Optional[List[str]] = None,
        max_distance_km: Optional[float] = None,
        min_rating: Optional[float] = None,
        price_range: Optional[tuple] = None,
        limit: int = 5
    ) -> List[Restaurant]:
        """搜索餐厅"""
        results = self._restaurants.copy()
        
        # 筛选逻辑
        if min_rating:
            results = [r for r in results if r.rating >= min_rating]
        
        if max_distance_km:
            results = [r for r in results if r.location.distance_km and r.location.distance_km <= max_distance_km]
        
        if features:
            results = [r for r in results if any(f in r.features for f in features)]
            results.sort(key=lambda r: sum(1 for f in features if f in r.features), reverse=True)
        
        if price_range:
            results = [r for r in results if price_range[0] <= r.price_per_person <= price_range[1]]
        
        if not features:
            results.sort(key=lambda x: x.location.distance_km or 999)

        return results[:limit]
    
    def get_restaurant(self, restaurant_id: str) -> Optional[Restaurant]:
        """获取餐厅详情"""
        for r in self._restaurants:
            if r.id == restaurant_id:
                return r
        return None
    
    def check_availability(self, restaurant_id: str, time_slot: str, people_count: int) -> dict:
        """检查餐厅可用性"""
        restaurant = self.get_restaurant(restaurant_id)
        if not restaurant:
            return {"available": False, "message": "餐厅不存在"}
        
        if time_slot in restaurant.available_times:
            return {
                "available": True,
                "message": f"{time_slot}有位置，当前排队{restaurant.queue_length}桌",
                "queue_length": restaurant.queue_length
            }
        
        return {
            "available": False,
            "message": f"{time_slot}无可用时段，建议选择其他时间",
            "nearby_times": restaurant.available_times
        }
    
    def book_restaurant(
        self,
        restaurant_id: str,
        time_slot: str,
        people_count: int,
        user_name: str,
        phone: str,
        notes: str = ""
    ) -> dict:
        """预订餐厅"""
        restaurant = self.get_restaurant(restaurant_id)
        if not restaurant:
            return {"success": False, "message": "餐厅不存在"}
        
        if time_slot not in restaurant.available_times:
            return {"success": False, "message": "该时段不可预订"}
        
        # 模拟预订成功
        booking_id = f"BK{random.randint(100000, 999999)}"
        return {
            "success": True,
            "booking_id": booking_id,
            "restaurant_name": restaurant.name,
            "address": restaurant.location.address,
            "time": time_slot,
            "people_count": people_count,
            "message": "预订成功！请准时到店，迟到15分钟将自动取消"
        }
