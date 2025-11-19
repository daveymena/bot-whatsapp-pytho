"""
Script para poblar la base de datos con datos de ejemplo
"""
from database.connection import SessionLocal, init_db
from database.models import Product, User
from datetime import datetime

def seed_products():
    db = SessionLocal()
    
    products = [
        # Productos físicos
        Product(
            name="iPhone 15 Pro",
            description="Smartphone Apple con chip A17 Pro, cámara de 48MP",
            price=4500000,
            category="Tecnología",
            stock=10,
            is_digital=False,
            is_dropshipping=False
        ),
        Product(
            name="Samsung Galaxy S24",
            description="Smartphone Samsung con IA integrada, pantalla AMOLED",
            price=3800000,
            category="Tecnología",
            stock=15,
            is_digital=False,
            is_dropshipping=False
        ),
        Product(
            name="AirPods Pro 2",
            description="Audífonos inalámbricos con cancelación de ruido",
            price=950000,
            category="Accesorios",
            stock=25,
            is_digital=False,
            is_dropshipping=False
        ),
        
        # Productos digitales
        Product(
            name="Curso de Marketing Digital",
            description="Curso completo de marketing digital con certificación",
            price=150000,
            category="Cursos",
            stock=999,
            is_digital=True,
            is_dropshipping=False
        ),
        Product(
            name="Megapack de Diseño Gráfico",
            description="Pack con plantillas, fuentes y recursos para diseñadores",
            price=80000,
            category="Recursos Digitales",
            stock=999,
            is_digital=True,
            is_dropshipping=False
        ),
        
        # Productos dropshipping
        Product(
            name="Smartwatch Deportivo",
            description="Reloj inteligente con monitor de salud",
            price=250000,
            category="Tecnología",
            stock=100,
            is_digital=False,
            is_dropshipping=True,
            dropi_product_id="DROPI123"
        ),
        Product(
            name="Lámpara LED Inteligente",
            description="Lámpara con control por app y cambio de colores",
            price=120000,
            category="Hogar",
            stock=50,
            is_digital=False,
            is_dropshipping=True,
            dropi_product_id="DROPI456"
        )
    ]
    
    for product in products:
        db.add(product)
    
    db.commit()
    print(f"✅ {len(products)} productos agregados")
    db.close()

def seed_users():
    db = SessionLocal()
    
    users = [
        User(
            phone="573001234567",
            name="Cliente de Prueba",
            email="test@example.com"
        )
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    print(f"✅ {len(users)} usuarios agregados")
    db.close()

if __name__ == "__main__":
    print("🌱 Poblando base de datos...")
    init_db()
    seed_products()
    seed_users()
    print("✅ Base de datos poblada correctamente")
