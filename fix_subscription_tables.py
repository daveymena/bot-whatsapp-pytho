"""
Script para actualizar las tablas de suscripciones
"""
import logging
from sqlalchemy import text
from database.connection import engine, SessionLocal
from database.models import SubscriptionPlan, Subscription
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_subscription_tables():
    """Actualiza las tablas de suscripciones"""
    db = SessionLocal()
    
    try:
        logger.info("🔧 Actualizando tablas de suscripciones...")
        
        # Agregar columnas faltantes a subscription_plans si no existen
        with engine.connect() as conn:
            # Verificar si la columna slug existe
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='subscription_plans' AND column_name='slug'
            """))
            
            if not result.fetchone():
                logger.info("Agregando columna 'slug' a subscription_plans...")
                conn.execute(text("ALTER TABLE subscription_plans ADD COLUMN slug VARCHAR UNIQUE"))
                conn.commit()
            
            # Verificar otras columnas
            columns_to_add = [
                ("description", "TEXT"),
                ("price_monthly", "FLOAT DEFAULT 0"),
                ("price_yearly", "FLOAT DEFAULT 0"),
                ("features", "JSON"),
                ("limits", "JSON"),
                ("is_active", "BOOLEAN DEFAULT TRUE"),
                ("is_popular", "BOOLEAN DEFAULT FALSE"),
                ("sort_order", "INTEGER DEFAULT 0"),
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
                ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            ]
            
            for col_name, col_type in columns_to_add:
                result = conn.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='subscription_plans' AND column_name='{col_name}'
                """))
                
                if not result.fetchone():
                    logger.info(f"Agregando columna '{col_name}' a subscription_plans...")
                    conn.execute(text(f"ALTER TABLE subscription_plans ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
        
        # Limpiar planes existentes
        logger.info("Limpiando planes existentes...")
        db.query(SubscriptionPlan).delete()
        db.commit()
        
        # Crear planes de suscripción
        logger.info("Creando planes de suscripción...")
        
        plans = [
            {
                "name": "Free",
                "slug": "free",
                "description": "Plan gratuito para probar el sistema",
                "price_monthly": 0,
                "price_yearly": 0,
                "features": [
                    "1 bot de WhatsApp",
                    "100 mensajes/mes",
                    "10 productos",
                    "Soporte por email"
                ],
                "limits": {
                    "messages": 100,
                    "products": 10,
                    "orders": 20,
                    "bots": 1
                },
                "is_active": True,
                "is_popular": False,
                "sort_order": 1
            },
            {
                "name": "Basic",
                "slug": "basic",
                "description": "Ideal para pequeños negocios",
                "price_monthly": 29000,
                "price_yearly": 290000,
                "features": [
                    "1 bot de WhatsApp",
                    "1,000 mensajes/mes",
                    "50 productos",
                    "Procesamiento de imágenes",
                    "Soporte prioritario"
                ],
                "limits": {
                    "messages": 1000,
                    "products": 50,
                    "orders": 200,
                    "bots": 1
                },
                "is_active": True,
                "is_popular": False,
                "sort_order": 2
            },
            {
                "name": "Pro",
                "slug": "pro",
                "description": "Para negocios en crecimiento",
                "price_monthly": 99000,
                "price_yearly": 990000,
                "features": [
                    "3 bots de WhatsApp",
                    "10,000 mensajes/mes",
                    "Productos ilimitados",
                    "IA avanzada",
                    "Procesamiento de audio",
                    "Análisis de sentimientos",
                    "Soporte 24/7"
                ],
                "limits": {
                    "messages": 10000,
                    "products": -1,
                    "orders": -1,
                    "bots": 3
                },
                "is_active": True,
                "is_popular": True,
                "sort_order": 3
            },
            {
                "name": "Enterprise",
                "slug": "enterprise",
                "description": "Solución completa para empresas",
                "price_monthly": 299000,
                "price_yearly": 2990000,
                "features": [
                    "Bots ilimitados",
                    "Mensajes ilimitados",
                    "Productos ilimitados",
                    "IA personalizada",
                    "Integración con CRM",
                    "API completa",
                    "Soporte dedicado",
                    "Onboarding personalizado"
                ],
                "limits": {
                    "messages": -1,
                    "products": -1,
                    "orders": -1,
                    "bots": -1
                },
                "is_active": True,
                "is_popular": False,
                "sort_order": 4
            }
        ]
        
        for plan_data in plans:
            plan = SubscriptionPlan(**plan_data)
            db.add(plan)
        
        db.commit()
        logger.info(f"✅ {len(plans)} planes creados exitosamente")
        
        # Asignar plan gratuito a usuarios existentes sin suscripción
        logger.info("Asignando plan gratuito a usuarios existentes...")
        
        free_plan = db.query(SubscriptionPlan).filter_by(slug='free').first()
        
        if free_plan:
            # Obtener usuarios admin sin suscripción
            from database.models import AdminUser
            admin_users = db.query(AdminUser).all()
            
            for user in admin_users:
                # Verificar si ya tiene suscripción
                existing_sub = db.query(Subscription).filter_by(admin_user_id=user.id).first()
                
                if not existing_sub:
                    subscription = Subscription(
                        admin_user_id=user.id,
                        plan_id=free_plan.id,
                        status='active',
                        billing_cycle='monthly',
                        start_date=datetime.utcnow(),
                        trial_end_date=datetime.utcnow() + timedelta(days=14),
                        auto_renew=False
                    )
                    db.add(subscription)
            
            db.commit()
            logger.info(f"✅ Plan gratuito asignado a {len(admin_users)} usuarios")
        
        logger.info("✅ Actualización completada exitosamente!")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_subscription_tables()
