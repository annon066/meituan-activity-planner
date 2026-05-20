"""Mock 位置服务 API"""
from typing import Optional, List
from models.schemas import Location


class MockLocationAPI:
    """Mock 位置服务 API"""
    
    def __init__(self):
        self._locations = {
            "home": Location(
                name="望京西园四区",
                address="朝阳区望京西园四区",
                latitude=39.98,
                longitude=116.47
            ),
            "work": Location(
                name="百度科技园",
                address="海淀区上地信息路",
                latitude=40.05,
                longitude=116.30
            )
        }
    
    def get_current_location(self) -> Location:
        """获取当前位置（模拟用户在家）"""
        return self._locations["home"]
    
    def geocode(self, address: str) -> Optional[Location]:
        """地址转坐标"""
        # 简化实现
        return Location(
            name=address,
            address=address,
            latitude=39.90,
            longitude=116.40
        )
    
    def reverse_geocode(self, latitude: float, longitude: float) -> str:
        """坐标转地址"""
        return "北京市朝阳区望京西园"
    
    def calculate_distance(self, loc1: Location, loc2: Location) -> float:
        """计算两点间距离（公里）"""
        # 简化实现，使用欧几里得距离近似
        import math
        lat_diff = (loc1.latitude - loc2.latitude) * 111  # 1度纬度约111km
        lon_diff = (loc1.longitude - loc2.longitude) * 111 * math.cos(math.radians(loc1.latitude))
        return round(math.sqrt(lat_diff**2 + lon_diff**2), 1)
    
    def calculate_travel_time(self, loc1: Location, loc2: Location, mode: str = "driving") -> int:
        """计算出行时间（分钟）"""
        distance = self.calculate_distance(loc1, loc2)
        
        if mode == "driving":
            # 假设平均速度30km/h（考虑城市交通）
            return int(distance / 30 * 60) + 10  # +10分钟缓冲
        elif mode == "transit":
            return int(distance / 20 * 60) + 15
        elif mode == "walking":
            return int(distance / 5 * 60)
        
        return int(distance * 5)
    
    def search_nearby(
        self,
        center: Location,
        radius_km: float,
        poi_type: str
    ) -> List[dict]:
        """搜索附近POI"""
        # 返回模拟数据
        return [
            {"name": "朝阳大悦城", "distance": 3.5, "type": "shopping"},
            {"name": "望京SOHO", "distance": 2.0, "type": "office"},
            {"name": "望京公园", "distance": 1.5, "type": "park"},
        ]
