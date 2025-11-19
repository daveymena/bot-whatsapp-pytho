"""
Script para recrear la tabla users correctamente
"""
from database.connection import engine

def recreate_users_table():
    """Recrea la tabla users con la estructura correcta"""
    
    print("🔧 Recreando tabla users...")
    
    try:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        # Hacer backup de datos existentes si hay
        print("\n💾 Haciendo backup de datos existentes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_backup AS 
            SELECT * FROM users;
        """)
        conn.commit()
        print("✅ Backup creado")
        
        # Eliminar tabla antigua
        print("\n🗑️  Eliminando tabla antigua...")
        cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
        conn.commit()
        print("✅ Tabla eliminada")
        
        # Crear tabla nueva con estructura correcta
        print("\n📋 Creando tabla nueva...")
        cursor.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                phone VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255),
                email VARCHAR(255),
                address TEXT,
                is_blocked BOOLEAN DEFAULT FALSE,
                spam_count INTEGER DEFAULT 0,
                total_purchases FLOAT DEFAULT 0,
                purchase_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Tabla creada correctamente")
        
        # Crear índices
        print("\n🔍 Creando índices...")
        cursor.execute("""
            CREATE INDEX idx_users_phone ON users(phone);
            CREATE INDEX idx_users_created_at ON users(created_at);
        """)
        conn.commit()
        print("✅ Índices creados")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Tabla users recreada exitosamente")
        print("\nAhora ejecuta: python test_bot_real.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_users_table()
