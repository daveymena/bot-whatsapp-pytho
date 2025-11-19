"""
Script de prueba para verificar que el dashboard y las APIs funcionen correctamente
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_auth_login():
    """Prueba el endpoint de login"""
    print("\n🔐 Probando autenticación...")
    
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "email": "admin@ventas.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso")
            print(f"   Usuario: {result['user']['name']}")
            print(f"   Email: {result['user']['email']}")
            print(f"   Token: {result['token'][:50]}...")
            return result['token']
        else:
            print(f"❌ Error en login: {response.status_code}")
            print(f"   {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return None

def test_stats_overview():
    """Prueba el endpoint de estadísticas"""
    print("\n📊 Probando estadísticas...")
    
    url = f"{BASE_URL}/api/stats/overview"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas")
            print(f"   Conversaciones: {stats.get('totalConversations', 0)}")
            print(f"   Productos: {stats.get('totalProducts', 0)}")
            print(f"   Clientes: {stats.get('totalCustomers', 0)}")
            print(f"   Mensajes: {stats.get('totalMessages', 0)}")
            print(f"   Conectado: {'Sí' if stats.get('isConnected') else 'No'}")
            return True
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_products():
    """Prueba el endpoint de productos"""
    print("\n📦 Probando productos...")
    
    url = f"{BASE_URL}/admin/products"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Productos obtenidos: {len(products)}")
            if products:
                print(f"   Ejemplo: {products[0].get('name', 'N/A')}")
            return True
        else:
            print(f"❌ Error obteniendo productos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_customers():
    """Prueba el endpoint de clientes"""
    print("\n👥 Probando clientes...")
    
    url = f"{BASE_URL}/admin/customers"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            customers = response.json()
            print(f"✅ Clientes obtenidos: {len(customers)}")
            if customers:
                print(f"   Ejemplo: {customers[0].get('name', 'N/A')}")
            return True
        else:
            print(f"❌ Error obteniendo clientes: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def test_whatsapp_status():
    """Prueba el endpoint de estado de WhatsApp"""
    print("\n💬 Probando estado de WhatsApp...")
    
    url = f"{BASE_URL}/admin/whatsapp/status"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            status = response.json()
            print("✅ Estado obtenido")
            print(f"   Estado: {status.get('status', 'UNKNOWN')}")
            if status.get('connection'):
                conn = status['connection']
                print(f"   Teléfono: {conn.get('phoneNumber', 'N/A')}")
                print(f"   Activo: {'Sí' if conn.get('isActive') else 'No'}")
            return True
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DEL DASHBOARD Y APIs")
    print("=" * 60)
    print(f"\n🌐 URL Base: {BASE_URL}")
    print("⚠️  Asegúrate de que el servidor Python esté corriendo")
    
    # Ejecutar pruebas
    results = []
    
    token = test_auth_login()
    results.append(("Autenticación", token is not None))
    
    results.append(("Estadísticas", test_stats_overview()))
    results.append(("Productos", test_products()))
    results.append(("Clientes", test_customers()))
    results.append(("WhatsApp Status", test_whatsapp_status()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El dashboard está listo.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    print("\n💡 Próximos pasos:")
    print("   1. Inicia el dashboard Next.js: cd dashboard-nextjs && npm run dev")
    print("   2. Abre http://localhost:3001")
    print("   3. Login con: admin@ventas.com / admin123")
    print("=" * 60)

if __name__ == "__main__":
    main()
