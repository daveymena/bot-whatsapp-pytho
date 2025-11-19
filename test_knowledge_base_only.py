"""
Prueba del bot usando SOLO la base de conocimiento (sin IA)
"""
import asyncio
import sys
sys.path.insert(0, '.')

from ai.knowledge_base import knowledge_base
from ai.hybrid_response_system import hybrid_system
from database.connection import init_db

async def test_knowledge_base():
    """Prueba las respuestas usando solo la base de conocimiento"""
    
    print("=" * 80)
    print("🧠 PRUEBA DE BASE DE CONOCIMIENTO (SIN IA)")
    print("=" * 80)
    
    # Inicializar BD
    init_db()
    
    # Desactivar IA para forzar uso de base de conocimiento
    hybrid_system.use_ai = False
    hybrid_system.ai_failures = hybrid_system.max_failures
    
    print(f"\n📊 Estado: {hybrid_system.get_status()}")
    
    # Contexto de prueba
    context = {
        'phone': '573001234567',
        'current_products': [],
        'current_category': None,
        'awaiting_payment_method': False
    }
    
    # Casos de prueba
    test_cases = [
        "Hola",
        "Busco audífonos",
        "Cuánto cuesta?",
        "Cómo puedo pagar?",
        "Lo quiero"
    ]
    
    print("\n" + "=" * 80)
    print("🧪 EJECUTANDO PRUEBAS")
    print("=" * 80)
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Prueba {i}/{len(test_cases)}")
        print(f"{'─' * 80}")
        print(f"📨 Mensaje: '{message}'")
        
        try:
            # Generar respuesta
            response = await knowledge_base.generate_response(message, context)
            
            print(f"\n✅ Respuesta ({len(response)} caracteres):")
            print("─" * 80)
            print(response)
            print("─" * 80)
            
            # Verificar longitud
            if len(response) < 50:
                print(f"⚠️  Respuesta corta ({len(response)} caracteres)")
            else:
                print(f"✅ Respuesta completa ({len(response)} caracteres)")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 80)
    print("\n💡 La base de conocimiento funciona como fallback cuando:")
    print("   - No hay API keys de Groq")
    print("   - Se alcanza el límite de requests")
    print("   - Hay errores en la API de IA")

if __name__ == "__main__":
    asyncio.run(test_knowledge_base())
