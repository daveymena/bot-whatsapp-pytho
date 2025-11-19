"""
Script para agregar productos de ejemplo a la base de datos
"""
from database.connection import SessionLocal
from database.models import Product
from datetime import datetime

def add_sample_products():
    """Agrega productos de ejemplo"""
    
    print("📦 Agregando productos de ejemplo...")
    
    db = SessionLocal()
    
    try:
        # Verificar si ya hay productos
        existing = db.query(Product).count()
        if existing > 0:
            print(f"⚠️  Ya hay {existing} productos en la base de datos")
            response = input("¿Deseas agregar más productos? (s/n): ")
            if response.lower() != 's':
                print("❌ Operación cancelada")
                return
        
        # Productos de ejemplo (usando categorías DIGITAL y PHYSICAL)
        sample_products = [
            {
                'name': 'Audífonos Bluetooth Pro',
                'description': 'Audífonos inalámbricos con cancelación de ruido, batería de 20 horas, sonido HD estéreo. Perfectos para música y llamadas.',
                'price': 120000,
                'category': 'PHYSICAL',
                'stock': 15,
                'warranty': '1 año de garantía',
                'is_digital': False,
                'is_dropshipping': False
            },
            {
                'name': 'Teclado Mecánico RGB',
                'description': 'Teclado mecánico gaming con luces RGB, switches azules, cable mallado. Ideal para gaming y trabajo.',
                'price': 180000,
                'category': 'PHYSICAL',
                'stock': 8,
                'warranty': '2 años de garantía',
                'is_digital': False,
                'is_dropshipping': False
            },
            {
                'name': 'Mouse Gamer 7200 DPI',
                'description': 'Mouse ergonómico con 7 botones programables, sensor óptico de alta precisión, luces RGB personalizables.',
                'price': 85000,
                'category': 'PHYSICAL',
                'stock': 20,
                'warranty': '1 año de garantía',
                'is_digital': False,
                'is_dropshipping': False
            },
            {
                'name': 'Curso Completo de Piano',
                'description': 'Curso digital con 76 lecciones en video HD, desde nivel básico hasta avanzado. Incluye partituras descargables y acceso de por vida.',
                'price': 150000,
                'category': 'DIGITAL',
                'stock': 999,
                'warranty': 'Acceso de por vida',
                'is_digital': True,
                'is_dropshipping': False
            },
            {
                'name': 'Curso de Guitarra para Principiantes',
                'description': 'Aprende guitarra desde cero con 50 lecciones prácticas, ejercicios interactivos y canciones populares. Incluye material descargable.',
                'price': 120000,
                'category': 'DIGITAL',
                'stock': 999,
                'warranty': 'Acceso de por vida',
                'is_digital': True,
                'is_dropshipping': False
            },
            {
                'name': 'Bolso Antirrobo Impermeable',
                'description': 'Bolso con cremallera oculta, puerto USB para cargar dispositivos, compartimentos organizadores. Material impermeable y resistente.',
                'price': 95000,
                'category': 'PHYSICAL',
                'stock': 12,
                'warranty': '6 meses de garantía',
                'is_digital': False,
                'is_dropshipping': True
            },
            {
                'name': 'Webcam Full HD 1080p',
                'description': 'Cámara web con micrófono integrado, enfoque automático, compatible con todas las plataformas. Ideal para videollamadas y streaming.',
                'price': 140000,
                'category': 'PHYSICAL',
                'stock': 10,
                'warranty': '1 año de garantía',
                'is_digital': False,
                'is_dropshipping': False
            },
            {
                'name': 'Megapack Digital Emprendedor',
                'description': 'Más de 17,000 recursos digitales: cursos, plantillas, ebooks, herramientas de diseño, audios y más. Licencia de reventa incluida.',
                'price': 80000,
                'category': 'DIGITAL',
                'stock': 999,
                'warranty': 'Actualizaciones gratis',
                'is_digital': True,
                'is_dropshipping': False
            }
        ]
        
        # Agregar productos
        added = 0
        for product_data in sample_products:
            # Verificar si ya existe
            existing_product = db.query(Product).filter(
                Product.name == product_data['name']
            ).first()
            
            if existing_product:
                print(f"⚠️  '{product_data['name']}' ya existe, actualizando...")
                for key, value in product_data.items():
                    setattr(existing_product, key, value)
                existing_product.updated_at = datetime.utcnow()
            else:
                print(f"➕ Agregando '{product_data['name']}'...")
                product = Product(**product_data)
                db.add(product)
                added += 1
            
            db.commit()
        
        print(f"\n✅ Operación completada:")
        print(f"   - Productos agregados: {added}")
        print(f"   - Total en base de datos: {db.query(Product).count()}")
        
        # Mostrar resumen
        print("\n📊 Productos disponibles:")
        products = db.query(Product).filter(Product.stock > 0).all()
        for p in products:
            print(f"   - {p.name}: ${p.price:,.0f} (Stock: {p.stock})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_products()
