"""
Script para probar el bot con respuestas concisas
"""
import asyncio
from whatsapp.message_handler import message_handler

async def test_concise_bot():
    """Prueba el bot con conversación real"""
    
    print("=" * 60)
    print("🧪 PRUEBA DEL BOT - RESPUESTAS CONCISAS")
    print("=" * 60)
    print()
    
    phone = "573001234567"
    
    # Conversación de prueba
    messages = [
        "Hola muy buenas",
        "Estoy interesado en el curso de piano",
        "Principiante",
        "Si me gustaría saber más"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"📱 Mensaje {i}: {msg}")
        print("-" * 60)
        
        try:
            response = await message_handler.handle_message(phone, msg)
            print(f"🤖 Respuesta ({len(response)} caracteres):")
            print(response)
            print()
            
            # Verificar longitud
            if len(response) > 300:
                print(f"⚠️  ADVERTENCIA: Respuesta muy larga ({len(response)} caracteres)")
            else:
                print(f"✅ Longitud adecuada ({len(response)} caracteres)")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_concise_bot())
