from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import ScheduledMessage, Reservation, Order
from whatsapp.baileys_client import baileys_client

scheduler = AsyncIOScheduler()

async def send_scheduled_messages():
    """Envía mensajes programados"""
    db = SessionLocal()
    try:
        now = datetime.now()
        messages = db.query(ScheduledMessage).filter(
            ScheduledMessage.scheduled_for <= now,
            ScheduledMessage.sent == False
        ).all()
        
        for msg in messages:
            try:
                await baileys_client.send_message(msg.user_phone, msg.message)
                msg.sent = True
                db.commit()
                print(f"✅ Mensaje programado enviado a {msg.user_phone}")
            except Exception as e:
                print(f"❌ Error enviando mensaje programado: {e}")
    finally:
        db.close()

async def send_reservation_reminders():
    """Envía recordatorios de reservas"""
    db = SessionLocal()
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0)
        tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59)
        
        reservations = db.query(Reservation).filter(
            Reservation.date >= tomorrow_start,
            Reservation.date <= tomorrow_end,
            Reservation.status == "confirmed",
            Reservation.reminder_sent == False
        ).all()
        
        for reservation in reservations:
            message = f"""🔔 *Recordatorio de Cita*

Hola {reservation.user_name}! 👋

Te recordamos tu cita para mañana:

📅 Fecha: {reservation.date.strftime('%d/%m/%Y')}
🕐 Hora: {reservation.date.strftime('%I:%M %p')}
🎯 Servicio: {reservation.service_type}

Por favor confirma tu asistencia respondiendo este mensaje.

¡Te esperamos! 😊"""
            
            try:
                await baileys_client.send_message(reservation.user_phone, message)
                reservation.reminder_sent = True
                db.commit()
                print(f"✅ Recordatorio enviado a {reservation.user_phone}")
            except Exception as e:
                print(f"❌ Error enviando recordatorio: {e}")
    finally:
        db.close()

async def send_order_updates():
    """Envía actualizaciones de pedidos"""
    db = SessionLocal()
    try:
        # Pedidos pendientes de pago por más de 24h
        cutoff = datetime.now() - timedelta(hours=24)
        pending_orders = db.query(Order).filter(
            Order.status == "pending",
            Order.created_at < cutoff
        ).all()
        
        for order in pending_orders:
            message = f"""⏰ *Recordatorio de Pedido*

Hola! Notamos que tu pedido #{order.order_number} aún está pendiente de pago.

💰 Total: ${order.total:,.0f} COP

¿Necesitas ayuda para completar tu compra? Estamos aquí para asistirte! 😊"""
            
            try:
                await baileys_client.send_message(order.user_phone, message)
                print(f"✅ Recordatorio de pago enviado a {order.user_phone}")
            except Exception as e:
                print(f"❌ Error enviando recordatorio de pago: {e}")
    finally:
        db.close()

def start_scheduler():
    """Inicia el programador de tareas"""
    # Mensajes programados - cada 5 minutos
    scheduler.add_job(send_scheduled_messages, 'interval', minutes=5)
    
    # Recordatorios de reservas - cada hora
    scheduler.add_job(send_reservation_reminders, 'interval', hours=1)
    
    # Actualizaciones de pedidos - cada 6 horas
    scheduler.add_job(send_order_updates, 'interval', hours=6)
    
    scheduler.start()
    print("✅ Programador de tareas iniciado")
