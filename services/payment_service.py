from typing import Dict, Optional
from database.connection import SessionLocal
from database.models import Order, User
from integrations.mercadopago_integration import mercadopago_integration
from integrations.paypal_integration import paypal_integration
from whatsapp.multimedia_handler import multimedia_handler
from datetime import datetime
from sqlalchemy import text
import uuid

class PaymentService:
    """Servicio centralizado para gestionar todos los métodos de pago"""
    
    def __init__(self):
        self.payment_methods = {
            "mercadopago": self._create_mercadopago_payment,
            "paypal": self._create_paypal_payment,
            "nequi": self._create_manual_payment,
            "daviplata": self._create_manual_payment,
            "banco": self._create_manual_payment,
            "contraentrega": self._create_cod_payment
        }
    
    async def create_payment(self, phone: str, order_data: Dict, method: str) -> Dict:
        """
        Crea un pago según el método seleccionado
        
        Args:
            phone: Teléfono del cliente
            order_data: Datos del pedido
            method: Método de pago (mercadopago, paypal, nequi, etc.)
            
        Returns:
            Dict con información del pago creado
        """
        method_lower = method.lower()
        
        if method_lower not in self.payment_methods:
            return {
                "success": False,
                "error": "Método de pago no válido"
            }
        
        # Crear orden en base de datos
        order = self._create_order(phone, order_data, method_lower)
        order_data['order_number'] = order.order_number
        
        # Procesar según método
        payment_handler = self.payment_methods[method_lower]
        result = await payment_handler(phone, order_data)
        
        return result
    
    async def _create_mercadopago_payment(self, phone: str, order_data: Dict) -> Dict:
        """Crea link de pago de Mercado Pago"""
        from whatsapp.baileys_client import baileys_client
        
        result = mercadopago_integration.create_payment_link(order_data)
        
        if result["success"]:
            # Mensaje con el link REAL
            message = f"""✅ *LINK DE PAGO MERCADOPAGO*

Pedido: #{order_data['order_number']}
Total: ${order_data['total']:,.0f} COP

💳 *Paga aquí:*
{result['init_point']}

✨ *Beneficios:*
• Tarjetas crédito/débito
• PSE
• Hasta 12 cuotas
• Pago 100% seguro

El link es válido por 24 horas 🚀"""
            
            # Enviar el mensaje con el link
            await baileys_client.send_message(phone, message)
            
            return {
                "success": True,
                "payment_url": result['init_point'],
                "order_number": order_data['order_number'],
                "message_sent": True
            }
        
        return result
    
    async def _create_paypal_payment(self, phone: str, order_data: Dict) -> Dict:
        """Crea link de pago de PayPal"""
        from whatsapp.baileys_client import baileys_client
        
        result = paypal_integration.create_payment_link(order_data)
        
        if result["success"]:
            total_usd = round(order_data['total'] / 4000, 2)  # Conversión aproximada
            
            message = f"""✅ *LINK DE PAGO PAYPAL*

Pedido: #{order_data['order_number']}
Total: ${order_data['total']:,.0f} COP (≈ ${total_usd} USD)

💳 *Paga aquí:*
{result['approval_url']}

✨ *Beneficios:*
• Pago internacional seguro
• Protección al comprador
• Múltiples métodos

El link es válido por 3 horas 🌎"""
            
            await baileys_client.send_message(phone, message)
            
            return {
                "success": True,
                "payment_url": result['approval_url'],
                "order_number": order_data['order_number'],
                "message_sent": True
            }
        
        return result
    
    async def _create_manual_payment(self, phone: str, order_data: Dict) -> Dict:
        """Crea pago manual (Nequi, Daviplata, Banco)"""
        from whatsapp.baileys_client import baileys_client
        from config.settings import settings
        
        method = order_data.get('payment_method', 'manual')
        
        # Información según método
        payment_info = {
            "nequi": f"""💜 *NEQUI*
Número: {settings.NEQUI_NUMBER}
Nombre: {settings.BUSINESS_NAME}""",
            
            "daviplata": f"""❤️ *DAVIPLATA*
Número: {settings.DAVIPLATA_NUMBER}
Nombre: {settings.BUSINESS_NAME}""",
            
            "banco": f"""🏦 *TRANSFERENCIA BANCARIA*
Banco: {settings.BANK_NAME}
Tipo: {settings.BANK_ACCOUNT_TYPE}
Cuenta: {settings.BANK_ACCOUNT_NUMBER}
Titular: {settings.BANK_ACCOUNT_HOLDER}"""
        }
        
        info = payment_info.get(method, payment_info["nequi"])
        
        message = f"""✅ *INFORMACIÓN DE PAGO*

Pedido: #{order_data['order_number']}
Total a pagar: ${order_data['total']:,.0f} COP

{info}

📸 *IMPORTANTE:*
Después de realizar la transferencia, envía el comprobante de pago por este chat.

Incluye:
• Captura del comprobante
• Número de referencia
• Hora de la transacción

Confirmaremos tu pago en menos de 5 minutos! ⚡"""
        
        await baileys_client.send_message(phone, message)
        
        return {
            "success": True,
            "requires_proof": True,
            "order_number": order_data['order_number']
        }
    
    async def _create_cod_payment(self, phone: str, order_data: Dict) -> Dict:
        """Crea pago contra entrega"""
        from whatsapp.baileys_client import baileys_client
        
        message = f"""✅ *PAGO CONTRA ENTREGA*

Pedido: #{order_data['order_number']}
Total a pagar: ${order_data['total']:,.0f} COP

💵 Pagarás en efectivo al recibir tu pedido.

📦 *Próximos pasos:*
1. Confirmaremos tu dirección de entrega
2. Coordinaremos el envío
3. Pagas al recibir el producto

⚠️ *Importante:*
• Ten el monto exacto preparado
• Verifica el producto antes de pagar
• Recibirás tu factura al momento

Tu pedido será procesado en las próximas horas! 🚚"""
        
        await baileys_client.send_message(phone, message)
        
        # Actualizar orden
        db = SessionLocal()
        order = db.query(Order).filter(
            Order.order_number == order_data['order_number']
        ).first()
        if order:
            order.status = "confirmed"
        db.commit()
        db.close()
        
        return {
            "success": True,
            "requires_delivery": True,
            "order_number": order_data['order_number']
        }
    
    def _create_order(self, phone: str, order_data: Dict, payment_method: str) -> Order:
        """Crea una orden en la base de datos"""
        db = SessionLocal()
        
        try:
            # Generar número de orden único
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            
            # Generar ID único (UUID como texto)
            order_id = uuid.uuid4().hex[:24]
            
            # Mapear a los nombres de columnas existentes en la BD
            order_dict = {
                'id': order_id,
                'order_number': order_number,
                'customerPhone': phone,
                'customerName': order_data.get('user_name', 'Cliente'),
                'customerEmail': order_data.get('user_email', 'cliente@example.com'),  # Email por defecto
                'customerAddress': order_data.get('delivery_address', 'Por confirmar'),
                'items': str(order_data['products']),
                'total': order_data['total'],
                'status': "pending",
                'paymentMethod': payment_method,
                'notes': ''
            }
            
            # Insertar usando SQL directo para evitar problemas con el modelo
            insert_sql = text("""
                INSERT INTO orders (id, order_number, "customerPhone", "customerName", "customerEmail", 
                                  "customerAddress", items, total, status, "paymentMethod", notes, "createdAt", "updatedAt")
                VALUES (:id, :order_number, :customerPhone, :customerName, :customerEmail,
                       :customerAddress, :items, :total, :status, :paymentMethod, :notes, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """)
            
            db.execute(insert_sql, order_dict)
            db.commit()
            
            # Crear objeto Order para retornar (sin agregar a la sesión ya que usamos SQL directo)
            order = Order()
            order.id = order_id
            order.order_number = order_number
            order.user_phone = phone
            order.user_name = order_data.get('user_name', 'Cliente')
            order.total = order_data['total']
            order.status = "pending"
            order.payment_method = payment_method
            
            return order
            
        except Exception as e:
            print(f"❌ Error creando orden: {e}")
            db.rollback()
            raise
        finally:
            db.close()
    
    async def confirm_payment(self, phone: str, order_number: str, proof_url: Optional[str] = None) -> Dict:
        """Confirma un pago manual"""
        from whatsapp.baileys_client import baileys_client
        
        db = SessionLocal()
        order = db.query(Order).filter(Order.order_number == order_number).first()
        
        if not order:
            db.close()
            return {"success": False, "error": "Orden no encontrada"}
        
        order.status = "paid"
        if proof_url:
            order.payment_proof = proof_url
        
        db.commit()
        db.close()
        
        # Enviar confirmación
        message = f"""✅ *PAGO CONFIRMADO*

Pedido: #{order_number}
Estado: Pagado ✓

🎉 ¡Gracias por tu compra!

📦 Tu pedido será procesado y enviado en las próximas 24-48 horas.

Te mantendremos informado del estado de tu envío! 🚚"""
        
        await baileys_client.send_message(phone, message)
        
        # Enviar factura
        await multimedia_handler.send_invoice(phone, order.__dict__)
        
        return {"success": True, "order_number": order_number}

payment_service = PaymentService()
