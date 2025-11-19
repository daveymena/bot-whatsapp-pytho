"""
Script para probar el bot SOLO con base de conocimiento local (SIN IA)
"""
import asyncio
from ai.knowledge_base import knowledge_base

async def test_local_bot():
    """Prueba el bot solo con base de conocimiento"""
    
    print("=" * 70)
    print("🤖 PRUEBA DEL BOT LOCAL (SIN IA)")
    print("=" * 70)
    print()
    
    context = {}
    
    # Conversación completa de ventas
    conversation = [
        ("Hola", "Saludo inicial"),
        ("Busco audífonos", "Búsqueda de producto"),
        ("¿Cuánto cuestan?", "Consulta de precio"),
        ("¿Cómo pago?", "Métodos de pago"),
        ("¿Cuándo llega?", "Información de envío"),
        ("¿Tienen garantía?", "Consulta de garantía"),
        ("Está muy caro", "Objeción de precio"),
        ("Lo voy a pensar", "Objeción de decisión"),
        ("Ok, lo quiero", "Intención de compra"),
    ]
    
    for message, description in conversation:
        print(f"📝 {description}")
        print(f"👤 Cliente: {message}")
        print("-" * 70)
        
        # Detectar intención
        intent = knowledge_base.detect_intent(message)
        print(f"🎯 Intención: {intent}")
        
        # Generar respuesta
        response = knowledge_base.generate_response(message, context)
        
        print(f"🤖 Bot:")
        print(response)
        print()
        print(f"📊 Análisis:")
        print(f"   - Longitud: {len(response)} caracteres")
        print(f"   - Tiene emojis: {'Sí' if any(c in response for c in '👋🎹📦💰✅🚚⏰🔥💳🎁🛡') else 'No'}")
        print(f"   - Tiene pregunta: {'Sí' if '?' in response else 'No'}")
        print()
    
    print("=" * 70)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 70)
    print()
    
    # Mostrar productos en contexto
    if context.get('current_products'):
        print("📦 Productos en contexto:")
        for p in context['current_products']:
            print(f"   - {p['name']}: ${p['price']:,.0f} (Stock: {p['stock']})")

async def test_multiple_products():
    """Prueba búsqueda de múltiples productos"""
    
    print("\n\n")
    print("=" * 70)
    print("🔍 PRUEBA DE BÚSQUEDA DE PRODUCTOS")
    print("=" * 70)
    print()
    
    searches = [
        "Busco audífonos",
        "Necesito un teclado",
        "Quiero un mouse",
        "Busco un curso de piano",
        "Necesito una laptop",
    ]
    
    for search in searches:
        context = {}
        print(f"👤 Cliente: {search}")
        print("-" * 70)
        
        category = knowledge_base.extract_product_category(search)
        print(f"📁 Categoría detectada: {category}")
        
        response = knowledge_base.generate_response(search, context)
        print(f"🤖 Bot:")
        print(response)
        print()

async def test_conversation_flow():
    """Prueba flujo completo de conversación"""
    
    print("\n\n")
    print("=" * 70)
    print("💬 PRUEBA DE FLUJO DE CONVERSACIÓN COMPLETO")
    print("=" * 70)
    print()
    
    context = {}
    
    # Simular conversación real
    messages = [
        "Hola buenos días",
        "Estoy buscando audífonos bluetooth",
        "¿Cuánto cuestan?",
        "¿Qué garantía tienen?",
        "¿Puedo pagar con Nequi?",
        "Perfecto, lo quiero"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n{'='*70}")
        print(f"Mensaje {i}/{len(messages)}")
        print(f"{'='*70}")
        print(f"👤 Cliente: {message}")
        print()
        
        # Generar respuesta
        response = knowledge_base.generate_response(message, context)
        
        print(f"🤖 Bot:")
        print(response)
        print()
        
        # Esperar un poco para simular conversación real
        await asyncio.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("✅ CONVERSACIÓN COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DEL BOT LOCAL\n")
    
    # Ejecutar todas las pruebas
    asyncio.run(test_local_bot())
    asyncio.run(test_multiple_products())
    asyncio.run(test_conversation_flow())
    
    print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS\n")
