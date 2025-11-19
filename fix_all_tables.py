"""
Script para corregir todas las tablas de la base de datos
"""
from database.connection import engine

def fix_all_tables():
    """Corrige todas las tablas para que coincidan con los modelos"""
    
    print("🔧 Corrigiendo todas las tablas de la base de datos...")
    
    try:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        # ===== TABLA USERS =====
        print("\n📋 Corrigiendo tabla 'users'...")
        users_columns = [
            ("address", "TEXT"),
            ("is_blocked", "BOOLEAN DEFAULT FALSE"),
            ("spam_count", "INTEGER DEFAULT 0"),
            ("total_purchases", "FLOAT DEFAULT 0"),
            ("purchase_count", "INTEGER DEFAULT 0"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
            ("last_interaction", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]
        
        for column_name, column_type in users_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name=%s
            """, (column_name,))
            
            if cursor.fetchone() is None:
                print(f"  ➕ Agregando columna '{column_name}'...")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                conn.commit()
        
        # ===== TABLA CONVERSATIONS =====
        print("\n📋 Corrigiendo tabla 'conversations'...")
        conversations_columns = [
            ("user_phone", "VARCHAR(50) NOT NULL"),
            ("message", "TEXT NOT NULL"),
            ("response", "TEXT"),
            ("intent", "VARCHAR(100)"),
            ("sentiment", "VARCHAR(50)"),
            ("agent_type", "VARCHAR(100)"),
            ("context", "JSON"),
            ("is_human", "BOOLEAN DEFAULT FALSE"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]
        
        for column_name, column_type in conversations_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='conversations' AND column_name=%s
            """, (column_name,))
            
            if cursor.fetchone() is None:
                print(f"  ➕ Agregando columna '{column_name}'...")
                # Para columnas NOT NULL, primero agregar sin NOT NULL
                if "NOT NULL" in column_type:
                    temp_type = column_type.replace("NOT NULL", "")
                    cursor.execute(f"ALTER TABLE conversations ADD COLUMN {column_name} {temp_type}")
                    # Si es user_phone o message, actualizar valores existentes
                    if column_name in ["user_phone", "message"]:
                        cursor.execute(f"UPDATE conversations SET {column_name} = '' WHERE {column_name} IS NULL")
                    conn.commit()
                    # Ahora agregar NOT NULL
                    cursor.execute(f"ALTER TABLE conversations ALTER COLUMN {column_name} SET NOT NULL")
                    conn.commit()
                else:
                    cursor.execute(f"ALTER TABLE conversations ADD COLUMN {column_name} {column_type}")
                    conn.commit()
        
        # ===== TABLA ORDERS =====
        print("\n📋 Corrigiendo tabla 'orders'...")
        orders_columns = [
            ("order_number", "VARCHAR(50) UNIQUE"),
            ("user_phone", "VARCHAR(50) NOT NULL"),
            ("user_name", "VARCHAR(255)"),
            ("products", "JSON"),
            ("subtotal", "FLOAT NOT NULL"),
            ("shipping", "FLOAT DEFAULT 0"),
            ("discount", "FLOAT DEFAULT 0"),
            ("total", "FLOAT NOT NULL"),
            ("status", "VARCHAR(50) DEFAULT 'pending'"),
            ("payment_method", "VARCHAR(100)"),
            ("payment_proof", "VARCHAR(500)"),
            ("delivery_address", "TEXT"),
            ("tracking_number", "VARCHAR(100)"),
            ("notes", "TEXT"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]
        
        for column_name, column_type in orders_columns:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='orders' AND column_name=%s
            """, (column_name,))
            
            if cursor.fetchone() is None:
                print(f"  ➕ Agregando columna '{column_name}'...")
                if "NOT NULL" in column_type:
                    temp_type = column_type.replace("NOT NULL", "")
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {column_name} {temp_type}")
                    # Actualizar valores por defecto
                    if column_name in ["user_phone"]:
                        cursor.execute(f"UPDATE orders SET {column_name} = '' WHERE {column_name} IS NULL")
                    elif column_name in ["subtotal", "total"]:
                        cursor.execute(f"UPDATE orders SET {column_name} = 0 WHERE {column_name} IS NULL")
                    conn.commit()
                    cursor.execute(f"ALTER TABLE orders ALTER COLUMN {column_name} SET NOT NULL")
                    conn.commit()
                else:
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {column_name} {column_type}")
                    conn.commit()
        
        cursor.close()
        conn.close()
        
        print("\n✅ Todas las tablas corregidas exitosamente")
        print("\nAhora ejecuta: python test_bot_real.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_all_tables()
