"""
Script para corregir y sincronizar la base de datos con los modelos
"""
from database.connection import SessionLocal
from sqlalchemy import text
import sys

def get_existing_columns(table_name):
    """Obtiene las columnas existentes de una tabla"""
    db = SessionLocal()
    
    query = text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = :table_name
    """)
    
    result = db.execute(query, {"table_name": table_name})
    columns = [row[0] for row in result]
    db.close()
    
    return columns

def fix_products_table():
    """Agrega todas las columnas faltantes a la tabla products"""
    print("\n📦 CORRIGIENDO TABLA PRODUCTS...")
    
    existing = get_existing_columns("products")
    print(f"   Columnas existentes: {', '.join(existing)}")
    
    required_columns = {
        "image_url": "VARCHAR",
        "images": "JSON",
        "variants": "JSON",
        "warranty": "VARCHAR",
        "is_dropshipping": "BOOLEAN DEFAULT FALSE",
        "is_digital": "BOOLEAN DEFAULT FALSE",
        "dropi_product_id": "VARCHAR",
        "views": "INTEGER DEFAULT 0",
        "sales_count": "INTEGER DEFAULT 0",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }
    
    db = SessionLocal()
    added = 0
    
    for column, datatype in required_columns.items():
        if column not in existing:
            try:
                sql = f"ALTER TABLE products ADD COLUMN {column} {datatype}"
                db.execute(text(sql))
                db.commit()
                print(f"   ✅ Agregada: {column}")
                added += 1
            except Exception as e:
                print(f"   ❌ Error en {column}: {e}")
        else:
            print(f"   ℹ️  Ya existe: {column}")
    
    db.close()
    print(f"   Total agregadas: {added}")

def fix_orders_table():
    """Agrega todas las columnas faltantes a la tabla orders"""
    print("\n📋 CORRIGIENDO TABLA ORDERS...")
    
    existing = get_existing_columns("orders")
    print(f"   Columnas existentes: {', '.join(existing)}")
    
    required_columns = {
        "order_number": "VARCHAR UNIQUE",
        "user_phone": "VARCHAR NOT NULL",
        "user_name": "VARCHAR",
        "products": "JSON",
        "subtotal": "FLOAT NOT NULL",
        "shipping": "FLOAT DEFAULT 0",
        "discount": "FLOAT DEFAULT 0",
        "total": "FLOAT NOT NULL",
        "status": "VARCHAR DEFAULT 'pending'",
        "payment_method": "VARCHAR",
        "payment_proof": "VARCHAR",
        "delivery_address": "TEXT",
        "tracking_number": "VARCHAR",
        "notes": "TEXT",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }
    
    db = SessionLocal()
    added = 0
    
    for column, datatype in required_columns.items():
        if column not in existing:
            try:
                # Para columnas NOT NULL, primero agregar sin restricción
                if "NOT NULL" in datatype:
                    base_type = datatype.replace("NOT NULL", "").strip()
                    sql = f"ALTER TABLE orders ADD COLUMN {column} {base_type}"
                else:
                    sql = f"ALTER TABLE orders ADD COLUMN {column} {datatype}"
                
                db.execute(text(sql))
                db.commit()
                print(f"   ✅ Agregada: {column}")
                added += 1
            except Exception as e:
                print(f"   ❌ Error en {column}: {e}")
        else:
            print(f"   ℹ️  Ya existe: {column}")
    
    db.close()
    print(f"   Total agregadas: {added}")

def create_indexes():
    """Crea índices para mejorar el rendimiento"""
    print("\n🔍 CREANDO ÍNDICES...")
    
    indexes = [
        ("idx_products_image_url", "products", "image_url"),
        ("idx_products_category", "products", "category"),
        ("idx_orders_order_number", "orders", "order_number"),
        ("idx_orders_user_phone", "orders", "user_phone"),
        ("idx_orders_payment_method", "orders", "payment_method"),
        ("idx_orders_status", "orders", "status")
    ]
    
    db = SessionLocal()
    created = 0
    
    for index_name, table, column in indexes:
        try:
            sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table}({column})"
            db.execute(text(sql))
            db.commit()
            print(f"   ✅ {index_name}")
            created += 1
        except Exception as e:
            print(f"   ❌ {index_name}: {e}")
    
    db.close()
    print(f"   Total creados: {created}")

def verify_tables():
    """Verifica que las tablas estén correctas"""
    print("\n✅ VERIFICANDO TABLAS...")
    
    products_cols = get_existing_columns("products")
    orders_cols = get_existing_columns("orders")
    
    print(f"\n   Products: {len(products_cols)} columnas")
    required_products = ["id", "name", "price", "image_url", "images", "views"]
    missing_products = [col for col in required_products if col not in products_cols]
    
    if missing_products:
        print(f"   ❌ Faltan: {', '.join(missing_products)}")
        return False
    else:
        print(f"   ✅ Todas las columnas necesarias presentes")
    
    print(f"\n   Orders: {len(orders_cols)} columnas")
    required_orders = ["id", "order_number", "user_phone", "total", "payment_method"]
    missing_orders = [col for col in required_orders if col not in orders_cols]
    
    if missing_orders:
        print(f"   ❌ Faltan: {', '.join(missing_orders)}")
        return False
    else:
        print(f"   ✅ Todas las columnas necesarias presentes")
    
    return True

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   CORRECCIÓN AUTOMÁTICA DE BASE DE DATOS              ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Corregir tablas
        fix_products_table()
        fix_orders_table()
        
        # Crear índices
        create_indexes()
        
        # Verificar
        if verify_tables():
            print("\n" + "=" * 60)
            print("🎉 ¡BASE DE DATOS CORREGIDA EXITOSAMENTE!")
            print("=" * 60)
            print()
            print("Ahora puedes ejecutar:")
            print("  python test_payment_integration.py")
            print()
        else:
            print("\n" + "=" * 60)
            print("⚠️  VERIFICACIÓN FALLÓ")
            print("=" * 60)
            print()
            print("Algunas columnas aún faltan. Revisa los errores arriba.")
            print()
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print()
        print("Por favor contacta a soporte.")
        sys.exit(1)
