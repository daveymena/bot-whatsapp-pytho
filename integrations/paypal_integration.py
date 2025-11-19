import paypalrestsdk
from typing import Dict
from config.settings import settings
from database.connection import SessionLocal
from database.models import Order

class PayPalIntegration:
    """Integración con PayPal para pagos internacionales"""
    
    def __init__(self):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # sandbox o live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
    
    def create_payment_link(self, order_data: Dict) -> Dict:
        """
        Crea un link de pago en PayPal
        
        Args:
            order_data: Diccionario con información del pedido
            
        Returns:
            Dict con approval_url (URL de pago) y payment_id
        """
        try:
            # Preparar items
            items = []
            for product in order_data['products']:
                items.append({
                    "name": product['name'],
                    "sku": str(product.get('id', '')),
                    "price": str(round(product['price'] / settings.USD_TO_COP_RATE, 2)),
                    "currency": "USD",
                    "quantity": product['quantity']
                })
            
            # Generar order_number si no existe
            if 'order_number' not in order_data:
                from datetime import datetime
                order_data['order_number'] = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Calcular total en USD
            total_usd = round(order_data['total'] / settings.USD_TO_COP_RATE, 2)
            
            # Crear pago
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{settings.BASE_URL}/payment/paypal/success",
                    "cancel_url": f"{settings.BASE_URL}/payment/paypal/cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": items
                    },
                    "amount": {
                        "total": str(total_usd),
                        "currency": "USD"
                    },
                    "description": f"Pedido #{order_data['order_number']}",
                    "invoice_number": order_data['order_number']
                }]
            })
            
            if payment.create():
                # Obtener URL de aprobación
                for link in payment.links:
                    if link.rel == "approval_url":
                        return {
                            "success": True,
                            "approval_url": link.href,
                            "payment_id": payment.id
                        }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
                
        except Exception as e:
            print(f"❌ Error creando pago PayPal: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Dict:
        """Ejecuta un pago aprobado por el usuario"""
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                # Actualizar orden
                invoice_number = payment.transactions[0].invoice_number
                
                db = SessionLocal()
                order = db.query(Order).filter(
                    Order.order_number == invoice_number
                ).first()
                
                if order:
                    order.status = "paid"
                    order.payment_method = "paypal"
                    db.commit()
                db.close()
                
                return {
                    "success": True,
                    "status": "approved",
                    "transaction_id": payment.id
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
                
        except Exception as e:
            print(f"❌ Error ejecutando pago PayPal: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_payment_details(self, payment_id: str) -> Dict:
        """Obtiene detalles de un pago"""
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            return {
                "success": True,
                "status": payment.state,
                "amount": payment.transactions[0].amount.total,
                "currency": payment.transactions[0].amount.currency,
                "invoice_number": payment.transactions[0].invoice_number
            }
        except Exception as e:
            print(f"❌ Error obteniendo detalles: {e}")
            return {"success": False, "error": str(e)}

paypal_integration = PayPalIntegration()
