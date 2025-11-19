from agents.base_agent import BaseAgent
from config.settings import settings
from services.payment_service import payment_service
from ai.context_manager import context_manager
from database.connection import SessionLocal
from database.models import Product
import re

class PaymentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agente de Pagos", "Especialista en métodos de pago y transacciones")
    
    def get_system_prompt(self) -> str:
        return f"""Eres el {self.name} de {settings.BUSINESS_NAME}, experto en procesar pagos.

MÉTODOS DE PAGO DISPONIBLES:

1. MERCADOPAGO 💳
   - Tarjetas de crédito/débito
   - PSE
   - Hasta 12 cuotas sin interés
   - Link de pago automático
   - Pago 100% seguro

2. PAYPAL 🌎
   - Pagos internacionales
   - Protección al comprador
   - Múltiples métodos de pago
   - Link de pago automático

3. NEQUI 💜
   - Número: {settings.NEQUI_NUMBER}
   - Instantáneo y seguro
   - Sin comisiones
   - Requiere comprobante

4. DAVIPLATA ❤️
   - Número: {settings.DAVIPLATA_NUMBER}
   - Rápido y confiable
   - Sin costos adicionales
   - Requiere comprobante

5. TRANSFERENCIA BANCARIA 🏦
   - Banco: {settings.BANK_NAME}
   - Tipo: {settings.BANK_ACCOUNT_TYPE}
   - Cuenta: {settings.BANK_ACCOUNT_NUMBER}
   - Titular: {settings.BANK_ACCOUNT_HOLDER}
   - Requiere comprobante

6. CONTRA ENTREGA 💵
   - Pago en efectivo al recibir
   - Disponible en: {settings.DELIVERY_ZONES}
   - Sin comisiones

PROCESO DE PAGO:
1. Confirmar productos y cantidades
2. Calcular total (productos + envío - descuentos)
3. Cliente elige método de pago
4. Generar link o proporcionar datos
5. Cliente realiza pago
6. Confirmar recepción
7. Procesar pedido

COMANDOS ESPECIALES:
- "mercadopago" o "mp" → Generar link de Mercado Pago
- "paypal" → Generar link de PayPal
- "nequi" → Información de Nequi
- "daviplata" → Información de Daviplata
- "banco" o "transferencia" → Datos bancarios
- "contraentrega" o "cod" → Pago contra entrega
- "confirmar pago" → Confirmar pago manual

INFORMACIÓN A SOLICITAR:
- Nombre completo
- Dirección de entrega
- Teléfono de contacto
- Método de pago preferido

PARA PAGOS MANUALES:
- Comprobante de pago (foto)
- Número de referencia
- Hora de transacción

SEGURIDAD:
- Verificar todos los pagos
- Confirmar antes de enviar
- Proteger datos del cliente
- Emitir factura

COMUNICACIÓN:
- Clara sobre montos
- Paciente con dudas
- Rápido en confirmaciones
- Profesional siempre

Facilita el proceso de pago para que sea simple, seguro y confiable."""
    
    async def process_message(self, phone: str, message: str, context: dict) -> str:
        """Procesa mensajes relacionados con pagos"""
        message_lower = message.lower()
        
        # Obtener contexto del usuario
        user_context = context_manager.get_context(phone)
        
        # Detectar método de pago solicitado
        if any(word in message_lower for word in ["mercadopago", "mercado pago", "mp", "tarjeta", "cuotas"]):
            return await self._process_mercadopago(phone, user_context)
        
        elif any(word in message_lower for word in ["paypal", "internacional"]):
            return await self._process_paypal(phone, user_context)
        
        elif "nequi" in message_lower:
            return await self._process_nequi(phone, user_context)
        
        elif "daviplata" in message_lower:
            return await self._process_daviplata(phone, user_context)
        
        elif any(word in message_lower for word in ["banco", "transferencia", "consignación"]):
            return await self._process_bank_transfer(phone, user_context)
        
        elif any(word in message_lower for word in ["contraentrega", "contra entrega", "efectivo", "cod"]):
            return await self._process_cod(phone, user_context)
        
        elif any(word in message_lower for word in ["confirmar", "pagué", "ya pagué", "comprobante"]):
            return await self._confirm_payment(phone, message)
        
        # Si no hay método específico, mostrar opciones
        return await self._show_payment_options(phone, user_context)
    
    async def _process_mercadopago(self, phone: str, context) -> str:
        """Genera link de pago de Mercado Pago"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return "Para generar el link de pago, primero necesito que confirmes tu pedido. ¿Qué productos deseas comprar?"
        
        result = await payment_service.create_payment(phone, order_data, "mercadopago")
        
        if result["success"]:
            return f"✅ ¡Perfecto! Te envié el link de pago de Mercado Pago. Puedes pagar con tarjeta, PSE o en cuotas. El link es válido por 24 horas."
        else:
            return f"❌ Hubo un problema generando el link. Por favor intenta con otro método de pago o contacta a soporte."
    
    async def _process_paypal(self, phone: str, context) -> str:
        """Genera link de pago de PayPal"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return "Para generar el link de PayPal, primero necesito que confirmes tu pedido. ¿Qué productos deseas comprar?"
        
        result = await payment_service.create_payment(phone, order_data, "paypal")
        
        if result["success"]:
            return f"✅ ¡Listo! Te envié el link de pago de PayPal. Es ideal para pagos internacionales. El link es válido por 3 horas."
        else:
            return f"❌ Hubo un problema generando el link. Por favor intenta con otro método de pago."
    
    async def _process_nequi(self, phone: str, context) -> str:
        """Procesa pago por Nequi"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return f"""💜 *PAGO POR NEQUI*

Número: {settings.NEQUI_NUMBER}
Nombre: {settings.BUSINESS_NAME}

Primero confirma tu pedido y luego te daré las instrucciones completas de pago."""
        
        result = await payment_service.create_payment(phone, order_data, "nequi")
        
        if result["success"]:
            return "✅ Te envié la información de pago por Nequi. Después de transferir, envíame el comprobante por favor! 📸"
        
        return "❌ Hubo un problema. Por favor intenta nuevamente."
    
    async def _process_daviplata(self, phone: str, context) -> str:
        """Procesa pago por Daviplata"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return f"""❤️ *PAGO POR DAVIPLATA*

Número: {settings.DAVIPLATA_NUMBER}
Nombre: {settings.BUSINESS_NAME}

Primero confirma tu pedido y luego te daré las instrucciones completas de pago."""
        
        result = await payment_service.create_payment(phone, order_data, "daviplata")
        
        if result["success"]:
            return "✅ Te envié la información de pago por Daviplata. Después de transferir, envíame el comprobante! 📸"
        
        return "❌ Hubo un problema. Por favor intenta nuevamente."
    
    async def _process_bank_transfer(self, phone: str, context) -> str:
        """Procesa pago por transferencia bancaria"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return f"""🏦 *TRANSFERENCIA BANCARIA*

Banco: {settings.BANK_NAME}
Tipo: {settings.BANK_ACCOUNT_TYPE}
Cuenta: {settings.BANK_ACCOUNT_NUMBER}
Titular: {settings.BANK_ACCOUNT_HOLDER}

Primero confirma tu pedido y luego te daré las instrucciones completas."""
        
        result = await payment_service.create_payment(phone, order_data, "banco")
        
        if result["success"]:
            return "✅ Te envié los datos bancarios. Después de transferir, envíame el comprobante! 📸"
        
        return "❌ Hubo un problema. Por favor intenta nuevamente."
    
    async def _process_cod(self, phone: str, context) -> str:
        """Procesa pago contra entrega"""
        order_data = self._prepare_order_data(phone, context)
        
        if not order_data:
            return "Para confirmar el pago contra entrega, primero necesito que confirmes tu pedido y dirección de entrega."
        
        result = await payment_service.create_payment(phone, order_data, "contraentrega")
        
        if result["success"]:
            return "✅ Perfecto! Tu pedido será enviado y pagarás en efectivo al recibirlo. 💵"
        
        return "❌ Hubo un problema. Por favor intenta nuevamente."
    
    async def _confirm_payment(self, phone: str, message: str) -> str:
        """Confirma un pago manual"""
        # Buscar número de orden en el contexto
        context = context_manager.get_context(phone)
        order_number = getattr(context, 'current_order', None)
        
        if not order_number:
            return "No encuentro un pedido pendiente. ¿Cuál es el número de tu orden? (ORD-XXXXXXXX)"
        
        result = await payment_service.confirm_payment(phone, order_number)
        
        if result["success"]:
            return "✅ ¡Pago confirmado! Tu pedido será procesado y enviado pronto. Gracias por tu compra! 🎉"
        
        return "❌ No pude confirmar el pago. Por favor verifica el número de orden o contacta a soporte."
    
    async def _show_payment_options(self, phone: str, context) -> str:
        """Muestra las opciones de pago disponibles"""
        return f"""💳 *MÉTODOS DE PAGO DISPONIBLES*

1️⃣ *Mercado Pago* (Recomendado)
   • Tarjetas crédito/débito
   • PSE
   • Hasta 12 cuotas
   • Link automático

2️⃣ *PayPal*
   • Pagos internacionales
   • Seguro y confiable

3️⃣ *Nequi* - {settings.NEQUI_NUMBER}
   • Transferencia instantánea

4️⃣ *Daviplata* - {settings.DAVIPLATA_NUMBER}
   • Rápido y fácil

5️⃣ *Transferencia Bancaria*
   • {settings.BANK_NAME}

6️⃣ *Contra Entrega*
   • Paga en efectivo al recibir

¿Cuál prefieres? Escribe el nombre del método."""
    
    def _prepare_order_data(self, phone: str, context) -> dict:
        """Prepara los datos de la orden desde el contexto"""
        cart = getattr(context, 'cart', [])
        
        if not cart:
            return None
        
        # Calcular totales
        subtotal = sum(item['price'] * item['quantity'] for item in cart)
        shipping = getattr(context, 'shipping_cost', 0)
        discount = getattr(context, 'discount', 0)
        total = subtotal + shipping - discount
        
        return {
            'user_phone': phone,
            'user_name': getattr(context, 'user_name', ''),
            'products': cart,
            'subtotal': subtotal,
            'shipping': shipping,
            'discount': discount,
            'total': total,
            'delivery_address': getattr(context, 'delivery_address', '')
        }
    
    def calculate_total(self, subtotal: float, shipping: float = 0, discount: float = 0):
        total = subtotal + shipping - discount
        return max(total, 0)
    
    def format_payment_info(self, method: str):
        info = {
            "nequi": f"Nequi: {settings.NEQUI_NUMBER}",
            "daviplata": f"Daviplata: {settings.DAVIPLATA_NUMBER}",
            "banco": f"Banco: {settings.BANK_NAME}\nCuenta: {settings.BANK_ACCOUNT_NUMBER}\nTitular: {settings.BANK_ACCOUNT_HOLDER}"
        }
        return info.get(method.lower(), "Método no disponible")
