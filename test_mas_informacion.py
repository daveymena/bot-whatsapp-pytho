"""
Test específico para "más información" sin IA
"""
import asyncio
import sys
sys.path.insert(0, '.')

from ai.knowledge_base import knowledge_base
from ai.hybrid_response_system import hybrid_system
from database.connection import init_db

async def test_mas_informacion():
    print("=" * 80)
    print("🧪 TEST: Solicitud de MÁS INFORMACIÓN (SIN IA)")
    print("=" * 80)
    
    init_db()
    
    # Forzar modo sin IA
    hybrid_system.use_ai = False
    hybrid_system.ai_failures = 3
    
    print(f"\n📊 Modo: {hybrid_system.get_status()['current_mode']}\n")
    
    # Contexto inicial
    context = {
        'phone': '573001234567',
        'current_products': [],
        'awaiting_payment_method': False
    }
    
    # Paso 1: Cliente busca producto
    print("━" * 80)
    print("PASO 1: Cliente busca producto")
    print("━" * 80)
    mensaje1 = "Estoy interesado en el curso de piano"
    print(f"👤 Cliente: {mensaje1}\n")
    
    respuesta1 = await knowledge_base.generate_response(mensaje1, context)
    print(f"🤖 Bot:\n{respuesta1}\n")
    
    # Paso 2: Cliente pide más información
    print("━" * 80)
    print("PASO 2: Cliente pide MÁS INFORMACIÓN")
    print("━" * 80)
    mensaje2 = "Tienes más información"
    print(f"👤 Cliente: {mensaje2}\n")
    
    respuesta2 = await knowledge_base.generate_response(mensaje2, context)
    print(f"🤖 Bot:\n{respuesta2}\n")
    
    # Análisis
    print("━" * 80)
    print("📊 ANÁLISIS")
    print("━" * 80)
    
    if len(respuesta2) > 200:
        print("✅ Respuesta detallada (más de 200 caracteres)")
    else:
        print(f"⚠️  Respuesta corta ({len(respuesta2)} caracteres)")
    
    if "descripción" in respuesta2.lower() or "información" in respuesta2.lower():
        print("✅ Proporciona información detallada")
    
    if "$" in respuesta2 and "COP" in respuesta2:
        print("✅ Incluye precio")
    
    if "stock" in respuesta2.lower() or "disponible" in respuesta2.lower():
        print("✅ Incluye disponibilidad")
    
    if "?" in respuesta2:
        print("✅ Termina con pregunta")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_mas_informacion())
