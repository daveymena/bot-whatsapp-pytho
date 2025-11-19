from sqlalchemy.orm import Session
from database.models import Order
from typing import List, Optional
from datetime import datetime

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: dict) -> Order:
        order = Order(**order_data)
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def get_orders_by_phone(db: Session, phone: str) -> List[Order]:
        return db.query(Order).filter(Order.user_phone == phone).all()
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            db.refresh(order)
        return order
    
    @staticmethod
    def get_pending_orders(db: Session) -> List[Order]:
        return db.query(Order).filter(Order.status == "pending").all()
    
    @staticmethod
    def calculate_order_total(products: List[dict]) -> float:
        total = 0
        for item in products:
            total += item.get("price", 0) * item.get("quantity", 1)
        return total
