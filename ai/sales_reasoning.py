"""
Motor de Razonamiento Inteligente para Ventas
Maneja el ciclo completo: Saludo → Presentación → Cierre
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class SalesStage(Enum):
    """Etapas del proceso de ventas"""
    GREETING = "greeting"              # Saludo inicial
    RAPPORT = "rapport"                # Construcción de confianza
    DISCOVERY = "discovery"            # Descubrimiento de necesidades
    PRESENTATION = "presentation"      # Presentación de productos
    HANDLING_OBJECTIONS = "objections" # Manejo de objeciones
    CLOSING = "closing"                # Cierre de venta
    POST_SALE = "post_sale"           # Post-venta

class CustomerIntent(Enum):
    """Intención del cliente"""
    BROWSING = "browsing"              # Solo mirando
    RESEARCHING = "researching"        # Investigando opciones
    COMPARING = "comparing"            # Comparando productos
    READY_TO_BUY = "ready_to_buy"     # Listo para comprar
    PRICE_SENSITIVE = "price_sensitive" # Sensible al precio
    QUALITY_FOCUSED = "quality_focused" # Enfocado en calidad

@dataclass
class SalesContext:
    """Contexto de la conversación de ventas"""
    stage: SalesStage = SalesStage.GREETING
    customer_intent: CustomerIntent = CustomerIntent.BROWSING
    mentioned_products: List[str] = None
    budget_range: Optional[Tuple[float, float]] = None
    objections: List[str] = None
    pain_points: List[str] = None
    buying_signals: int = 0
    urgency_level: int = 0  # 0-10
    trust_level: int = 5    # 0-10
    
    def __post_init__(self):
        if self.mentioned_products is None:
            self.mentioned_products = []
        if self.objections is None:
            self.objections = []
        if self.pain_points is None:
            self.pain_points = []

class SalesReasoningEngine:
    """Motor de razonamiento para ventas profesionales"""
    
    def __init__(self):
        self.greeting_patterns = {
            'formal': ['buenos días', 'buenas tardes', 'buenas noches'],
            'casual': ['hola', 'hey', 'qué tal', 'cómo estás'],
            'enthusiastic': ['hola!', 'hey!', 'qué tal!']
        }
        
        self.buying_signals = [
            'cuánto cuesta', 'precio', 'comprar', 'adquirir',
            'me interesa', 'lo quiero', 'cómo pago', 'envío',
            'disponible', 'stock', 'cuándo llega'
        ]
        
        self.objection_patterns = {
            'price': ['caro', 'costoso', 'precio alto', 'muy caro'],
            'trust': ['seguro', 'confiable', 'garantía', 'devolución'],
            'timing': ['después', 'más tarde', 'pensarlo', 'consultar'],
            'competition': ['otro lugar', 'más barato', 'competencia']
        }

    
    def analyze_message(self, message: str, context: SalesContext) -> Dict:
        """Analiza el mensaje y determina la mejor estrategia con razonamiento profundo"""
        message_lower = message.lower()
        
        # Detectar señales de compra
        buying_signal_count = sum(
            1 for signal in self.buying_signals 
            if signal in message_lower
        )
        
        # Detectar objeciones
        objections = []
        for obj_type, patterns in self.objection_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                objections.append(obj_type)
        
        # RAZONAMIENTO PROFUNDO: Detectar solicitud de más información
        asking_for_details = any(word in message_lower for word in [
            'más información', 'mas informacion', 'más info', 'mas info',
            'detalles', 'características', 'caracteristicas', 'más detalles',
            'cuéntame más', 'cuentame mas', 'qué más', 'que mas',
            'tienes más', 'tienes mas', 'información adicional'
        ])
        
        # RAZONAMIENTO PROFUNDO: Detectar interés positivo
        showing_interest = any(word in message_lower for word in [
            'interesado', 'interesada', 'me interesa', 'me gusta',
            'suena bien', 'se ve bien', 'parece bueno', 'parece bien',
            'excelente', 'perfecto', 'genial'
        ])
        
        # RAZONAMIENTO PROFUNDO: Detectar dudas que necesitan resolverse
        has_doubts = any(word in message_lower for word in [
            'pero', 'duda', 'no sé', 'no se', 'no estoy seguro',
            'no estoy segura', 'pensarlo', 'pensar', 'después',
            'mas tarde', 'más tarde'
        ])
        
        # Determinar etapa actual
        current_stage = self._determine_stage(message_lower, context)
        
        # RAZONAMIENTO: Si pide más info, está en presentación
        if asking_for_details:
            current_stage = SalesStage.PRESENTATION
            buying_signal_count += 1  # Pedir info es señal de interés
        
        # RAZONAMIENTO: Si muestra interés, avanzar a cierre
        if showing_interest:
            buying_signal_count += 2
            if current_stage == SalesStage.PRESENTATION:
                current_stage = SalesStage.CLOSING
        
        # RAZONAMIENTO: Si tiene dudas, manejar objeciones
        if has_doubts and not objections:
            objections.append('timing')
            current_stage = SalesStage.HANDLING_OBJECTIONS
        
        # Calcular nivel de urgencia
        urgency = self._calculate_urgency(message_lower, context)
        
        # Determinar intención del cliente
        intent = self._determine_intent(message_lower, context)
        
        # RAZONAMIENTO: Ajustar intención basado en contexto
        if asking_for_details:
            intent = CustomerIntent.RESEARCHING
        elif showing_interest:
            intent = CustomerIntent.READY_TO_BUY
        
        return {
            'stage': current_stage,
            'intent': intent,
            'buying_signals': buying_signal_count,
            'objections': objections,
            'urgency': urgency,
            'asking_for_details': asking_for_details,
            'showing_interest': showing_interest,
            'has_doubts': has_doubts,
            'recommended_action': self._recommend_action(
                current_stage, intent, buying_signal_count, objections
            )
        }
    
    def _determine_stage(self, message: str, context: SalesContext) -> SalesStage:
        """Determina la etapa actual de la venta"""
        # Saludo inicial
        if any(greeting in message for greeting in ['hola', 'buenos', 'buenas']):
            if context.stage == SalesStage.GREETING:
                return SalesStage.RAPPORT
            return context.stage
        
        # Descubrimiento (preguntas sobre necesidades)
        if any(word in message for word in ['busco', 'necesito', 'quiero', 'me interesa']):
            return SalesStage.DISCOVERY
        
        # Presentación (preguntas sobre productos)
        if any(word in message for word in ['características', 'especificaciones', 'detalles']):
            return SalesStage.PRESENTATION
        
        # Manejo de objeciones
        if any(word in message for word in ['pero', 'caro', 'duda', 'problema']):
            return SalesStage.HANDLING_OBJECTIONS
        
        # Cierre (señales de compra)
        if any(word in message for word in ['comprar', 'pedir', 'ordenar', 'confirmar']):
            return SalesStage.CLOSING
        
        return context.stage
    
    def _determine_intent(self, message: str, context: SalesContext) -> CustomerIntent:
        """Determina la intención del cliente"""
        # Listo para comprar
        if any(word in message for word in ['comprar', 'pedir', 'ordenar', 'lo quiero']):
            return CustomerIntent.READY_TO_BUY
        
        # Comparando
        if any(word in message for word in ['comparar', 'diferencia', 'mejor', 'vs']):
            return CustomerIntent.COMPARING
        
        # Sensible al precio
        if any(word in message for word in ['precio', 'costo', 'barato', 'descuento']):
            return CustomerIntent.PRICE_SENSITIVE
        
        # Enfocado en calidad
        if any(word in message for word in ['calidad', 'garantía', 'durabilidad', 'marca']):
            return CustomerIntent.QUALITY_FOCUSED
        
        # Investigando
        if any(word in message for word in ['información', 'detalles', 'características']):
            return CustomerIntent.RESEARCHING
        
        return CustomerIntent.BROWSING
    
    def _calculate_urgency(self, message: str, context: SalesContext) -> int:
        """Calcula el nivel de urgencia (0-10)"""
        urgency = 0
        
        # Palabras de urgencia
        urgent_words = ['urgente', 'rápido', 'ya', 'ahora', 'hoy', 'inmediato']
        urgency += sum(2 for word in urgent_words if word in message)
        
        # Señales de compra aumentan urgencia
        urgency += context.buying_signals
        
        # Limitar a 10
        return min(urgency, 10)
    
    def _recommend_action(self, stage: SalesStage, intent: CustomerIntent, 
                         buying_signals: int, objections: List[str]) -> str:
        """Recomienda la mejor acción a tomar"""
        # Alta intención de compra
        if buying_signals >= 2 and not objections:
            return "CLOSE_SALE"
        
        # Objeciones presentes
        if objections:
            return f"HANDLE_OBJECTION_{objections[0].upper()}"
        
        # Según la etapa
        if stage == SalesStage.GREETING:
            return "BUILD_RAPPORT"
        elif stage == SalesStage.DISCOVERY:
            return "ASK_QUESTIONS"
        elif stage == SalesStage.PRESENTATION:
            return "PRESENT_PRODUCT"
        elif stage == SalesStage.CLOSING:
            return "CLOSE_SALE"
        
        return "CONTINUE_CONVERSATION"
    
    def generate_response_strategy(self, analysis: Dict, products: List[Dict]) -> Dict:
        """Genera estrategia de respuesta basada en el análisis"""
        action = analysis['recommended_action']
        
        strategies = {
            'BUILD_RAPPORT': {
                'tone': 'friendly',
                'focus': 'relationship',
                'include_products': False,
                'ask_questions': True
            },
            'ASK_QUESTIONS': {
                'tone': 'consultative',
                'focus': 'needs_discovery',
                'include_products': False,
                'ask_questions': True
            },
            'PRESENT_PRODUCT': {
                'tone': 'enthusiastic',
                'focus': 'product_benefits',
                'include_products': True,
                'ask_questions': False
            },
            'CLOSE_SALE': {
                'tone': 'confident',
                'focus': 'action',
                'include_products': True,
                'ask_questions': False
            },
            'HANDLE_OBJECTION_PRICE': {
                'tone': 'understanding',
                'focus': 'value_justification',
                'include_products': True,
                'ask_questions': False
            },
            'CONTINUE_CONVERSATION': {
                'tone': 'professional',
                'focus': 'general',
                'include_products': False,
                'ask_questions': True
            }
        }
        
        return strategies.get(action, strategies['CONTINUE_CONVERSATION'])

sales_reasoning = SalesReasoningEngine()
