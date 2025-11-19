"""
Script para recrear la tabla conversations correctamente
"""
from database.connection import engine

def recreate_conversations_table():
    """Recrea la tabla conversations con la estructura correcta"""
    
    print("🔧 Recreando tabla conversations...")
    
    try:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        # Hacer backup de datos existentes si hay
        print("\n💾 Haciendo backup de datos existentes...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations_backup AS 
            SELECT * FROM conversations;
        """)
        conn.commit()
        print("✅ Backup creado")
        
        # Eliminar tabla antigua
        print("\n🗑️  Eliminando tabla antigua...")
        cursor.execute("DROP TABLE IF EXISTS conversations CASCADE;")
        conn.commit()
        print("✅ Tabla eliminada")
        
        # Crear tabla nueva con estructura correcta
        print("\n📋 Creando tabla nueva...")
        cursor.execute("""
            CREATE TABLE conversations (
                id SERIAL PRIMARY KEY,
                user_phone VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                intent VARCHAR(100),
                sentiment VARCHAR(50),
                agent_type VARCHAR(100),
                context JSON,
                is_human BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Tabla creada correctamente")
        
        # Crear índices
        print("\n🔍 Creando índices...")
        cursor.execute("""
            CREATE INDEX idx_conversations_user_phone ON conversations(user_phone);
            CREATE INDEX idx_conversations_created_at ON conversations(created_at);
            CREATE INDEX idx_conversations_intent ON conversations(intent);
        """)
        conn.commit()
        print("✅ Índices creados")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Tabla conversations recreada exitosamente")
        print("\nAhora ejecuta: python test_bot_real.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    recreate_conversations_table()
