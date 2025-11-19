"""
Test para generar links de pago REALES con Mercado Pago y PayPal
"""
import asyncio
from services.payment_service import payment_service
from database.connection import SessionLocal
from database.models import Product

async def test_mercadopago_link():
    """Genera un link REAL de Mercado Pago"""
    
    print("=" * 70)
    print("💳 TEST: Generar Link de Mercado Pago REAL")
    print("=" * 70)
    print()
    
    # Obtener un producto real de la BD
    db = SessionLocal()
    product = db.query(Product).filter(Product.stock > 0).first()
    db.close()
    
    if not product:
        print("❌ No hay productos disponibles en la BD")
        return
    
    print(f"📦 Producto: {product.name}")
    print(f"💰 Precio: ${product.price:,.0f} COP")
    print()
    
    # Preparar datos de la orden
    order_data = {
        'user_phone': '573001234567',
        'user_name': 'Cliente de Prueba',
        'products': [{
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }],
        'subtotal': float(product.price),
        'shipping': 0,
        'discount': 0,
        'total': float(product.price),
        'delivery_address': 'Bogotá, Colombia'
    }
    
    print("🔄 Generando link de Mercado Pago...")
    print()
    
    try:
        result = await payment_service.create_payment(
            '573001234567',
            order_data,
            'mercadopago'
        )
        
        if result['success']:
            print("✅ ¡Link generado exitosamente!")
            print()
            print(f"🔗 Link de pago:")
            print(f"   {result.get('payment_url', 'No disponible')}")
            print()
            print(f"📋 Número de orden: {result.get('order_number')}")
            print()
            print("💡 Puedes abrir este link en tu navegador para probar el pago")
        else:
            print("❌ Error generando link:")
            print(f"   {result.get('error', 'Error desconocido')}")
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)

async def test_paypal_link():
    """Genera un link REAL de PayPal"""
    
    print("\n\n")
    print("=" * 70)
    print("🌎 TEST: Generar Link de PayPal REAL")
    print("=" * 70)
    print()
    
    # Obtener un producto real de la BD
    db = SessionLocal()
    product = db.query(Product).filter(Product.stock > 0).first()
    db.close()
    
    if not product:
        print("❌ No hay productos disponibles en la BD")
        return
    
    print(f"📦 Producto: {product.name}")
    print(f"💰 Precio: ${product.price:,.0f} COP (≈ ${product.price/4000:.2f} USD)")
    print()
    
    # Preparar datos de la orden
    order_data = {
        'user_phone': '573001234567',
        'user_name': 'Test Customer',
        'products': [{
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }],
        'subtotal': float(product.price),
        'shipping': 0,
        'discount': 0,
        'total': float(product.price),
        'delivery_address': 'Bogotá, Colombia'
    }
    
    print("🔄 Generando link de PayPal...")
    print()
    
    try:
        result = await payment_service.create_payment(
            '573001234567',
            order_data,
            'paypal'
        )
        
        if result['success']:
            print("✅ ¡Link generado exitosamente!")
            print()
            print(f"🔗 Link de pago:")
            print(f"   {result.get('payment_url', 'No disponible')}")
            print()
            print(f"📋 Número de orden: {result.get('order_number')}")
            print()
            print("💡 Puedes abrir este link en tu navegador para probar el pago")
        else:
            print("❌ Error generando link:")
            print(f"   {result.get('error', 'Error desconocido')}")
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)

async def test_nequi_info():
    """Muestra información de pago por Nequi"""
    
    print("\n\n")
    print("=" * 70)
    print("💜 TEST: Información de Pago por Nequi")
    print("=" * 70)
    print()
    
    # Obtener un producto real de la BD
    db = SessionLocal()
    product = db.query(Product).filter(Product.stock > 0).first()
    db.close()
    
    if not product:
        print("❌ No hay productos disponibles en la BD")
        return
    
    print(f"📦 Producto: {product.name}")
    print(f"💰 Precio: ${product.price:,.0f} COP")
    print()
    
    # Preparar datos de la orden
    order_data = {
        'user_phone': '573001234567',
        'user_name': 'Cliente de Prueba',
        'products': [{
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }],
        'subtotal': float(product.price),
        'shipping': 0,
        'discount': 0,
        'total': float(product.price),
        'delivery_address': 'Bogotá, Colombia'
    }
    
    print("🔄 Generando información de pago...")
    print()
    
    try:
        result = await payment_service.create_payment(
            '573001234567',
            order_data,
            'nequi'
        )
        
        if result['success']:
            print("✅ ¡Información generada exitosamente!")
            print()
            print(f"📋 Número de orden: {result.get('order_number')}")
            print(f"💜 Requiere comprobante: {result.get('requires_proof', False)}")
            print()
            print("💡 El cliente debe enviar el comprobante después de transferir")
        else:
            print("❌ Error generando información:")
            print(f"   {result.get('error', 'Error desconocido')}")
    
    except Exception as e:
        print(f"❌ Excepción: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DE LINKS DE PAGO REALES\n")
    print("⚠️  ADVERTENCIA: Estos son links REALES de producción")
    print("   No completes los pagos a menos que sea intencional\n")
    
    # Ejecutar todas las pruebas
    asyncio.run(test_mercadopago_link())
    asyncio.run(test_paypal_link())
    asyncio.run(test_nequi_info())
    
    print("\n\n✅ TODAS LAS PRUEBAS COMPLETADAS\n")
    print("💡 Los links generados son REALES y funcionales")
    print("   Puedes usarlos para probar el flujo completo de pago\n")
