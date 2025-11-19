from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database.connection import get_db
from database.models import *
from ai.context_manager import context_manager
from datetime import datetime, timedelta
from typing import List, Dict
import os

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Panel de administración principal"""
    template_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas del bot"""
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

@router.get("/whatsapp/status")
async def get_whatsapp_status():
    """Obtiene el estado de la conexión de WhatsApp"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:3002/status", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
    except Exception as e:
        print(f"Error obteniendo estado de WhatsApp: {e}")
    
    return {
        "success": False,
        "status": "DISCONNECTED",
        "connection": {
            "phoneNumber": None,
            "lastConnectedAt": None,
            "isActive": False
        },
        "qrCode": None
    }

@router.post("/whatsapp/disconnect")
async def disconnect_whatsapp():
    """Desconecta WhatsApp"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:3002/disconnect", timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.json()
        return {"success": False, "error": "No se pudo desconectar"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/reconnect")
async def reconnect_whatsapp():
    """Reconecta WhatsApp"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("http://localhost:3002/reconnect", timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.json()
        return {"success": False, "error": "No se pudo reconectar"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
async def get_products(db: Session = Depends(get_db)):
    """Obtiene todos los productos"""
    products = db.query(Product).all()
    
    return [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "category": p.category,
        "stock": p.stock,
        "image_url": p.image_url,
        "is_digital": p.is_digital,
        "is_dropshipping": p.is_dropshipping,
        "views": p.views,
        "sales_count": p.sales_count
    } for p in products]

@router.get("/customers")
async def get_customers(db: Session = Depends(get_db)):
    """Obtiene todos los clientes"""
    customers = db.query(User).all()
    
    return [{
        "id": c.id,
        "phone": c.phone,
        "name": c.name,
        "email": c.email,
        "total_purchases": c.total_purchases,
        "purchase_count": c.purchase_count,
        "last_interaction": c.last_interaction.isoformat() if c.last_interaction else None
    } for c in customers]

@router.get("/conversations/recent")
async def get_recent_conversations(limit: int = 20, db: Session = Depends(get_db)):
    """Obtiene las conversaciones más recientes"""
    conversations = db.query(Conversation).order_by(
        desc(Conversation.created_at)
    ).limit(limit).all()
    
    return [{
        "phone": conv.user_phone,
        "message": conv.message,
        "response": conv.response,
        "intent": conv.intent,
        "sentiment": conv.sentiment,
        "agent_type": conv.agent_type,
        "is_human": conv.is_human,
        "created_at": conv.created_at.isoformat()
    } for conv in conversations]

@router.get("/orders/recent")
async def get_recent_orders(limit: int = 20, db: Session = Depends(get_db)):
    """Obtiene los pedidos más recientes"""
    orders = db.query(Order).order_by(desc(Order.created_at)).limit(limit).all()
    
    return [{
        "order_number": order.order_number,
        "user_phone": order.user_phone,
        "user_name": order.user_name,
        "total": order.total,
        "status": order.status,
        "payment_method": order.payment_method,
        "created_at": order.created_at.isoformat()
    } for order in orders]


@router.post("/products")
async def create_product(product_data: dict, db: Session = Depends(get_db)):
    """Crea un nuevo producto"""
    try:
        product = Product(
            name=product_data.get("name"),
            description=product_data.get("description"),
            price=product_data.get("price"),
            stock=product_data.get("stock", 0),
            category=product_data.get("category"),
            warranty=product_data.get("warranty"),
            image_url=product_data.get("image_url"),
            is_digital=product_data.get("is_digital", False),
            is_dropshipping=product_data.get("is_dropshipping", False)
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return {"success": True, "product_id": product.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/products/{product_id}")
async def update_product(product_id: int, product_data: dict, db: Session = Depends(get_db)):
    """Actualiza un producto"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        for key, value in product_data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.commit()
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Elimina un producto"""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        db.delete(product)
        db.commit()
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products/import")
async def import_products(data: dict, db: Session = Depends(get_db)):
    """Importa múltiples productos"""
    try:
        products_data = data.get("products", [])
        imported = 0
        
        for product_data in products_data:
            product = Product(
                name=product_data.get("name"),
                description=product_data.get("description"),
                price=product_data.get("price"),
                stock=product_data.get("stock", 0),
                category=product_data.get("category"),
                warranty=product_data.get("warranty"),
                image_url=product_data.get("image_url"),
                is_digital=product_data.get("is_digital", False),
                is_dropshipping=product_data.get("is_dropshipping", False)
            )
            
            db.add(product)
            imported += 1
        
        db.commit()
        
        return {"success": True, "imported": imported}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
