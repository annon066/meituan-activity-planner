"""工具层 - 规划辅助工具"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class PlanningTool:
    """规划辅助工具"""

    def __init__(self):
        self.name = "planning_tool"
        self.description = """
        规划辅助工具，提供时间分配、方案优化、冲突检测等功能。
        """

    def allocate_time(
        self,
        start_time: str,
        end_time: str,
        activities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """分配时间段，餐厅活动自动对齐可用时段"""
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        total_minutes = int((end - start).total_seconds() / 60)

        total_needed = sum(a.get("duration_minutes", 60) for a in activities)

        if total_needed > total_minutes:
            scale = total_minutes / total_needed
            for a in activities:
                a["duration_minutes"] = int(a.get("duration_minutes", 60) * scale)

        current = start
        allocated = []

        for activity in activities:
            duration = activity.get("duration_minutes", 60)
            activity["start_time"] = current.strftime("%H:%M")
            activity["end_time"] = (current + timedelta(minutes=duration)).strftime("%H:%M")
            allocated.append(activity)
            current += timedelta(minutes=duration)

        # 对餐厅活动对齐到可用时段
        for activity in allocated:
            if activity.get("type") == "restaurant" and activity.get("available_times"):
                snapped = self._snap_to_available_time(
                    activity["start_time"], activity["available_times"]
                )
                if snapped:
                    start_dt = datetime.strptime(snapped, "%H:%M")
                    activity["start_time"] = snapped
                    activity["end_time"] = (start_dt + timedelta(
                        minutes=activity.get("duration_minutes", 90)
                    )).strftime("%H:%M")

        return allocated

    def _snap_to_available_time(self, desired_time: str, available_times: List[str]) -> Optional[str]:
        """找到最近的可用时段（优先选>=期望时间的最近时段）"""
        desired = datetime.strptime(desired_time, "%H:%M")
        candidates = []
        for t in available_times:
            slot = datetime.strptime(t, "%H:%M")
            diff_minutes = (slot - desired).total_seconds() / 60
            candidates.append((t, diff_minutes))

        future_slots = [(t, d) for t, d in candidates if d >= 0]
        if future_slots:
            future_slots.sort(key=lambda x: x[1])
            return future_slots[0][0]

        past_slots = [(t, d) for t, d in candidates if d < 0 and abs(d) <= 60]
        if past_slots:
            past_slots.sort(key=lambda x: abs(x[1]))
            return past_slots[0][0]

        return available_times[0] if available_times else None
    
    def check_conflicts(
        self,
        activities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """检查时间冲突"""
        conflicts = []
        sorted_activities = sorted(activities, key=lambda x: x.get("start_time", ""))
        
        for i in range(len(sorted_activities) - 1):
            current = sorted_activities[i]
            next_activity = sorted_activities[i + 1]
            
            if current.get("end_time", "") > next_activity.get("start_time", ""):
                conflicts.append({
                    "type": "time_overlap",
                    "activity1": current.get("name", "活动1"),
                    "activity2": next_activity.get("name", "活动2"),
                    "message": f"{current.get('name')} 和 {next_activity.get('name')} 时间重叠"
                })
        
        return conflicts
    
    def optimize_order(
        self,
        activities: List[Dict[str, Any]],
        start_location: Dict[str, float] = None
    ) -> List[Dict[str, Any]]:
        """优化活动顺序（简化版：按类型排序）
        
        规则：活动 -> 餐厅（午餐/晚餐）-> 活动
        """
        # 分类
        restaurants = [a for a in activities if a.get("type") == "restaurant"]
        lunch = [a for a in restaurants if "lunch" in a.get("meal_type", "").lower() or a.get("time_preference") == "lunch"]
        dinner = [a for a in restaurants if "dinner" in a.get("meal_type", "").lower() or a.get("time_preference") == "dinner"]
        other_restaurants = [a for a in restaurants if a not in lunch and a not in dinner]
        
        other_activities = [a for a in activities if a.get("type") != "restaurant"]
        
        # 排序：活动 -> 午餐 -> 活动 -> 晚餐
        optimized = []
        mid_point = len(other_activities) // 2
        
        optimized.extend(other_activities[:mid_point])
        optimized.extend(lunch)
        optimized.extend(other_restaurants)
        optimized.extend(other_activities[mid_point:])
        optimized.extend(dinner)
        
        return optimized
    
    def estimate_budget(
        self,
        activities: List[Dict[str, Any]],
        people_count: int
    ) -> Dict[str, Any]:
        """估算预算"""
        total = 0
        breakdown = []
        
        for a in activities:
            price = a.get("price", 0)
            if a.get("type") == "restaurant":
                cost = price * people_count
            else:
                cost = price * people_count
            
            total += cost
            breakdown.append({
                "name": a.get("name", "活动"),
                "per_person": price,
                "total": cost
            })
        
        return {
            "total": total,
            "per_person": total // people_count if people_count > 0 else total,
            "breakdown": breakdown
        }
    
    def generate_summary(
        self,
        activities: List[Dict[str, Any]],
        user_name: str = "您"
    ) -> str:
        """生成方案摘要"""
        lines = [
            f"📅 下午活动方案",
            f"👤 {user_name} 您好，已为您安排以下活动：",
            ""
        ]
        
        for i, a in enumerate(activities, 1):
            emoji = "🍽️" if a.get("type") == "restaurant" else "🎯"
            time_str = f"{a.get('start_time', '')}-{a.get('end_time', '')}"
            lines.append(f"{i}. {emoji} {time_str} | {a.get('name', '活动')}")
        
        return "\n".join(lines)
