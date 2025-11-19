"""
Script para crear la tabla de usuarios administradores
"""
from database.connection import engine
from database.models import Base, AdminUser
from sqlalchemy import inspect

def create_admin_users_table():
    """Crear tabla admin_users si no existe"""
    inspector = inspect(engine)
    
    if 'admin_users' not in inspector.get_table_names():
        print("📝 Creando tabla admin_users...")
        AdminUser.__table__.create(engine)
        print("✅ Tabla admin_users creada exitosamente")
    else:
        print("ℹ️  La tabla admin_users ya existe")

if __name__ == "__main__":
    create_admin_users_table()
