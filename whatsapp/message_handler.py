from typing import Dict
from agents.sales_agent import SalesAgent
from agents.products_agent import ProductsAgent
from agents.dropshipping_agent import DropshippingAgent
from agents.reservations_agent import ReservationsAgent
from agents.payment_agent import PaymentAgent
from agents.professional_sales_agent import professional_sales_agent  # NUEVO
from ai.intent_detector import intent_detector, Intent
from ai.context_manager import context_manager
from services.spam_detector import spam_detector
from services.sales_funnel import sales_funnel
from database.connection import SessionLocal
from database.models import ChatLog, Conversation, User
from datetime import datetime
import os

class MessageHandler:
    def __init__(self):
        # Verificar si el agente profesional está habilitado
        use_professional = os.getenv('ENABLE_PROFESSIONAL_SALES', 'true').lower() == 'true'
        
        self.agents = {
            "professional_sales": professional_sales_agent,  # NUEVO - Agente principal
            "sales": SalesAgent(),
            "products": ProductsAgent(),
            "dropshipping": DropshippingAgent(),
            "reservations": ReservationsAgent(),
            "payment": PaymentAgent()
        }
        
        self.use_professional_sales = use_professional
        
    async def handle_message(self, phone: str, message: str) -> str:
        """Procesa un mensaje entrante con detección avanzada de intención"""
        db = SessionLocal()
        
        try:
            # 1. Verificar si el usuario está bloqueado
            if spam_detector.should_block_user(phone, db):
                return "⛔ Tu cuenta ha sido bloqueada por actividad sospechosa. Contacta a soporte."
            
            # 2. Detectar spam
            if spam_detector.is_spam(phone, message):
                spam_detector.increment_spam_count(phone, db)
                return spam_detector.get_spam_response()
            
            # 3. Verificar si hay control humano activo
            context = context_manager.get_context(phone)
            if context.is_human_takeover:
                # No procesar con bot, solo registrar
                self._log_message(phone, message, "human_control", "neutral", db)
                return None  # No responder automáticamente
            
            # 4. Detectar intención y sentimiento
            intent, confidence = intent_detector.detect_intent(message)
            sentiment = intent_detector.analyze_sentiment(message)
            entities = intent_detector.extract_entities(message)
            
            # 5. Actualizar contexto
            context_manager.update_context(
                phone,
                current_intent=intent.value,
                sentiment=sentiment
            )
            
            # 6. Avanzar en el embudo de ventas
            funnel_stage = sales_funnel.advance_stage(phone, intent.value, message)
            
            # 7. Determinar agente apropiado
            if self.use_professional_sales:
                # Usar agente profesional de ventas (maneja todo el ciclo)
                agent_type = "professional_sales"
                agent = self.agents[agent_type]
            else:
                # Usar sistema de agentes múltiples (legacy)
                agent_type = self._determine_agent(intent, context, message)
                agent = self.agents[agent_type]
            
            # 8. Procesar con el agente
            context_dict = context.__dict__
            response = await agent.process_message(phone, message, context_dict)
            
            # 9. Verificar si hay fotos para enviar
            photos_to_send = context_dict.get('photos_to_send', [])
            
            # 10. Registrar conversación
            self._log_conversation(phone, message, response, intent.value, sentiment, agent_type, db)
            
            # 11. Actualizar usuario
            self._update_user(phone, db)
            
            # 12. Retornar respuesta con fotos si las hay
            if photos_to_send:
                return {
                    'text': response,
                    'photos': photos_to_send
                }
            
            return response
            
        except Exception as e:
            print(f"❌ Error en message_handler: {e}")
            return "Disculpa, tuve un problema. ¿Podrías intentar de nuevo?"
        finally:
            db.close()
    
    def _determine_agent(self, intent: Intent, context, message: str) -> str:
        """Determina qué agente debe manejar el mensaje basado en intención"""
        
        # Mapeo de intenciones a agentes
        intent_to_agent = {
            Intent.PRODUCT_INQUIRY: "products",
            Intent.PRICE_INQUIRY: "products",
            Intent.AVAILABILITY: "products",
            Intent.BUY_INTENT: "sales",
            Intent.PAYMENT_INFO: "payment",
            Intent.RESERVATION: "reservations",
            Intent.SUPPORT: "sales",
            Intent.COMPLAINT: "sales"
        }
        
        # Verificar si hay producto de dropshipping mencionado
        if "dropi" in message.lower() or context.current_product and "dropi" in context.current_product:
            return "dropshipping"
        
        # Usar mapeo de intención
        agent = intent_to_agent.get(intent, "sales")
        
        # Mantener agente actual si está en medio de un proceso
        if context.stage in ["closing", "negotiating"]:
            return context.current_agent if hasattr(context, 'current_agent') else agent
        
        return agent
    
    def _log_message(self, phone: str, message: str, intent: str, sentiment: str, db):
        """Registra el mensaje en el log"""
        log = ChatLog(
            user_phone=phone,
            message_type="text",
            content=message,
            direction="incoming",
            intent=intent,
            sentiment=sentiment
        )
        db.add(log)
        db.commit()
    
    def _log_conversation(self, phone: str, message: str, response: str, intent: str, sentiment: str, agent_type: str, db):
        """Registra la conversación completa"""
        conversation = Conversation(
            user_phone=phone,
            message=message,
            response=response,
            intent=intent,
            sentiment=sentiment,
            agent_type=agent_type,
            is_human=False
        )
        db.add(conversation)
        db.commit()
    
    def _update_user(self, phone: str, db):
        """Actualiza información del usuario"""
        user = db.query(User).filter(User.phone == phone).first()
        
        if not user:
            user = User(phone=phone)
            db.add(user)
        
        user.last_interaction = datetime.now()
        db.commit()
    
    def enable_human_takeover(self, phone: str, agent_id: str):
        """Activa el modo de control humano"""
        context_manager.enable_human_takeover(phone, agent_id)
        return f"✅ Control humano activado para {phone}"
    
    def disable_human_takeover(self, phone: str):
        """Desactiva el modo de control humano"""
        context_manager.disable_human_takeover(phone)
        return f"✅ Bot reactivado para {phone}"

message_handler = MessageHandler()
