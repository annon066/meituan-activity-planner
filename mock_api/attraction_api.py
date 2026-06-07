"""Mock 景点/活动 API"""
import random
from typing import List, Optional
from models.schemas import Attraction, Location


class MockAttractionAPI:
    """Mock 景点/活动查询 API"""
    
    def __init__(self):
        self._attractions = self._init_attractions()
    
    def _init_attractions(self) -> List[Attraction]:
        """初始化 Mock 景点数据"""
        return [
            # 亲子类
            Attraction(
                id="a001", name="朝阳公园儿童乐园",
                location=Location(name="朝阳公园", address="朝阳区朝阳公园南路1号", latitude=39.94, longitude=116.47, distance_km=4.0),
                type="亲子乐园", rating=4.6, price=50, duration_minutes=120,
                features=["儿童游乐设施", "户外活动", "亲子互动", "免费停车"],
                opening_hours="09:00-17:00", booking_required=False
            ),
            Attraction(
                id="a002", name="乐高探索中心(蓝色港湾店)",
                location=Location(name="蓝色港湾", address="朝阳区朝阳公园路6号", latitude=39.95, longitude=116.47, distance_km=4.5),
                type="亲子乐园", rating=4.7, price=180, duration_minutes=150,
                features=["室内游乐", "乐高主题", "适合5-10岁", "4D影院"],
                opening_hours="10:00-20:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00"]
            ),
            Attraction(
                id="a003", name="北京海洋馆",
                location=Location(name="动物园", address="海淀区高梁桥斜街乙18号", latitude=39.94, longitude=116.33, distance_km=9.5),
                type="亲子乐园", rating=4.8, price=175, duration_minutes=180,
                features=["海洋生物", "海豚表演", "科普教育", "海底隧道"],
                opening_hours="09:00-17:30", booking_required=True,
                available_slots=["10:00", "13:00", "14:00"]
            ),
            Attraction(
                id="a013", name="蹦床公园(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                type="亲子乐园", rating=4.5, price=88, duration_minutes=90,
                features=["蹦床运动", "亲子同乐", "释放活力", "室内活动"],
                opening_hours="10:00-21:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a014", name="MELAND Club(朝阳大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                type="亲子乐园", rating=4.7, price=198, duration_minutes=180,
                features=["室内游乐场", "多种区域", "适合全年龄段", "家长休息区"],
                opening_hours="10:00-21:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00"]
            ),
            Attraction(
                id="a015", name="北京动物园",
                location=Location(name="动物园", address="海淀区高梁桥斜街乙18号", latitude=39.94, longitude=116.33, distance_km=9.5),
                type="亲子乐园", rating=4.6, price=15, duration_minutes=180,
                features=["各种动物", "熊猫馆", "户外活动", "科普教育"],
                opening_hours="07:30-18:00", booking_required=False
            ),
            Attraction(
                id="a016", name="中国科技馆",
                location=Location(name="奥林匹克公园", address="朝阳区北辰东路5号", latitude=39.99, longitude=116.39, distance_km=7.5),
                type="亲子乐园", rating=4.8, price=40, duration_minutes=180,
                features=["科技展览", "互动体验", "科普教育", "适合各年龄"],
                opening_hours="09:30-17:00", booking_required=True,
                available_slots=["10:00", "13:00", "14:00", "15:00"]
            ),
            Attraction(
                id="a017", name="儿童艺术剧场(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路", latitude=39.93, longitude=116.45, distance_km=6.8),
                type="亲子乐园", rating=4.5, price=128, duration_minutes=90,
                features=["儿童话剧", "互动演出", "教育意义", "室内活动"],
                opening_hours="14:00开场", booking_required=True,
                available_slots=["14:00", "15:30"]
            ),
            # 展览类
            Attraction(
                id="a004", name="今日美术馆-当代艺术展",
                location=Location(name="百子湾", address="朝阳区百子湾路32号", latitude=39.91, longitude=116.48, distance_km=6.0),
                type="展览", rating=4.5, price=80, duration_minutes=90,
                features=["当代艺术", "打卡拍照", "文艺氛围", "小众展览"],
                opening_hours="10:00-18:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00"]
            ),
            Attraction(
                id="a005", name="798艺术区",
                location=Location(name="798", address="朝阳区酒仙桥路2号", latitude=39.98, longitude=116.49, distance_km=7.5),
                type="展览", rating=4.6, price=0, duration_minutes=120,
                features=["艺术园区", "免费开放", "拍照圣地", "文创店铺"],
                opening_hours="全天开放", booking_required=False
            ),
            Attraction(
                id="a006", name="国家博物馆",
                location=Location(name="天安门", address="东城区东长安街16号", latitude=39.90, longitude=116.40, distance_km=9.0),
                type="展览", rating=4.9, price=0, duration_minutes=180,
                features=["历史文化", "免费预约", "国宝展览", "教育意义"],
                opening_hours="09:00-17:00", booking_required=True,
                available_slots=["09:00", "10:00", "13:00", "14:00"]
            ),
            Attraction(
                id="a018", name="尤伦斯当代艺术中心",
                location=Location(name="798", address="朝阳区酒仙桥路2号", latitude=39.98, longitude=116.49, distance_km=7.5),
                type="展览", rating=4.6, price=120, duration_minutes=120,
                features=["当代艺术", "国际展览", "艺术教育", "咖啡厅"],
                opening_hours="10:00-19:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a019", name="故宫博物院",
                location=Location(name="故宫", address="东城区景山前街4号", latitude=39.92, longitude=116.40, distance_km=8.5),
                type="展览", rating=4.9, price=60, duration_minutes=180,
                features=["历史文化", "世界遗产", "古建筑", "文物收藏"],
                opening_hours="08:30-17:00", booking_required=True,
                available_slots=["09:00", "13:00", "14:00"]
            ),
            Attraction(
                id="a020", name="中国国家博物馆",
                location=Location(name="天安门", address="东城区东长安街16号", latitude=39.90, longitude=116.40, distance_km=9.0),
                type="展览", rating=4.9, price=0, duration_minutes=180,
                features=["历史文化", "大型展览", "珍贵文物", "教育意义"],
                opening_hours="09:00-17:00", booking_required=True,
                available_slots=["09:00", "10:00", "13:00", "14:00"]
            ),
            # CityWalk类
            Attraction(
                id="a007", name="三里屯太古里",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=5.5),
                type="citywalk", rating=4.5, price=0, duration_minutes=90,
                features=["购物逛街", "网红打卡", "美食街", "时尚街区"],
                opening_hours="10:00-22:00", booking_required=False
            ),
            Attraction(
                id="a008", name="南锣鼓巷",
                location=Location(name="南锣鼓巷", address="东城区南锣鼓巷", latitude=39.94, longitude=116.40, distance_km=7.5),
                type="citywalk", rating=4.3, price=0, duration_minutes=90,
                features=["老北京胡同", "小吃街", "文创店铺", "历史街区"],
                opening_hours="全天开放", booking_required=False
            ),
            Attraction(
                id="a021", name="蓝色港湾",
                location=Location(name="蓝色港湾", address="朝阳区朝阳公园路6号", latitude=39.95, longitude=116.47, distance_km=4.5),
                type="citywalk", rating=4.5, price=0, duration_minutes=120,
                features=["购物中心", "湖边散步", "美食广场", "周末市集"],
                opening_hours="10:00-22:00", booking_required=False
            ),
            Attraction(
                id="a022", name="什刹海",
                location=Location(name="什刹海", address="西城区什刹海", latitude=39.94, longitude=116.38, distance_km=8.0),
                type="citywalk", rating=4.4, price=0, duration_minutes=120,
                features=["湖边散步", "古建筑", "酒吧街", "文化街区"],
                opening_hours="全天开放", booking_required=False
            ),
            Attraction(
                id="a023", name="前门大街",
                location=Location(name="前门", address="东城区前门大街", latitude=39.90, longitude=116.40, distance_km=8.5),
                type="citywalk", rating=4.3, price=0, duration_minutes=90,
                features=["商业步行街", "老字号", "特色小吃", "文化街区"],
                opening_hours="10:00-22:00", booking_required=False
            ),
            Attraction(
                id="a024", name="簋街",
                location=Location(name="簋街", address="东城区东直门内大街", latitude=39.95, longitude=116.43, distance_km=6.0),
                type="citywalk", rating=4.4, price=0, duration_minutes=90,
                features=["美食街", "夜生活", "小吃聚集", "热闹氛围"],
                opening_hours="18:00-04:00", booking_required=False
            ),
            # 电影/演出类
            Attraction(
                id="a009", name="博纳国际影城(悠唐店)",
                location=Location(name="悠唐购物中心", address="朝阳区朝阳门外大街悠唐购物中心", latitude=39.92, longitude=116.44, distance_km=5.0),
                type="电影", rating=4.4, price=60, duration_minutes=120,
                features=["最新上映", "IMAX厅", "情侣座", "杜比全景声"],
                opening_hours="09:00-24:00", booking_required=True,
                available_slots=["14:30", "17:00", "19:30", "21:00"]
            ),
            Attraction(
                id="a010", name="蜂巢剧场",
                location=Location(name="东直门", address="东城区东直门外新中街3号", latitude=39.95, longitude=116.44, distance_km=6.0),
                type="话剧", rating=4.7, price=280, duration_minutes=150,
                features=["先锋话剧", "孟京辉作品", "文艺青年必去", "小剧场"],
                opening_hours="19:30开场", booking_required=True,
                available_slots=["19:30"]
            ),
            Attraction(
                id="a025", name="开心麻花剧场(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                type="话剧", rating=4.6, price=260, duration_minutes=120,
                features=["喜剧话剧", "轻松搞笑", "适合聚会", "互动体验"],
                opening_hours="19:30开场", booking_required=True,
                available_slots=["19:30"]
            ),
            Attraction(
                id="a026", name="中国国家大剧院",
                location=Location(name="天安门广场", address="西城区西长安街2号", latitude=39.90, longitude=116.39, distance_km=9.0),
                type="演出", rating=4.8, price=380, duration_minutes=150,
                features=["音乐剧", "歌剧", "芭蕾舞", "世界级演出"],
                opening_hours="14:00/19:30开场", booking_required=True,
                available_slots=["14:00", "19:30"]
            ),
            Attraction(
                id="a027", name="德云社(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路", latitude=39.93, longitude=116.45, distance_km=6.8),
                type="演出", rating=4.5, price=198, duration_minutes=120,
                features=["相声表演", "传统文化", "搞笑", "老少皆宜"],
                opening_hours="19:30开场", booking_required=True,
                available_slots=["19:30"]
            ),
            Attraction(
                id="a028", name="百老汇影城(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                type="电影", rating=4.5, price=65, duration_minutes=120,
                features=["最新上映", "杜比厅", "IMAX", "4DX厅"],
                opening_hours="09:00-24:00", booking_required=True,
                available_slots=["14:00", "17:00", "19:30", "21:00"]
            ),
            # 活动体验类
            Attraction(
                id="a011", name="超级猩猩健身(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路", latitude=39.93, longitude=116.45, distance_km=5.5),
                type="健身", rating=4.8, price=69, duration_minutes=60,
                features=["团课", "减脂塑形", "专业教练", "无推销"],
                opening_hours="07:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a012", name="密室逃脱(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                type="密室", rating=4.5, price=168, duration_minutes=90,
                features=["沉浸体验", "团队协作", "烧脑解谜", "剧情精彩"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "16:00", "18:00", "20:00"]
            ),
            Attraction(
                id="a029", name="剧本杀(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                type="密室", rating=4.6, price=188, duration_minutes=180,
                features=["角色扮演", "推理破案", "沉浸体验", "适合聚会"],
                opening_hours="14:00开场", booking_required=True,
                available_slots=["14:00", "16:00", "18:00"]
            ),
            Attraction(
                id="a030", name="KTV(欢唱KTV)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                type="娱乐", rating=4.3, price=88, duration_minutes=180,
                features=["唱歌", "聚会", "包间", "小食饮料"],
                opening_hours="12:00-02:00", booking_required=True,
                available_slots=["14:00", "16:00", "18:00", "20:00"]
            ),
            Attraction(
                id="a031", name="VR体验馆(三里屯店)",
                location=Location(name="三里屯", address="朝阳区三里屯路19号", latitude=39.93, longitude=116.45, distance_km=6.8),
                type="娱乐", rating=4.4, price=98, duration_minutes=60,
                features=["VR游戏", "沉浸式体验", "科技感", "多人互动"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a032", name="射箭馆(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                type="娱乐", rating=4.5, price=78, duration_minutes=60,
                features=["射箭运动", "释放压力", "专业指导", "适合新手"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a033", name="保龄球馆(望京店)",
                location=Location(name="望京SOHO", address="朝阳区望京街10号", latitude=39.99, longitude=116.48, distance_km=5.2),
                type="娱乐", rating=4.4, price=68, duration_minutes=90,
                features=["保龄球", "休闲运动", "适合聚会", "室内活动"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a034", name="台球厅(朝阳大悦城店)",
                location=Location(name="朝阳大悦城", address="朝阳区朝阳北路101号", latitude=39.92, longitude=116.46, distance_km=3.5),
                type="娱乐", rating=4.3, price=55, duration_minutes=90,
                features=["台球", "休闲", "适合小聚", "室内活动"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            # 自然风光类
            Attraction(
                id="a035", name="奥林匹克森林公园",
                location=Location(name="奥林匹克公园", address="朝阳区科荟路33号", latitude=40.01, longitude=116.39, distance_km=8.0),
                type="自然风光", rating=4.7, price=0, duration_minutes=180,
                features=["户外跑步", "骑自行车", "野餐", "亲子活动"],
                opening_hours="06:00-21:00", booking_required=False
            ),
            Attraction(
                id="a036", name="北海公园",
                location=Location(name="北海公园", address="西城区文津街1号", latitude=39.92, longitude=116.38, distance_km=7.5),
                type="自然风光", rating=4.6, price=10, duration_minutes=120,
                features=["古建筑", "划船", "历史公园", "湖景"],
                opening_hours="06:00-21:00", booking_required=False
            ),
            Attraction(
                id="a037", name="颐和园",
                location=Location(name="颐和园", address="海淀区新建宫门路19号", latitude=40.00, longitude=116.27, distance_km=15.0),
                type="自然风光", rating=4.8, price=30, duration_minutes=240,
                features=["皇家园林", "历史遗迹", "湖光山色", "世界遗产"],
                opening_hours="06:30-18:00", booking_required=True,
                available_slots=["09:00", "13:00"]
            ),
            # 运动休闲类
            Attraction(
                id="a038", name="滑雪场(乔波滑雪馆)",
                location=Location(name="顺义", address="顺义区顺安路6号", latitude=40.13, longitude=116.65, distance_km=25.0),
                type="运动", rating=4.5, price=268, duration_minutes=180,
                features=["室内滑雪", "四季滑雪", "适合新手", "教练指导"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "16:00", "18:00"]
            ),
            Attraction(
                id="a039", name="攀岩馆(合生汇店)",
                location=Location(name="合生汇", address="朝阳区西大望路合生汇", latitude=39.91, longitude=116.47, distance_km=6.0),
                type="运动", rating=4.6, price=98, duration_minutes=90,
                features=["室内攀岩", "挑战自我", "专业装备", "适合新手"],
                opening_hours="10:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
            Attraction(
                id="a040", name="游泳馆(朝阳体育中心)",
                location=Location(name="朝阳体育中心", address="朝阳区姚家园路", latitude=39.93, longitude=116.51, distance_km=6.5),
                type="运动", rating=4.5, price=48, duration_minutes=90,
                features=["室内泳池", "恒温泳池", "专业泳池", "亲子游泳"],
                opening_hours="06:00-22:00", booking_required=True,
                available_slots=["14:00", "15:00", "16:00", "17:00"]
            ),
        ]
    
    def search_attractions(
        self,
        attraction_type: Optional[str] = None,
        features: Optional[List[str]] = None,
        max_distance_km: Optional[float] = None,
        min_rating: Optional[float] = None,
        price_range: Optional[tuple] = None,
        duration_max: Optional[int] = None,
        limit: int = 5
    ) -> List[Attraction]:
        """搜索景点/活动"""
        results = self._attractions.copy()
        
        if attraction_type:
            results = [a for a in results if attraction_type in a.type]
        
        if min_rating:
            results = [a for a in results if a.rating >= min_rating]
        
        if max_distance_km:
            results = [a for a in results if a.location.distance_km and a.location.distance_km <= max_distance_km]
        
        if features:
            results = [a for a in results if any(f in a.features for f in features)]
        
        if price_range:
            results = [a for a in results if price_range[0] <= a.price <= price_range[1]]
        
        if duration_max:
            results = [a for a in results if a.duration_minutes <= duration_max]
        
        # 按距离排序
        results.sort(key=lambda x: x.location.distance_km or 999)
        
        return results[:limit]
    
    def get_attraction(self, attraction_id: str) -> Optional[Attraction]:
        """获取景点详情"""
        for a in self._attractions:
            if a.id == attraction_id:
                return a
        return None
    
    def check_availability(self, attraction_id: str, time_slot: str) -> dict:
        """检查景点可用性"""
        attraction = self.get_attraction(attraction_id)
        if not attraction:
            return {"available": False, "message": "景点不存在"}
        
        if not attraction.booking_required:
            return {"available": True, "message": "无需预约，可直接前往"}
        
        if time_slot in attraction.available_slots:
            return {"available": True, "message": f"{time_slot}时段可预约"}
        
        return {
            "available": False,
            "message": f"{time_slot}时段不可预约",
            "available_slots": attraction.available_slots
        }
    
    def book_attraction(
        self,
        attraction_id: str,
        time_slot: str,
        people_count: int,
        user_name: str,
        phone: str
    ) -> dict:
        """预订景点/活动"""
        attraction = self.get_attraction(attraction_id)
        if not attraction:
            return {"success": False, "message": "景点不存在"}
        
        if attraction.booking_required and time_slot not in attraction.available_slots:
            return {"success": False, "message": "该时段不可预订"}
        
        booking_id = f"AT{random.randint(100000, 999999)}"
        return {
            "success": True,
            "booking_id": booking_id,
            "attraction_name": attraction.name,
            "address": attraction.location.address,
            "time": time_slot,
            "people_count": people_count,
            "total_price": attraction.price * people_count,
            "message": "预订成功！请准时到达"
        }
