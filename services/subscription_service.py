"""
Subscription Service - Gestión de suscripciones y límites
"""

from datetime import datetime, timedelta
from database.models import Subscription, SubscriptionPlan, UsageMetrics, PaymentHistory
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_subscription(self, user_id: int):
        """Obtener suscripción activa del usuario"""
        return self.db.query(Subscription).filter(
            Subscription.admin_user_id == user_id,
            Subscription.status.in_(['active', 'trial'])
        ).first()
    
    def get_plan(self, plan_id: int):
        """Obtener plan por ID"""
        return self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id,
            SubscriptionPlan.is_active == True
        ).first()
    
    def get_plan_by_slug(self, slug: str):
        """Obtener plan por slug"""
        return self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.slug == slug,
            SubscriptionPlan.is_active == True
        ).first()
    
    def check_limit(self, user_id: int, metric_type: str):
        """
        Verificar si el usuario ha alcanzado su límite
        
        Returns:
            tuple: (allowed: bool, current_count: int, limit: int, message: str)
        """
        subscription = self.get_user_subscription(user_id)
        
        if not subscription:
            return False, 0, 0, "No hay suscripción activa"
        
        plan = self.get_plan(subscription.plan_id)
        if not plan:
            return False, 0, 0, "Plan no encontrado"
        
        limits = plan.limits or {}
        limit = limits.get(metric_type, float('inf'))
        
        # Si el límite es infinito, permitir
        if limit == float('inf') or limit == -1:
            return True, 0, -1, "Ilimitado"
        
        # Obtener uso actual del mes
        today = datetime.utcnow().date()
        first_day = today.replace(day=1)
        
        usage = self.db.query(UsageMetrics).filter(
            UsageMetrics.admin_user_id == user_id,
            UsageMetrics.metric_type == metric_type,
            UsageMetrics.date >= first_day,
            UsageMetrics.period == 'monthly'
        ).first()
        
        current_count = usage.count if usage else 0
        
        if current_count >= limit:
            return False, current_count, limit, f"Límite de {metric_type} alcanzado ({current_count}/{limit})"
        
        return True, current_count, limit, "OK"

    
    def increment_usage(self, user_id: int, metric_type: str, count: int = 1):
        """Incrementar contador de uso"""
        today = datetime.utcnow().date()
        
        usage = self.db.query(UsageMetrics).filter(
            UsageMetrics.admin_user_id == user_id,
            UsageMetrics.metric_type == metric_type,
            UsageMetrics.date == today,
            UsageMetrics.period == 'monthly'
        ).first()
        
        if usage:
            usage.count += count
            usage.updated_at = datetime.utcnow()
        else:
            usage = UsageMetrics(
                admin_user_id=user_id,
                metric_type=metric_type,
                count=count,
                period='monthly',
                date=today
            )
            self.db.add(usage)
        
        self.db.commit()
        logger.info(f"Usage incremented: user={user_id}, type={metric_type}, count={count}")
    
    def create_subscription(self, user_id: int, plan_id: int, billing_cycle: str = 'monthly'):
        """Crear nueva suscripción"""
        plan = self.get_plan(plan_id)
        if not plan:
            raise ValueError("Plan no encontrado")
        
        # Cancelar suscripción anterior si existe
        old_subscription = self.get_user_subscription(user_id)
        if old_subscription:
            old_subscription.status = 'cancelled'
            old_subscription.cancelled_at = datetime.utcnow()
        
        # Calcular fechas
        start_date = datetime.utcnow()
        if billing_cycle == 'yearly':
            end_date = start_date + timedelta(days=365)
        else:
            end_date = start_date + timedelta(days=30)
        
        # Crear nueva suscripción
        subscription = Subscription(
            admin_user_id=user_id,
            plan_id=plan_id,
            status='active',
            billing_cycle=billing_cycle,
            start_date=start_date,
            end_date=end_date,
            auto_renew=True
        )
        
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        logger.info(f"Subscription created: user={user_id}, plan={plan.name}")
        return subscription
    
    def create_trial_subscription(self, user_id: int, trial_days: int = 14):
        """Crear suscripción de prueba"""
        # Buscar plan Pro o el más alto
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.slug == 'pro',
            SubscriptionPlan.is_active == True
        ).first()
        
        if not plan:
            # Si no hay plan Pro, usar el primero disponible
            plan = self.db.query(SubscriptionPlan).filter(
                SubscriptionPlan.is_active == True
            ).first()
        
        if not plan:
            raise ValueError("No hay planes disponibles")
        
        start_date = datetime.utcnow()
        trial_end = start_date + timedelta(days=trial_days)
        
        subscription = Subscription(
            admin_user_id=user_id,
            plan_id=plan.id,
            status='trial',
            billing_cycle='monthly',
            start_date=start_date,
            trial_end_date=trial_end,
            end_date=trial_end,
            auto_renew=False
        )
        
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        
        logger.info(f"Trial subscription created: user={user_id}, days={trial_days}")
        return subscription
    
    def cancel_subscription(self, subscription_id: int, reason: str = None):
        """Cancelar suscripción"""
        subscription = self.db.query(Subscription).get(subscription_id)
        if not subscription:
            raise ValueError("Suscripción no encontrada")
        
        subscription.status = 'cancelled'
        subscription.cancelled_at = datetime.utcnow()
        subscription.cancellation_reason = reason
        subscription.auto_renew = False
        
        self.db.commit()
        logger.info(f"Subscription cancelled: id={subscription_id}")
        return subscription
    
    def record_payment(self, user_id: int, subscription_id: int, amount: float, 
                      payment_method: str, transaction_id: str = None):
        """Registrar pago"""
        payment = PaymentHistory(
            admin_user_id=user_id,
            subscription_id=subscription_id,
            amount=amount,
            payment_method=payment_method,
            status='completed',
            transaction_id=transaction_id,
            completed_at=datetime.utcnow()
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        logger.info(f"Payment recorded: user={user_id}, amount={amount}")
        return payment
    
    def get_usage_stats(self, user_id: int):
        """Obtener estadísticas de uso del usuario"""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return None
        
        plan = self.get_plan(subscription.plan_id)
        limits = plan.limits or {}
        
        today = datetime.utcnow().date()
        first_day = today.replace(day=1)
        
        stats = {}
        for metric_type in ['messages', 'products', 'orders', 'api_calls']:
            usage = self.db.query(UsageMetrics).filter(
                UsageMetrics.admin_user_id == user_id,
                UsageMetrics.metric_type == metric_type,
                UsageMetrics.date >= first_day,
                UsageMetrics.period == 'monthly'
            ).first()
            
            current = usage.count if usage else 0
            limit = limits.get(metric_type, -1)
            
            stats[metric_type] = {
                'current': current,
                'limit': limit,
                'percentage': (current / limit * 100) if limit > 0 else 0
            }
        
        return {
            'subscription': {
                'plan_name': plan.name,
                'status': subscription.status,
                'end_date': subscription.end_date.isoformat() if subscription.end_date else None
            },
            'usage': stats
        }
