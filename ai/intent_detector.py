import re
from typing import Dict, List, Tuple
from enum import Enum

class Intent(Enum):
    GREETING = "greeting"
    PRODUCT_INQUIRY = "product_inquiry"
    PRICE_INQUIRY = "price_inquiry"
    AVAILABILITY = "availability"
    BUY_INTENT = "buy_intent"
    SUPPORT = "support"
    COMPLAINT = "complaint"
    BUSINESS_INFO = "business_info"
    PAYMENT_INFO = "payment_info"
    SHIPPING_INFO = "shipping_info"
    RESERVATION = "reservation"
    CANCEL = "cancel"
    THANKS = "thanks"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"

class IntentDetector:
    def __init__(self):
        self.patterns = {
            Intent.GREETING: [
                r'\b(hola|buenos días|buenas tardes|buenas noches|hey|saludos|qué tal)\b',
                r'^(hola|hey|buenas)$'
            ],
            Intent.PRODUCT_INQUIRY: [
                r'\b(producto|artículo|item|qué venden|qué tienen|catálogo|mostrar|ver)\b',
                r'\b(información sobre|detalles de|características de)\b',
                r'\b(me interesa|busco|necesito|quiero ver)\b'
            ],
            Intent.PRICE_INQUIRY: [
                r'\b(cuánto|precio|vale|cuesta|valor|cuánto cuesta|cuánto vale)\b',
                r'\b(qué precio|a cuánto|cuánto sale)\b',
                r'\$|cop|pesos'
            ],
            Intent.AVAILABILITY: [
                r'\b(disponible|hay|tienen|stock|existencia|queda)\b',
                r'\b(lo tienen|está disponible|tienen en stock)\b'
            ],
            Intent.BUY_INTENT: [
                r'\b(comprar|pedir|ordenar|adquirir|llevar|me lo llevo)\b',
                r'\b(quiero uno|dame|envíame|lo quiero|me interesa comprarlo)\b',
                r'\b(proceder|confirmar pedido|hacer pedido)\b'
            ],
            Intent.SUPPORT: [
                r'\b(problema|error|falla|no funciona|ayuda|soporte)\b',
                r'\b(no me sirve|está dañado|no enciende|no carga)\b',
                r'\b(cómo usar|cómo funciona|cómo configurar)\b'
            ],
            Intent.COMPLAINT: [
                r'\b(queja|reclamo|molesto|insatisfecho|mal servicio)\b',
                r'\b(no llegó|tardó mucho|mala calidad)\b'
            ],
            Intent.BUSINESS_INFO: [
                r'\b(horario|ubicación|dirección|dónde están|dónde quedan)\b',
                r'\b(teléfono|contacto|email|correo)\b',
                r'\b(quiénes son|empresa|negocio)\b'
            ],
            Intent.PAYMENT_INFO: [
                r'\b(pago|pagar|transferencia|nequi|daviplata|mercadopago|paypal)\b',
                r'\b(método de pago|formas de pago|cómo pago)\b',
                r'\b(tarjeta|efectivo|contra entrega)\b'
            ],
            Intent.SHIPPING_INFO: [
                r'\b(envío|entrega|domicilio|delivery|despacho)\b',
                r'\b(cuánto demora|tiempo de entrega|cuándo llega)\b',
                r'\b(costo de envío|envío gratis)\b'
            ],
            Intent.RESERVATION: [
                r'\b(reserva|cita|agendar|turno|hora)\b',
                r'\b(disponibilidad para|cuándo puedo|horarios disponibles)\b'
            ],
            Intent.CANCEL: [
                r'\b(cancelar|anular|no quiero|mejor no|desistir)\b',
                r'\b(cambié de opinión|ya no)\b'
            ],
            Intent.THANKS: [
                r'\b(gracias|muchas gracias|te agradezco|excelente|perfecto)\b',
                r'\b(ok gracias|vale gracias|listo gracias)\b'
            ],
            Intent.GOODBYE: [
                r'\b(adiós|chao|hasta luego|nos vemos|bye)\b',
                r'\b(que tengas buen día|buen día|buena tarde)\b'
            ]
        }
        
        # Palabras clave para entidades
        self.entity_patterns = {
            'product_name': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            'price': r'\$?\d+(?:,\d{3})*(?:\.\d{2})?',
            'phone': r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'time': r'\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?\b'
        }
    
    def detect_intent(self, message: str) -> Tuple[Intent, float]:
        """Detecta la intención del mensaje con score de confianza"""
        message_lower = message.lower()
        
        scores = {}
        for intent, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    score += 1
            
            if score > 0:
                scores[intent] = score / len(patterns)
        
        if not scores:
            return Intent.UNKNOWN, 0.0
        
        best_intent = max(scores.items(), key=lambda x: x[1])
        return best_intent[0], best_intent[1]
    
    def detect_multiple_intents(self, message: str) -> List[Tuple[Intent, float]]:
        """Detecta múltiples intenciones en un mensaje"""
        message_lower = message.lower()
        
        intents = []
        for intent, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    score += 1
            
            if score > 0:
                confidence = score / len(patterns)
                if confidence > 0.3:  # Umbral mínimo
                    intents.append((intent, confidence))
        
        return sorted(intents, key=lambda x: x[1], reverse=True)
    
    def extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extrae entidades del mensaje"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, message)
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def analyze_sentiment(self, message: str) -> str:
        """Análisis básico de sentimiento"""
        positive_words = ['excelente', 'genial', 'perfecto', 'bueno', 'gracias', 'me gusta']
        negative_words = ['malo', 'terrible', 'pésimo', 'problema', 'error', 'molesto', 'queja']
        
        message_lower = message.lower()
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

intent_detector = IntentDetector()
