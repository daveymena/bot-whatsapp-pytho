from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from integrations.mercadopago_integration import mercadopago_integration
from integrations.paypal_integration import paypal_integration
from database.connection import SessionLocal
from database.models import Order
from datetime import datetime
import uuid

router = APIRouter(prefix="/shop", tags=["shop"])

class ProductItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

class PaymentRequest(BaseModel):
    products: List[ProductItem]
    total: float

class OrderRequest(BaseModel):
    name: str
    phone: str
    email: str = ""
    address: str
    notes: str = ""
    products: List[ProductItem]
    total: float
    payment_method: str

@router.post("/payment/create-mercadopago")
async def create_mercadopago_payment(request: PaymentRequest):
    """Crea un link de pago de Mercado Pago desde la tienda"""
    try:
        # Generar número de orden
        order_number = f"SHOP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        order_data = {
            'order_number': order_number,
            'products': [p.dict() for p in request.products],
            'total': request.total
        }
        
        result = mercadopago_integration.create_payment_link(order_data)
        
        if result["success"]:
            return {
                "success": True,
                "init_point": result["init_point"],
                "order_number": order_number
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Error al crear pago"))
            
    except Exception as e:
        print(f"❌ Error en Mercado Pago: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/payment/create-paypal")
async def create_paypal_payment(request: PaymentRequest):
    """Crea un link de pago de PayPal desde la tienda"""
    try:
        # Generar número de orden
        order_number = f"SHOP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        order_data = {
            'order_number': order_number,
            'products': [p.dict() for p in request.products],
            'total': request.total
        }
        
        result = paypal_integration.create_payment_link(order_data)
        
        if result["success"]:
            return {
                "success": True,
                "approval_url": result["approval_url"],
                "order_number": order_number
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Error al crear pago"))
            
    except Exception as e:
        print(f"❌ Error en PayPal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders")
async def create_order(request: OrderRequest):
    """Crea una orden desde la tienda (contra entrega o WhatsApp)"""
    try:
        db = SessionLocal()
        
        # Generar número de orden
        order_number = f"SHOP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        order_id = uuid.uuid4().hex[:24]
        
        # Crear orden
        order = Order(
            id=order_id,
            order_number=order_number,
            user_phone=request.phone,
            user_name=request.name,
            products=[p.dict() for p in request.products],
            subtotal=request.total,
            shipping=0,
            discount=0,
            total=request.total,
            status="pending" if request.payment_method == "contraentrega" else "confirmed",
            payment_method=request.payment_method,
            delivery_address=request.address,
            notes=request.notes
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        db.close()
        
        # TODO: Enviar notificación por WhatsApp al cliente y al admin
        
        return {
            "success": True,
            "order_number": order_number,
            "message": "Pedido creado exitosamente. Te contactaremos pronto por WhatsApp."
        }
        
    except Exception as e:
        print(f"❌ Error creando orden: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products")
async def get_shop_products():
    """Obtiene productos para la tienda pública"""
    from admin.products_routes import get_products
    return await get_products()

@router.get("/products/{product_id}")
async def get_shop_product(product_id: int):
    """Obtiene un producto específico para la tienda"""
    from admin.products_routes import get_product
    return await get_product(product_id)
