"""工具层 - 位置工具"""
from typing import List, Dict, Any
from models.schemas import Location
from mock_api.location_api import MockLocationAPI


class LocationTool:
    """位置服务工具"""
    
    def __init__(self):
        self.api = MockLocationAPI()
        self.name = "location_tool"
        self.description = """
        位置服务工具，提供定位、距离计算、出行时间估算等功能。
        """
    
    def get_current_location(self) -> Dict[str, Any]:
        """获取当前位置"""
        loc = self.api.get_current_location()
        return {
            "name": loc.name,
            "address": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude
        }
    
    def calculate_distance(
        self,
        loc1: Dict[str, float],
        loc2: Dict[str, float]
    ) -> float:
        """计算两点间距离"""
        location1 = Location(
            name="", address="",
            latitude=loc1["latitude"],
            longitude=loc1["longitude"]
        )
        location2 = Location(
            name="", address="",
            latitude=loc2["latitude"],
            longitude=loc2["longitude"]
        )
        return self.api.calculate_distance(location1, location2)
    
    def calculate_travel_time(
        self,
        loc1: Dict[str, float],
        loc2: Dict[str, float],
        mode: str = "driving"
    ) -> int:
        """计算出行时间（分钟）"""
        location1 = Location(
            name="", address="",
            latitude=loc1["latitude"],
            longitude=loc1["longitude"]
        )
        location2 = Location(
            name="", address="",
            latitude=loc2["latitude"],
            longitude=loc2["longitude"]
        )
        return self.api.calculate_travel_time(location1, location2, mode)
    
    def search_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_km: float,
        poi_type: str = None
    ) -> List[Dict[str, Any]]:
        """搜索附近POI"""
        center = Location(
            name="", address="",
            latitude=latitude,
            longitude=longitude
        )
        return self.api.search_nearby(center, radius_km, poi_type)
    
    def plan_route(
        self,
        start: Dict[str, float],
        waypoints: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """规划路线（简化版）"""
        total_distance = 0
        total_time = 0
        segments = []
        
        prev = start
        for wp in waypoints:
            loc_prev = Location("", "", prev["latitude"], prev["longitude"])
            loc_wp = Location("", "", wp["latitude"], wp["longitude"])
            
            dist = self.api.calculate_distance(loc_prev, loc_wp)
            time = self.api.calculate_travel_time(loc_prev, loc_wp)
            
            total_distance += dist
            total_time += time
            
            segments.append({
                "from": prev.get("name", "起点"),
                "to": wp.get("name", "目的地"),
                "distance_km": dist,
                "time_minutes": time
            })
            
            prev = wp
        
        return {
            "total_distance_km": round(total_distance, 1),
            "total_time_minutes": total_time,
            "segments": segments
        }
