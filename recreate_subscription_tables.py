"""
Script para recrear las tablas de suscripciones desde cero
"""
import logging
from sqlalchemy import text
from database.connection import engine, SessionLocal
from database.models import SubscriptionPlan, Subscription
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_subscription_tables():
    """Elimina y recrea las tablas de suscripciones"""
    
    try:
        logger.info("🔧 Recreando tablas de suscripciones...")
        
        with engine.connect() as conn:
            # Eliminar tablas en orden (por dependencias)
            logger.info("Eliminando tablas existentes...")
            conn.execute(text("DROP TABLE IF EXISTS subscriptions CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS subscription_plans CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS payment_history CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS usage_metrics CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS verification_codes CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS licenses CASCADE"))
            conn.commit()
            
            logger.info("Creando nuevas tablas...")
            # Crear tabla subscription_plans
            conn.execute(text("""
                CREATE TABLE subscription_plans (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    slug VARCHAR UNIQUE NOT NULL,
                    description TEXT,
                    price_monthly FLOAT DEFAULT 0,
                    price_yearly FLOAT DEFAULT 0,
                    features JSON,
                    limits JSON,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_popular BOOLEAN DEFAULT FALSE,
                    sort_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Crear tabla subscriptions
            conn.execute(text("""
                CREATE TABLE subscriptions (
                    id SERIAL PRIMARY KEY,
                    admin_user_id INTEGER NOT NULL,
                    plan_id INTEGER NOT NULL,
                    status VARCHAR DEFAULT 'active',
                    billing_cycle VARCHAR DEFAULT 'monthly',
                    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_date TIMESTAMP,
                    trial_end_date TIMESTAMP,
                    auto_renew BOOLEAN DEFAULT TRUE,
                    payment_method VARCHAR,
                    stripe_subscription_id VARCHAR,
                    mercadopago_subscription_id VARCHAR,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cancelled_at TIMESTAMP,
                    cancellation_reason TEXT
                )
            """))
            
            # Crear tabla payment_history
            conn.execute(text("""
                CREATE TABLE payment_history (
                    id SERIAL PRIMARY KEY,
                    admin_user_id INTEGER NOT NULL,
                    subscription_id INTEGER,
                    amount FLOAT NOT NULL,
                    currency VARCHAR DEFAULT 'COP',
                    payment_method VARCHAR,
                    status VARCHAR DEFAULT 'pending',
                    transaction_id VARCHAR,
                    stripe_payment_intent_id VARCHAR,
                    mercadopago_payment_id VARCHAR,
                    paypal_order_id VARCHAR,
                    description TEXT,
                    payment_metadata JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                )
            """))
            
            # Crear tabla usage_metrics
            conn.execute(text("""
                CREATE TABLE usage_metrics (
                    id SERIAL PRIMARY KEY,
                    admin_user_id INTEGER NOT NULL,
                    metric_type VARCHAR NOT NULL,
                    count INTEGER DEFAULT 0,
                    period VARCHAR DEFAULT 'monthly',
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Crear índices
            conn.execute(text("CREATE INDEX idx_subscriptions_admin_user ON subscriptions(admin_user_id)"))
            conn.execute(text("CREATE INDEX idx_payment_history_admin_user ON payment_history(admin_user_id)"))
            conn.execute(text("CREATE INDEX idx_usage_metrics_admin_user ON usage_metrics(admin_user_id)"))
            conn.execute(text("CREATE INDEX idx_usage_metrics_date ON usage_metrics(date)"))
            
            conn.commit()
            logger.info("✅ Tablas creadas exitosamente")
        
        # Insertar planes de suscripción
        db = SessionLocal()
        try:
            logger.info("Insertando planes de suscripción...")
            
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
            
            # Asignar plan gratuito a usuarios existentes
            logger.info("Asignando plan gratuito a usuarios existentes...")
            
            free_plan = db.query(SubscriptionPlan).filter_by(slug='free').first()
            
            if free_plan:
                from database.models import AdminUser
                admin_users = db.query(AdminUser).all()
                
                for user in admin_users:
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
            
            logger.info("✅ Migración completada exitosamente!")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    recreate_subscription_tables()
