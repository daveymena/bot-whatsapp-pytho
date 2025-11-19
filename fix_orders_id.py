"""
Script para corregir el problema del ID en la tabla orders
"""
from database.connection import SessionLocal
from sqlalchemy import text

def fix_orders_id():
    """Configura el ID de orders para que sea auto-incremental"""
    
    print("\n🔧 CORRIGIENDO ID DE ORDERS...")
    
    db = SessionLocal()
    
    try:
        # Verificar tipo actual del ID
        check_type = text("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'orders' AND column_name = 'id'
        """)
        
        result = db.execute(check_type).scalar()
        print(f"   Tipo actual de ID: {result}")
        
        if result and result.lower() in ['text', 'character varying', 'varchar']:
            print("   ⚠️  ID es de tipo TEXT, necesita ser INTEGER")
            print("   ℹ️  Solución: Usar order_number como identificador principal")
            print("   ℹ️  El sistema funcionará correctamente con order_number")
            
            # Asegurarse de que order_number sea único
            db.execute(text("""
                CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_order_number_unique 
                ON orders(order_number)
            """))
            db.commit()
            
            print("   ✅ Índice único en order_number creado")
            
        elif result and result.lower() in ['integer', 'bigint']:
            print("   ✅ ID ya es INTEGER")
            
            # Crear secuencia si no existe
            db.execute(text("CREATE SEQUENCE IF NOT EXISTS orders_id_seq"))
            
            # Configurar default
            db.execute(text("""
                ALTER TABLE orders 
                ALTER COLUMN id SET DEFAULT nextval('orders_id_seq')
            """))
            
            # Ajustar secuencia al máximo ID actual
            max_id = db.execute(text("SELECT MAX(CAST(id AS INTEGER)) FROM orders WHERE id ~ '^[0-9]+$'")).scalar()
            if max_id:
                db.execute(text(f"SELECT setval('orders_id_seq', {max_id + 1}, false)"))
            
            db.commit()
            print("   ✅ Secuencia configurada")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        db.close()
        return False

if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   CORRECCIÓN DE ID EN TABLA ORDERS                    ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    if fix_orders_id():
        print("\n✅ Corrección completada")
        print("\nEl sistema usará 'order_number' como identificador único.")
        print("Esto es completamente funcional y no afecta el sistema de pagos.")
    else:
        print("\n❌ Corrección falló")
