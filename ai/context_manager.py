from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

@dataclass
class ConversationContext:
    user_phone: str
    current_intent: str = "unknown"
    current_product: Optional[str] = None
    current_service: Optional[str] = None
    stage: str = "initial"  # initial, browsing, negotiating, closing, support
    mentioned_products: List[str] = field(default_factory=list)
    user_data: Dict[str, Any] = field(default_factory=dict)
    objections: List[str] = field(default_factory=list)
    sentiment: str = "neutral"
    last_interaction: datetime = field(default_factory=datetime.now)
    interaction_count: int = 0
    is_human_takeover: bool = False
    human_agent_id: Optional[str] = None
    
class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.ttl = timedelta(hours=24)
    
    def get_context(self, phone: str) -> ConversationContext:
        """Obtiene o crea el contexto de un usuario"""
        if phone not in self.contexts:
            self.contexts[phone] = ConversationContext(user_phone=phone)
        
        context = self.contexts[phone]
        context.last_interaction = datetime.now()
        context.interaction_count += 1
        
        return context
    
    def update_context(self, phone: str, **kwargs):
        """Actualiza el contexto con nuevos datos"""
        context = self.get_context(phone)
        
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
    
    def add_mentioned_product(self, phone: str, product: str):
        """Agrega un producto mencionado al contexto"""
        context = self.get_context(phone)
        if product not in context.mentioned_products:
            context.mentioned_products.append(product)
    
    def add_objection(self, phone: str, objection: str):
        """Registra una objeción del cliente"""
        context = self.get_context(phone)
        context.objections.append(objection)
    
    def set_stage(self, phone: str, stage: str):
        """Actualiza la etapa de la conversación"""
        context = self.get_context(phone)
        context.stage = stage
    
    def enable_human_takeover(self, phone: str, agent_id: str):
        """Activa el modo de control humano"""
        context = self.get_context(phone)
        context.is_human_takeover = True
        context.human_agent_id = agent_id
    
    def disable_human_takeover(self, phone: str):
        """Desactiva el modo de control humano"""
        context = self.get_context(phone)
        context.is_human_takeover = False
        context.human_agent_id = None
    
    def get_summary(self, phone: str) -> Dict[str, Any]:
        """Obtiene un resumen del contexto"""
        context = self.get_context(phone)
        
        return {
            "phone": context.user_phone,
            "stage": context.stage,
            "current_intent": context.current_intent,
            "current_product": context.current_product,
            "mentioned_products": context.mentioned_products,
            "objections_count": len(context.objections),
            "sentiment": context.sentiment,
            "interactions": context.interaction_count,
            "is_human_takeover": context.is_human_takeover,
            "last_interaction": context.last_interaction.isoformat()
        }
    
    def cleanup_old_contexts(self):
        """Limpia contextos antiguos"""
        cutoff_time = datetime.now() - self.ttl
        
        to_remove = [
            phone for phone, context in self.contexts.items()
            if context.last_interaction < cutoff_time
        ]
        
        for phone in to_remove:
            del self.contexts[phone]
    
    def clear_context(self, phone: str):
        """Limpia el contexto de un usuario"""
        if phone in self.contexts:
            del self.contexts[phone]

context_manager = ContextManager()
