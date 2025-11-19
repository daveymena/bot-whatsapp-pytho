from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String)
    stock = Column(Integer, default=0)
    image_url = Column(String)
    images = Column(JSON)
    variants = Column(JSON)
    warranty = Column(String)
    is_dropshipping = Column(Boolean, default=False)
    is_digital = Column(Boolean, default=False)
    dropi_product_id = Column(String, nullable=True)
    views = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String)
    email = Column(String)
    address = Column(Text)
    is_blocked = Column(Boolean, default=False)
    spam_count = Column(Integer, default=0)
    total_purchases = Column(Float, default=0)
    purchase_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    name = Column(String)
    phone = Column(String)
    business_name = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    verification_code = Column(String)
    reset_code = Column(String)
    reset_code_expires = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text)
    intent = Column(String)
    sentiment = Column(String)
    agent_type = Column(String)
    context = Column(JSON)
    is_human = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True)
    user_phone = Column(String, nullable=False)
    user_name = Column(String)
    products = Column(JSON)
    subtotal = Column(Float, nullable=False)
    shipping = Column(Float, default=0)
    discount = Column(Float, default=0)
    total = Column(Float, nullable=False)
    status = Column(String, default="pending")
    payment_method = Column(String)
    payment_proof = Column(String)
    delivery_address = Column(Text)
    tracking_number = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String, nullable=False)
    user_name = Column(String)
    service_type = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    notes = Column(Text)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String, nullable=False)
    message_type = Column(String)
    content = Column(Text)
    direction = Column(String)
    intent = Column(String)
    sentiment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    metric_type = Column(String)
    metric_value = Column(Float)
    extra_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_phone = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    message_type = Column(String)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================
# SISTEMA DE MEMBRESÍAS Y SUSCRIPCIONES
# ============================================

class SubscriptionPlan(Base):
    """Planes de suscripción disponibles"""
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Free, Basic, Pro, Enterprise
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text)
    price_monthly = Column(Float, default=0)
    price_yearly = Column(Float, default=0)
    features = Column(JSON)  # Lista de características
    limits = Column(JSON)  # {'messages': 1000, 'products': 50, 'orders': 100}
    is_active = Column(Boolean, default=True)
    is_popular = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Subscription(Base):
    """Suscripciones de usuarios"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, nullable=False, index=True)
    plan_id = Column(Integer, nullable=False)
    status = Column(String, default='active')  # active, cancelled, expired, trial, suspended
    billing_cycle = Column(String, default='monthly')  # monthly, yearly
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    trial_end_date = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    payment_method = Column(String)  # stripe, mercadopago, paypal, manual
    stripe_subscription_id = Column(String)
    mercadopago_subscription_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = Column(DateTime)
    cancellation_reason = Column(Text)

class PaymentHistory(Base):
    """Historial de pagos de suscripciones"""
    __tablename__ = "payment_history"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, nullable=False, index=True)
    subscription_id = Column(Integer)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='COP')
    payment_method = Column(String)  # stripe, mercadopago, paypal
    status = Column(String, default='pending')  # pending, completed, failed, refunded
    transaction_id = Column(String)
    stripe_payment_intent_id = Column(String)
    mercadopago_payment_id = Column(String)
    paypal_order_id = Column(String)
    description = Column(Text)
    payment_metadata = Column(JSON)  # Cambiado de 'metadata' (palabra reservada)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

class UsageMetrics(Base):
    """Métricas de uso por usuario"""
    __tablename__ = "usage_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, nullable=False, index=True)
    metric_type = Column(String, nullable=False)  # messages, products, orders, api_calls
    count = Column(Integer, default=0)
    period = Column(String, default='monthly')  # daily, monthly, yearly
    date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VerificationCode(Base):
    """Códigos de verificación para email, teléfono y recuperación de contraseña"""
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    code = Column(String(6), nullable=False)
    type = Column(String, nullable=False)  # email, phone, password_reset
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime)
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class License(Base):
    """Licencias del sistema (alternativa a suscripciones)"""
    __tablename__ = "licenses"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, index=True)
    license_key = Column(String, unique=True, nullable=False, index=True)
    license_type = Column(String, nullable=False)  # trial, basic, pro, enterprise, lifetime
    status = Column(String, default='active')  # active, expired, revoked, suspended
    max_bots = Column(Integer, default=1)
    max_messages = Column(Integer, default=1000)
    max_products = Column(Integer, default=50)
    features = Column(JSON)
    issued_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    activated_at = Column(DateTime)
    last_validated = Column(DateTime)
    hardware_id = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
