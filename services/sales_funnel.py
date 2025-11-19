from typing import Dict, Any
from enum import Enum
from ai.context_manager import context_manager

class FunnelStage(Enum):
    AWARENESS = "awareness"  # Conocimiento
    INTEREST = "interest"  # Interés
    DESIRE = "desire"  # Deseo
    ACTION = "action"  # Acción/Compra
    RETENTION = "retention"  # Retención

class SalesFunnel:
    """Embudo de ventas automatizado con metodología AIDA"""
    
    def __init__(self):
        self.stage_messages = {
            FunnelStage.AWARENESS: {
                "greeting": "¡Hola! 👋 Bienvenido a {business_name}. ¿En qué puedo ayudarte hoy?",
                "intro": "Tenemos productos increíbles: físicos, digitales y servicios. ¿Qué te interesa?"
            },
            FunnelStage.INTEREST: {
                "product_show": "¡Excelente elección! 🎯 Déjame mostrarte los detalles...",
                "features": "Este producto tiene características increíbles que te van a encantar:",
                "benefits": "Los beneficios que obtendrás son:"
            },
            FunnelStage.DESIRE: {
                "social_proof": "Más de {count} clientes satisfechos ya lo tienen! ⭐",
                "urgency": "⚡ Solo quedan {stock} unidades disponibles!",
                "limited_offer": "🔥 Oferta especial: {discount}% de descuento solo hoy!",
                "testimonial": "Mira lo que dicen nuestros clientes: '{testimonial}'"
            },
            FunnelStage.ACTION: {
                "cta": "¿Listo para hacer tu pedido? 🛒",
                "payment": "Perfecto! Acepto estos métodos de pago:",
                "data_collection": "Para procesar tu pedido necesito:",
                "confirmation": "✅ ¡Pedido confirmado! Tu número de orden es: {order_number}"
            },
            FunnelStage.RETENTION: {
                "thank_you": "¡Gracias por tu compra! 🎉",
                "follow_up": "¿Cómo va todo con tu producto?",
                "upsell": "Te puede interesar también:",
                "loyalty": "Como cliente frecuente, tengo una oferta especial para ti!"
            }
        }
    
    def get_current_stage(self, phone: str) -> FunnelStage:
        """Determina la etapa actual del cliente en el embudo"""
        context = context_manager.get_context(phone)
        
        if context.stage == "initial":
            return FunnelStage.AWARENESS
        elif context.stage == "browsing":
            return FunnelStage.INTEREST
        elif context.stage == "negotiating":
            return FunnelStage.DESIRE
        elif context.stage == "closing":
            return FunnelStage.ACTION
        else:
            return FunnelStage.RETENTION
    
    def advance_stage(self, phone: str, intent: str, message: str):
        """Avanza al cliente a la siguiente etapa del embudo"""
        current_stage = self.get_current_stage(phone)
        
        # Lógica de avance basada en intención
        if intent == "product_inquiry" and current_stage == FunnelStage.AWARENESS:
            context_manager.set_stage(phone, "browsing")
            return FunnelStage.INTEREST
        
        elif intent == "price_inquiry" and current_stage == FunnelStage.INTEREST:
            context_manager.set_stage(phone, "negotiating")
            return FunnelStage.DESIRE
        
        elif intent == "buy_intent":
            context_manager.set_stage(phone, "closing")
            return FunnelStage.ACTION
        
        return current_stage
    
    def handle_objection(self, objection_type: str) -> str:
        """Maneja objeciones comunes"""
        objections = {
            "price_high": """Entiendo tu preocupación por el precio. 💡

Déjame explicarte el valor que obtienes:
✅ Calidad garantizada
✅ Soporte incluido
✅ Garantía de {warranty}
✅ Envío seguro

Además, puedes pagar en cuotas sin interés! 💳""",
            
            "need_time": """¡Claro! Tómate tu tiempo. ⏰

Pero déjame contarte algo: esta oferta especial termina pronto y el stock es limitado.

¿Qué tal si reservo uno para ti por 24 horas? Sin compromiso. 😊""",
            
            "trust": """Entiendo perfectamente tu precaución. 🛡️

Somos una empresa establecida con:
✅ Más de {years} años en el mercado
✅ Miles de clientes satisfechos
✅ Garantía de devolución
✅ Pagos seguros

¿Quieres ver testimonios de clientes reales?""",
            
            "comparison": """¡Excelente que compares! 🔍

Nuestra ventaja competitiva:
✅ Mejor relación calidad-precio
✅ Atención personalizada 24/7
✅ Envío más rápido
✅ Garantía extendida

¿Qué característica es más importante para ti?"""
        }
        
        return objections.get(objection_type, "Entiendo tu punto. ¿Qué más te gustaría saber?")
    
    def get_data_collection_flow(self, phone: str) -> Dict[str, Any]:
        """Define el flujo de recolección de datos"""
        context = context_manager.get_context(phone)
        
        required_data = {
            "name": "¿Cuál es tu nombre completo? 📝",
            "address": "¿Cuál es tu dirección de entrega? 📍",
            "payment_method": "¿Cómo prefieres pagar? (Nequi, Daviplata, Transferencia, etc.) 💳",
            "confirmation": "Perfecto! Confirma tus datos:\n\nNombre: {name}\nDirección: {address}\nPago: {payment_method}\n\n¿Todo correcto? ✅"
        }
        
        # Determinar qué dato falta
        for key, question in required_data.items():
            if key not in context.user_data:
                return {"field": key, "question": question}
        
        return {"field": "complete", "question": ""}

sales_funnel = SalesFunnel()
