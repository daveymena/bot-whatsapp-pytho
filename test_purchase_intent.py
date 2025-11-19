"""
Test rápido para verificar la intención de compra
"""
import asyncio
from agents.local_sales_agent import local_sales_agent

async def test():
    phone = "test123"
    
    messages = [
        "Hola",
        "Busco audífonos",
        "¿Cuánto cuestan?",
        "¿Tienen garantía?",
        "¿Cómo pago?",
        "Perfecto, los quiero"
    ]
    
    print("=" * 70)
    print("🧪 TEST: Intención de Compra")
    print("=" * 70)
    
    for i, msg in enumerate(messages, 1):
        print(f"\n{i}. 👤 Cliente: {msg}")
        print("-" * 70)
        response = await local_sales_agent.process_message(phone, msg, {})
        print(f"🤖 Bot:\n{response}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test())
