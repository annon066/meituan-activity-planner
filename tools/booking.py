"""工具层 - 预订工具"""
from typing import Dict, Any, List
from mock_api.booking_api import MockBookingAPI, MockDeliveryAPI


class BookingTool:
    """统一预订工具"""
    
    def __init__(self):
        self.booking_api = MockBookingAPI()
        self.delivery_api = MockDeliveryAPI()
        self.name = "booking_tool"
        self.description = """
        统一预订工具，支持餐厅预订、景点预订、外卖配送等。
        """
    
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
        return self.booking_api.create_booking(
            venue_type=venue_type,
            venue_id=venue_id,
            venue_name=venue_name,
            time_slot=time_slot,
            people_count=people_count,
            user_name=user_name,
            phone=phone,
            price=price,
            notes=notes
        )
    
    def create_delivery(
        self,
        items: List[dict],
        delivery_address: str,
        delivery_time: str,
        user_name: str,
        phone: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """创建配送订单（如送蛋糕/鲜花到餐厅）"""
        return self.delivery_api.create_order(
            items=items,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
            user_name=user_name,
            phone=phone,
            notes=notes
        )
    
    def get_booking(self, booking_id: str) -> Dict[str, Any]:
        """获取预订信息"""
        return self.booking_api.get_booking(booking_id)
    
    def cancel_booking(self, booking_id: str) -> Dict[str, Any]:
        """取消预订"""
        return self.booking_api.cancel_booking(booking_id)
    
    def list_user_bookings(self, user_name: str) -> List[Dict[str, Any]]:
        """列出用户所有预订"""
        return self.booking_api.list_bookings(user_name)
    
    def batch_book(self, bookings: List[Dict]) -> Dict[str, Any]:
        """批量预订"""
        results = []
        success_count = 0
        
        for b in bookings:
            result = self.create_booking(**b)
            if result.get("status") == "confirmed":
                success_count += 1
            results.append(result)
        
        return {
            "total": len(bookings),
            "success": success_count,
            "results": results
        }
