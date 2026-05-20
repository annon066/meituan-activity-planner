"""工具函数"""
from datetime import datetime


def format_time(time_str: str) -> str:
    """格式化时间显示"""
    try:
        dt = datetime.strptime(time_str, "%H:%M")
        return dt.strftime("%H:%M")
    except:
        return time_str


def format_price(price: int) -> str:
    """格式化价格显示"""
    if price >= 100:
        return f"¥{price}"
    return f"¥{price}"


def format_distance(distance_km: float) -> str:
    """格式化距离显示"""
    if distance_km < 1:
        return f"{int(distance_km * 1000)}米"
    return f"{distance_km}公里"


def print_separator(char: str = "-", length: int = 50):
    """打印分隔线"""
    print(char * length)
