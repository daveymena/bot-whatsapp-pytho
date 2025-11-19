"""
Script para probar el flujo AIDA completo del bot
"""
import asyncio
from whatsapp.message_handler import message_handler

async def test_aida_flow():
    """Prueba el flujo AIDA completo"""
    
    print("=" * 70)
    print("🧪 PRUEBA DEL FLUJO AIDA COMPLETO")
    print("=" * 70)
    print()
    
    phone = "573001234567"
    
    # Conversación completa siguiendo AIDA
    conversations = [
        {
            "name": "ESCENARIO 1: Curso Digital",
            "messages": [
                "Hola, buenas",
                "Estoy buscando un curso de piano",
                "Soy principiante",
                "Sí, me interesa. ¿Cuánto cuesta?",
                "Está un poco caro",
                "Ok, lo quiero"
            ]
        },
        {
            "name": "ESCENARIO 2: Producto Físico",
            "messages": [
                "Hola",
                "Busco audífonos",
                "Para música",
                "¿Tienen garantía?",
                "Perfecto, ¿cómo pago?"
            ]
        }
    ]
    
    for scenario in conversations:
        print("\n" + "=" * 70)
        print(f"📋 {scenario['name']}")
        print("=" * 70)
        print()
        
        for i, msg in enumerate(scenario['messages'], 1):
            print(f"👤 Cliente: {msg}")
            print("-" * 70)
            
            try:
                response = await message_handler.handle_message(phone, msg)
                print(f"🤖 Bot ({len(response)} caracteres):")
                print(response)
                print()
                
                # Análisis de la respuesta
                has_emoji = any(char in response for char in "👋🎹📦💰✅🚚⏰🔥💳🎁")
                has_question = '?' in response
                has_bullets = '*' in response or '•' in response
                
                print("📊 Análisis:")
                print(f"  ✅ Emojis: {'Sí' if has_emoji else 'No'}")
                print(f"  ✅ Pregunta al final: {'Sí' if has_question else 'No'}")
                print(f"  ✅ Formato bullets: {'Sí' if has_bullets else 'No'}")
                print(f"  ✅ Longitud: {len(response)} caracteres")
                print()
                
                # Esperar un poco para simular conversación real
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print()
        
        print("\n" + "=" * 70)
        print(f"✅ {scenario['name']} COMPLETADO")
        print("=" * 70)
        print("\n\n")
    
    print("=" * 70)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_aida_flow())
