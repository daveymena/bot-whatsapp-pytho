"""
Analizador de Sentimiento en Tiempo Real
Detecta emociones y ajusta tono de respuesta
"""
from typing import Dict, Tuple
from enum import Enum
import re

class Sentiment(Enum):
    """Sentimientos detectables"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    EXCITED = "excited"

class EmotionLevel(Enum):
    """Nivel de emoción"""
    CALM = "calm"
    MODERATE = "moderate"
    INTENSE = "intense"

class SentimentAnalyzer:
    """Analiza sentimiento y emoción en mensajes"""
    
    def __init__(self):
        self.sentiment_patterns = {
            Sentiment.VERY_POSITIVE: {
                'keywords': ['excelente', 'perfecto', 'increíble', 'maravilloso', 
                           'fantástico', 'genial', 'súper', 'encantado', 'feliz'],
                'emojis': ['😍', '🤩', '🎉', '🥳', '❤️', '💯', '🔥', '⭐'],
                'score': 2
            },
            Sentiment.POSITIVE: {
                'keywords': ['bueno', 'bien', 'gracias', 'ok', 'vale', 'listo',
                           'me gusta', 'interesante', 'útil'],
                'emojis': ['😊', '🙂', '👍', '✅', '😄'],
                'score': 1
            },
            Sentiment.NEGATIVE: {
                'keywords': ['malo', 'no me gusta', 'problema', 'error', 'falla',
                           'decepcionado', 'insatisfecho'],
                'emojis': ['😞', '😔', '👎', '😕'],
                'score': -1
            },
            Sentiment.VERY_NEGATIVE: {
                'keywords': ['pésimo', 'terrible', 'horrible', 'desastre', 'fraude',
                           'estafa', 'nunca más', 'muy malo'],
                'emojis': ['😡', '🤬', '😠', '💢'],
                'score': -2
            },
            Sentiment.FRUSTRATED: {
                'keywords': ['no entiendo', 'no funciona', 'otra vez', 'siempre',
                           'cansado', 'harto', 'molesto'],
                'emojis': ['😤', '😩', '😫'],
                'score': -1.5
            },
            Sentiment.CONFUSED: {
                'keywords': ['no entiendo', 'confuso', 'no sé', 'cómo', 'qué significa',
                           'explica', 'no comprendo'],
                'emojis': ['🤔', '😕', '❓'],
                'score': 0
            },
            Sentiment.EXCITED: {
                'keywords': ['wow', 'guau', 'increíble', 'lo quiero', 'necesito',
                           'urgente', 'ya', 'ahora'],
                'emojis': ['🤩', '😲', '🎊', '🎁'],
                'score': 1.5
            }
        }
        
        # Intensificadores
        self.intensifiers = {
            'muy': 1.5,
            'super': 1.5,
            'demasiado': 1.3,
            'bastante': 1.2,
            'realmente': 1.2,
            'extremadamente': 1.8
        }
        
        # Negadores
        self.negators = ['no', 'nunca', 'jamás', 'tampoco']
    
    def analyze(self, message: str) -> Dict:
        """Analiza sentimiento completo del mensaje"""
        
        message_lower = message.lower()
        
        # Calcular score de sentimiento
        sentiment_score = 0
        detected_sentiments = []
        
        for sentiment, patterns in self.sentiment_patterns.items():
            # Buscar keywords
            keyword_matches = sum(
                1 for keyword in patterns['keywords'] 
                if keyword in message_lower
            )
            
            # Buscar emojis
            emoji_matches = sum(
                1 for emoji in patterns['emojis']
                if emoji in message
            )
            
            if keyword_matches > 0 or emoji_matches > 0:
                detected_sentiments.append(sentiment)
                sentiment_score += patterns['score'] * (keyword_matches + emoji_matches)
        
        # Aplicar intensificadores
        for intensifier, multiplier in self.intensifiers.items():
            if intensifier in message_lower:
                sentiment_score *= multiplier
        
        # Aplicar negadores (invierte sentimiento)
        negation_count = sum(1 for neg in self.negators if neg in message_lower)
        if negation_count % 2 == 1:  # Número impar de negaciones
            sentiment_score *= -1
        
        # Determinar sentimiento principal
        primary_sentiment = self._calculate_primary_sentiment(sentiment_score)
        
        # Detectar nivel de emoción
        emotion_level = self._detect_emotion_level(message, sentiment_score)
        
        # Detectar urgencia
        urgency = self._detect_urgency(message_lower)
        
        return {
            'primary_sentiment': primary_sentiment,
            'sentiment_score': sentiment_score,
            'detected_sentiments': detected_sentiments,
            'emotion_level': emotion_level,
            'urgency': urgency,
            'requires_escalation': self._should_escalate(
                primary_sentiment, emotion_level, message_lower
            ),
            'recommended_tone': self._recommend_tone(primary_sentiment, emotion_level)
        }
    
    def _calculate_primary_sentiment(self, score: float) -> Sentiment:
        """Calcula sentimiento principal basado en score"""
        if score >= 2:
            return Sentiment.VERY_POSITIVE
        elif score >= 0.5:
            return Sentiment.POSITIVE
        elif score <= -2:
            return Sentiment.VERY_NEGATIVE
        elif score <= -0.5:
            return Sentiment.NEGATIVE
        else:
            return Sentiment.NEUTRAL
    
    def _detect_emotion_level(self, message: str, score: float) -> EmotionLevel:
        """Detecta nivel de emoción"""
        
        # Contar signos de exclamación
        exclamation_count = message.count('!')
        
        # Contar mayúsculas
        uppercase_ratio = sum(1 for c in message if c.isupper()) / max(len(message), 1)
        
        # Calcular intensidad
        intensity = abs(score) + (exclamation_count * 0.5) + (uppercase_ratio * 2)
        
        if intensity >= 3:
            return EmotionLevel.INTENSE
        elif intensity >= 1.5:
            return EmotionLevel.MODERATE
        else:
            return EmotionLevel.CALM
    
    def _detect_urgency(self, message: str) -> int:
        """Detecta nivel de urgencia (0-10)"""
        urgency_keywords = {
            'urgente': 3,
            'ya': 2,
            'ahora': 2,
            'inmediato': 3,
            'rápido': 2,
            'pronto': 1,
            'hoy': 2,
            'necesito': 1
        }
        
        urgency = 0
        for keyword, score in urgency_keywords.items():
            if keyword in message:
                urgency += score
        
        return min(urgency, 10)
    
    def _should_escalate(self, sentiment: Sentiment, 
                        emotion_level: EmotionLevel, message: str) -> bool:
        """Determina si debe escalar a humano"""
        
        # Sentimiento muy negativo con emoción intensa
        if sentiment == Sentiment.VERY_NEGATIVE and emotion_level == EmotionLevel.INTENSE:
            return True
        
        # Frustración repetida
        if sentiment == Sentiment.FRUSTRATED and emotion_level != EmotionLevel.CALM:
            return True
        
        # Palabras clave de escalamiento
        escalation_keywords = [
            'hablar con', 'gerente', 'supervisor', 'humano', 'persona',
            'demanda', 'abogado', 'denuncia', 'fraude'
        ]
        
        if any(keyword in message for keyword in escalation_keywords):
            return True
        
        return False
    
    def _recommend_tone(self, sentiment: Sentiment, 
                       emotion_level: EmotionLevel) -> str:
        """Recomienda tono de respuesta"""
        
        if sentiment in [Sentiment.VERY_NEGATIVE, Sentiment.FRUSTRATED]:
            return 'empathetic_apologetic'
        
        elif sentiment == Sentiment.CONFUSED:
            return 'patient_explanatory'
        
        elif sentiment in [Sentiment.VERY_POSITIVE, Sentiment.EXCITED]:
            return 'enthusiastic_matching'
        
        elif emotion_level == EmotionLevel.INTENSE:
            return 'calm_professional'
        
        else:
            return 'friendly_professional'
    
    def generate_tone_instructions(self, analysis: Dict) -> str:
        """Genera instrucciones de tono para la IA"""
        
        tone = analysis['recommended_tone']
        sentiment = analysis['primary_sentiment']
        
        instructions = {
            'empathetic_apologetic': """
⚠️ TONO REQUERIDO: Empático y Disculpante
- Reconoce el problema inmediatamente
- Muestra empatía genuina
- Ofrece solución concreta
- Evita excusas o justificaciones
- Usa frases como: "Entiendo tu frustración", "Lamento mucho esto"
""",
            'patient_explanatory': """
⚠️ TONO REQUERIDO: Paciente y Explicativo
- Explica paso a paso
- Usa lenguaje simple
- Confirma comprensión
- Ofrece ayuda adicional
- Usa frases como: "Déjame explicarte", "Es muy sencillo"
""",
            'enthusiastic_matching': """
⚠️ TONO REQUERIDO: Entusiasta y Positivo
- Iguala la energía del cliente
- Usa emojis positivos
- Celebra la decisión
- Facilita el proceso
- Usa frases como: "¡Excelente elección!", "¡Me encanta tu entusiasmo!"
""",
            'calm_professional': """
⚠️ TONO REQUERIDO: Calmado y Profesional
- Mantén la calma
- Sé directo y claro
- Evita emociones extremas
- Enfócate en soluciones
- Usa frases como: "Entiendo", "Permíteme ayudarte"
""",
            'friendly_professional': """
⚠️ TONO REQUERIDO: Amigable y Profesional
- Mantén tono conversacional
- Usa emojis moderadamente
- Sé servicial
- Guía la conversación
- Usa frases como: "Con gusto", "Claro que sí"
"""
        }
        
        return instructions.get(tone, instructions['friendly_professional'])

sentiment_analyzer = SentimentAnalyzer()
