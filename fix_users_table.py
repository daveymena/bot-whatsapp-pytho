"""
Script para corregir la tabla users completamente
"""
from database.connection import engine

def fix_users_table():
    """Corrige la tabla users para que coincida con el modelo"""
    
    print("🔧 Corrigiendo tabla users...")
    
    try:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        # 1. Agregar columnas faltantes
        columns_to_add = [
            ("address", "TEXT"),
            ("is_blocked", "BOOLEAN DEFAULT FALSE"),
            ("spam_count", "INTEGER DEFAULT 0"),
            ("total_purchases", "FLOAT DEFAULT 0"),
            ("purchase_count", "INTEGER DEFAULT 0"),
            ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
            ("last_interaction", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]
        
        for column_name, column_type in columns_to_add:
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name=%s
            """, (column_name,))
            
            if cursor.fetchone() is None:
                print(f"➕ Agregando columna '{column_name}'...")
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                conn.commit()
                print(f"✅ Columna '{column_name}' agregada")
        
        # 2. Renombrar columnas camelCase a snake_case (si existen)
        columns_to_rename = [
            ("createdAt", "created_at"),
            ("lastInteraction", "last_interaction"),
        ]
        
        for old_name, new_name in columns_to_rename:
            # Verificar si la columna antigua existe
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name=%s
            """, (old_name,))
            
            if cursor.fetchone() is not None:
                # Verificar si la nueva no existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name=%s
                """, (new_name,))
                
                if cursor.fetchone() is None:
                    print(f"🔄 Renombrando '{old_name}' a '{new_name}'...")
                    # Usar comillas dobles para nombres con mayúsculas
                    cursor.execute(f'ALTER TABLE users RENAME COLUMN "{old_name}" TO {new_name}')
                    conn.commit()
                    print(f"✅ Columna renombrada")
                else:
                    print(f"⚠️  '{old_name}' existe pero '{new_name}' también, eliminando '{old_name}'...")
                    cursor.execute(f'ALTER TABLE users DROP COLUMN "{old_name}"')
                    conn.commit()
                    print(f"✅ Columna antigua eliminada")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Tabla users completamente corregida")
        print("\nAhora ejecuta: python test_bot_real.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_users_table()
