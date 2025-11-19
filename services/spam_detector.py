from datetime import datetime, timedelta
from typing import Dict, List
from database.models import User
from sqlalchemy.orm import Session

class SpamDetector:
    """Detector y bloqueador de spam"""
    
    def __init__(self):
        self.message_history: Dict[str, List[datetime]] = {}
        self.blocked_phrases = [
            "spam", "publicidad", "oferta masiva", "cadena",
            "reenviar", "compartir con todos"
        ]
        self.max_messages_per_minute = 10
        self.max_same_message_count = 3
        self.recent_messages: Dict[str, List[str]] = {}
    
    def is_spam(self, phone: str, message: str) -> bool:
        """Detecta si un mensaje es spam"""
        
        # 1. Verificar frases bloqueadas
        message_lower = message.lower()
        if any(phrase in message_lower for phrase in self.blocked_phrases):
            return True
        
        # 2. Verificar frecuencia de mensajes
        if self._is_flooding(phone):
            return True
        
        # 3. Verificar mensajes repetidos
        if self._is_repeating(phone, message):
            return True
        
        # 4. Verificar longitud excesiva
        if len(message) > 2000:
            return True
        
        return False
    
    def _is_flooding(self, phone: str) -> bool:
        """Detecta flooding (muchos mensajes en poco tiempo)"""
        now = datetime.now()
        
        if phone not in self.message_history:
            self.message_history[phone] = []
        
        # Limpiar mensajes antiguos (más de 1 minuto)
        cutoff = now - timedelta(minutes=1)
        self.message_history[phone] = [
            ts for ts in self.message_history[phone] if ts > cutoff
        ]
        
        # Agregar mensaje actual
        self.message_history[phone].append(now)
        
        # Verificar si excede el límite
        return len(self.message_history[phone]) > self.max_messages_per_minute
    
    def _is_repeating(self, phone: str, message: str) -> bool:
        """Detecta mensajes repetidos"""
        if phone not in self.recent_messages:
            self.recent_messages[phone] = []
        
        # Mantener solo los últimos 10 mensajes
        self.recent_messages[phone] = self.recent_messages[phone][-10:]
        
        # Contar repeticiones del mensaje actual
        count = self.recent_messages[phone].count(message)
        
        # Agregar mensaje actual
        self.recent_messages[phone].append(message)
        
        return count >= self.max_same_message_count
    
    def should_block_user(self, phone: str, db: Session) -> bool:
        """Determina si un usuario debe ser bloqueado"""
        user = db.query(User).filter(User.phone == phone).first()
        
        if not user:
            return False
        
        # Bloquear si ya está marcado como bloqueado
        if user.is_blocked:
            return True
        
        # Bloquear si tiene muchos reportes de spam
        if user.spam_count >= 5:
            user.is_blocked = True
            db.commit()
            return True
        
        return False
    
    def increment_spam_count(self, phone: str, db: Session):
        """Incrementa el contador de spam de un usuario"""
        user = db.query(User).filter(User.phone == phone).first()
        
        if user:
            user.spam_count += 1
            db.commit()
    
    def get_spam_response(self) -> str:
        """Respuesta automática para spam detectado"""
        return """⚠️ Hemos detectado actividad inusual.

Por favor:
- Evita enviar mensajes repetidos
- Espera respuesta antes de enviar más mensajes
- Usa un lenguaje apropiado

Si necesitas ayuda urgente, escribe "AYUDA"."""

spam_detector = SpamDetector()
