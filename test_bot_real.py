"""
Script para probar el bot en tiempo real
Simula un mensaje de WhatsApp
"""
import asyncio
import sys
sys.path.insert(0, '.')

from whatsapp.message_handler import message_handler

async def test_real_message():
    """Prueba con un mensaje real"""
    
    print("=" * 60)
    print("🧪 PRUEBA DEL BOT EN TIEMPO REAL")
    print("=" * 60)
    print()
    
    test_phone = "573001234567"
    test_messages = [
        "Hola",
        "Busco audífonos",
        "¿Cuánto cuestan?",
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📱 Mensaje {i}: {message}")
        print("-" * 60)
        
        try:
            response = await message_handler.handle_message(test_phone, message)
            print(f"🤖 Respuesta: {response}")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_real_message())
