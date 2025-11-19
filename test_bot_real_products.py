"""
Test del bot con productos reales de la base de datos
"""
import asyncio
from whatsapp.message_handler import message_handler
from database.connection import SessionLocal
from database.models import Product

async def test_bot_responses():
    """Prueba respuestas del bot con productos reales"""
    
    print("\n" + "="*60)
    print("TEST: BOT CON PRODUCTOS REALES")
    print("="*60)
    
    # Verificar productos en BD
    db = SessionLocal()
    total_products = db.query(Product).count()
    products_with_price = db.query(Product).filter(Product.price != None).count()
    products_available = db.query(Product).filter(
        (Product.stock > 0) | (Product.stock == None)
    ).filter(Product.price != None).count()
    
    print(f"\n📊 PRODUCTOS EN BASE DE DATOS:")
    print(f"   Total: {total_products}")
    print(f"   Con precio: {products_with_price}")
    print(f"   Disponibles: {products_available}")
    
    # Obtener algunos productos de ejemplo
    sample_products = db.query(Product).filter(
        Product.price != None
    ).limit(5).all()
    
    print(f"\n📦 PRODUCTOS DE EJEMPLO:")
    for i, p in enumerate(sample_products, 1):
        print(f"\n{i}. {p.name}")
        print(f"   💰 Precio: ${float(p.price):,.0f}")
        print(f"   📦 Stock: {p.stock if p.stock else 'Disponible'}")
        print(f"   🏷️ Categoría: {p.category}")
    
    db.close()
    
    # Test de conversación
    test_phone = "573001234567"
    
    print(f"\n" + "="*60)
    print("SIMULACIÓN DE CONVERSACIÓN")
    print("="*60)
    
    test_messages = [
        "Hola",
        "Quiero ver productos",
        "Tienes laptops?",
        "Cuánto cuesta?",
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}] Cliente: {message}")
        response = await message_handler.handle_message(test_phone, message)
        print(f"[{i}] Bot: {response[:200]}..." if len(response) > 200 else f"[{i}] Bot: {response}")
        print("-" * 60)
        
        # Pequeña pausa entre mensajes
        await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    print("✅ TEST COMPLETADO")
    print("="*60)
    print("\n💡 Verifica que el bot:")
    print("   1. Muestra productos reales de tu base de datos")
    print("   2. Muestra precios correctos")
    print("   3. No inventa información")
    print("   4. Responde de forma natural")

if __name__ == "__main__":
    asyncio.run(test_bot_responses())
