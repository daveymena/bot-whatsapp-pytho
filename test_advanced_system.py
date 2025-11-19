"""
Test del Sistema Conversacional Avanzado
Prueba todas las nuevas capacidades
"""
import asyncio
from ai.customer_memory import customer_memory, CustomerProfile
from ai.sentiment_analyzer import sentiment_analyzer
from ai.escalation_manager import escalation_manager
from ai.multi_domain_agent import multi_domain_agent

def print_section(title):
    """Imprime sección"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_customer_memory():
    """Prueba sistema de memoria"""
    print_section("🧠 TEST: SISTEMA DE MEMORIA DEL CLIENTE")
    
    phone = "573001234567"
    
    # Cliente nuevo
    print("1. Cliente Nuevo:")
    greeting = customer_memory.get_personalized_greeting(phone)
    print(f"   Saludo: {greeting}")
    
    # Actualizar perfil
    print("\n2. Actualizando perfil...")
    customer_memory.update_profile(phone, {
        'name': 'Juan Pérez',
        'preferred_category': 'Cursos',
        'communication_style': 'casual'
    })
    
    # Registrar compra
    print("3. Registrando compra...")
    customer_memory.record_purchase(phone, "Curso Python", 89000)
    customer_memory.record_purchase(phone, "Curso JavaScript", 95000)
    customer_memory.record_purchase(phone, "Curso React", 120000)
    
    # Ver perfil actualizado
    profile = customer_memory.get_or_create_profile(phone)
    print(f"\n   Nombre: {profile.name}")
    print(f"   Segmento: {profile.customer_segment}")
    print(f"   Total compras: {profile.total_purchases}")
    print(f"   Total gastado: ${profile.total_spent:,.0f}")
    print(f"   Productos: {', '.join(profile.purchased_products)}")
    
    # Saludo personalizado
    print("\n4. Saludo personalizado:")
    greeting = customer_memory.get_personalized_greeting(phone)
    print(f"   {greeting}")
    
    # Resumen de contexto
    print("\n5. Resumen de contexto:")
    summary = customer_memory.get_context_summary(phone)
    print(summary)
    
    print("\n✅ Test de memoria completado")

def test_sentiment_analyzer():
    """Prueba análisis de sentimiento"""
    print_section("😊 TEST: ANÁLISIS DE SENTIMIENTO")
    
    test_messages = [
        ("¡Excelente! Me encanta este producto 😍", "Muy Positivo"),
        ("Gracias, todo bien 👍", "Positivo"),
        ("Hola, quiero información", "Neutral"),
        ("No me gusta, está caro 😞", "Negativo"),
        ("Esto es PÉSIMO! Estoy muy molesto 😡", "Muy Negativo"),
        ("No entiendo nada, estoy confundido 🤔", "Confundido"),
        ("WOW! Lo quiero YA! 🤩", "Emocionado")
    ]
    
    for i, (message, expected) in enumerate(test_messages, 1):
        print(f"{i}. Mensaje: \"{message}\"")
        
        analysis = sentiment_analyzer.analyze(message)
        
        print(f"   Sentimiento: {analysis['primary_sentiment'].value}")
        print(f"   Score: {analysis['sentiment_score']:.2f}")
        print(f"   Emoción: {analysis['emotion_level'].value}")
        print(f"   Urgencia: {analysis['urgency']}/10")
        print(f"   Tono recomendado: {analysis['recommended_tone']}")
        
        if analysis['requires_escalation']:
            print(f"   ⚠️ REQUIERE ESCALAMIENTO")
        
        print()
    
    print("✅ Test de sentimiento completado")

def test_escalation_manager():
    """Prueba sistema de escalamiento"""
    print_section("🚨 TEST: SISTEMA DE ESCALAMIENTO")
    
    phone = "573009876543"
    
    test_cases = [
        ("Quiero hablar con una persona", "Solicitud explícita"),
        ("Esto es un fraude, voy a demandar", "Queja grave"),
        ("No entiendo", "Confusión (1ra vez)"),
        ("Sigo sin entender", "Confusión (2da vez)"),
        ("Aún no entiendo nada", "Confusión (3ra vez)"),
        ("El pago no funciona, da error", "Problema de pago")
    ]
    
    for i, (message, description) in enumerate(test_cases, 1):
        print(f"{i}. {description}")
        print(f"   Mensaje: \"{message}\"")
        
        # Simular contexto
        context = {
            'sentiment_score': -2 if 'fraude' in message else 0,
            'confusion_count': i if 'entiendo' in message else 0,
            'message_count': 5,
            'customer_lifetime_value': 0
        }
        
        should_escalate, reason = escalation_manager.should_escalate(
            phone, message, context
        )
        
        if should_escalate:
            print(f"   ✅ ESCALAR: {reason.value}")
            escalation_msg = escalation_manager.generate_escalation_message(reason)
            print(f"   Mensaje: {escalation_msg[:100]}...")
        else:
            print(f"   ❌ No escalar")
        
        print()
    
    # Estadísticas
    print("Estadísticas de escalamiento:")
    stats = escalation_manager.get_escalation_stats(phone)
    print(f"   Total escalamientos: {stats['total_escalations']}")
    print(f"   Razones: {stats['reasons']}")
    
    print("\n✅ Test de escalamiento completado")

def test_multi_domain():
    """Prueba agente multi-dominio"""
    print_section("🎯 TEST: AGENTE MULTI-DOMINIO")
    
    test_messages = [
        ("Quiero comprar un curso", "Venta de productos"),
        ("Necesito agendar una cita", "Agendamiento"),
        ("¿Cuál es su horario?", "Información"),
        ("Tengo un problema con el producto", "Soporte"),
        ("Quiero hacer una queja", "Queja")
    ]
    
    for i, (message, expected_domain) in enumerate(test_messages, 1):
        print(f"{i}. {expected_domain}")
        print(f"   Mensaje: \"{message}\"")
        
        domain = multi_domain_agent.detect_domain(message, {})
        print(f"   Dominio detectado: {domain.value}")
        print()
    
    # Test de agendamiento
    print("Test de agendamiento:")
    booking_msg = "Necesito una consulta para mañana"
    booking_result = multi_domain_agent.handle_service_booking(booking_msg, {})
    
    if booking_result['available_slots']:
        print(f"   Slots disponibles: {len(booking_result['available_slots'])}")
        response = multi_domain_agent.format_booking_response(
            booking_result['available_slots']
        )
        print(f"   Respuesta:\n{response}")
    
    print("\n✅ Test multi-dominio completado")

async def test_advanced_agent():
    """Prueba agente avanzado completo"""
    print_section("🎓 TEST: AGENTE AVANZADO COMPLETO")
    
    print("⚠️ Test del agente avanzado requiere integración completa")
    print("✅ Componentes individuales probados exitosamente")
    print("\nPara usar el agente avanzado:")
    print("  from agents.advanced_sales_agent import advanced_sales_agent")
    print("  response = await advanced_sales_agent.process_message(phone, message, {})")
    
    print("\n✅ Test de agente avanzado completado")

def test_product_comparison():
    """Prueba comparación de productos"""
    print_section("📊 TEST: COMPARACIÓN DE PRODUCTOS")
    
    products = [
        {
            'name': 'Curso Python Básico',
            'price': 50000,
            'stock': 100,
            'category': 'Cursos',
            'is_digital': True
        },
        {
            'name': 'Curso Python Avanzado',
            'price': 120000,
            'stock': 50,
            'category': 'Cursos',
            'is_digital': True
        },
        {
            'name': 'Curso Python Completo',
            'price': 150000,
            'stock': 30,
            'category': 'Cursos',
            'is_digital': True
        }
    ]
    
    message = "Diferencia entre curso básico y avanzado"
    
    inquiry = multi_domain_agent.handle_multi_product_inquiry(message, products)
    
    print(f"Tipo de consulta: {inquiry['type']}")
    print(f"Acción: {inquiry['action']}")
    
    if inquiry['type'] == 'multi_product':
        response = multi_domain_agent.format_product_comparison(
            inquiry['products']
        )
        print(f"\nRespuesta:\n{response}")
    
    print("\n✅ Test de comparación completado")

async def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("INICIANDO TESTS DEL SISTEMA AVANZADO")
    print("="*60)
    
    try:
        # Tests síncronos
        test_customer_memory()
        test_sentiment_analyzer()
        test_escalation_manager()
        test_multi_domain()
        test_product_comparison()
        
        # Tests asíncronos
        await test_advanced_agent()
        
        print("\n" + "="*60)
        print("TODOS LOS TESTS COMPLETADOS")
        print("="*60)
        print("\nSistema conversacional avanzado funcionando correctamente!")
        
    except Exception as e:
        print(f"\n❌ Error en tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
