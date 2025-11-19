"""
Agente de Ventas LOCAL (Sin IA)
Usa solo base de conocimiento y datos reales
"""
from agents.base_agent import BaseAgent
from ai.knowledge_base import knowledge_base
from ai.sales_reasoning import sales_reasoning, SalesContext, SalesStage
from database.connection import SessionLocal
from database.models import Product
from config.settings import settings
from typing import Dict, List

class LocalSalesAgent(BaseAgent):
    """Agente de ventas que funciona 100% local sin IA"""
    
    def __init__(self):
        super().__init__(
            "Agente de Ventas Local",
            "Experto en ventas usando solo base de conocimiento"
        )
        self.sales_contexts = {}  # Almacena contextos de ventas por usuario
    
    def get_system_prompt(self) -> str:
        """Retorna el prompt del sistema (no usado en modo local)"""
        return f"""Agente de Ventas Local de {settings.BUSINESS_NAME}.
Funciona 100% con base de conocimiento sin necesidad de IA."""
    
    async def process_message(self, phone: str, message: str, context: dict) -> str:
        """Procesa el mensaje usando SOLO base de conocimiento"""
        
        from ai.conversation_context import conversation_context_manager
        
        # Obtener contexto conversacional
        conv_context = conversation_context_manager.get_context(phone)
        
        # Detectar intención
        intent = knowledge_base.detect_intent(message)
        
        # Analizar contexto del mensaje
        is_about_current = conv_context.is_talking_about_product(message)
        wants_change = conv_context.wants_to_change_product(message)
        new_product_category = conv_context.extract_new_product_from_message(message)
        
        # Preparar contexto para knowledge_base
        kb_context = {
            'current_products': conv_context.current_products,
            'current_category': conv_context.current_category,
            'stage': conv_context.stage,
            'buying_signals': conv_context.buying_signals,
            'is_talking_about_product': is_about_current,
            'wants_to_change_product': wants_change,
            'new_product_category': new_product_category
        }
        
        # Generar respuesta usando base de conocimiento
        response = await knowledge_base.generate_response(message, kb_context)
        
        # Actualizar contexto conversacional
        conv_context.update_stage(intent)
        conv_context.increment_buying_signals(intent)
        conv_context.add_message(message, intent, response)
        
        # Actualizar productos si cambiaron
        if kb_context.get('current_products') != conv_context.current_products:
            conv_context.current_products = kb_context.get('current_products', [])
            conv_context.current_category = kb_context.get('current_category')
        
        # Post-procesar respuesta
        final_response = self._post_process_response(response, kb_context)
        
        return final_response
    
    def _post_process_response(self, response: str, sales_ctx: Dict) -> str:
        """Post-procesa la respuesta para asegurar calidad"""
        
        # Limitar longitud
        if len(response) > 450:
            cut_point = response[:450].rfind('.')
            if cut_point > 300:
                response = response[:cut_point + 1]
            else:
                cut_point = response[:450].rfind('\n')
                if cut_point > 300:
                    response = response[:cut_point]
                else:
                    response = response[:447] + "..."
        
        # Agregar información de pago si está en cierre
        if sales_ctx.get('buying_signals', 0) >= 2:
            if 'pago' not in response.lower() and 'nequi' not in response.lower():
                if len(response) < 350:
                    response += f"\n\n💳 Aceptamos: Nequi, Daviplata, Transferencia"
        
        return response

local_sales_agent = LocalSalesAgent()
