from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.connection import get_db
from database.models import *
from ai.context_manager import context_manager
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/stats", tags=["stats"])

@router.get("/overview")
async def get_overview_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas generales del dashboard"""
    try:
        # Conversaciones totales y activas
        total_conversations = db.query(Conversation).count()
        active_conversations = len(context_manager.contexts)
        
        # Productos
        total_products = db.query(Product).count()
        
        # Clientes
        total_customers = db.query(User).count()
        
        # Mensajes
        total_messages = db.query(ChatLog).count()
        
        # Estado de conexión (verificar con Baileys server)
        is_connected = False
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:3002/status", timeout=aiohttp.ClientTimeout(total=2)) as response:
                    if response.status == 200:
                        data = await response.json()
                        is_connected = data.get("success", False) and data.get("status") == "CONNECTED"
        except:
            pass
        
        return {
            "totalConversations": total_conversations,
            "activeConversations": active_conversations,
            "totalProducts": total_products,
            "totalCustomers": total_customers,
            "totalMessages": total_messages,
            "isConnected": is_connected
        }
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return {
            "totalConversations": 0,
            "activeConversations": 0,
            "totalProducts": 0,
            "totalCustomers": 0,
            "totalMessages": 0,
            "isConnected": False
        }

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas detalladas para el dashboard"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Conversaciones activas
    active_conversations = len(context_manager.contexts)
    
    # Pedidos hoy
    orders_today = db.query(Order).filter(Order.created_at >= today).count()
    
    # Ventas hoy
    sales_today = db.query(func.sum(Order.total)).filter(
        Order.created_at >= today,
        Order.status != "cancelled"
    ).scalar() or 0
    
    # Mensajes hoy
    messages_today = db.query(ChatLog).filter(ChatLog.created_at >= today).count()
    
    # Tasa de conversión
    conversations_with_intent = db.query(Conversation).filter(
        Conversation.created_at >= today,
        Conversation.intent == "buy_intent"
    ).count()
    
    conversion_rate = (orders_today / conversations_with_intent * 100) if conversations_with_intent > 0 else 0
    
    return {
        "active_conversations": active_conversations,
        "orders_today": orders_today,
        "sales_today": float(sales_today),
        "messages_today": messages_today,
        "conversion_rate": round(conversion_rate, 2)
    }

@router.get("/sales")
async def get_sales_stats(days: int = 7, db: Session = Depends(get_db)):
    """Obtiene estadísticas de ventas"""
    start_date = datetime.now() - timedelta(days=days)
    
    orders = db.query(Order).filter(
        Order.created_at >= start_date,
        Order.status != "cancelled"
    ).all()
    
    total_sales = sum(order.total for order in orders)
    total_orders = len(orders)
    average_order = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        "total_sales": float(total_sales),
        "total_orders": total_orders,
        "average_order": float(average_order),
        "period_days": days
    }

@router.get("/products/top")
async def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """Obtiene los productos más vendidos"""
    products = db.query(Product).order_by(
        Product.sales_count.desc()
    ).limit(limit).all()
    
    return [{
        "id": p.id,
        "name": p.name,
        "sales_count": p.sales_count,
        "views": p.views,
        "price": p.price,
        "stock": p.stock
    } for p in products]

@router.get("/customers/top")
async def get_top_customers(limit: int = 10, db: Session = Depends(get_db)):
    """Obtiene los mejores clientes"""
    customers = db.query(User).order_by(
        User.total_purchases.desc()
    ).limit(limit).all()
    
    return [{
        "id": c.id,
        "phone": c.phone,
        "name": c.name,
        "total_purchases": c.total_purchases,
        "purchase_count": c.purchase_count
    } for c in customers]
