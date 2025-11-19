"""Script para inicializar la base de datos"""
from database.connection import engine
from database.models import Base

print("🔧 Creando tablas en la base de datos...")

try:
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente!")
    print("\nTablas creadas:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")
except Exception as e:
    print(f"❌ Error creando tablas: {e}")
