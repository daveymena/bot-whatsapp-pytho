"""
Script de prueba para el Sistema de Ventas Profesional con IA
"""
import asyncio
from agents.professional_sales_agent import professional_sales_agent
from ai.sales_reasoning import sales_reasoning, SalesContext
from database.connection import SessionLocal
from database.models import Product

async def test_sales_flow():
    """Prueba el flujo completo de ventas"""
    
    print("=" * 60)
    print("🧪 PRUEBA DEL SISTEMA DE VENTAS PROFESIONAL")
    print("=" * 60)
    print()
    
    # Teléfono de prueba
    test_phone = "573001234567"
    
    # Escenario 1: Saludo
    print("📱 Escenario 1: Saludo Inicial")
    print("-" * 60)
    message1 = "Hola"
    print(f"Cliente: {message1}")
    response1 = await professional_sales_agent.process_message(test_phone, message1, {})
    print(f"Bot: {response1}")
    print()
    
    # Escenario 2: Búsqueda de producto
    print("📱 Escenario 2: Búsqueda de Producto")
    print("-" * 60)
    message2 = "Busco audífonos bluetooth"
    print(f"Cliente: {message2}")
    response2 = await professional_sales_agent.process_message(test_phone, message2, {})
    print(f"Bot: {response2}")
    print()
    
    # Escenario 3: Pregunta por precio
    print("📱 Escenario 3: Pregunta por Precio")
    print("-" * 60)
    message3 = "¿Cuánto cuestan?"
    print(f"Cliente: {message3}")
    response3 = await professional_sales_agent.process_message(test_phone, message3, {})
    print(f"Bot: {response3}")
    print()
    
    # Escenario 4: Objeción de precio
    print("📱 Escenario 4: Objeción de Precio")
    print("-" * 60)
    message4 = "Están muy caros"
    print(f"Cliente: {message4}")
    response4 = await professional_sales_agent.process_message(test_phone, message4, {})
    print(f"Bot: {response4}")
    print()
    
    # Escenario 5: Señal de compra
    print("📱 Escenario 5: Señal de Compra")
    print("-" * 60)
    message5 = "Ok, me convenciste. ¿Cómo compro?"
    print(f"Cliente: {message5}")
    response5 = await professional_sales_agent.process_message(test_phone, message5, {})
    print(f"Bot: {response5}")
    print()
    
    # Mostrar contexto final
    if test_phone in professional_sales_agent.sales_contexts:
        ctx = professional_sales_agent.sales_contexts[test_phone]
        print("📊 CONTEXTO FINAL")
        print("-" * 60)
        print(f"Etapa: {ctx.stage.value}")
        print(f"Intención: {ctx.customer_intent.value}")
        print(f"Señales de compra: {ctx.buying_signals}")
        print(f"Urgencia: {ctx.urgency_level}/10")
        print(f"Productos mencionados: {ctx.mentioned_products}")
        print(f"Objeciones: {ctx.objections}")
        print()
    
    print("=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

async def test_reasoning_engine():
    """Prueba el motor de razonamiento"""
    
    print("\n" + "=" * 60)
    print("🧠 PRUEBA DEL MOTOR DE RAZONAMIENTO")
    print("=" * 60)
    print()
    
    test_messages = [
        "Hola, buenos días",
        "Busco audífonos bluetooth",
        "¿Cuánto cuestan?",
        "Están muy caros",
        "Lo quiero comprar"
    ]
    
    ctx = SalesContext()
    
    for msg in test_messages:
        print(f"Mensaje: '{msg}'")
        analysis = sales_reasoning.analyze_message(msg, ctx)
        print(f"  Etapa: {analysis['stage'].value}")
        print(f"  Intención: {analysis['intent'].value}")
        print(f"  Señales de compra: {analysis['buying_signals']}")
        print(f"  Objeciones: {analysis['objections']}")
        print(f"  Acción recomendada: {analysis['recommended_action']}")
        print()
        
        # Actualizar contexto
        ctx.stage = analysis['stage']
        ctx.customer_intent = analysis['intent']
        ctx.buying_signals += analysis['buying_signals']

async def test_product_access():
    """Prueba el acceso al catálogo de productos"""
    
    print("\n" + "=" * 60)
    print("📦 PRUEBA DE ACCESO AL CATÁLOGO")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        # Obtener productos
        products = db.query(Product).filter(Product.stock > 0).limit(5).all()
        
        if products:
            print(f"✅ Encontrados {len(products)} productos en el catálogo:")
            print()
            for p in products:
                print(f"  • {p.name}")
                print(f"    Precio: ${p.price:,.0f} COP")
                print(f"    Stock: {p.stock} unidades")
                print(f"    Categoría: {p.category}")
                print()
        else:
            print("⚠️  No hay productos en el catálogo")
            print("   Agrega productos desde el dashboard para probar el sistema")
    
    finally:
        db.close()

async def main():
    """Ejecuta todas las pruebas"""
    
    print("\n")
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE VENTAS PROFESIONAL")
    print()
    
    # Prueba 1: Acceso al catálogo
    await test_product_access()
    
    # Prueba 2: Motor de razonamiento
    await test_reasoning_engine()
    
    # Prueba 3: Flujo completo de ventas
    await test_sales_flow()
    
    print("\n")
    print("🎉 TODAS LAS PRUEBAS COMPLETADAS")
    print()
    print("Próximos pasos:")
    print("1. Reinicia el servidor Python: python main.py")
    print("2. Envía un mensaje de WhatsApp al bot")
    print("3. Observa el sistema en acción")
    print()

if __name__ == "__main__":
    asyncio.run(main())
