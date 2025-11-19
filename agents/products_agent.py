from agents.base_agent import BaseAgent
from config.settings import settings
from sqlalchemy.orm import Session
from database.models import Product
from database.connection import SessionLocal
from whatsapp.multimedia_handler import multimedia_handler
from ai.context_manager import context_manager
import re

class ProductsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agente de Productos", "Especialista en catálogo y productos")
    
    def get_system_prompt(self) -> str:
        return f"""Eres el {self.name} de {settings.BUSINESS_NAME}, experto en nuestro catálogo completo.

TU ESPECIALIDAD:
- Conocimiento profundo de todos los productos
- Productos físicos, digitales y dropshipping
- Especificaciones técnicas y características
- Comparativas entre productos
- Recomendaciones personalizadas

TIPOS DE PRODUCTOS:
1. FÍSICOS: Electrónica, tecnología, accesorios
2. DIGITALES: Cursos online, megapacks, ebooks
3. DROPSHIPPING: Productos Dropi con envío directo

INFORMACIÓN QUE PROPORCIONAS:
- Descripción detallada
- Precio y formas de pago
- Disponibilidad y stock
- Tiempo de entrega
- Garantías y políticas
- Fotos y especificaciones

TÉCNICAS DE VENTA:
- Cross-selling: Productos complementarios
- Up-selling: Versiones premium
- Bundles: Paquetes con descuento
- Urgencia: Stock limitado, ofertas temporales

COMANDOS ESPECIALES:
- "catálogo" o "productos" → Mostrar catálogo con fotos
- "buscar [nombre]" → Buscar producto específico
- "categoría [nombre]" → Filtrar por categoría
- "fotos" o "imágenes" → Enviar fotos del producto actual
- "más fotos" → Enviar imágenes adicionales

ESTILO:
- Entusiasta sobre los productos
- Detallista pero conciso
- Usa comparaciones y ejemplos
- Destaca beneficios sobre características
- Responde dudas técnicas con claridad
- SIEMPRE envía fotos cuando sea posible

Cuando un cliente pregunte por productos, busca en la base de datos, envía fotos y presenta opciones relevantes con entusiasmo profesional."""
    
    async def process_message(self, phone: str, message: str, context: dict) -> str:
        """Procesa mensajes relacionados con productos"""
        message_lower = message.lower()
        
        # Detectar comandos
        if any(word in message_lower for word in ["catálogo", "catalogo", "productos", "qué tienen", "que tienen"]):
            return await self._show_catalog(phone, message)
        
        elif any(word in message_lower for word in ["buscar", "busco", "necesito", "quiero ver"]):
            return await self._search_product(phone, message)
        
        elif any(word in message_lower for word in ["categoría", "categoria", "tipo"]):
            return await self._filter_by_category(phone, message)
        
        elif any(word in message_lower for word in ["fotos", "imágenes", "imagenes", "foto", "imagen", "ver"]):
            return await self._send_product_photos(phone, context)
        
        elif any(word in message_lower for word in ["más fotos", "mas fotos", "otras fotos"]):
            return await self._send_more_photos(phone, context)
        
        # Buscar producto por nombre mencionado
        return await self._smart_search(phone, message)
    
    async def _show_catalog(self, phone: str, message: str) -> str:
        """Muestra el catálogo completo con fotos"""
        # Detectar si hay categoría específica
        category = None
        if "electrónica" in message.lower() or "electronica" in message.lower():
            category = "Electrónica"
        elif "tecnología" in message.lower() or "tecnologia" in message.lower():
            category = "Tecnología"
        
        await multimedia_handler.send_catalog(phone, category=category)
        
        return "Te envié nuestro catálogo con fotos! 📸 Escribe el número del producto que te interese para ver más detalles."
    
    async def _search_product(self, phone: str, message: str) -> str:
        """Busca un producto específico"""
        # Extraer nombre del producto
        patterns = [
            r"buscar\s+(.+)",
            r"busco\s+(.+)",
            r"necesito\s+(.+)",
            r"quiero ver\s+(.+)"
        ]
        
        product_name = None
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                product_name = match.group(1).strip()
                break
        
        if not product_name:
            return "¿Qué producto estás buscando? Dime el nombre y te muestro fotos y detalles."
        
        # Buscar en base de datos
        result = await multimedia_handler.send_product_by_name(phone, product_name)
        
        if result:
            # Guardar en contexto
            context_manager.update_context(phone, current_product=product_name)
            return f"Te envié la información y fotos de {product_name}! ¿Te gustaría comprarlo?"
        else:
            return f"No encontré '{product_name}'. ¿Quieres ver el catálogo completo?"
    
    async def _filter_by_category(self, phone: str, message: str) -> str:
        """Filtra productos por categoría"""
        # Extraer categoría
        categories = ["electrónica", "tecnología", "accesorios", "hogar", "deportes"]
        
        category = None
        for cat in categories:
            if cat in message.lower():
                category = cat.capitalize()
                break
        
        if not category:
            return "¿Qué categoría te interesa? Tenemos: Electrónica, Tecnología, Accesorios, Hogar, Deportes."
        
        await multimedia_handler.send_catalog(phone, category=category)
        
        return f"Te envié los productos de {category} con fotos! 📸"
    
    async def _send_product_photos(self, phone: str, context: dict) -> str:
        """Envía fotos del producto actual"""
        current_product = context.get('current_product')
        
        if not current_product:
            return "¿De qué producto quieres ver fotos? Dime el nombre o número."
        
        result = await multimedia_handler.send_product_by_name(phone, current_product)
        
        if result:
            return "Te envié las fotos! 📸 ¿Qué te parece?"
        else:
            return "No pude encontrar fotos de ese producto. ¿Quieres ver otro?"
    
    async def _send_more_photos(self, phone: str, context: dict) -> str:
        """Envía fotos adicionales del producto"""
        current_product = context.get('current_product')
        
        if not current_product:
            return "¿De qué producto quieres ver más fotos?"
        
        db = SessionLocal()
        product = db.query(Product).filter(
            Product.name.ilike(f"%{current_product}%")
        ).first()
        db.close()
        
        if product and product.id:
            await multimedia_handler.send_product_images(phone, product.id)
            return "Te envié todas las fotos disponibles! 📸"
        else:
            return "No tengo más fotos de ese producto."
    
    async def _smart_search(self, phone: str, message: str) -> str:
        """Búsqueda inteligente basada en palabras clave"""
        db = SessionLocal()
        
        # Buscar productos que coincidan con palabras del mensaje
        words = message.lower().split()
        products = []
        
        for word in words:
            if len(word) > 3:  # Ignorar palabras muy cortas
                results = db.query(Product).filter(
                    Product.name.ilike(f"%{word}%") | 
                    Product.description.ilike(f"%{word}%")
                ).limit(3).all()
                products.extend(results)
        
        db.close()
        
        if products:
            # Eliminar duplicados
            unique_products = list({p.id: p for p in products}.values())
            
            if len(unique_products) == 1:
                # Un solo producto encontrado
                product = unique_products[0]
                await multimedia_handler.send_product_images(phone, product.id)
                context_manager.update_context(phone, current_product=product.name)
                return f"Encontré este producto que podría interesarte! 📦"
            else:
                # Múltiples productos
                await multimedia_handler.send_catalog(phone, products=unique_products[:5])
                return f"Encontré {len(unique_products)} productos relacionados! ¿Cuál te interesa?"
        
        return "Cuéntame más sobre lo que buscas para ayudarte mejor."
    
    async def search_products(self, db: Session, query: str, category: str = None):
        filters = []
        if category:
            filters.append(Product.category == category)
        
        if query:
            filters.append(
                Product.name.ilike(f"%{query}%") | 
                Product.description.ilike(f"%{query}%")
            )
        
        products = db.query(Product).filter(*filters).all()
        return products
