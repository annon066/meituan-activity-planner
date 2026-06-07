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
                features=["亲子友好", "有儿童座椅", "环境宽敞", "儿童餐"],
                available_times=["12:00", "12:30", "17:30", "18:00", "18:30"],
                queue_length=12, has_private_room=True, children_facilities=True
            ),
            Restaurant(
                id="r002", name="海底捞(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.7, price_per_person=120, cuisine_type="火锅",
                features=["亲子友好", "美甲服务", "儿童游乐区", "儿童套餐"],
                available_times=["11:00", "14:00", "17:00", "20:00"],
                queue_length=25, has_private_room=True, children_facilities=True
            ),
            Restaurant(
                id="r013", name="棒约翰(大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.4, price_per_person=55, cuisine_type="披萨",
                features=["亲子友好", "儿童套餐", "DIY披萨"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00"],
                queue_length=8, has_private_room=False, children_facilities=True
            ),
            Restaurant(
                id="r014", name="必胜客(荟聚店)",
                location=Location(name="荟聚中心", address="大兴区欣雅街", latitude=39.79, longitude=116.33, distance_km=12.0),
                rating=4.3, price_per_person=68, cuisine_type="西餐",
                features=["亲子友好", "儿童套餐", "生日派对"],
                available_times=["11:00", "12:30", "17:30", "18:30"],
                queue_length=15, has_private_room=True, children_facilities=True
            ),
            # 轻食/减肥友好餐厅
            Restaurant(
                id="r003", name="Wagas(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=75, cuisine_type="西式轻食",
                features=["低卡轻食", "健康沙拉", "果汁饮品", "素食"],
                available_times=["11:30", "12:00", "18:00", "19:00"],
                queue_length=3, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r004", name="新元素(国贸店)",
                location=Location(name="国贸", address="朝阳区建国门外大街1号", latitude=39.91, longitude=116.46, distance_km=7.1),
                rating=4.6, price_per_person=95, cuisine_type="健康轻食",
                features=["低卡轻食", "有机食材", "适合减肥", "冷压果汁"],
                available_times=["11:00", "12:30", "18:30"],
                queue_length=5, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r015", name="Pure Wholefoods(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=88, cuisine_type="轻食",
                features=["有机食材", "无麸质", "低碳水", "植物蛋白"],
                available_times=["11:00", "12:00", "14:00", "18:00"],
                queue_length=4, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r016", name="SHAKE SHACK(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.4, price_per_person=72, cuisine_type="美式汉堡",
                features=["低卡轻食", "无激素牛肉", "新鲜食材"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00", "19:00"],
                queue_length=10, has_private_room=False, children_facilities=False
            ),
            # 聚会餐厅
            Restaurant(
                id="r005", name="胡桃里音乐酒馆(工体店)",
                location=Location(name="工人体育场", address="朝阳区工体北路", latitude=39.93, longitude=116.45, distance_km=5.5),
                rating=4.4, price_per_person=150, cuisine_type="创意菜",
                features=["聚会推荐", "现场音乐", "氛围感强", "小酌"],
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
            Restaurant(
                id="r017", name="湊湊火锅(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=145, cuisine_type="火锅",
                features=["聚会推荐", "台式火锅", "奶茶配火锅"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=20, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r018", name="丰茂烤串(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.6, price_per_person=110, cuisine_type="烤串",
                features=["聚会推荐", "自烤自吃", "现穿现烤"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=12, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r019", name="哥老官美蛙鱼头(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                rating=4.7, price_per_person=135, cuisine_type="火锅",
                features=["聚会推荐", "美蛙鱼头", "网红店"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=30, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r020", name="喜家德虾仁水饺(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.5, price_per_person=45, cuisine_type="东北菜",
                features=["聚会推荐", "虾仁水饺", "现包现煮"],
                available_times=["11:00", "12:00", "17:00", "18:00"],
                queue_length=8, has_private_room=True, children_facilities=False
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
            # 粤菜/茶餐厅
            Restaurant(
                id="r021", name="点都德(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=95, cuisine_type="粤菜",
                features=["早茶晚茶", "亲子友好", "传统点心"],
                available_times=["11:00", "14:00", "17:00", "18:00"],
                queue_length=10, has_private_room=True, children_facilities=True
            ),
            Restaurant(
                id="r022", name="翠华餐厅(国贸店)",
                location=Location(name="国贸", address="朝阳区建国门外大街1号", latitude=39.91, longitude=116.46, distance_km=7.1),
                rating=4.4, price_per_person=82, cuisine_type="港式茶餐厅",
                features=["港式风味", "奶茶冰沙", "菠萝包"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00"],
                queue_length=12, has_private_room=False, children_facilities=True
            ),
            # 日韩料理
            Restaurant(
                id="r023", name="将太无二(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.6, price_per_person=135, cuisine_type="日式料理",
                features=["创意寿司", "刺身拼盘", "日式装修"],
                available_times=["11:30", "12:30", "17:30", "18:30"],
                queue_length=8, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r024", name="姜太公烤肉(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.5, price_per_person=118, cuisine_type="韩式烤肉",
                features=["韩式烤肉", "泡菜无限", "小菜丰富"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=15, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r025", name="权金城烤肉(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                rating=4.4, price_per_person=108, cuisine_type="韩式烤肉",
                features=["聚会推荐", "韩式烤肉", "免费小菜"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=18, has_private_room=True, children_facilities=False
            ),
            # 西餐/特色菜
            Restaurant(
                id="r026", name="蓝蛙(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=128, cuisine_type="美式西餐",
                features=["汉堡薯条", "鸡尾酒", "氛围好"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00", "20:00"],
                queue_length=6, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r027", name="莫莉幻想(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                rating=4.4, price_per_person=115, cuisine_type="美式西餐",
                features=["亲子友好", "儿童游乐", "儿童菜单"],
                available_times=["11:00", "12:00", "17:00", "18:00"],
                queue_length=10, has_private_room=False, children_facilities=True
            ),
            # 火锅系列
            Restaurant(
                id="r028", name="巴奴毛肚火锅(国贸店)",
                location=Location(name="国贸", address="朝阳区建国门外大街1号", latitude=39.91, longitude=116.46, distance_km=7.1),
                rating=4.7, price_per_person=145, cuisine_type="火锅",
                features=["毛肚招牌", "菌汤锅底", "服务好"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=22, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r029", name="小龙坎老火锅(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=125, cuisine_type="川味火锅",
                features=["川味火锅", "正宗", "辣度可选"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=25, has_private_room=True, children_facilities=False
            ),
            Restaurant(
                id="r030", name="半天妖青花椒烤鱼(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                rating=4.4, price_per_person=95, cuisine_type="烤鱼",
                features=["聚会推荐", "烤鱼", "青花椒"],
                available_times=["17:00", "18:00", "19:00", "20:00"],
                queue_length=18, has_private_room=True, children_facilities=False
            ),
            # 面食类
            Restaurant(
                id="r031", name="九毛九(大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.5, price_per_person=55, cuisine_type="山西面食",
                features=["亲子友好", "手工面", "性价比高"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00"],
                queue_length=15, has_private_room=False, children_facilities=True
            ),
            Restaurant(
                id="r032", name="和府捞面(国贸店)",
                location=Location(name="国贸", address="朝阳区建国门外大街1号", latitude=39.91, longitude=116.46, distance_km=7.1),
                rating=4.4, price_per_person=48, cuisine_type="苏式面",
                features=["书店面馆", "安静", "汤面"],
                available_times=["11:00", "12:00", "14:00", "17:00", "18:00"],
                queue_length=8, has_private_room=False, children_facilities=False
            ),
            # 甜品/下午茶
            Restaurant(
                id="r033", name="Lady M(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.7, price_per_person=65, cuisine_type="甜品",
                features=["网红蛋糕", "下午茶", "拍照打卡"],
                available_times=["14:00", "15:00", "16:00"],
                queue_length=20, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r034", name="喜茶(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                rating=4.5, price_per_person=35, cuisine_type="奶茶",
                features=["网红奶茶", "芝士茶", "多肉葡萄"],
                available_times=["14:00", "15:00", "16:00", "17:00"],
                queue_length=30, has_private_room=False, children_facilities=False
            ),
            Restaurant(
                id="r035", name="奈雪的茶(大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.4, price_per_person=38, cuisine_type="奶茶",
                features=["茶饮软欧包", "网红店", "亲子友好"],
                available_times=["14:00", "15:00", "16:00", "17:00"],
                queue_length=25, has_private_room=False, children_facilities=True
            ),
            Restaurant(
                id="r036", name="DQ冰雪皇后(大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                rating=4.3, price_per_person=28, cuisine_type="冰淇淋",
                features=["冰淇淋", "亲子友好", "甜点"],
                available_times=["14:00", "15:00", "16:00", "17:00", "18:00"],
                queue_length=10, has_private_room=False, children_facilities=True
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
