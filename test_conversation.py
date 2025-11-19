"""
Script para probar conversaciones con el bot
"""
import asyncio
from whatsapp.message_handler import message_handler

async def test_conversation():
    test_phone = "573001234567"
    
    print("🤖 Iniciando prueba de conversación\n")
    
    # Escenario 1: Saludo inicial
    print("=" * 50)
    print("ESCENARIO 1: Saludo inicial")
    print("=" * 50)
    response = await message_handler.handle_message(test_phone, "Hola")
    print(f"Bot: {response}\n")
    
    # Escenario 2: Consulta de productos
    print("=" * 50)
    print("ESCENARIO 2: Consulta de productos")
    print("=" * 50)
    response = await message_handler.handle_message(test_phone, "Quiero ver productos de tecnología")
    print(f"Bot: {response}\n")
    
    # Escenario 3: Manejo de objeción de precio
    print("=" * 50)
    print("ESCENARIO 3: Objeción de precio")
    print("=" * 50)
    response = await message_handler.handle_message(test_phone, "Me parece muy caro")
    print(f"Bot: {response}\n")
    
    # Escenario 4: Reserva de servicio
    print("=" * 50)
    print("ESCENARIO 4: Reserva de servicio")
    print("=" * 50)
    response = await message_handler.handle_message(test_phone, "Necesito agendar una cita para peluquería")
    print(f"Bot: {response}\n")
    
    # Escenario 5: Consulta de pago
    print("=" * 50)
    print("ESCENARIO 5: Métodos de pago")
    print("=" * 50)
    response = await message_handler.handle_message(test_phone, "¿Cómo puedo pagar?")
    print(f"Bot: {response}\n")

if __name__ == "__main__":
    asyncio.run(test_conversation())
