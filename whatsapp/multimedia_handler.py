import os
from PIL import Image
from typing import Optional, List
import aiohttp
from config.settings import settings
from database.connection import SessionLocal
from database.models import Product

class MultimediaHandler:
    """Maneja envío y procesamiento de multimedia"""
    
    def __init__(self):
        self.temp_dir = "./temp-media"
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def send_product_image(self, phone: str, product_data: dict):
        """Envía imagen de producto con caption"""
        from whatsapp.baileys_client import baileys_client
        
        image_url = product_data.get("image_url")
        if not image_url:
            return False
        
        caption = f"""📦 *{product_data['name']}*

{product_data.get('description', '')}

💰 Precio: ${product_data['price']:,.0f} COP
📊 Stock: {product_data.get('stock', 'Disponible')}

¿Te interesa? ¡Escríbeme! 😊"""
        
        try:
            # Descargar imagen
            image_path = await self._download_image(image_url)
            
            # Optimizar imagen
            optimized_path = self.optimize_image(image_path)
            
            # Enviar imagen
            await baileys_client.send_image(phone, optimized_path, caption)
            
            # Limpiar archivos temporales
            os.remove(image_path)
            if optimized_path != image_path:
                os.remove(optimized_path)
            
            # Actualizar vistas del producto
            self._update_product_views(product_data.get('id'))
            
            return True
        except Exception as e:
            print(f"❌ Error enviando imagen: {e}")
            return False
    
    async def send_product_images(self, phone: str, product_id: int):
        """Envía todas las imágenes de un producto desde la base de datos"""
        from whatsapp.baileys_client import baileys_client
        
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        db.close()
        
        if not product:
            return False
        
        # Enviar imagen principal
        if product.image_url:
            await self.send_product_image(phone, {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'image_url': product.image_url
            })
        
        # Enviar imágenes adicionales si existen
        if product.images and isinstance(product.images, list):
            for i, img_url in enumerate(product.images[:3], 1):  # Máximo 3 adicionales
                try:
                    image_path = await self._download_image(img_url)
                    optimized_path = self.optimize_image(image_path)
                    
                    caption = f"📸 Imagen {i+1} de {product.name}"
                    await baileys_client.send_image(phone, optimized_path, caption)
                    
                    os.remove(image_path)
                    if optimized_path != image_path:
                        os.remove(optimized_path)
                except Exception as e:
                    print(f"❌ Error enviando imagen adicional: {e}")
        
        return True
    
    async def send_catalog(self, phone: str, products: list = None, category: str = None):
        """Envía catálogo de productos con imágenes"""
        from whatsapp.baileys_client import baileys_client
        
        db = SessionLocal()
        
        # Si no se proporcionan productos, obtener de la base de datos
        if products is None:
            query = db.query(Product).filter(Product.stock > 0)
            if category:
                query = query.filter(Product.category == category)
            products = query.limit(10).all()
        
        db.close()
        
        if not products:
            await baileys_client.send_message(phone, "No hay productos disponibles en este momento.")
            return
        
        # Enviar mensaje de catálogo
        catalog_text = "🛍️ *CATÁLOGO DE PRODUCTOS*\n\n"
        
        for i, product in enumerate(products[:10], 1):
            if isinstance(product, dict):
                catalog_text += f"{i}. *{product['name']}*\n"
                catalog_text += f"   💰 ${product['price']:,.0f} COP\n"
                catalog_text += f"   📦 Stock: {product.get('stock', 'Disponible')}\n\n"
            else:
                catalog_text += f"{i}. *{product.name}*\n"
                catalog_text += f"   💰 ${product.price:,.0f} COP\n"
                catalog_text += f"   📦 Stock: {product.stock}\n\n"
        
        catalog_text += "\n📱 Escribe el número del producto para ver fotos y detalles!"
        
        await baileys_client.send_message(phone, catalog_text)
        
        # Enviar imágenes de los primeros 3 productos
        for i, product in enumerate(products[:3]):
            if isinstance(product, dict):
                if product.get('image_url'):
                    await self.send_product_image(phone, product)
            else:
                if product.image_url:
                    await self.send_product_image(phone, {
                        'id': product.id,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'stock': product.stock,
                        'image_url': product.image_url
                    })
    
    async def send_product_by_name(self, phone: str, product_name: str):
        """Busca y envía un producto por nombre"""
        from whatsapp.baileys_client import baileys_client
        
        db = SessionLocal()
        product = db.query(Product).filter(
            Product.name.ilike(f"%{product_name}%")
        ).first()
        db.close()
        
        if not product:
            await baileys_client.send_message(
                phone, 
                f"No encontré ningún producto con el nombre '{product_name}'. ¿Quieres ver el catálogo completo?"
            )
            return False
        
        # Enviar todas las imágenes del producto
        await self.send_product_images(phone, product.id)
        
        # Enviar información detallada
        details = f"""📦 *{product.name}*

📝 *Descripción:*
{product.description or 'Sin descripción'}

💰 *Precio:* ${product.price:,.0f} COP
📊 *Stock:* {product.stock} unidades
📂 *Categoría:* {product.category or 'General'}"""
        
        if product.warranty:
            details += f"\n🛡️ *Garantía:* {product.warranty}"
        
        if product.variants:
            details += f"\n\n🎨 *Variantes disponibles:*"
            for variant in product.variants:
                details += f"\n• {variant}"
        
        details += "\n\n¿Te gustaría comprarlo? 🛒"
        
        await baileys_client.send_message(phone, details)
        
        return True
    
    def _update_product_views(self, product_id: int):
        """Actualiza el contador de vistas de un producto"""
        if not product_id:
            return
        
        db = SessionLocal()
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.views = (product.views or 0) + 1
            db.commit()
        db.close()
    
    async def send_payment_qr(self, phone: str, payment_data: dict):
        """Envía código QR de pago"""
        from whatsapp.baileys_client import baileys_client
        
        # Aquí iría la generación del QR
        # Por ahora enviamos la información de pago
        
        message = f"""💳 *INFORMACIÓN DE PAGO*

Pedido: #{payment_data['order_number']}
Total: ${payment_data['total']:,.0f} COP

*Métodos disponibles:*

1️⃣ Nequi: {settings.NEQUI_NUMBER}
2️⃣ Daviplata: {settings.DAVIPLATA_NUMBER}
3️⃣ Transferencia Bancaria
   Banco: {settings.BANK_NAME}
   Cuenta: {settings.BANK_ACCOUNT_NUMBER}

Envía tu comprobante de pago para confirmar! 📸"""
        
        await baileys_client.send_message(phone, message)
    
    async def send_invoice(self, phone: str, order_data: dict):
        """Envía factura del pedido"""
        from whatsapp.baileys_client import baileys_client
        
        invoice = f"""🧾 *FACTURA*

Pedido: #{order_data['order_number']}
Fecha: {order_data['created_at']}

*Cliente:*
{order_data['user_name']}
{order_data['user_phone']}

*Productos:*
"""
        
        for product in order_data['products']:
            invoice += f"• {product['name']} x{product['quantity']}\n"
            invoice += f"  ${product['price']:,.0f} COP\n"
        
        invoice += f"""
*Resumen:*
Subtotal: ${order_data['subtotal']:,.0f} COP
Envío: ${order_data['shipping']:,.0f} COP
Descuento: -${order_data['discount']:,.0f} COP
━━━━━━━━━━━━━━━━━━━━
*TOTAL: ${order_data['total']:,.0f} COP*

¡Gracias por tu compra! 🎉"""
        
        await baileys_client.send_message(phone, invoice)
    
    async def _download_image(self, url: str) -> str:
        """Descarga una imagen desde URL"""
        filename = f"{self.temp_dir}/{os.path.basename(url)}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await response.read())
        
        return filename
    
    def optimize_image(self, image_path: str, max_size: tuple = (1280, 1280)) -> str:
        """Optimiza una imagen para WhatsApp"""
        img = Image.open(image_path)
        
        # Redimensionar si es muy grande
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Guardar optimizada
        optimized_path = f"{self.temp_dir}/optimized_{os.path.basename(image_path)}"
        img.save(optimized_path, optimize=True, quality=85)
        
        return optimized_path

multimedia_handler = MultimediaHandler()
