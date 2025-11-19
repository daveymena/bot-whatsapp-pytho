"""
Script de diagnóstico completo del bot
Prueba todas las funcionalidades implementadas
"""
import asyncio
import sys
sys.path.insert(0, '.')

from whatsapp.message_handler import message_handler
from ai.hybrid_response_system import hybrid_system
from database.connection import init_db

async def test_bot_responses():
    """Prueba las respuestas del bot con diferentes mensajes"""
    
    print("=" * 80)
    print("🔍 DIAGNÓSTICO COMPLETO DEL BOT")
    print("=" * 80)
    
    # Inicializar BD
    init_db()
    
    # Estado del sistema híbrido
    status = hybrid_system.get_status()
    print(f"\n📊 Estado Sistema Híbrido:")
    print(f"   - IA Habilitada: {status['ai_enabled']}")
    print(f"   - Fallos IA: {status['ai_failures']}")
    print(f"   - Modo Actual: {status['current_mode']}")
    
    # Teléfono de prueba
    test_phone = "573001234567"
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Saludo inicial",
            "message": "Hola",
            "expected": ["Alex", "Tecnovariedades", "ayudarte"]
        },
        {
            "name": "Búsqueda de producto",
            "message": "Busco audífonos",
            "expected": ["producto", "precio", "stock", "📦", "💰"]
        },
        {
            "name": "Consulta de precio",
            "message": "Cuánto cuesta?",
            "expected": ["precio", "$", "COP"]
        },
        {
            "name": "Métodos de pago",
            "message": "Cómo puedo pagar?",
            "expected": ["Nequi", "Daviplata", "MercadoPago", "PayPal"]
        },
        {
            "name": "Intención de compra",
            "message": "Lo quiero",
            "expected": ["perfecto", "nombre", "ciudad"]
        }
    ]
    
    print("\n" + "=" * 80)
    print("🧪 EJECUTANDO PRUEBAS")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Prueba {i}/{len(test_cases)}: {test['name']}")
        print(f"{'─' * 80}")
        print(f"📨 Mensaje: '{test['message']}'")
        
        try:
            # Procesar mensaje
            response = await message_handler.handle_message(test_phone, test['message'])
            
            print(f"\n✅ Respuesta recibida ({len(response)} caracteres):")
            print("─" * 80)
            print(response)
            print("─" * 80)
            
            # Verificar palabras esperadas
            found_keywords = []
            missing_keywords = []
            
            for keyword in test['expected']:
                if keyword.lower() in response.lower():
                    found_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)
            
            if found_keywords:
                print(f"\n✅ Palabras clave encontradas: {', '.join(found_keywords)}")
            
            if missing_keywords:
                print(f"⚠️  Palabras clave faltantes: {', '.join(missing_keywords)}")
            
            # Verificar longitud
            if len(response) < 50:
                print(f"⚠️  ADVERTENCIA: Respuesta muy corta ({len(response)} caracteres)")
            elif len(response) > 200:
                print(f"✅ Respuesta completa ({len(response)} caracteres)")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Estado final del sistema
    print("\n" + "=" * 80)
    print("📊 ESTADO FINAL DEL SISTEMA")
    print("=" * 80)
    
    final_status = hybrid_system.get_status()
    print(f"   - IA Habilitada: {final_status['ai_enabled']}")
    print(f"   - Fallos IA: {final_status['ai_failures']}")
    print(f"   - Modo Actual: {final_status['current_mode']}")
    
    if final_status['ai_failures'] > 0:
        print(f"\n⚠️  ADVERTENCIA: Se detectaron {final_status['ai_failures']} fallos de IA")
        print("   El sistema está usando la base de conocimiento como fallback")
    else:
        print("\n✅ Sistema funcionando correctamente con IA")
    
    print("\n" + "=" * 80)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_bot_responses())
