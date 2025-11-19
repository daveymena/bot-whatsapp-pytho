"""
Sistema de Escalamiento Inteligente
Detecta cuándo transferir a humano
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EscalationReason(Enum):
    """Razones de escalamiento"""
    NEGATIVE_SENTIMENT = "negative_sentiment"
    REPEATED_CONFUSION = "repeated_confusion"
    COMPLEX_QUERY = "complex_query"
    EXPLICIT_REQUEST = "explicit_request"
    HIGH_VALUE_CUSTOMER = "high_value_customer"
    COMPLAINT = "complaint"
    TECHNICAL_ISSUE = "technical_issue"
    PAYMENT_ISSUE = "payment_issue"

@dataclass
class EscalationTrigger:
    """Trigger de escalamiento"""
    reason: EscalationReason
    confidence: float
    message: str
    timestamp: datetime
    context: Dict

class EscalationManager:
    """Gestiona el escalamiento a agentes humanos"""
    
    def __init__(self):
        self.escalation_history: Dict[str, List[EscalationTrigger]] = {}
        
        # Umbrales de escalamiento
        self.thresholds = {
            'confusion_count': 3,           # 3 mensajes confusos seguidos
            'negative_sentiment_score': -2, # Score muy negativo
            'conversation_length': 15,      # 15+ mensajes sin resolución
            'high_value_threshold': 500000  # Cliente con compras > $500k
        }
        
        # Palabras clave de escalamiento explícito
        self.explicit_keywords = [
            'hablar con', 'persona', 'humano', 'operador', 'agente',
            'gerente', 'supervisor', 'encargado', 'responsable'
        ]
        
        # Palabras clave de quejas
        self.complaint_keywords = [
            'queja', 'reclamo', 'demanda', 'denuncia', 'fraude',
            'estafa', 'abogado', 'defensa del consumidor'
        ]
    
    def should_escalate(self, phone: str, message: str, 
                       context: Dict) -> tuple[bool, Optional[EscalationReason]]:
        """Determina si debe escalar la conversación"""
        
        message_lower = message.lower()
        
        # 1. Solicitud explícita
        if any(keyword in message_lower for keyword in self.explicit_keywords):
            self._record_trigger(
                phone, 
                EscalationReason.EXPLICIT_REQUEST,
                1.0,
                message,
                context
            )
            return True, EscalationReason.EXPLICIT_REQUEST
        
        # 2. Queja o reclamo
        if any(keyword in message_lower for keyword in self.complaint_keywords):
            self._record_trigger(
                phone,
                EscalationReason.COMPLAINT,
                0.9,
                message,
                context
            )
            return True, EscalationReason.COMPLAINT
        
        # 3. Sentimiento muy negativo
        sentiment_score = context.get('sentiment_score', 0)
        if sentiment_score <= self.thresholds['negative_sentiment_score']:
            self._record_trigger(
                phone,
                EscalationReason.NEGATIVE_SENTIMENT,
                0.8,
                message,
                context
            )
            return True, EscalationReason.NEGATIVE_SENTIMENT
        
        # 4. Confusión repetida
        confusion_count = context.get('confusion_count', 0)
        if confusion_count >= self.thresholds['confusion_count']:
            self._record_trigger(
                phone,
                EscalationReason.REPEATED_CONFUSION,
                0.7,
                message,
                context
            )
            return True, EscalationReason.REPEATED_CONFUSION
        
        # 5. Cliente de alto valor
        customer_value = context.get('customer_lifetime_value', 0)
        if customer_value >= self.thresholds['high_value_threshold']:
            # Solo escalar si hay algún problema
            if sentiment_score < 0 or confusion_count > 1:
                self._record_trigger(
                    phone,
                    EscalationReason.HIGH_VALUE_CUSTOMER,
                    0.8,
                    message,
                    context
                )
                return True, EscalationReason.HIGH_VALUE_CUSTOMER
        
        # 6. Conversación muy larga sin resolución
        conversation_length = context.get('message_count', 0)
        if conversation_length >= self.thresholds['conversation_length']:
            self._record_trigger(
                phone,
                EscalationReason.COMPLEX_QUERY,
                0.6,
                message,
                context
            )
            return True, EscalationReason.COMPLEX_QUERY
        
        # 7. Problema de pago
        payment_keywords = ['no puedo pagar', 'error de pago', 'no funciona el pago']
        if any(keyword in message_lower for keyword in payment_keywords):
            self._record_trigger(
                phone,
                EscalationReason.PAYMENT_ISSUE,
                0.9,
                message,
                context
            )
            return True, EscalationReason.PAYMENT_ISSUE
        
        return False, None
    
    def _record_trigger(self, phone: str, reason: EscalationReason,
                       confidence: float, message: str, context: Dict):
        """Registra un trigger de escalamiento"""
        
        if phone not in self.escalation_history:
            self.escalation_history[phone] = []
        
        trigger = EscalationTrigger(
            reason=reason,
            confidence=confidence,
            message=message,
            timestamp=datetime.now(),
            context=context
        )
        
        self.escalation_history[phone].append(trigger)
        
        logger.info(f"Escalamiento registrado para {phone}: {reason.value}")
    
    def generate_escalation_message(self, reason: EscalationReason) -> str:
        """Genera mensaje de escalamiento apropiado"""
        
        messages = {
            EscalationReason.EXPLICIT_REQUEST: """
Claro, entiendo que prefieres hablar con una persona 😊

Un momento por favor, estoy conectándote con uno de nuestros asesores humanos.

⏱ Tiempo estimado de espera: 2-5 minutos
""",
            EscalationReason.COMPLAINT: """
Lamento mucho la situación 😔

Voy a conectarte inmediatamente con nuestro supervisor para que te ayude a resolver esto de la mejor manera.

⏱ Un momento por favor...
""",
            EscalationReason.NEGATIVE_SENTIMENT: """
Entiendo tu frustración y quiero ayudarte 🙏

Permíteme conectarte con uno de nuestros especialistas que podrá atenderte mejor.

⏱ Un momento por favor...
""",
            EscalationReason.REPEATED_CONFUSION: """
Disculpa si no he sido claro 😊

Déjame conectarte con un asesor que podrá explicarte mejor y resolver todas tus dudas.

⏱ Un momento por favor...
""",
            EscalationReason.HIGH_VALUE_CUSTOMER: """
Como cliente preferencial, quiero asegurarte la mejor atención 🌟

Te estoy conectando con nuestro equipo VIP.

⏱ Un momento por favor...
""",
            EscalationReason.COMPLEX_QUERY: """
Tu consulta requiere atención especializada 👨‍💼

Te estoy conectando con un experto que podrá ayudarte mejor.

⏱ Un momento por favor...
""",
            EscalationReason.PAYMENT_ISSUE: """
Entiendo que hay un problema con el pago 💳

Te estoy conectando con nuestro equipo de pagos para resolverlo inmediatamente.

⏱ Un momento por favor...
""",
            EscalationReason.TECHNICAL_ISSUE: """
Veo que hay un problema técnico 🔧

Te estoy conectando con nuestro soporte técnico especializado.

⏱ Un momento por favor...
"""
        }
        
        return messages.get(reason, messages[EscalationReason.EXPLICIT_REQUEST])
    
    def get_escalation_stats(self, phone: str) -> Dict:
        """Obtiene estadísticas de escalamiento para un cliente"""
        
        if phone not in self.escalation_history:
            return {
                'total_escalations': 0,
                'reasons': {},
                'last_escalation': None
            }
        
        triggers = self.escalation_history[phone]
        
        reasons_count = {}
        for trigger in triggers:
            reason = trigger.reason.value
            reasons_count[reason] = reasons_count.get(reason, 0) + 1
        
        return {
            'total_escalations': len(triggers),
            'reasons': reasons_count,
            'last_escalation': triggers[-1].timestamp if triggers else None
        }

escalation_manager = EscalationManager()
