"""Mock 预订服务 API"""
import random
from typing import Dict, Any
from datetime import datetime


class MockBookingAPI:
    """Mock 统一预订服务 API"""
    
    def __init__(self):
        self._bookings: Dict[str, Dict] = {}
    
    def create_booking(
        self,
        venue_type: str,
        venue_id: str,
        venue_name: str,
        time_slot: str,
        people_count: int,
        user_name: str,
        phone: str,
        price: int = 0,
        notes: str = ""
    ) -> Dict[str, Any]:
        """创建预订"""
        booking_id = f"BK{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        booking = {
            "booking_id": booking_id,
            "venue_type": venue_type,
            "venue_id": venue_id,
            "venue_name": venue_name,
            "time_slot": time_slot,
            "people_count": people_count,
            "user_name": user_name,
            "phone": phone,
            "price": price,
            "notes": notes,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "qr_code": f"QR{booking_id}"
        }
        
        self._bookings[booking_id] = booking
        return booking
    
    def get_booking(self, booking_id: str) -> Dict[str, Any]:
        """获取预订信息"""
        return self._bookings.get(booking_id, {})
    
    def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """取消预订"""
        if booking_id in self._bookings:
            self._bookings[booking_id]["status"] = "cancelled"
            return {"success": True, "message": "预订已取消"}
        return {"success": False, "message": "预订不存在"}
    
    def list_bookings(self, user_name: str = None) -> list:
        """列出预订"""
        bookings = list(self._bookings.values())
        if user_name:
            bookings = [b for b in bookings if b.get("user_name") == user_name]
        return bookings


class MockDeliveryAPI:
    """Mock 外卖/配送服务 API"""
    
    def __init__(self):
        self._orders: Dict[str, Dict] = {}
    
    def create_order(
        self,
        items: list,
        delivery_address: str,
        delivery_time: str,
        user_name: str,
        phone: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """创建配送订单（如送蛋糕、鲜花到餐厅）"""
        order_id = f"DD{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}"
        
        order = {
            "order_id": order_id,
            "items": items,
            "delivery_address": delivery_address,
            "delivery_time": delivery_time,
            "user_name": user_name,
            "phone": phone,
            "notes": notes,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "estimated_arrival": delivery_time
        }
        
        self._orders[order_id] = order
        return order
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """获取订单信息"""
        return self._orders.get(order_id, {})
    
    def track_order(self, order_id: str) -> Dict[str, Any]:
        """追踪订单"""
        order = self._orders.get(order_id)
        if not order:
            return {"error": "订单不存在"}
        
        return {
            "order_id": order_id,
            "status": order["status"],
            "estimated_arrival": order["estimated_arrival"],
            "rider_name": "张师傅",
            "rider_phone": "138****5678"
        }
