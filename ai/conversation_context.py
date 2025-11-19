"""
Sistema de Gestión de Contexto Conversacional
Mantiene el hilo de la conversación y maneja múltiples productos
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ConversationContext:
    """Gestiona el contexto de una conversación"""
    
    def __init__(self, phone: str):
        self.phone = phone
        self.current_products = []  # Productos actuales en discusión
        self.all_mentioned_products = []  # Todos los productos mencionados
        self.current_category = None
        self.stage = 'greeting'  # greeting, discovery, presentation, objection, closing
        self.buying_signals = 0
        self.last_intent = None
        self.last_message_time = datetime.now()
        self.conversation_history = []  # Historial de mensajes
        self.pending_questions = []  # Preguntas pendientes del cliente
        
    def add_message(self, message: str, intent: str, response: str):
        """Agrega un mensaje al historial"""
        self.conversation_history.append({
            'message': message,
            'intent': intent,
            'response': response,
            'timestamp': datetime.now()
        })
        self.last_intent = intent
        self.last_message_time = datetime.now()
        
        # Mantener solo últimos 10 mensajes
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def add_products(self, products: List[Dict], category: str = None):
        """Agrega productos al contexto"""
        self.current_products = products
        if category:
            self.current_category = category
        
        # Agregar a historial de productos mencionados
        for product in products:
            if product not in self.all_mentioned_products:
                self.all_mentioned_products.append(product)
    
    def get_current_product(self) -> Optional[Dict]:
        """Obtiene el producto actual en discusión"""
        if self.current_products:
            return self.current_products[0]
        return None
    
    def has_active_product(self) -> bool:
        """Verifica si hay un producto activo en la conversación"""
        return len(self.current_products) > 0
    
    def is_talking_about_product(self, message: str) -> bool:
        """Verifica si el mensaje se refiere al producto actual"""
        if not self.has_active_product():
            return False
        
        # Palabras que indican continuidad de conversación sobre el producto
        continuity_words = [
            "ese", "este", "eso", "lo", "la", "el",
            "cuánto", "precio", "cuesta", "vale",
            "garantía", "envío", "pago",
            "sí", "si", "ok", "perfecto", "me interesa"
        ]
        
        message_lower = message.lower()
        return any(word in message_lower for word in continuity_words)
    
    def wants_to_change_product(self, message: str) -> bool:
        """Detecta si el cliente quiere cambiar de producto"""
        change_indicators = [
            "otro", "otra", "diferente", "mejor",
            "más barato", "mas barato", "más caro",
            "también", "además", "y",
            "pero", "prefiero", "quisiera"
        ]
        
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in change_indicators)
    
    def extract_new_product_from_message(self, message: str) -> Optional[str]:
        """Extrae mención de nuevo producto del mensaje"""
        from ai.knowledge_base import knowledge_base
        
        # Buscar categorías de productos en el mensaje
        for category, keywords in knowledge_base.product_keywords.items():
            if any(keyword in message.lower() for keyword in keywords):
                return category
        
        return None
    
    def update_stage(self, intent: str):
        """Actualiza la etapa de la conversación según la intención"""
        stage_map = {
            'greeting': 'greeting',
            'product_inquiry': 'discovery',
            'price_inquiry': 'presentation',
            'payment_inquiry': 'closing',
            'shipping_inquiry': 'closing',
            'warranty_inquiry': 'presentation',
            'purchase_intent': 'closing'
        }
        
        new_stage = stage_map.get(intent, self.stage)
        
        # No retroceder en el embudo de ventas
        stage_order = ['greeting', 'discovery', 'presentation', 'objection', 'closing']
        current_index = stage_order.index(self.stage) if self.stage in stage_order else 0
        new_index = stage_order.index(new_stage) if new_stage in stage_order else 0
        
        if new_index >= current_index:
            self.stage = new_stage
    
    def increment_buying_signals(self, intent: str):
        """Incrementa señales de compra según la intención"""
        buying_intents = ['price_inquiry', 'payment_inquiry', 'shipping_inquiry', 'purchase_intent']
        if intent in buying_intents:
            self.buying_signals += 1
    
    def get_context_summary(self) -> str:
        """Obtiene un resumen del contexto actual"""
        summary = f"Etapa: {self.stage}, "
        
        if self.has_active_product():
            product = self.get_current_product()
            summary += f"Producto actual: {product['name']}, "
        
        summary += f"Señales de compra: {self.buying_signals}"
        
        return summary
    
    def should_remind_product(self) -> bool:
        """Determina si debe recordar el producto al cliente"""
        # Si han pasado más de 2 mensajes sin mencionar el producto
        if len(self.conversation_history) >= 2:
            last_two = self.conversation_history[-2:]
            product_mentioned = any(
                'product' in msg.get('intent', '') 
                for msg in last_two
            )
            return not product_mentioned and self.has_active_product()
        
        return False
    
    def clear_products(self):
        """Limpia los productos actuales (para cambio de tema)"""
        self.current_products = []
        self.current_category = None
    
    def reset(self):
        """Resetea el contexto (nueva conversación)"""
        self.current_products = []
        self.all_mentioned_products = []
        self.current_category = None
        self.stage = 'greeting'
        self.buying_signals = 0
        self.last_intent = None
        self.conversation_history = []
        self.pending_questions = []


class ConversationContextManager:
    """Gestor de contextos de conversación para múltiples usuarios"""
    
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.cleanup_interval = timedelta(hours=24)  # Limpiar contextos antiguos
    
    def get_context(self, phone: str) -> ConversationContext:
        """Obtiene o crea el contexto para un usuario"""
        if phone not in self.contexts:
            self.contexts[phone] = ConversationContext(phone)
        
        # Verificar si el contexto es muy antiguo
        context = self.contexts[phone]
        if datetime.now() - context.last_message_time > self.cleanup_interval:
            # Resetear contexto si es muy antiguo
            context.reset()
        
        return context
    
    def cleanup_old_contexts(self):
        """Limpia contextos antiguos"""
        current_time = datetime.now()
        phones_to_remove = []
        
        for phone, context in self.contexts.items():
            if current_time - context.last_message_time > self.cleanup_interval:
                phones_to_remove.append(phone)
        
        for phone in phones_to_remove:
            del self.contexts[phone]
    
    def get_all_contexts(self) -> Dict[str, ConversationContext]:
        """Obtiene todos los contextos activos"""
        return self.contexts

# Instancia global del gestor de contextos
conversation_context_manager = ConversationContextManager()
