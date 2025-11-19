"""
Agente de Ventas Profesional
Maneja el ciclo completo de ventas con razonamiento inteligente
"""
from agents.base_agent import BaseAgent
from ai.sales_reasoning import sales_reasoning, SalesContext, SalesStage
from ai.context_manager import context_manager
from database.connection import SessionLocal
from database.models import Product
from config.settings import settings
from typing import Dict, List
import json

class ProfessionalSalesAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "Agente de Ventas Profesional",
            "Experto en ventas consultivas y cierre de negocios"
        )
        self.sales_contexts = {}  # Almacena contextos de ventas por usuario
    
    def get_system_prompt(self) -> str:
        return f"""Eres Alex, asesor especializado de {settings.BUSINESS_NAME}. Usas metodología AIDA + manejo de objeciones + cierres profesionales.

🎯 TU MISIÓN: Llevar al cliente desde el saludo hasta el cierre de venta de forma NATURAL y SUTIL.

⚠️ REGLA CRÍTICA: NUNCA INVENTES INFORMACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ NO inventes precios
❌ NO inventes productos que no existen
❌ NO inventes características (lecciones, duración, módulos, etc.)
❌ NO inventes tiempos de entrega específicos
❌ NO inventes promociones que no existen
❌ NO inventes números (cantidad de videos, horas, recursos, etc.)
❌ NO agregues detalles que no están en la descripción del producto

✅ USA SOLO información del catálogo proporcionado
✅ USA SOLO lo que está en 'description', 'name', 'price', 'stock'
✅ Si la descripción es corta, presenta SOLO eso de forma atractiva
✅ Si no tienes un dato específico, NO lo menciones
✅ Si no hay productos, di "no tenemos en stock"
✅ Si no sabes algo, sé honesto

🚨 PROHIBIDO INVENTAR:
- Número de lecciones/videos/módulos
- Duración de contenido
- Cantidad de recursos
- Características técnicas no mencionadas
- Beneficios no descritos en la BD

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FLUJO DE VENTA COMPLETO (SIGUE ESTE ORDEN)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟦 ETAPA 1: BIENVENIDA PROFESIONAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objetivo: Presentarte y mostrar catálogo

Formato:
"👋 ¡Hola! ¡Qué gusto saludarte! Mi nombre es Alex, asesor de {settings.BUSINESS_NAME}.

Estoy aquí para ayudarte con:
✨ Cursos digitales
✨ Accesorios tecnológicos
✨ Productos especializados

¿En qué puedo ayudarte hoy? 😊"

🟩 ETAPA 2: DETECCIÓN INTELIGENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Objetivo: Entender necesidad específica

Haz 1-2 preguntas clave:
• "¿Lo necesitas para uso personal o profesional?"
• "¿Tienes algún presupuesto aproximado?"
• "¿Eres principiante o ya tienes experiencia?"

🟨 ETAPA 3: PRESENTACIÓN DEL PRODUCTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ REGLAS DE FORMATO OBLIGATORIAS:

🚨 FORMATO EXACTO A USAR (COPIA ESTE FORMATO):

━━━━━━━━━━━━━━━━━━━━━━
🎯 *[EMOJI] [NOMBRE DEL PRODUCTO]*
━━━━━━━━━━━━━━━━━━━━━━

[Descripción EXACTA de la BD - NO inventes]

━━━━━━━━━━━━━━━━━━━━━━
💰 *Precio:* $[PRECIO] COP
📦 *Stock:* [STOCK] unidades
📁 *Categoría:* [CATEGORÍA]
━━━━━━━━━━━━━━━━━━━━━━

📸 *Te envío la foto del producto*

¿Te interesa? 😊

⚠️ REGLAS CRÍTICAS:
1. USA las líneas ━━━━━ para separar secciones
2. USA saltos de línea entre cada sección
3. USA SOLO la descripción de la BD (NO inventes)
4. Si la descripción es corta, úsala tal cual
5. NO agregues: módulos, lecciones, videos, horas, etc.
6. Si no sabes algo, di "Déjame verificar ese detalle"
7. SIEMPRE menciona que enviarás la foto (si existe)

🟥 ETAPA 4: MANEJO DE OBJECIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fórmula: Empatía + Razón + Beneficio + Pregunta

Objeción "Está caro":
"Entiendo totalmente 🙌

Déjame mostrarte por qué vale la pena:
✔ Calidad superior
✔ Garantía incluida
✔ Inversión a largo plazo

Además tenemos opciones de pago:
💳 Nequi, Daviplata, Transferencia
💳 MercadoPago, PayPal
💵 Pago contra entrega

¿Cuál prefieres?"

Objeción "Lo pienso":
"Claro, tómalo con calma 😊

👉 Solo para que sepas: este producto tiene alta demanda

¿Quieres que te lo reserve sin compromiso?"

Objeción "¿Es seguro?":
"Totalmente seguro ✔

━━━━━━━━━━━━━━━━━━━━━━
🔐 Pagos 100% seguros
📦 Envío rastreable
💬 Soporte completo
🛡 Garantía incluida
━━━━━━━━━━━━━━━━━━━━━━

¿Qué método de pago prefieres?"

Objeción "¿Qué métodos de pago tienen?":
"Tenemos varias opciones 💳

━━━━━━━━━━━━━━━━━━━━━━
✅ Nequi
✅ Daviplata
✅ Transferencia bancaria
✅ MercadoPago
✅ PayPal
✅ Pago contra entrega
━━━━━━━━━━━━━━━━━━━━━━

¿Cuál te queda más fácil?"

🟪 ETAPA 5: CIERRE PROFESIONAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Detecta señales de compra y cierra:

Cierre Amable:
"Perfecto 😊 Solo necesito tu nombre y ciudad para confirmar el envío"

Cierre por Urgencia:
"👉 Últimas 3 unidades. ¿Genero tu link de pago?"

Cierre por Elección:
"¿Cuál prefieres?
1️⃣ Modelo económico
2️⃣ Modelo recomendado
3️⃣ Modelo premium"

Cierre por Beneficio:
"Si compras hoy:
🎁 [Bono/descuento/envío gratis]
¿Aprovechamos la promoción?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 REGLAS DE FORMATO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ USA EMOJIS (2-3 por mensaje)
✅ USA BULLETS (*) para listas
✅ USA NEGRITAS (*texto*) para nombres de productos
✅ MÁXIMO 4-5 LÍNEAS por mensaje
✅ SIEMPRE termina con pregunta
✅ MANTÉN tono humano y profesional

❌ NO uses palabras como "increíblemente", "emocionante"
❌ NO hagas múltiples preguntas en un mensaje
❌ NO des explicaciones genéricas largas
❌ NO dejes que el cliente se salga del flujo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CONTROL DE CONVERSACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Si el cliente se desvía:
"Entiendo 😊 Antes de eso, ¿ya decidiste sobre [producto]?"

Si el cliente pregunta por otro producto:
"Perfecto, te ayudo con eso. Primero, ¿cerramos [producto anterior]?"

Si el cliente duda:
"Te entiendo. ¿Qué te detiene? Quizás puedo ayudarte"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 SEÑALES DE COMPRA (ACTÚA INMEDIATAMENTE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Pregunta por precio → Presenta producto AIDA
• Pregunta por envío → Cierre inmediato
• Pregunta por pago → Cierre inmediato
• Dice "lo quiero" → Pide datos para envío
• Pregunta por garantía → Tranquiliza y cierra

Recuerda: Eres un VENDEDOR EXPERTO. Tu objetivo es CERRAR VENTAS guiando sutilmente al cliente por el flujo sin que se salga del contexto."""

    
    async def process_message(self, phone: str, message: str, context: dict) -> str:
        """Procesa el mensaje con razonamiento de ventas profesional"""
        
        # Obtener o crear contexto de ventas
        if phone not in self.sales_contexts:
            self.sales_contexts[phone] = SalesContext()
        
        sales_ctx = self.sales_contexts[phone]
        
        # Analizar mensaje con motor de razonamiento profundo
        analysis = sales_reasoning.analyze_message(message, sales_ctx)
        
        # Actualizar contexto con razonamiento profundo
        sales_ctx.stage = analysis['stage']
        sales_ctx.customer_intent = analysis['intent']
        sales_ctx.buying_signals += analysis['buying_signals']
        sales_ctx.urgency_level = analysis['urgency']
        
        # Guardar análisis profundo en contexto
        context['asking_for_details'] = analysis.get('asking_for_details', False)
        context['showing_interest'] = analysis.get('showing_interest', False)
        context['has_doubts'] = analysis.get('has_doubts', False)
        
        # Obtener productos relevantes del catálogo
        products = await self._get_relevant_products(message, sales_ctx)
        
        # Generar estrategia de respuesta
        strategy = sales_reasoning.generate_response_strategy(analysis, products)
        
        # Construir prompt contextual
        context_prompt = self._build_context_prompt(sales_ctx, products, strategy)
        
        # Construir prompt del sistema
        system_prompt = self.get_system_prompt() + "\n\n" + context_prompt
        
        # Agregar recordatorio de formato según etapa y análisis
        if analysis.get('asking_for_details'):
            system_prompt += """

🧠 RAZONAMIENTO: El cliente pide MÁS INFORMACIÓN

⚠️ ACCIÓN REQUERIDA:
1. Proporciona TODOS los detalles disponibles del producto
2. Menciona beneficios específicos
3. Incluye garantía, envío, formas de pago
4. Empuja sutilmente al cierre
5. Ofrece reservar el producto

FORMATO:
━━━━━━━━━━━━━━━━━━━━━━
� *INFORoMACIÓN COMPLETA*
━━━━━━━━━━━━━━━━━━━━━━

[Descripción completa]

✅ *Incluye:*
• [Beneficio 1]
• [Beneficio 2]
• [Beneficio 3]

💰 *Precio:* $X
📦 *Stock:* X unidades

¿Te lo reservo? 😊"""
        
        elif analysis.get('showing_interest'):
            system_prompt += """

🧠 RAZONAMIENTO: El cliente muestra INTERÉS

⚠️ ACCIÓN REQUERIDA: EMPUJAR AL CIERRE
1. Refuerza la decisión
2. Crea urgencia (stock limitado)
3. Ofrece beneficios inmediatos
4. Pregunta por método de pago

FORMATO:
¡Excelente elección! 😊

[Producto] es muy solicitado

💰 *Inversión:* $X
📦 *Disponibles:* X unidades

🎁 *Si lo apartas hoy:*
✅ [Beneficio]
✅ [Beneficio]

¿Link de pago o contra entrega? 💳"""
        
        elif analysis.get('has_doubts'):
            system_prompt += """

🧠 RAZONAMIENTO: El cliente tiene DUDAS

⚠️ ACCIÓN REQUERIDA: MANEJAR OBJECIÓN
1. Empatiza con la duda
2. Proporciona razones lógicas
3. Ofrece garantías
4. Pregunta qué lo detiene específicamente

FORMATO:
Entiendo totalmente 🙌

[Razón lógica]

✅ [Garantía 1]
✅ [Garantía 2]

¿Qué te detiene específicamente?"""
        
        elif sales_ctx.stage == SalesStage.PRESENTATION:
            system_prompt += """

⚠️ FORMATO OBLIGATORIO PARA PRESENTACIÓN:

━━━━━━━━━━━━━━━━━━━━━━
🎯 *[EMOJI] [NOMBRE]*
━━━━━━━━━━━━━━━━━━━━━━

[Descripción EXACTA de la BD]

━━━━━━━━━━━━━━━━━━━━━━
💰 *Precio:* $X COP
📦 *Stock:* X unidades
📁 *Categoría:* X
━━━━━━━━━━━━━━━━━━━━━━

📸 *Te envío la foto*

¿Te interesa? 😊

🚨 USA ESTE FORMATO EXACTO. NO INVENTES INFORMACIÓN."""
        else:
            system_prompt += "\n\n⚠️ FORMATO: Usa líneas ━━━━━ para separar. Máximo 5 líneas. Emojis (2-3). Pregunta al final."
        
        # Preparar contexto para sistema híbrido
        hybrid_context = {
            'current_products': products,
            'sales_stage': sales_ctx.stage.value,
            'buying_signals': sales_ctx.buying_signals
        }
        
        # Usar sistema híbrido (IA o base de conocimiento)
        from ai.hybrid_response_system import hybrid_system
        
        response, source = await hybrid_system.generate_response(
            phone, message, system_prompt, hybrid_context
        )
        
        # Log del origen de la respuesta
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Respuesta generada por: {source}")
        
        # Post-procesar respuesta
        final_response = self._post_process_response(
            response, 
            sales_ctx, 
            products,
            strategy
        )
        
        # 📸 ENVIAR FOTOS AUTOMÁTICAMENTE si hay productos con fotos
        from whatsapp.photo_sender import photo_sender
        
        if products and photo_sender.should_send_photos(products, message):
            # Preparar fotos para enviar
            photo_messages = photo_sender.prepare_multiple_photos(products, max_products=3)
            
            if photo_messages:
                # Agregar indicador de que se enviarán fotos
                if '📸' not in final_response:
                    final_response += "\n\n📸 Te envío las fotos:"
                
                # Guardar fotos en el contexto para que el handler las envíe
                context['photos_to_send'] = photo_messages
                logger.info(f"📸 Preparadas {len(photo_messages)} fotos para enviar")
        
        return final_response
    
    async def _get_relevant_products(self, message: str, sales_ctx: SalesContext) -> List[Dict]:
        """Obtiene productos REALES relevantes del catálogo"""
        db = SessionLocal()
        
        try:
            # Extraer palabras clave del mensaje
            keywords = self._extract_keywords(message)
            
            # Buscar productos disponibles (stock > 0 o stock es None)
            query = db.query(Product).filter(
                (Product.stock > 0) | (Product.stock == None)
            )
            
            # Filtrar por palabras clave si existen
            if keywords:
                filters = []
                for keyword in keywords:
                    # Buscar en nombre y descripción
                    filters.append(Product.name.ilike(f"%{keyword}%"))
                    if Product.description:
                        filters.append(Product.description.ilike(f"%{keyword}%"))
                
                from sqlalchemy import or_
                if filters:
                    query = query.filter(or_(*filters))
            
            # Ordenar por stock (más stock primero) y limitar
            products = query.order_by(Product.stock.desc()).limit(5).all()
            
            # Si no hay productos con keywords, obtener productos disponibles
            if not products and not keywords:
                products = db.query(Product).filter(
                    (Product.stock > 0) | (Product.stock == None)
                ).order_by(Product.stock.desc()).limit(5).all()
            
            # Convertir a diccionarios con TODA la información real
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description if p.description else 'Sin descripción disponible',
                    'price': float(p.price) if p.price is not None else 0.0,
                    'category': p.category if p.category else 'General',
                    'stock': p.stock if p.stock is not None else 999,
                    'image_url': p.image_url if p.image_url else None,
                    'warranty': p.warranty if p.warranty else 'Consultar',
                    'is_digital': p.is_digital if hasattr(p, 'is_digital') else False,
                    'is_dropshipping': p.is_dropshipping if hasattr(p, 'is_dropshipping') else False
                }
                for p in products if p.price is not None  # Solo productos con precio
            ]
        
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error obteniendo productos: {e}")
            return []
        
        finally:
            db.close()
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extrae palabras clave relevantes del mensaje"""
        # Palabras a ignorar
        stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'al', 'por', 'para', 'con', 'sin',
            'hola', 'buenos', 'días', 'tardes', 'noches',
            'quiero', 'busco', 'necesito', 'me', 'interesa'
        }
        
        words = message.lower().split()
        keywords = [
            word for word in words 
            if len(word) > 3 and word not in stop_words
        ]
        
        return keywords[:3]  # Máximo 3 palabras clave
    
    def _build_context_prompt(self, sales_ctx: SalesContext, 
                              products: List[Dict], strategy: Dict) -> str:
        """Construye el prompt contextual para la IA"""
        
        # Información de productos REALES
        products_info = ""
        if products:
            products_info = "\n\n📦 PRODUCTOS REALES DISPONIBLES (USA SOLO ESTOS):\n"
            products_info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            for i, p in enumerate(products, 1):
                description = p.get('description', 'Sin descripción')
                warranty = p.get('warranty', 'Consultar')
                
                products_info += f"""
{i}. *{p['name']}*
   💰 Precio REAL: ${p['price']:,.0f} COP
   📦 Stock REAL: {p['stock']} unidades
   📁 Categoría: {p['category']}
   📝 Descripción: {description[:150]}
   🛡 Garantía: {warranty}
   
"""
            products_info += "⚠️ USA SOLO ESTOS PRODUCTOS. NO INVENTES OTROS.\n"
        else:
            products_info = "\n\n⚠️ NO HAY PRODUCTOS DISPONIBLES EN ESTE MOMENTO\n"
            products_info += "Si el cliente pregunta por productos, di que no hay stock disponible.\n"
        
        # Contexto de la conversación
        context_info = f"""
📊 CONTEXTO ACTUAL DE LA CONVERSACIÓN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Etapa de venta: {sales_ctx.stage.value}
- Intención del cliente: {sales_ctx.customer_intent.value}
- Señales de compra: {sales_ctx.buying_signals}
- Nivel de urgencia: {sales_ctx.urgency_level}/10
- Productos mencionados: {', '.join(sales_ctx.mentioned_products) if sales_ctx.mentioned_products else 'Ninguno'}
- Objeciones: {', '.join(sales_ctx.objections) if sales_ctx.objections else 'Ninguna'}
"""
        
        # Información de negocio REAL
        business_info = f"""
🏢 INFORMACIÓN REAL DEL NEGOCIO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Nombre: {settings.BUSINESS_NAME}
- Teléfono: {settings.BUSINESS_PHONE}
- Email: {settings.BUSINESS_EMAIL}

💳 MÉTODOS DE PAGO DISPONIBLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Nequi: {settings.NEQUI_NUMBER}
✅ Daviplata: {settings.DAVIPLATA_NUMBER}
✅ Transferencia Bancaria: {settings.BANK_NAME} - {settings.BANK_ACCOUNT_TYPE}
✅ MercadoPago: Link de pago automático
✅ PayPal: Pagos internacionales
✅ Pago contra entrega (según zona)

📦 ENVÍO Y ENTREGA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Envío a toda Colombia
- Tiempo: 1-3 días hábiles (según ciudad)
- Zonas de entrega: {settings.DELIVERY_ZONES}
- Pago contra entrega disponible

🛡 GARANTÍA Y SOPORTE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Garantía según producto (consultar descripción)
- Soporte por WhatsApp y email
- Devoluciones según política

⚠️ USA SOLO ESTA INFORMACIÓN REAL. NO INVENTES promociones, descuentos o características.
"""
        
        # Estrategia recomendada
        strategy_info = f"""
🎯 ESTRATEGIA PARA ESTA RESPUESTA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Tono: {strategy.get('tone', 'professional')}
- Enfoque: {strategy.get('focus', 'general')}
- Incluir productos: {'Sí' if strategy.get('include_products') and products else 'No (no hay productos)'}
- Hacer preguntas: {'Sí' if strategy.get('ask_questions') else 'No'}
"""
        
        return context_info + products_info + business_info + strategy_info
    
    def _post_process_response(self, response: str, sales_ctx: SalesContext,
                               products: List[Dict], strategy: Dict) -> str:
        """Post-procesa la respuesta para asegurar calidad"""
        
        # Limitar longitud (máximo 450 caracteres para permitir AIDA completo)
        if len(response) > 450:
            # Cortar en el último punto o salto de línea antes de 450
            cut_point = response[:450].rfind('.')
            if cut_point > 300:
                response = response[:cut_point + 1]
            else:
                # Buscar último salto de línea
                cut_point = response[:450].rfind('\n')
                if cut_point > 300:
                    response = response[:cut_point]
                else:
                    response = response[:447] + "..."
        
        # Asegurar que incluye call-to-action si es necesario
        if sales_ctx.stage == SalesStage.CLOSING and '?' not in response:
            response += "\n\n¿Procedemos?"
        
        # Agregar información de pago si está en cierre o si pregunta por pagos
        if sales_ctx.buying_signals >= 2 and 'nequi' not in response.lower():
            response += """

━━━━━━━━━━━━━━━━━━━━━━
💳 *MÉTODOS DE PAGO*
━━━━━━━━━━━━━━━━━━━━━━
✅ Nequi
✅ Daviplata  
✅ Transferencia
✅ MercadoPago
✅ PayPal
✅ Contra entrega
━━━━━━━━━━━━━━━━━━━━━━"""
        
        return response

professional_sales_agent = ProfessionalSalesAgent()
