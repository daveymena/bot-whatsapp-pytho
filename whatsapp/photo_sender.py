"""
Módulo para enviar fotos de productos automáticamente
"""
import os
import logging
from typing import List, Dict, Optional
from database.connection import SessionLocal
from database.models import Product

logger = logging.getLogger(__name__)

class PhotoSender:
    """Maneja el envío automático de fotos de productos"""
    
    def __init__(self):
        self.smart_photos_enabled = os.getenv('SMART_PHOTOS_ENABLED', 'true').lower() == 'true'
        self.auto_send_photos = os.getenv('AUTO_SEND_PHOTOS', 'true').lower() == 'true'
        self.max_photos_per_product = int(os.getenv('SMART_PHOTOS_MAX_PER_PRODUCT', '3'))
    
    def should_send_photos(self, products: List[Dict], message: str) -> bool:
        """Determina si se deben enviar fotos basado en el contexto"""
        
        if not self.smart_photos_enabled or not self.auto_send_photos:
            return False
        
        # Siempre enviar fotos si hay productos disponibles
        if not products:
            return False
        
        # Verificar si algún producto tiene foto
        has_photos = any(p.get('image_url') or p.get('images') for p in products)
        
        return has_photos
    
    def get_product_photos(self, product: Dict) -> List[str]:
        """Obtiene las URLs de fotos de un producto"""
        photos = []
        
        # Foto principal
        if product.get('image_url'):
            photos.append(product['image_url'])
        
        # Fotos adicionales
        if product.get('images') and isinstance(product['images'], list):
            for img in product['images']:
                if img and img not in photos:
                    photos.append(img)
                    if len(photos) >= self.max_photos_per_product:
                        break
        
        return photos
    
    def prepare_photo_message(self, product: Dict, include_details: bool = True) -> Dict:
        """Prepara el mensaje con foto del producto"""
        
        photos = self.get_product_photos(product)
        
        if not photos:
            return None
        
        # Construir caption con información del producto
        caption = ""
        
        if include_details:
            caption = f"""📸 *{product['name']}*

💰 *Precio:* ${product['price']:,.0f} COP
📦 *Stock:* {product['stock']} unidades disponibles
"""
            
            # Agregar categoría si existe
            if product.get('category'):
                caption += f"📁 *Categoría:* {product['category']}\n"
            
            # Agregar descripción corta si existe
            if product.get('description'):
                desc = product['description'][:100]
                if len(product['description']) > 100:
                    desc += "..."
                caption += f"\n{desc}\n"
        
        return {
            'photos': photos,
            'caption': caption.strip(),
            'product_id': product['id'],
            'product_name': product['name']
        }
    
    def prepare_multiple_photos(self, products: List[Dict], max_products: int = 3) -> List[Dict]:
        """Prepara fotos de múltiples productos"""
        
        photo_messages = []
        
        for product in products[:max_products]:
            photo_msg = self.prepare_photo_message(product, include_details=True)
            if photo_msg:
                photo_messages.append(photo_msg)
        
        return photo_messages
    
    def get_photo_instructions(self, product_name: str) -> str:
        """Genera instrucciones para cuando no hay foto disponible"""
        
        return f"""📸 *Foto de {product_name}*

Lo siento, actualmente no tengo la foto de este producto disponible en el sistema.

¿Te gustaría que:
1️⃣ Te envíe más información del producto
2️⃣ Te muestre productos similares con fotos
3️⃣ Te contacte con un asesor para enviarte la foto

¿Qué prefieres? 😊"""
    
    def format_product_with_photo_indicator(self, product: Dict) -> str:
        """Formatea la información del producto indicando si tiene foto"""
        
        has_photo = bool(product.get('image_url') or product.get('images'))
        photo_indicator = "📸" if has_photo else "📄"
        
        text = f"""{photo_indicator} *{product['name']}*
💰 ${product['price']:,.0f} COP
📦 Stock: {product['stock']} unidades
"""
        
        if has_photo:
            text += "✅ Foto disponible\n"
        else:
            text += "⚠️ Sin foto disponible\n"
        
        return text

# Instancia global
photo_sender = PhotoSender()
