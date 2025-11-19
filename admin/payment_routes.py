from fastapi import APIRouter, Request, HTTPException
from integrations.mercadopago_integration import mercadopago_integration
from integrations.paypal_integration import paypal_integration
from services.payment_service import payment_service
from whatsapp.baileys_client import baileys_client
from database.connection import SessionLocal
from database.models import Order

router = APIRouter(prefix="/payment", tags=["payments"])

@router.post("/webhook/mercadopago")
async def mercadopago_webhook(request: Request):
    """Webhook para notificaciones de Mercado Pago"""
    try:
        data = await request.json()
        result = mercadopago_integration.process_webhook(data)
        
        if result.get("success") and result.get("status") == "approved":
            # Notificar al cliente
            order_number = result.get("external_reference")
            if order_number:
                db = SessionLocal()
                order = db.query(Order).filter(Order.order_number == order_number).first()
                if order:
                    message = f"""✅ *PAGO CONFIRMADO*

Pedido: #{order_number}
Monto: ${result['amount']:,.0f} COP

🎉 ¡Tu pago fue aprobado!

📦 Tu pedido será procesado y enviado en las próximas 24-48 horas.

Gracias por tu compra! 🚀"""
                    
                    await baileys_client.send_message(order.user_phone, message)
                db.close()
        
        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Error en webhook Mercado Pago: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/success")
async def payment_success(request: Request):
    """Página de éxito después del pago"""
    return {
        "status": "success",
        "message": "¡Pago exitoso! Recibirás una confirmación por WhatsApp."
    }

@router.get("/failure")
async def payment_failure(request: Request):
    """Página de fallo en el pago"""
    return {
        "status": "failure",
        "message": "El pago no pudo ser procesado. Por favor intenta nuevamente."
    }

@router.get("/pending")
async def payment_pending(request: Request):
    """Página de pago pendiente"""
    return {
        "status": "pending",
        "message": "Tu pago está siendo procesado. Te notificaremos cuando se confirme."
    }

@router.get("/paypal/success")
async def paypal_success(payment_id: str, PayerID: str):
    """Callback de éxito de PayPal"""
    try:
        result = paypal_integration.execute_payment(payment_id, PayerID)
        
        if result["success"]:
            # Notificar al cliente
            db = SessionLocal()
            order = db.query(Order).filter(Order.payment_method == "paypal").order_by(Order.created_at.desc()).first()
            if order:
                message = f"""✅ *PAGO PAYPAL CONFIRMADO*

Pedido: #{order.order_number}
Transaction ID: {result['transaction_id']}

🎉 ¡Tu pago fue aprobado!

📦 Tu pedido será procesado y enviado pronto.

Gracias por tu compra! 🌎"""
                
                await baileys_client.send_message(order.user_phone, message)
            db.close()
            
            return {
                "status": "success",
                "message": "¡Pago exitoso! Recibirás confirmación por WhatsApp."
            }
        else:
            return {
                "status": "error",
                "message": "No se pudo procesar el pago."
            }
    except Exception as e:
        print(f"❌ Error en callback PayPal: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/paypal/cancel")
async def paypal_cancel():
    """Callback de cancelación de PayPal"""
    return {
        "status": "cancelled",
        "message": "Pago cancelado. Puedes intentar nuevamente cuando desees."
    }

@router.post("/confirm-manual")
async def confirm_manual_payment(phone: str, order_number: str, proof_url: str = None):
    """Confirma un pago manual (Nequi, Daviplata, Banco)"""
    try:
        result = await payment_service.confirm_payment(phone, order_number, proof_url)
        return result
    except Exception as e:
        print(f"❌ Error confirmando pago: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{order_number}")
async def get_payment_status(order_number: str):
    """Consulta el estado de un pago"""
    try:
        db = SessionLocal()
        order = db.query(Order).filter(Order.order_number == order_number).first()
        db.close()
        
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        
        return {
            "order_number": order.order_number,
            "status": order.status,
            "payment_method": order.payment_method,
            "total": order.total,
            "created_at": order.created_at
        }
    except Exception as e:
        print(f"❌ Error consultando estado: {e}")
        raise HTTPException(status_code=500, detail=str(e))
