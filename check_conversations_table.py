"""
Script para verificar y corregir la tabla conversations
"""
from database.connection import engine

def check_and_fix_conversations():
    """Verifica y corrige la tabla conversations"""
    
    print("🔍 Verificando tabla conversations...")
    
    try:
        conn = engine.raw_connection()
        cursor = conn.cursor()
        
        # Ver todas las columnas actuales
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name='conversations'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 Columnas actuales:")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) nullable={col[2]} default={col[3]}")
        
        # Verificar si id tiene autoincremento
        cursor.execute("""
            SELECT column_name, column_default
            FROM information_schema.columns 
            WHERE table_name='conversations' AND column_name='id'
        """)
        
        id_info = cursor.fetchone()
        print(f"\n🔑 Columna ID: {id_info}")
        
        # Si id no tiene autoincremento, corregirlo
        if id_info and (id_info[1] is None or 'nextval' not in str(id_info[1])):
            print("\n🔧 Corrigiendo columna ID para que sea autoincremental...")
            
            # Crear secuencia si no existe
            cursor.execute("""
                CREATE SEQUENCE IF NOT EXISTS conversations_id_seq;
            """)
            conn.commit()
            
            # Asignar la secuencia a la columna id
            cursor.execute("""
                ALTER TABLE conversations 
                ALTER COLUMN id SET DEFAULT nextval('conversations_id_seq');
            """)
            conn.commit()
            
            # Actualizar el valor de la secuencia al máximo actual
            cursor.execute("""
                SELECT setval('conversations_id_seq', COALESCE((SELECT MAX(id) FROM conversations), 0) + 1, false);
            """)
            conn.commit()
            
            print("✅ Columna ID corregida")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Verificación completada")
        print("\nAhora ejecuta: python test_bot_real.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_and_fix_conversations()
