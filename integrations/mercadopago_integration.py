import mercadopago
from typing import Dict, Optional
from config.settings import settings
from database.connection import SessionLocal
from database.models import Order
import uuid

class MercadoPagoIntegration:
    """Integración con Mercado Pago para generar links de pago dinámicos"""
    
    def __init__(self):
        self.sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    def create_payment_link(self, order_data: Dict) -> Dict:
        """
        Crea un link de pago dinámico en Mercado Pago
        
        Args:
            order_data: Diccionario con información del pedido
            
        Returns:
            Dict con init_point (URL de pago) y preference_id
        """
        try:
            # Preparar items
            items = []
            for product in order_data['products']:
                items.append({
                    "title": product['name'],
                    "quantity": product['quantity'],
                    "unit_price": float(product['price']),
                    "currency_id": "COP"
                })
            
            # Generar order_number si no existe
            if 'order_number' not in order_data:
                from datetime import datetime
                order_data['order_number'] = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Crear preferencia de pago (simplificada)
            preference_data = {
                "items": items,
                "external_reference": order_data['order_number'],
                "payment_methods": {
                    "installments": 12  # Hasta 12 cuotas
                }
            }
            
            # Crear preferencia
            preference_response = self.sdk.preference().create(preference_data)
            
            # Debug: ver respuesta completa
            print(f"🔍 Respuesta de Mercado Pago: {preference_response}")
            
            # Verificar si la respuesta fue exitosa
            if preference_response["status"] not in [200, 201]:
                return {
                    "success": False,
                    "error": f"Error de API: {preference_response.get('status')} - {preference_response.get('response')}"
                }
            
            preference = preference_response["response"]
            
            # Verificar que tenga init_point
            if "init_point" not in preference:
                print(f"⚠️  Respuesta sin init_point: {preference}")
                return {
                    "success": False,
                    "error": "La respuesta de Mercado Pago no contiene init_point"
                }
            
            return {
                "success": True,
                "init_point": preference["init_point"],  # URL para pagar
                "preference_id": preference["id"],
                "sandbox_init_point": preference.get("sandbox_init_point")  # Para testing
            }
            
        except Exception as e:
            print(f"❌ Error creando link de Mercado Pago: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_payment_status(self, payment_id: str) -> Dict:
        """Consulta el estado de un pago"""
        try:
            payment_info = self.sdk.payment().get(payment_id)
            payment = payment_info["response"]
            
            return {
                "success": True,
                "status": payment["status"],
                "status_detail": payment["status_detail"],
                "amount": payment["transaction_amount"],
                "external_reference": payment.get("external_reference")
            }
        except Exception as e:
            print(f"❌ Error consultando pago: {e}")
            return {"success": False, "error": str(e)}
    
    def process_webhook(self, data: Dict) -> Dict:
        """Procesa notificaciones de Mercado Pago"""
        try:
            if data.get("type") == "payment":
                payment_id = data["data"]["id"]
                payment_info = self.get_payment_status(payment_id)
                
                if payment_info["success"]:
                    # Actualizar orden en base de datos
                    db = SessionLocal()
                    order = db.query(Order).filter(
                        Order.order_number == payment_info["external_reference"]
                    ).first()
                    
                    if order:
                        if payment_info["status"] == "approved":
                            order.status = "paid"
                            order.payment_method = "mercadopago"
                        elif payment_info["status"] == "rejected":
                            order.status = "payment_failed"
                        
                        db.commit()
                    db.close()
                
                return payment_info
            
            return {"success": True, "message": "Webhook procesado"}
            
        except Exception as e:
            print(f"❌ Error procesando webhook: {e}")
            return {"success": False, "error": str(e)}

mercadopago_integration = MercadoPagoIntegration()
