"""
Script de prueba para verificar la integración de pagos y fotos
"""
import asyncio
from services.payment_service import payment_service
from whatsapp.multimedia_handler import multimedia_handler
from database.connection import SessionLocal, init_db
from database.models import Product, Order
from config.settings import settings

async def test_mercadopago():
    """Prueba la integración de Mercado Pago"""
    print("\n🧪 PROBANDO MERCADO PAGO...")
    
    order_data = {
        'order_number': 'TEST-001',
        'user_phone': '573005560186',
        'user_name': 'Cliente de Prueba',
        'products': [
            {'name': 'Producto Test', 'quantity': 1, 'price': 50000}
        ],
        'subtotal': 50000,
        'shipping': 5000,
        'discount': 0,
        'total': 55000
    }
    
    try:
        result = await payment_service.create_payment('573005560186', order_data, 'mercadopago')
        
        if result['success']:
            print("✅ Mercado Pago: OK")
            print(f"   Link de pago: {result.get('payment_url', 'N/A')}")
        else:
            print(f"❌ Mercado Pago: ERROR - {result.get('error')}")
    except Exception as e:
        print(f"❌ Mercado Pago: EXCEPCIÓN - {e}")

async def test_paypal():
    """Prueba la integración de PayPal"""
    print("\n🧪 PROBANDO PAYPAL...")
    
    order_data = {
        'order_number': 'TEST-002',
        'user_phone': '573005560186',
        'user_name': 'Cliente de Prueba',
        'products': [
            {'id': 1, 'name': 'Producto Test', 'quantity': 1, 'price': 50000}
        ],
        'subtotal': 50000,
        'shipping': 5000,
        'discount': 0,
        'total': 55000
    }
    
    try:
        result = await payment_service.create_payment('573005560186', order_data, 'paypal')
        
        if result['success']:
            print("✅ PayPal: OK")
            print(f"   Link de pago: {result.get('payment_url', 'N/A')}")
        else:
            print(f"❌ PayPal: ERROR - {result.get('error')}")
    except Exception as e:
        print(f"❌ PayPal: EXCEPCIÓN - {e}")

async def test_manual_payments():
    """Prueba los pagos manuales"""
    print("\n🧪 PROBANDO PAGOS MANUALES...")
    
    order_data = {
        'order_number': 'TEST-003',
        'user_phone': '573005560186',
        'user_name': 'Cliente de Prueba',
        'products': [
            {'name': 'Producto Test', 'quantity': 1, 'price': 50000}
        ],
        'subtotal': 50000,
        'shipping': 5000,
        'discount': 0,
        'total': 55000
    }
    
    methods = ['nequi', 'daviplata', 'banco']
    
    for method in methods:
        try:
            result = await payment_service.create_payment('573005560186', order_data, method)
            
            if result['success']:
                print(f"✅ {method.upper()}: OK")
            else:
                print(f"❌ {method.upper()}: ERROR - {result.get('error')}")
        except Exception as e:
            print(f"❌ {method.upper()}: EXCEPCIÓN - {e}")

def test_database_products():
    """Prueba la conexión con productos en la base de datos"""
    print("\n🧪 PROBANDO BASE DE DATOS...")
    
    try:
        db = SessionLocal()
        products = db.query(Product).limit(5).all()
        
        if products:
            print(f"✅ Base de datos: OK ({len(products)} productos encontrados)")
            for product in products:
                print(f"   - {product.name}: ${product.price:,.0f} COP")
                if product.image_url:
                    print(f"     📸 Imagen: {product.image_url[:50]}...")
        else:
            print("⚠️  Base de datos: Sin productos")
        
        db.close()
    except Exception as e:
        print(f"❌ Base de datos: ERROR - {e}")

async def test_multimedia():
    """Prueba el envío de fotos"""
    print("\n🧪 PROBANDO ENVÍO DE FOTOS...")
    
    try:
        db = SessionLocal()
        product = db.query(Product).filter(Product.image_url.isnot(None)).first()
        db.close()
        
        if product:
            print(f"✅ Producto con foto encontrado: {product.name}")
            print(f"   URL: {product.image_url}")
            
            # Nota: No enviamos realmente por WhatsApp en el test
            print("   ℹ️  Envío de WhatsApp omitido en modo test")
        else:
            print("⚠️  No hay productos con fotos en la base de datos")
    except Exception as e:
        print(f"❌ Multimedia: ERROR - {e}")

def test_configuration():
    """Verifica la configuración"""
    print("\n🧪 VERIFICANDO CONFIGURACIÓN...")
    
    checks = {
        "Mercado Pago Token": bool(settings.MERCADOPAGO_ACCESS_TOKEN),
        "PayPal Client ID": bool(settings.PAYPAL_CLIENT_ID),
        "PayPal Secret": bool(settings.PAYPAL_CLIENT_SECRET),
        "Nequi": bool(settings.NEQUI_NUMBER),
        "Daviplata": bool(settings.DAVIPLATA_NUMBER),
        "Banco": bool(settings.BANK_ACCOUNT_NUMBER),
        "Base URL": bool(settings.BASE_URL),
        "Fotos habilitadas": settings.PHOTOS_ENABLED
    }
    
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}: {'Configurado' if status else 'NO configurado'}")

async def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🚀 PRUEBA DE INTEGRACIÓN - PAGOS Y FOTOS")
    print("=" * 60)
    
    # Verificar configuración
    test_configuration()
    
    # Verificar base de datos
    test_database_products()
    
    # Probar multimedia
    await test_multimedia()
    
    # Probar pagos (solo si están configurados)
    if settings.MERCADOPAGO_ACCESS_TOKEN:
        await test_mercadopago()
    else:
        print("\n⚠️  Mercado Pago no configurado, omitiendo prueba")
    
    if settings.PAYPAL_CLIENT_ID:
        await test_paypal()
    else:
        print("\n⚠️  PayPal no configurado, omitiendo prueba")
    
    # Probar pagos manuales
    await test_manual_payments()
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("\nRevisa los resultados arriba para verificar que todo funcione correctamente.")
    print("Si hay errores, verifica tu archivo .env y las credenciales de las APIs.\n")

if __name__ == "__main__":
    asyncio.run(main())
