"""
Sistema Híbrido de Respuestas
Intenta usar IA primero, si falla usa base de conocimiento
"""
from typing import Dict, Optional
import logging
from ai.knowledge_base import knowledge_base
from ai.groq_client import groq_client
from ai.conversation_manager import conversation_manager

logger = logging.getLogger(__name__)

class HybridResponseSystem:
    """Sistema que combina IA y base de conocimiento"""
    
    def __init__(self):
        self.use_ai = True  # Flag para controlar uso de IA
        self.ai_failures = 0  # Contador de fallos
        self.max_failures = 3  # Máximo de fallos antes de desactivar IA temporalmente
    
    async def generate_response(
        self, 
        phone: str, 
        message: str, 
        system_prompt: str,
        context: Dict
    ) -> tuple[str, str]:
        """
        Genera respuesta usando IA o base de conocimiento
        
        Returns:
            tuple: (response, source) donde source es 'ai' o 'knowledge_base'
        """
        
        # Intentar con IA primero si está habilitada
        if self.use_ai and self.ai_failures < self.max_failures:
            try:
                response = await self._generate_ai_response(
                    phone, message, system_prompt
                )
                
                # Validar que la respuesta no esté vacía
                if not response or len(response.strip()) < 10:
                    logger.warning("Respuesta de IA muy corta, usando base de conocimiento")
                    raise Exception("Respuesta de IA inválida")
                
                # Resetear contador de fallos si funciona
                self.ai_failures = 0
                
                return response, "ai"
                
            except Exception as e:
                logger.warning(f"IA falló, usando base de conocimiento: {e}")
                self.ai_failures += 1
                
                # Si hay muchos fallos, desactivar IA temporalmente
                if self.ai_failures >= self.max_failures:
                    logger.warning("IA desactivada temporalmente por múltiples fallos")
                    self.use_ai = False
        
        # Usar base de conocimiento como fallback
        response = await self._generate_knowledge_response(message, context)
        return response, "knowledge_base"
    
    async def _generate_ai_response(
        self, 
        phone: str, 
        message: str, 
        system_prompt: str
    ) -> str:
        """Genera respuesta usando IA"""
        
        try:
            # Obtener historial
            history = conversation_manager.get_history(phone)
            
            # Construir mensajes
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history[-6:])  # Últimos 3 intercambios
            messages.append({"role": "user", "content": message})
            
            # Generar respuesta
            response = await groq_client.generate_response(messages)
            
            # Guardar en historial
            conversation_manager.add_message(phone, "user", message)
            conversation_manager.add_message(phone, "assistant", response)
            
            return response
        except Exception as e:
            # Si es error 429 (rate limit), desactivar IA temporalmente
            if "429" in str(e) or "Too Many Requests" in str(e):
                logger.warning("⚠️ Límite de API alcanzado, cambiando a base de conocimiento")
                self.use_ai = False
                self.ai_failures = self.max_failures
            raise
    
    async def _generate_knowledge_response(self, message: str, context: Dict) -> str:
        """Genera respuesta usando base de conocimiento"""
        
        # Detectar si es una objeción
        objection_keywords = ["caro", "pensar", "después", "seguro", "confianza"]
        if any(keyword in message.lower() for keyword in objection_keywords):
            return knowledge_base.handle_objection(message, context)
        
        # Generar respuesta normal
        return await knowledge_base.generate_response(message, context)
    
    def reset_ai(self):
        """Resetea el sistema de IA"""
        self.use_ai = True
        self.ai_failures = 0
        logger.info("Sistema de IA reseteado")
    
    def get_status(self) -> Dict:
        """Obtiene el estado del sistema"""
        return {
            "ai_enabled": self.use_ai,
            "ai_failures": self.ai_failures,
            "current_mode": "ai" if self.use_ai else "knowledge_base"
        }

hybrid_system = HybridResponseSystem()
