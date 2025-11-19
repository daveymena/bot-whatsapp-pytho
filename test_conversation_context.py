"""
Script para probar la gestión de contexto conversacional
"""
import asyncio
from agents.local_sales_agent import local_sales_agent

async def test_single_product_conversation():
    """Prueba conversación sobre un solo producto"""
    
    print("=" * 70)
    print("🧪 PRUEBA: Conversación sobre UN producto")
    print("=" * 70)
    print()
    
    phone = "573001111111"
    
    messages = [
        "Hola",
        "Busco audífonos bluetooth",
        "¿Cuánto cuestan?",
        "¿Tienen garantía?",
        "¿Cómo pago?",
        "Perfecto, lo quiero"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📱 Mensaje {i}: {message}")
        print("-" * 70)
        
        response = await local_sales_agent.process_message(phone, message, {})
        
        print(f"🤖 Bot:")
        print(response)
        
        await asyncio.sleep(0.3)
    
    print("\n" + "=" * 70)
    print("✅ Conversación completada")
    print("=" * 70)

async def test_product_change_conversation():
    """Prueba conversación con cambio de producto"""
    
    print("\n\n")
    print("=" * 70)
    print("🧪 PRUEBA: Conversación con CAMBIO de producto")
    print("=" * 70)
    print()
    
    phone = "573002222222"
    
    messages = [
        "Hola",
        "Busco audífonos",
        "¿Cuánto cuestan?",
        "Están caros, ¿tienes teclados?",
        "¿Cuánto cuesta el teclado?",
        "Mejor me llevo los audífonos",
        "¿Cómo pago?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📱 Mensaje {i}: {message}")
        print("-" * 70)
        
        response = await local_sales_agent.process_message(phone, message, {})
        
        print(f"🤖 Bot:")
        print(response)
        
        await asyncio.sleep(0.3)
    
    print("\n" + "=" * 70)
    print("✅ Conversación completada")
    print("=" * 70)

async def test_multiple_products_conversation():
    """Prueba conversación sobre múltiples productos al mismo tiempo"""
    
    print("\n\n")
    print("=" * 70)
    print("🧪 PRUEBA: Conversación sobre MÚLTIPLES productos")
    print("=" * 70)
    print()
    
    phone = "573003333333"
    
    messages = [
        "Hola",
        "Necesito audífonos y un mouse",
        "¿Cuánto cuestan los audífonos?",
        "¿Y el mouse?",
        "¿Puedo llevar ambos?",
        "¿Cuánto sería el total?",
        "Ok, los quiero"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📱 Mensaje {i}: {message}")
        print("-" * 70)
        
        response = await local_sales_agent.process_message(phone, message, {})
        
        print(f"🤖 Bot:")
        print(response)
        
        await asyncio.sleep(0.3)
    
    print("\n" + "=" * 70)
    print("✅ Conversación completada")
    print("=" * 70)

async def test_context_continuity():
    """Prueba continuidad del contexto"""
    
    print("\n\n")
    print("=" * 70)
    print("🧪 PRUEBA: CONTINUIDAD del contexto")
    print("=" * 70)
    print()
    
    phone = "573004444444"
    
    messages = [
        "Hola",
        "Busco audífonos",
        "¿Cuánto cuestan?",
        "¿Qué garantía tienen?",  # Debe referirse a los audífonos
        "¿Cómo los pago?",  # Debe referirse a los audífonos
        "¿Cuándo llegan?",  # Debe referirse a los audífonos
        "Perfecto, los quiero"  # Debe referirse a los audífonos
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📱 Mensaje {i}: {message}")
        print("-" * 70)
        
        response = await local_sales_agent.process_message(phone, message, {})
        
        print(f"🤖 Bot:")
        print(response)
        
        # Verificar que mantiene contexto
        if i > 2:
            if "audífono" in response.lower() or "auricular" in response.lower():
                print("✅ Mantiene contexto del producto")
            else:
                print("⚠️  Posible pérdida de contexto")
        
        await asyncio.sleep(0.3)
    
    print("\n" + "=" * 70)
    print("✅ Conversación completada")
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DE CONTEXTO CONVERSACIONAL\n")
    
    # Ejecutar todas las pruebas
    asyncio.run(test_single_product_conversation())
    asyncio.run(test_product_change_conversation())
    asyncio.run(test_multiple_products_conversation())
    asyncio.run(test_context_continuity())
    
    print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS\n")
