"""
Sistema de Memoria del Cliente
Recuerda preferencias, historial y personaliza experiencia
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class CustomerProfile:
    """Perfil completo del cliente"""
    phone: str
    name: Optional[str] = None
    email: Optional[str] = None
    
    # Preferencias
    preferred_payment: Optional[str] = None
    preferred_category: Optional[str] = None
    budget_range: Optional[tuple] = None
    
    # Historial
    total_purchases: int = 0
    total_spent: float = 0.0
    last_purchase_date: Optional[datetime] = None
    purchased_products: List[str] = field(default_factory=list)
    
    # Comportamiento
    avg_response_time: int = 0  # segundos
    preferred_contact_time: Optional[str] = None  # 'morning', 'afternoon', 'evening'
    communication_style: str = 'formal'  # 'formal', 'casual', 'technical'
    
    # Interacciones
    total_conversations: int = 0
    last_interaction: Optional[datetime] = None
    common_questions: List[str] = field(default_factory=list)
    objections_history: List[str] = field(default_factory=list)
    
    # Segmentación
    customer_segment: str = 'new'  # 'new', 'regular', 'vip', 'at_risk'
    lifetime_value: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para almacenamiento"""
        return {
            'phone': self.phone,
            'name': self.name,
            'email': self.email,
            'preferred_payment': self.preferred_payment,
            'preferred_category': self.preferred_category,
            'budget_range': self.budget_range,
            'total_purchases': self.total_purchases,
            'total_spent': self.total_spent,
            'last_purchase_date': self.last_purchase_date.isoformat() if self.last_purchase_date else None,
            'purchased_products': self.purchased_products,
            'avg_response_time': self.avg_response_time,
            'preferred_contact_time': self.preferred_contact_time,
            'communication_style': self.communication_style,
            'total_conversations': self.total_conversations,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None,
            'common_questions': self.common_questions,
            'objections_history': self.objections_history,
            'customer_segment': self.customer_segment,
            'lifetime_value': self.lifetime_value
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CustomerProfile':
        """Crea perfil desde diccionario"""
        if data.get('last_purchase_date'):
            data['last_purchase_date'] = datetime.fromisoformat(data['last_purchase_date'])
        if data.get('last_interaction'):
            data['last_interaction'] = datetime.fromisoformat(data['last_interaction'])
        return cls(**data)

class CustomerMemorySystem:
    """Sistema de memoria persistente del cliente"""
    
    def __init__(self):
        self.profiles: Dict[str, CustomerProfile] = {}
        self.interaction_cache: Dict[str, List[Dict]] = {}
    
    def get_or_create_profile(self, phone: str) -> CustomerProfile:
        """Obtiene o crea perfil del cliente"""
        if phone not in self.profiles:
            self.profiles[phone] = CustomerProfile(phone=phone)
            logger.info(f"Nuevo perfil creado para {phone}")
        
        return self.profiles[phone]
    
    def update_profile(self, phone: str, updates: Dict):
        """Actualiza perfil del cliente"""
        profile = self.get_or_create_profile(phone)
        
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.last_interaction = datetime.now()
        profile.total_conversations += 1
        
        logger.info(f"Perfil actualizado para {phone}")
    
    def record_purchase(self, phone: str, product_name: str, amount: float):
        """Registra una compra"""
        profile = self.get_or_create_profile(phone)
        
        profile.total_purchases += 1
        profile.total_spent += amount
        profile.last_purchase_date = datetime.now()
        profile.purchased_products.append(product_name)
        profile.lifetime_value = profile.total_spent
        
        # Actualizar segmento
        profile.customer_segment = self._calculate_segment(profile)
        
        logger.info(f"Compra registrada para {phone}: {product_name} - ${amount}")
    
    def _calculate_segment(self, profile: CustomerProfile) -> str:
        """Calcula segmento del cliente"""
        if profile.total_purchases == 0:
            return 'new'
        elif profile.total_purchases >= 5 or profile.total_spent >= 500000:
            return 'vip'
        elif profile.total_purchases >= 2:
            return 'regular'
        elif profile.last_purchase_date:
            days_since_purchase = (datetime.now() - profile.last_purchase_date).days
            if days_since_purchase > 90:
                return 'at_risk'
        
        return 'regular'
    
    def get_personalized_greeting(self, phone: str) -> str:
        """Genera saludo personalizado"""
        profile = self.get_or_create_profile(phone)
        
        # Cliente nuevo
        if profile.total_conversations == 0:
            return "👋 ¡Hola! Bienvenido/a. ¿En qué puedo ayudarte hoy?"
        
        # Cliente recurrente
        name = profile.name or "amigo/a"
        
        if profile.customer_segment == 'vip':
            return f"👋 ¡Hola {name}! Qué gusto verte de nuevo 🌟 ¿En qué puedo ayudarte hoy?"
        elif profile.customer_segment == 'regular':
            return f"👋 ¡Hola {name}! ¿Cómo te fue con tu última compra? ¿En qué más puedo ayudarte?"
        elif profile.customer_segment == 'at_risk':
            return f"👋 ¡Hola {name}! Hace tiempo no hablábamos. Tenemos productos nuevos que te pueden interesar 😊"
        
        return f"👋 ¡Hola {name}! ¿En qué puedo ayudarte hoy?"
    
    def get_product_recommendations(self, phone: str, 
                                   available_products: List[Dict]) -> List[Dict]:
        """Recomienda productos basados en historial"""
        profile = self.get_or_create_profile(phone)
        
        recommendations = []
        
        # Filtrar por categoría preferida
        if profile.preferred_category:
            recommendations = [
                p for p in available_products 
                if p.get('category') == profile.preferred_category
            ]
        
        # Filtrar por rango de presupuesto
        if profile.budget_range and not recommendations:
            min_budget, max_budget = profile.budget_range
            recommendations = [
                p for p in available_products
                if min_budget <= p['price'] <= max_budget
            ]
        
        # Si no hay recomendaciones específicas, productos populares
        if not recommendations:
            recommendations = sorted(
                available_products, 
                key=lambda x: x.get('stock', 0), 
                reverse=True
            )[:3]
        
        return recommendations[:3]  # Máximo 3 recomendaciones
    
    def detect_communication_style(self, message: str) -> str:
        """Detecta estilo de comunicación del cliente"""
        message_lower = message.lower()
        
        # Formal
        formal_indicators = ['usted', 'señor', 'señora', 'buenos días', 'buenas tardes']
        if any(ind in message_lower for ind in formal_indicators):
            return 'formal'
        
        # Técnico
        technical_indicators = ['especificaciones', 'características técnicas', 'compatibilidad']
        if any(ind in message_lower for ind in technical_indicators):
            return 'technical'
        
        # Casual por defecto
        return 'casual'
    
    def record_objection(self, phone: str, objection: str):
        """Registra objeción del cliente"""
        profile = self.get_or_create_profile(phone)
        
        if objection not in profile.objections_history:
            profile.objections_history.append(objection)
    
    def get_context_summary(self, phone: str) -> str:
        """Genera resumen de contexto para la IA"""
        profile = self.get_or_create_profile(phone)
        
        summary = f"""
📊 PERFIL DEL CLIENTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Segmento: {profile.customer_segment.upper()}
- Compras totales: {profile.total_purchases}
- Valor total: ${profile.total_spent:,.0f}
- Estilo de comunicación: {profile.communication_style}
"""
        
        if profile.preferred_category:
            summary += f"- Categoría preferida: {profile.preferred_category}\n"
        
        if profile.preferred_payment:
            summary += f"- Método de pago preferido: {profile.preferred_payment}\n"
        
        if profile.purchased_products:
            summary += f"- Últimas compras: {', '.join(profile.purchased_products[-3:])}\n"
        
        if profile.objections_history:
            summary += f"- Objeciones previas: {', '.join(set(profile.objections_history))}\n"
        
        summary += "\n💡 RECOMENDACIÓN: "
        
        if profile.customer_segment == 'vip':
            summary += "Cliente VIP - Ofrecer atención premium y productos exclusivos"
        elif profile.customer_segment == 'at_risk':
            summary += "Cliente en riesgo - Ofrecer incentivos para reactivar"
        elif profile.customer_segment == 'new':
            summary += "Cliente nuevo - Construir confianza y educar sobre productos"
        else:
            summary += "Cliente regular - Mantener relación y ofrecer upselling"
        
        return summary

customer_memory = CustomerMemorySystem()
