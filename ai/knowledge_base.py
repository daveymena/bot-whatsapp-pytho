"""
Base de Conocimiento para respuestas sin IA
Sistema híbrido que funciona cuando no hay tokens disponibles
"""
from typing import Dict, List, Optional, Tuple
import re
from database.connection import SessionLocal
from database.models import Product
from config.settings import settings

class KnowledgeBase:
    """Base de conocimiento para respuestas automáticas"""
    
    def __init__(self):
        self.greetings = [
            "hola", "buenos días", "buenas tardes", "buenas noches",
            "hey", "saludos", "qué tal", "cómo estás"
        ]
        
        self.product_keywords = {
            "audífonos": ["audifonos", "audifono", "auriculares", "headphones", "audífono", "auricular"],
            "teclado": ["teclado", "keyboard", "teclados"],
            "mouse": ["mouse", "ratón", "raton", "mice"],
            "laptop": ["laptop", "portátil", "portatil", "notebook", "computador", "computadora", "pc"],
            "curso": ["curso", "clase", "lección", "leccion", "aprender", "cursos", "clases"],
            "piano": ["piano", "pianos"],
            "guitarra": ["guitarra", "guitarras"],
            "bolso": ["bolso", "mochila", "maleta", "cartera", "bolsos", "mochilas"],
            "webcam": ["webcam", "camara", "cámara", "cam"],
            "microfono": ["microfono", "micrófono", "mic"],
            "parlante": ["parlante", "altavoz", "bocina", "speaker", "parlantes"],
            "cable": ["cable", "cables"],
            "cargador": ["cargador", "cargadores", "adaptador"],
            "memoria": ["memoria", "usb", "pendrive", "sd", "microsd"]
        }
        
        self.price_keywords = [
            "cuánto", "cuanto", "precio", "cuesta", "vale", "valor", "costo"
        ]
        
        self.payment_keywords = [
            "pago", "pagar", "forma de pago", "método de pago", "como pago"
        ]
        
        self.shipping_keywords = [
            "envío", "envio", "entrega", "delivery", "cuándo llega", "cuando llega"
        ]
        
        self.warranty_keywords = [
            "garantía", "garantia", "devolución", "devolucion", "cambio"
        ]
        
        self.buy_keywords = [
            "lo quiero", "lo compro", "comprar", "compro", "adquirir"
        ]
        
        self.affirmative_keywords = [
            "sí", "si", "ok", "dale", "perfecto", "excelente", "genial", "bueno"
        ]
    
    def detect_intent(self, message: str) -> str:
        """Detecta la intención del mensaje"""
        message_lower = message.lower()
        
        # Saludo (solo si es mensaje corto y no tiene otras palabras clave)
        if any(greeting in message_lower for greeting in self.greetings):
            # Si solo es saludo, retornar greeting
            if len(message_lower.split()) <= 3:
                return "greeting"
        
        # Búsqueda de producto (prioridad alta, pero no si es intención de compra)
        search_keywords = ["busco", "buscar", "necesito", "estoy buscando", "me gustaría ver"]
        if any(keyword in message_lower for keyword in search_keywords):
            return "product_inquiry"
        
        # "Quiero" puede ser búsqueda o compra, depende del contexto
        if "quiero" in message_lower:
            # Si dice "lo quiero", "los quiero", "la quiero" es compra
            if any(word in message_lower for word in ["lo quiero", "los quiero", "la quiero", "las quiero"]):
                return "purchase_intent"
            # Si dice "quiero un/una" es búsqueda
            elif any(word in message_lower for word in ["quiero un", "quiero una", "quiero el", "quiero la"]):
                return "product_inquiry"
        
        # Verificar si menciona algún producto específico
        for category, keywords in self.product_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return "product_inquiry"
        
        # Precio
        if any(keyword in message_lower for keyword in self.price_keywords):
            return "price_inquiry"
        
        # Pago
        if any(keyword in message_lower for keyword in self.payment_keywords):
            return "payment_inquiry"
        
        # Envío
        if any(keyword in message_lower for keyword in self.shipping_keywords):
            return "shipping_inquiry"
        
        # Garantía
        if any(keyword in message_lower for keyword in self.warranty_keywords):
            return "warranty_inquiry"
        
        # Compra
        if any(keyword in message_lower for keyword in self.buy_keywords):
            return "purchase_intent"
        
        # Afirmación (puede ser intención de compra si hay contexto)
        if any(keyword in message_lower for keyword in self.affirmative_keywords):
            # Si el mensaje es corto y afirmativo, probablemente es intención de compra
            if len(message_lower.split()) <= 3:
                return "purchase_intent"
        
        return "general"
    
    def extract_product_category(self, message: str) -> Optional[str]:
        """Extrae la categoría de producto del mensaje"""
        message_lower = message.lower()
        
        for category, keywords in self.product_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return None
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Obtiene productos de una categoría"""
        db = SessionLocal()
        try:
            from sqlalchemy import or_
            
            # Buscar productos que coincidan con la categoría
            keywords = self.product_keywords.get(category, [category])
            
            # Crear filtros de búsqueda
            filters = []
            for keyword in keywords:
                filters.append(Product.name.ilike(f"%{keyword}%"))
                if Product.description:
                    filters.append(Product.description.ilike(f"%{keyword}%"))
            
            # Buscar productos con stock
            if filters:
                products = db.query(Product).filter(
                    Product.stock > 0,
                    or_(*filters)
                ).limit(3).all()
            else:
                products = db.query(Product).filter(
                    Product.stock > 0
                ).limit(3).all()
            
            return [
                {
                    'id': p.id,
                    'name': p.name,
                    'description': p.description if p.description else 'Sin descripción',
                    'price': float(p.price),
                    'category': p.category if p.category else 'General',
                    'stock': p.stock
                }
                for p in products
            ]
        finally:
            db.close()
    
    async def generate_response(self, message: str, context: Dict) -> str:
        """Genera respuesta basada en reglas sin usar IA con razonamiento profundo"""
        intent = self.detect_intent(message)
        message_lower = message.lower()
        
        # Verificar si está hablando del producto actual
        is_about_current = context.get('is_talking_about_product', False)
        wants_change = context.get('wants_to_change_product', False)
        current_products = context.get('current_products', [])
        
        # RAZONAMIENTO: Detectar si pide más información sobre el producto actual
        asking_for_more_info = any(word in message_lower for word in [
            'más información', 'mas informacion', 'más info', 'mas info',
            'detalles', 'características', 'caracteristicas', 'más detalles',
            'mas detalles', 'cuéntame más', 'cuentame mas', 'qué más',
            'que mas', 'tienes más', 'tienes mas', 'información adicional',
            'informacion adicional', 'más datos', 'mas datos'
        ])
        
        # RAZONAMIENTO: Detectar si está interesado pero necesita convencimiento
        showing_interest = any(word in message_lower for word in [
            'interesado', 'interesada', 'me interesa', 'me gusta',
            'suena bien', 'se ve bien', 'parece bueno', 'parece bien'
        ])
        
        # SALUDO
        if intent == "greeting":
            return self._greeting_response()
        
        # SI PIDE MÁS INFORMACIÓN DEL PRODUCTO ACTUAL
        if asking_for_more_info and current_products:
            return self._detailed_product_info_response(current_products[0], context)
        
        # SI MUESTRA INTERÉS, EMPUJAR AL CIERRE
        if showing_interest and current_products:
            return self._interest_to_closing_response(current_products[0], context)
        
        # BÚSQUEDA DE PRODUCTO
        elif intent == "product_inquiry":
            category = self.extract_product_category(message)
            
            # Si quiere cambiar de producto
            if wants_change and current_products:
                return self._handle_product_change(message, category, context)
            
            return self._product_inquiry_response(category, context)
        
        # PRECIO (puede ser del producto actual o general)
        elif intent == "price_inquiry":
            if is_about_current or current_products:
                return self._price_inquiry_response(context)
            else:
                return "¿Qué producto te interesa? Te doy el precio 😊"
        
        # PAGO
        elif intent == "payment_inquiry":
            # Si ya está esperando selección de método, procesar
            if context.get('awaiting_payment_method'):
                return await self.process_payment_method_selection(message, context)
            return self._payment_inquiry_response(context)
        
        # ENVÍO
        elif intent == "shipping_inquiry":
            return self._shipping_inquiry_response(context)
        
        # GARANTÍA
        elif intent == "warranty_inquiry":
            return self._warranty_inquiry_response(context)
        
        # INTENCIÓN DE COMPRA
        elif intent == "purchase_intent":
            return self._purchase_intent_response(context)
        
        # GENERAL
        else:
            # Si está esperando método de pago, procesar
            if context.get('awaiting_payment_method'):
                return await self.process_payment_method_selection(message, context)
            
            # Si hay producto activo, puede ser una pregunta sobre él
            if current_products:
                return self._contextual_product_response(message, current_products[0], context)
            return self._general_response()
    
    def _greeting_response(self) -> str:
        """Respuesta de saludo"""
        return f"""👋 ¡Hola! ¡Qué gusto saludarte! Mi nombre es Alex, asesor de {settings.BUSINESS_NAME}.

Estoy aquí para ayudarte con:
✨ Cursos digitales
✨ Accesorios tecnológicos
✨ Productos especializados

¿En qué puedo ayudarte hoy? 😊"""
    
    def _product_inquiry_response(self, category: Optional[str], context: Dict) -> str:
        """Respuesta de búsqueda de producto"""
        if not category:
            return "¿Qué tipo de producto buscas? 😊"
        
        # Obtener productos REALES de la base de datos
        products = self.get_products_by_category(category)
        
        if not products:
            # Si no hay productos de esa categoría, buscar cualquier producto disponible
            db = SessionLocal()
            try:
                all_products = db.query(Product).filter(Product.stock > 0).limit(3).all()
                if all_products:
                    products = [
                        {
                            'id': p.id,
                            'name': p.name,
                            'description': p.description if p.description else 'Sin descripción',
                            'price': float(p.price),
                            'category': p.category if p.category else 'General',
                            'stock': p.stock
                        }
                        for p in all_products
                    ]
                else:
                    return f"""En este momento no tengo {category} en stock.

¿Te interesa ver otros productos disponibles? 😊"""
            finally:
                db.close()
        
        # Guardar productos en contexto
        context['current_products'] = products
        context['current_category'] = category
        
        # Presentar primer producto REAL con formato AIDA
        product = products[0]
        
        # Usar descripción real
        description = product['description'] if product['description'] != 'Sin descripción' else "Producto de calidad"
        
        # Limitar descripción a 80 caracteres
        if len(description) > 80:
            description = description[:77] + "..."
        
        response = f"""🔥 Perfecto! Tengo este producto disponible:

📦 *{product['name'][:60]}*
💰 ${product['price']:,.0f}
✅ {description}
📦 Stock: {product['stock']} unidades

¿Te interesa? 😊"""
        
        return response
    
    def _price_inquiry_response(self, context: Dict) -> str:
        """Respuesta de consulta de precio"""
        products = context.get('current_products', [])
        
        if not products:
            return "¿Qué producto te interesa? Te doy el precio 😊"
        
        product = products[0]
        
        # Usar solo información REAL del producto
        response = f"""💰 *{product['name']}*
Precio: ${product['price']:,.0f}
Stock disponible: {product['stock']} unidades

💳 Métodos de pago:
✅ Nequi
✅ Daviplata
✅ Transferencia

¿Te gustaría comprarlo? 😊"""
        
        return response
    
    def _payment_inquiry_response(self, context: Dict) -> str:
        """Respuesta de consulta de pago con opciones de links dinámicos"""
        products = context.get('current_products', [])
        
        base_response = """💳 *MÉTODOS DE PAGO DISPONIBLES*

1️⃣ *Mercado Pago* (Link automático)
   • Tarjetas crédito/débito
   • PSE
   • Hasta 12 cuotas

2️⃣ *PayPal* (Link automático)
   • Pagos internacionales

3️⃣ *Nequi* (Transferencia)
4️⃣ *Daviplata* (Transferencia)
5️⃣ *Transferencia Bancaria*
6️⃣ *Contra Entrega* 💵"""
        
        if products:
            product = products[0]
            base_response += f"\n\n¿Con cuál método quieres pagar *{product['name'][:40]}*?"
            base_response += "\n\nEscribe el número o nombre del método 😊"
        else:
            base_response += "\n\n¿Cuál prefieres? Escribe el número o nombre 😊"
        
        # Marcar que necesita procesar pago
        context['awaiting_payment_method'] = True
        
        return base_response
    
    async def process_payment_method_selection(self, method: str, context: Dict) -> str:
        """Procesa la selección de método de pago y genera links si es necesario"""
        from services.payment_service import payment_service
        
        method_lower = method.lower()
        products = context.get('current_products', [])
        
        if not products:
            return "Primero necesito que selecciones un producto. ¿Qué te gustaría comprar? 😊"
        
        # Preparar datos de la orden
        product = products[0]
        order_data = {
            'user_phone': context.get('phone', ''),
            'user_name': context.get('user_name', 'Cliente'),
            'products': [{
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            }],
            'subtotal': product['price'],
            'shipping': 0,
            'discount': 0,
            'total': product['price'],
            'delivery_address': context.get('delivery_address', '')
        }
        
        # Detectar método
        if any(word in method_lower for word in ["mercadopago", "mercado", "mp", "1", "tarjeta", "cuotas"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "mercadopago"
            )
            if result["success"]:
                # El link REAL ya fue enviado en un mensaje separado
                return f"✅ ¡Listo! Revisa el mensaje anterior con el link de Mercado Pago 💳\n\nPuedes pagar con tarjeta, PSE o hasta 12 cuotas sin interés 😊"
            return f"❌ Hubo un problema: {result.get('error', 'Error desconocido')}. Intenta con otro método 😊"
        
        elif any(word in method_lower for word in ["paypal", "2", "internacional"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "paypal"
            )
            if result["success"]:
                return f"✅ ¡Listo! Revisa el mensaje anterior con el link de PayPal 🌎\n\nPago internacional seguro con protección al comprador 😊"
            return f"❌ Hubo un problema: {result.get('error', 'Error desconocido')}. Intenta con otro método 😊"
        
        elif any(word in method_lower for word in ["nequi", "3"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "nequi"
            )
            if result["success"]:
                return "✅ Te envié la información de Nequi. Después de transferir, envíame el comprobante 📸"
            return "❌ Hubo un problema. Intenta nuevamente 😊"
        
        elif any(word in method_lower for word in ["daviplata", "4"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "daviplata"
            )
            if result["success"]:
                return "✅ Te envié la información de Daviplata. Después de transferir, envíame el comprobante 📸"
            return "❌ Hubo un problema. Intenta nuevamente 😊"
        
        elif any(word in method_lower for word in ["banco", "transferencia", "5"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "banco"
            )
            if result["success"]:
                return "✅ Te envié los datos bancarios. Después de transferir, envíame el comprobante 📸"
            return "❌ Hubo un problema. Intenta nuevamente 😊"
        
        elif any(word in method_lower for word in ["contraentrega", "contra entrega", "efectivo", "6", "cod"]):
            result = await payment_service.create_payment(
                context.get('phone', ''), order_data, "contraentrega"
            )
            if result["success"]:
                return "✅ Perfecto! Pagarás en efectivo al recibir tu pedido 💵"
            return "❌ Hubo un problema. Intenta nuevamente 😊"
        
        # Si no reconoce el método
        return """No reconocí ese método. Por favor elige uno:

1️⃣ Mercado Pago
2️⃣ PayPal
3️⃣ Nequi
4️⃣ Daviplata
5️⃣ Transferencia
6️⃣ Contra Entrega

Escribe el número o nombre 😊"""
    
    def _shipping_inquiry_response(self, context: Dict) -> str:
        """Respuesta de consulta de envío"""
        products = context.get('current_products', [])
        
        base_response = """🚚 Información de envío:

✅ Envío a toda Colombia
✅ Tiempo: 1-3 días hábiles
✅ Envío asegurado
✅ Guía de rastreo incluida"""
        
        if products:
            product = products[0]
            base_response += f"\n\n¿Confirmo el envío de *{product['name'][:40]}*? 😊"
        else:
            base_response += "\n\n¿A qué ciudad lo necesitas? 😊"
        
        return base_response
    
    def _warranty_inquiry_response(self, context: Dict) -> str:
        """Respuesta de consulta de garantía"""
        products = context.get('current_products', [])
        
        base_response = """🛡 Garantía incluida:

✅ 1 año de garantía
✅ Cambios por defecto de fábrica
✅ Soporte técnico
✅ Devolución si no estás satisfecho"""
        
        if products:
            product = products[0]
            base_response += f"\n\n¿Alguna otra duda sobre *{product['name'][:40]}*? 😊"
        else:
            base_response += "\n\n¿Tienes alguna otra duda? 😊"
        
        return base_response
    
    def _purchase_intent_response(self, context: Dict) -> str:
        """Respuesta de intención de compra"""
        products = context.get('current_products', [])
        
        if not products:
            return "¿Qué producto te gustaría comprar? 😊"
        
        product = products[0]
        
        # Si ya mostró métodos de pago, proceder con datos
        if context.get('awaiting_payment_method'):
            return f"""¡Perfecto! 😊 Vamos a procesar tu pedido de *{product['name'][:50]}*

Solo necesito:
* Tu nombre completo
* Ciudad de entrega

¿Me los compartes?"""
        
        # Si no, mostrar métodos de pago primero
        return f"""¡Excelente! 😊 Quieres *{product['name'][:50]}*

💰 Total: ${product['price']:,.0f}

¿Con cuál método quieres pagar?

1️⃣ Mercado Pago (Link automático)
2️⃣ PayPal
3️⃣ Nequi
4️⃣ Daviplata
5️⃣ Transferencia
6️⃣ Contra Entrega

Escribe el número o nombre 😊"""
    
    def _general_response(self) -> str:
        """Respuesta general"""
        return """Puedo ayudarte con:

✅ Ver productos disponibles
✅ Información de precios
✅ Métodos de pago
✅ Tiempos de envío
✅ Garantías

¿Qué te gustaría saber? 😊"""
    
    def _general_product_response(self, context: Dict) -> str:
        """Respuesta general sobre el producto actual"""
        products = context.get('current_products', [])
        if not products:
            return self._general_response()
        
        product = products[0]
        
        return f"""Sobre *{product['name'][:50]}*:

💰 Precio: ${product['price']:,.0f}
📦 Stock: {product['stock']} unidades
🛡 Garantía: Incluida

¿Qué más te gustaría saber? 😊"""
    
    def _detailed_product_info_response(self, product: Dict, context: Dict) -> str:
        """Respuesta detallada cuando piden más información"""
        
        # Construir respuesta con toda la información disponible
        response = f"""📋 *INFORMACIÓN COMPLETA*
━━━━━━━━━━━━━━━━━━━━━━

🎯 *{product['name'][:60]}*

📝 *Descripción:*
{product.get('description', 'Producto de alta calidad')}

━━━━━━━━━━━━━━━━━━━━━━
💰 *Precio:* ${product['price']:,.0f} COP
📦 *Stock:* {product['stock']} unidades
📁 *Categoría:* {product.get('category', 'General')}
━━━━━━━━━━━━━━━━━━━━━━

✅ *Incluye:*
• Garantía de calidad
• Soporte técnico
• Envío a toda Colombia

💳 *Formas de pago:*
• Nequi / Daviplata
• MercadoPago (cuotas)
• PayPal
• Contra entrega

🚚 *Envío:* 1-3 días hábiles

¿Te gustaría reservarlo? 😊"""
        
        return response
    
    def _interest_to_closing_response(self, product: Dict, context: Dict) -> str:
        """Respuesta cuando muestra interés - empujar al cierre"""
        
        return f"""¡Excelente elección! 😊

*{product['name'][:50]}* es uno de nuestros productos más solicitados.

━━━━━━━━━━━━━━━━━━━━━━
💰 *Inversión:* ${product['price']:,.0f}
📦 *Disponibles:* {product['stock']} unidades
━━━━━━━━━━━━━━━━━━━━━━

🎁 *Si lo apartas hoy:*
✅ Garantía incluida
✅ Envío asegurado
✅ Soporte completo

¿Quieres que te genere el link de pago o prefieres contra entrega? 💳"""
    
    def _contextual_product_response(self, message: str, product: Dict, context: Dict) -> str:
        """Respuesta contextual basada en el mensaje y producto actual"""
        
        message_lower = message.lower()
        
        # Si pregunta por características específicas
        if any(word in message_lower for word in ['cómo', 'como', 'funciona', 'sirve', 'usa']):
            return f"""Sobre *{product['name'][:50]}*:

{product.get('description', 'Es un producto de alta calidad diseñado para satisfacer tus necesidades.')}

💰 Precio: ${product['price']:,.0f}
📦 Stock: {product['stock']} unidades

¿Te gustaría comprarlo? 😊"""
        
        # Si pregunta por disponibilidad
        if any(word in message_lower for word in ['disponible', 'hay', 'tienen', 'queda']):
            return f"""✅ ¡Sí! Tenemos *{product['name'][:50]}* disponible

📦 Stock actual: {product['stock']} unidades
💰 Precio: ${product['price']:,.0f}

¿Lo apartamos para ti? 😊"""
        
        # Si pregunta por calidad
        if any(word in message_lower for word in ['calidad', 'bueno', 'recomendable', 'vale la pena']):
            return f"""¡Totalmente! *{product['name'][:50]}* es excelente

✅ Alta calidad
✅ Garantía incluida
✅ Muy solicitado
✅ Buenas opiniones

💰 ${product['price']:,.0f}
📦 {product['stock']} disponibles

¿Te lo reservo? 😊"""
        
        # Si pregunta por comparación
        if any(word in message_lower for word in ['mejor', 'diferencia', 'comparar', 'otro']):
            return f"""*{product['name'][:50]}* es nuestra mejor opción en esta categoría

✨ *Ventajas:*
• Excelente relación calidad-precio
• Garantía incluida
• Envío rápido
• Stock disponible

💰 ${product['price']:,.0f}

¿Quieres ver otros productos o te decides por este? 😊"""
        
        # Respuesta general con empuje al cierre
        return f"""Sobre *{product['name'][:50]}*:

💰 Precio: ${product['price']:,.0f}
📦 Stock: {product['stock']} unidades
✅ Garantía incluida

¿Qué más necesitas saber para decidirte? 😊"""
    
    def _handle_product_change(self, message: str, new_category: Optional[str], context: Dict) -> str:
        """Maneja el cambio de producto en la conversación"""
        current_product = context.get('current_products', [{}])[0]
        
        # Si menciona un nuevo producto
        if new_category:
            new_products = self.get_products_by_category(new_category)
            
            if new_products:
                context['current_products'] = new_products
                context['current_category'] = new_category
                
                new_product = new_products[0]
                
                return f"""Perfecto, también tengo {new_category}:

📦 *{new_product['name'][:60]}*
💰 ${new_product['price']:,.0f}
📦 Stock: {new_product['stock']} unidades

¿Te interesa este o prefieres el anterior? 😊"""
        
        # Si solo dice "otro" sin especificar
        return f"""¿Qué otro producto te gustaría ver?

Tengo:
✨ Accesorios tecnológicos
✨ Cursos digitales
✨ Productos especializados

¿Qué te interesa? 😊"""
    
    def handle_objection(self, objection_type: str, context: Dict) -> str:
        """Maneja objeciones comunes"""
        
        if "caro" in objection_type.lower() or "precio" in objection_type.lower():
            return """Entiendo totalmente 🙌 Déjame mostrarte por qué:

✔ Calidad superior
✔ Garantía real
✔ Ahorras a largo plazo

Además ofrecemos:
💳 Pago flexible
🚚 Envío asegurado

¿Te gustaría ver opciones de pago?"""
        
        elif "pensar" in objection_type.lower() or "después" in objection_type.lower():
            return """Claro, tómalo con calma 😊

👉 Solo para que sepas: este modelo tiene alto movimiento.

¿Quieres que te lo reserve sin compromiso?"""
        
        elif "seguro" in objection_type.lower() or "confianza" in objection_type.lower():
            return """Totalmente ✔

🔐 Pagos 100% seguros
📦 Envío rastreable
💬 Soporte completo
🛡 Garantía incluida

¿Te gustaría ver opiniones de clientes?"""
        
        else:
            return """Entiendo tu preocupación 😊

¿Qué te detiene específicamente? Quizás puedo ayudarte a resolverlo."""

knowledge_base = KnowledgeBase()
