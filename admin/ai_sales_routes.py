"""
Rutas API para el Sistema de Ventas con IA
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database.connection import get_db
from database.models import Conversation, Product, Order
from ai.context_manager import context_manager
from agents.professional_sales_agent import professional_sales_agent
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter(prefix="/admin/ai-sales", tags=["ai-sales"])

@router.get("/stats")
async def get_ai_sales_stats(db: Session = Depends(get_db)):
    """Obtiene estadísticas del sistema de ventas IA"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)
    
    # Conversaciones activas
    active_conversations = len(context_manager.contexts)
    
    # Conversaciones por etapa
    stages_count = {}
    for phone, ctx in professional_sales_agent.sales_contexts.items():
        stage = ctx.stage.value
        stages_count[stage] = stages_count.get(stage, 0) + 1
    
    # Señales de compra detectadas
    total_buying_signals = sum(
        ctx.buying_signals 
        for ctx in professional_sales_agent.sales_contexts.values()
    )
    
    # Conversiones esta semana
    conversions = db.query(Order).filter(
        Order.created_at >= week_ago
    ).count()
    
    # Tasa de conversión
    total_conversations = db.query(Conversation).filter(
        Conversation.created_at >= week_ago
    ).count()
    
    conversion_rate = (conversions / total_conversations * 100) if total_conversations > 0 else 0
    
    return {
        "active_conversations": active_conversations,
        "stages": stages_count,
        "buying_signals": total_buying_signals,
        "conversions_week": conversions,
        "conversion_rate": round(conversion_rate, 2),
        "total_conversations_week": total_conversations
    }

@router.get("/conversations")
async def get_active_conversations(db: Session = Depends(get_db)):
    """Obtiene conversaciones activas con su etapa"""
    conversations = []
    
    for phone, sales_ctx in professional_sales_agent.sales_contexts.items():
        # Obtener última conversación
        last_conv = db.query(Conversation).filter(
            Conversation.user_phone == phone
        ).order_by(desc(Conversation.created_at)).first()
        
        if last_conv:
            conversations.append({
                "phone": phone,
                "stage": sales_ctx.stage.value,
                "intent": sales_ctx.customer_intent.value,
                "buying_signals": sales_ctx.buying_signals,
                "urgency": sales_ctx.urgency_level,
                "trust": sales_ctx.trust_level,
                "mentioned_products": sales_ctx.mentioned_products,
                "objections": sales_ctx.objections,
                "last_message": last_conv.message,
                "last_response": last_conv.response,
                "last_interaction": last_conv.created_at.isoformat()
            })
    
    return conversations

@router.get("/products/recommended")
async def get_recommended_products(db: Session = Depends(get_db)):
    """Obtiene productos más recomendados por la IA"""
    # Productos más mencionados en conversaciones
    mentioned_products = []
    for sales_ctx in professional_sales_agent.sales_contexts.values():
        mentioned_products.extend(sales_ctx.mentioned_products)
    
    # Contar frecuencia
    from collections import Counter
    product_counts = Counter(mentioned_products)
    
    # Obtener productos de la BD
    products = []
    for product_name, count in product_counts.most_common(10):
        product = db.query(Product).filter(
            Product.name.ilike(f"%{product_name}%")
        ).first()
        
        if product:
            products.append({
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "mentions": count,
                "stock": product.stock,
                "category": product.category
            })
    
    return products

@router.get("/objections")
async def get_common_objections():
    """Obtiene objeciones más comunes"""
    all_objections = []
    for sales_ctx in professional_sales_agent.sales_contexts.values():
        all_objections.extend(sales_ctx.objections)
    
    from collections import Counter
    objection_counts = Counter(all_objections)
    
    return [
        {"type": obj, "count": count}
        for obj, count in objection_counts.most_common(10)
    ]

@router.post("/config")
async def update_config(config: Dict):
    """Actualiza configuración del sistema de ventas IA"""
    # Aquí puedes agregar lógica para actualizar configuración
    # Por ahora solo retorna éxito
    return {"success": True, "config": config}

@router.get("/performance")
async def get_performance_metrics(db: Session = Depends(get_db)):
    """Obtiene métricas de rendimiento del sistema"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Métricas por etapa
    stage_metrics = {}
    for stage in ["greeting", "rapport", "discovery", "presentation", "objections", "closing"]:
        conversations_in_stage = sum(
            1 for ctx in professional_sales_agent.sales_contexts.values()
            if ctx.stage.value == stage
        )
        stage_metrics[stage] = conversations_in_stage
    
    # Tiempo promedio hasta cierre
    closed_orders = db.query(Order).filter(
        Order.created_at >= today
    ).all()
    
    return {
        "stage_distribution": stage_metrics,
        "closed_today": len(closed_orders),
        "average_urgency": sum(
            ctx.urgency_level 
            for ctx in professional_sales_agent.sales_contexts.values()
        ) / len(professional_sales_agent.sales_contexts) if professional_sales_agent.sales_contexts else 0
    }
