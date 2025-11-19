"""
Script de migración para agregar columnas de pagos y fotos
"""
from database.connection import SessionLocal, engine
from sqlalchemy import text
import sys

def migrate_database():
    """Agrega las columnas necesarias para el sistema de pagos y fotos"""
    
    print("=" * 60)
    print("🔄 MIGRANDO BASE DE DATOS")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    migrations = [
        # Productos - Agregar columnas de fotos
        {
            "name": "products.image_url",
            "sql": "ALTER TABLE products ADD COLUMN IF NOT EXISTS image_url VARCHAR",
            "description": "URL de imagen principal del producto"
        },
        {
            "name": "products.images",
            "sql": "ALTER TABLE products ADD COLUMN IF NOT EXISTS images JSON",
            "description": "Array de URLs de imágenes adicionales"
        },
        {
            "name": "products.views",
            "sql": "ALTER TABLE products ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0",
            "description": "Contador de vistas del producto"
        },
        
        # Órdenes - Agregar columnas de pagos
        {
            "name": "orders.order_number",
            "sql": "ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_number VARCHAR UNIQUE",
            "description": "Número único de orden"
        },
        {
            "name": "orders.payment_method",
            "sql": "ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method VARCHAR",
            "description": "Método de pago utilizado"
        },
        {
            "name": "orders.payment_proof",
            "sql": "ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_proof VARCHAR",
            "description": "URL del comprobante de pago"
        },
        
        # Índices para mejorar rendimiento
        {
            "name": "idx_products_image_url",
            "sql": "CREATE INDEX IF NOT EXISTS idx_products_image_url ON products(image_url)",
            "description": "Índice para búsqueda de productos con fotos"
        },
        {
            "name": "idx_orders_order_number",
            "sql": "CREATE INDEX IF NOT EXISTS idx_orders_order_number ON orders(order_number)",
            "description": "Índice para búsqueda rápida de órdenes"
        },
        {
            "name": "idx_orders_payment_method",
            "sql": "CREATE INDEX IF NOT EXISTS idx_orders_payment_method ON orders(payment_method)",
            "description": "Índice para análisis de métodos de pago"
        }
    ]
    
    success_count = 0
    error_count = 0
    
    for migration in migrations:
        try:
            print(f"[{migrations.index(migration) + 1}/{len(migrations)}] {migration['name']}...")
            print(f"    {migration['description']}")
            
            db.execute(text(migration['sql']))
            db.commit()
            
            print(f"    ✅ Completado")
            success_count += 1
            
        except Exception as e:
            error_msg = str(e)
            
            # Ignorar errores de columnas que ya existen
            if "already exists" in error_msg or "duplicate" in error_msg.lower():
                print(f"    ℹ️  Ya existe, omitiendo")
                success_count += 1
            else:
                print(f"    ❌ Error: {error_msg}")
                error_count += 1
        
        print()
    
    db.close()
    
    print("=" * 60)
    print(f"✅ Migraciones completadas: {success_count}")
    if error_count > 0:
        print(f"❌ Errores: {error_count}")
    print("=" * 60)
    print()
    
    if error_count > 0:
        print("⚠️  Algunas migraciones fallaron. Revisa los errores arriba.")
        return False
    else:
        print("🎉 ¡Base de datos actualizada exitosamente!")
        return True

def verify_migration():
    """Verifica que las columnas se hayan agregado correctamente"""
    
    print("\n🔍 VERIFICANDO MIGRACIÓN...")
    print()
    
    db = SessionLocal()
    
    checks = [
        {
            "name": "Productos con image_url",
            "sql": "SELECT COUNT(*) FROM products WHERE image_url IS NOT NULL"
        },
        {
            "name": "Productos con images",
            "sql": "SELECT COUNT(*) FROM products WHERE images IS NOT NULL"
        },
        {
            "name": "Órdenes con order_number",
            "sql": "SELECT COUNT(*) FROM orders WHERE order_number IS NOT NULL"
        }
    ]
    
    for check in checks:
        try:
            result = db.execute(text(check['sql'])).scalar()
            print(f"✅ {check['name']}: {result}")
        except Exception as e:
            print(f"❌ {check['name']}: Error - {e}")
    
    db.close()
    print()

def add_sample_images():
    """Agrega URLs de imágenes de ejemplo a productos existentes"""
    
    print("📸 AGREGANDO IMÁGENES DE EJEMPLO...")
    print()
    
    db = SessionLocal()
    
    try:
        # Actualizar productos sin imágenes con URLs de ejemplo
        update_sql = """
        UPDATE products 
        SET image_url = 'https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=' || name,
            images = '["https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Imagen+1", 
                      "https://via.placeholder.com/800x600/50C878/FFFFFF?text=Imagen+2"]'::json
        WHERE image_url IS NULL
        """
        
        result = db.execute(text(update_sql))
        db.commit()
        
        print(f"✅ {result.rowcount} productos actualizados con imágenes de ejemplo")
        print("   Nota: Estas son imágenes placeholder. Reemplázalas con URLs reales.")
        
    except Exception as e:
        print(f"❌ Error agregando imágenes: {e}")
        db.rollback()
    
    db.close()
    print()

def update_existing_orders():
    """Actualiza órdenes existentes con números de orden"""
    
    print("📦 ACTUALIZANDO ÓRDENES EXISTENTES...")
    print()
    
    db = SessionLocal()
    
    try:
        # Generar números de orden para órdenes sin número
        update_sql = """
        UPDATE orders 
        SET order_number = 'ORD-' || TO_CHAR(created_at, 'YYYYMMDD') || '-' || 
                          UPPER(SUBSTRING(MD5(RANDOM()::TEXT) FROM 1 FOR 6))
        WHERE order_number IS NULL
        """
        
        result = db.execute(text(update_sql))
        db.commit()
        
        print(f"✅ {result.rowcount} órdenes actualizadas con números de orden")
        
    except Exception as e:
        print(f"❌ Error actualizando órdenes: {e}")
        db.rollback()
    
    db.close()
    print()

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   MIGRACIÓN DE BASE DE DATOS - PAGOS Y FOTOS          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    # Confirmar antes de continuar
    response = input("¿Deseas continuar con la migración? (s/n): ")
    
    if response.lower() != 's':
        print("\n❌ Migración cancelada")
        sys.exit(0)
    
    print()
    
    # Ejecutar migración
    success = migrate_database()
    
    if success:
        # Verificar migración
        verify_migration()
        
        # Preguntar si agregar datos de ejemplo
        response = input("\n¿Deseas agregar imágenes de ejemplo a los productos? (s/n): ")
        if response.lower() == 's':
            add_sample_images()
        
        # Preguntar si actualizar órdenes
        response = input("¿Deseas generar números de orden para órdenes existentes? (s/n): ")
        if response.lower() == 's':
            update_existing_orders()
        
        print("\n" + "=" * 60)
        print("🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 60)
        print()
        print("Próximos pasos:")
        print("1. Ejecuta: python test_payment_integration.py")
        print("2. Agrega URLs reales de imágenes a tus productos")
        print("3. Configura tus credenciales de pago en .env")
        print("4. Inicia el sistema: START_WITH_PAYMENTS.bat")
        print()
    else:
        print("\n" + "=" * 60)
        print("❌ MIGRACIÓN FALLÓ")
        print("=" * 60)
        print()
        print("Por favor revisa los errores arriba y:")
        print("1. Verifica que la base de datos esté accesible")
        print("2. Verifica que tengas permisos de ALTER TABLE")
        print("3. Contacta a soporte si el problema persiste")
        print()
        sys.exit(1)
