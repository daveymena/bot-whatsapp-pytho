"""
Migración completa de base de datos para SaaS
Crea todas las tablas nuevas necesarias
"""

from database.connection import engine, Base
from database.models import (
    Product, User, AdminUser, Order, Conversation, Reservation,
    ChatLog, Analytics, ScheduledMessage,
    # Nuevas tablas
    SubscriptionPlan, Subscription, PaymentHistory, UsageMetrics,
    VerificationCode, License
)
from sqlalchemy.orm import Session
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Crear todas las tablas"""
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tables created successfully")

def seed_subscription_plans():
    """Crear planes de suscripción iniciales"""
    logger.info("Seeding subscription plans...")
    
    from database.connection import SessionLocal
    db = SessionLocal()
    
    try:
        # Verificar si ya existen planes
        existing = db.query(SubscriptionPlan).first()
        if existing:
            logger.info("Plans already exist, skipping...")
            return
        
        plans = [
            {
                'name': 'Free',
                'slug': 'free',
                'description': 'Plan gratuito para empezar',
                'price_monthly': 0,
                'price_yearly': 0,
                'features': [
                    '1 bot de WhatsApp',
                    '100 mensajes/mes',
                    '10 productos',
                    'Soporte por email'
                ],
                'limits': {
                    'messages': 100,
                    'products': 10,
                    'orders': 20,
                    'api_calls': 100
                },
                'is_active': True,
                'is_popular': False,
                'sort_order': 1
            },
            {
                'name': 'Basic',
                'slug': 'basic',
                'description': 'Para pequeños negocios',
                'price_monthly': 29000,
                'price_yearly': 290000,
                'features': [
                    '1 bot de WhatsApp',
                    '1,000 mensajes/mes',
                    '50 productos',
                    'Análisis básicos',
                    'Soporte prioritario'
                ],
                'limits': {
                    'messages': 1000,
                    'products': 50,
                    'orders': 200,
                    'api_calls': 1000
                },
                'is_active': True,
                'is_popular': False,
                'sort_order': 2
            },
            {
                'name': 'Pro',
                'slug': 'pro',
                'description': 'Para negocios en crecimiento',
                'price_monthly': 99000,
                'price_yearly': 990000,
                'features': [
                    '3 bots de WhatsApp',
                    '10,000 mensajes/mes',
                    'Productos ilimitados',
                    'Análisis avanzados',
                    'Integraciones premium',
                    'Soporte 24/7'
                ],
                'limits': {
                    'messages': 10000,
                    'products': -1,  # ilimitado
                    'orders': -1,
                    'api_calls': 10000
                },
                'is_active': True,
                'is_popular': True,
                'sort_order': 3
            },
            {
                'name': 'Enterprise',
                'slug': 'enterprise',
                'description': 'Para grandes empresas',
                'price_monthly': 299000,
                'price_yearly': 2990000,
                'features': [
                    'Bots ilimitados',
                    'Mensajes ilimitados',
                    'Todo ilimitado',
                    'API completa',
                    'White-label',
                    'Soporte dedicado',
                    'Onboarding personalizado'
                ],
                'limits': {
                    'messages': -1,
                    'products': -1,
                    'orders': -1,
                    'api_calls': -1
                },
                'is_active': True,
                'is_popular': False,
                'sort_order': 4
            }
        ]
        
        for plan_data in plans:
            plan = SubscriptionPlan(**plan_data)
            db.add(plan)
        
        db.commit()
        logger.info(f"✅ Created {len(plans)} subscription plans")
        
    except Exception as e:
        logger.error(f"Error seeding plans: {e}")
        db.rollback()
    finally:
        db.close()

def assign_free_plan_to_existing_users():
    """Asignar plan gratuito a usuarios existentes"""
    logger.info("Assigning free plan to existing users...")
    
    from database.connection import SessionLocal
    db = SessionLocal()
    
    try:
        # Obtener plan gratuito
        free_plan = db.query(SubscriptionPlan).filter_by(slug='free').first()
        if not free_plan:
            logger.error("Free plan not found")
            return
        
        # Obtener usuarios sin suscripción
        users = db.query(AdminUser).all()
        count = 0
        
        for user in users:
            existing_sub = db.query(Subscription).filter_by(
                admin_user_id=user.id,
                status='active'
            ).first()
            
            if not existing_sub:
                subscription = Subscription(
                    admin_user_id=user.id,
                    plan_id=free_plan.id,
                    status='active',
                    billing_cycle='monthly',
                    start_date=datetime.utcnow(),
                    auto_renew=True
                )
                db.add(subscription)
                count += 1
        
        db.commit()
        logger.info(f"✅ Assigned free plan to {count} users")
        
    except Exception as e:
        logger.error(f"Error assigning plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("🚀 Starting SaaS migration...")
    
    # 1. Crear tablas
    create_tables()
    
    # 2. Crear planes de suscripción
    seed_subscription_plans()
    
    # 3. Asignar plan gratuito a usuarios existentes
    assign_free_plan_to_existing_users()
    
    logger.info("✅ Migration completed successfully!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Update .env with email settings (SMTP_USER, SMTP_PASSWORD)")
    logger.info("2. Update .env with OpenAI API key for audio/image processing")
    logger.info("3. Run: pip install openai gtts pytesseract")
    logger.info("4. Restart the system")
