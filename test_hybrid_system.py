"""
Script para probar el sistema híbrido (IA + Base de Conocimiento)
"""
import asyncio
from ai.hybrid_response_system import hybrid_system
from ai.knowledge_base import knowledge_base

async def test_hybrid_system():
    """Prueba el sistema híbrido"""
    
    print("=" * 70)
    print("🧪 PRUEBA DEL SISTEMA HÍBRIDO")
    print("=" * 70)
    print()
    
    phone = "573001234567"
    context = {}
    
    # Pruebas con diferentes tipos de mensajes
    test_messages = [
        ("Hola", "Saludo"),
        ("Busco audífonos", "Búsqueda de producto"),
        ("¿Cuánto cuesta?", "Consulta de precio"),
        ("Está muy caro", "Objeción de precio"),
        ("¿Cómo pago?", "Consulta de pago"),
        ("¿Tienen garantía?", "Consulta de garantía"),
        ("Lo quiero", "Intención de compra"),
    ]
    
    print("📊 Estado inicial del sistema:")
    status = hybrid_system.get_status()
    print(f"  - IA habilitada: {status['ai_enabled']}")
    print(f"  - Modo actual: {status['current_mode']}")
    print()
    
    for message, description in test_messages:
        print(f"📝 {description}")
        print(f"👤 Cliente: {message}")
        print("-" * 70)
        
        try:
            # Generar respuesta con sistema híbrido
            response, source = await hybrid_system.generate_response(
                phone, message, "Eres un asesor de ventas profesional", context
            )
            
            print(f"🤖 Bot ({source}):")
            print(response)
            print()
            
            # Mostrar análisis
            print(f"📊 Origen: {source.upper()}")
            print(f"   Longitud: {len(response)} caracteres")
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 70)
    print("📊 Estado final del sistema:")
    status = hybrid_system.get_status()
    print(f"  - IA habilitada: {status['ai_enabled']}")
    print(f"  - Fallos de IA: {status['ai_failures']}")
    print(f"  - Modo actual: {status['current_mode']}")
    print()
    
    print("=" * 70)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 70)

async def test_knowledge_base_only():
    """Prueba solo la base de conocimiento"""
    
    print("\n\n")
    print("=" * 70)
    print("🧪 PRUEBA DE BASE DE CONOCIMIENTO (SIN IA)")
    print("=" * 70)
    print()
    
    context = {}
    
    test_messages = [
        "Hola buenos días",
        "Busco un curso de piano",
        "¿Cuánto cuesta?",
        "Está caro",
        "¿Cómo pago?",
        "Lo quiero"
    ]
    
    for message in test_messages:
        print(f"👤 Cliente: {message}")
        print("-" * 70)
        
        # Detectar intención
        intent = knowledge_base.detect_intent(message)
        print(f"🎯 Intención detectada: {intent}")
        
        # Generar respuesta
        response = knowledge_base.generate_response(message, context)
        print(f"🤖 Bot:")
        print(response)
        print()
    
    print("=" * 70)
    print("✅ PRUEBA DE BASE DE CONOCIMIENTO COMPLETADA")
    print("=" * 70)

async def test_objection_handling():
    """Prueba el manejo de objeciones"""
    
    print("\n\n")
    print("=" * 70)
    print("🧪 PRUEBA DE MANEJO DE OBJECIONES")
    print("=" * 70)
    print()
    
    context = {}
    
    objections = [
        ("Está muy caro", "Objeción de precio"),
        ("Lo voy a pensar", "Objeción de decisión"),
        ("¿Es seguro comprar aquí?", "Objeción de confianza"),
    ]
    
    for objection, description in objections:
        print(f"📝 {description}")
        print(f"👤 Cliente: {objection}")
        print("-" * 70)
        
        response = knowledge_base.handle_objection(objection, context)
        print(f"🤖 Bot:")
        print(response)
        print()
    
    print("=" * 70)
    print("✅ PRUEBA DE OBJECIONES COMPLETADA")
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DEL SISTEMA HÍBRIDO\n")
    
    # Ejecutar todas las pruebas
    asyncio.run(test_hybrid_system())
    asyncio.run(test_knowledge_base_only())
    asyncio.run(test_objection_handling())
    
    print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS\n")
