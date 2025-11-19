from sqlalchemy.orm import Session
from database.models import Reservation
from typing import List, Optional
from datetime import datetime, timedelta

class ReservationService:
    @staticmethod
    def create_reservation(db: Session, reservation_data: dict) -> Reservation:
        reservation = Reservation(**reservation_data)
        db.add(reservation)
        db.commit()
        db.refresh(reservation)
        return reservation
    
    @staticmethod
    def get_reservation_by_id(db: Session, reservation_id: int) -> Optional[Reservation]:
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    @staticmethod
    def get_reservations_by_phone(db: Session, phone: str) -> List[Reservation]:
        return db.query(Reservation).filter(Reservation.user_phone == phone).all()
    
    @staticmethod
    def get_available_slots(db: Session, date: datetime, service_type: str) -> List[str]:
        # Obtener reservas existentes para ese día
        start_of_day = date.replace(hour=0, minute=0, second=0)
        end_of_day = date.replace(hour=23, minute=59, second=59)
        
        existing = db.query(Reservation).filter(
            Reservation.date >= start_of_day,
            Reservation.date <= end_of_day,
            Reservation.service_type == service_type,
            Reservation.status != "cancelled"
        ).all()
        
        # Generar slots disponibles
        all_slots = []
        for hour in range(8, 18):
            all_slots.append(f"{hour:02d}:00")
            all_slots.append(f"{hour:02d}:30")
        
        # Remover slots ocupados
        occupied_times = [r.date.strftime("%H:%M") for r in existing]
        available = [slot for slot in all_slots if slot not in occupied_times]
        
        return available
    
    @staticmethod
    def cancel_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if reservation:
            reservation.status = "cancelled"
            db.commit()
            db.refresh(reservation)
        return reservation
    
    @staticmethod
    def confirm_reservation(db: Session, reservation_id: int) -> Optional[Reservation]:
        reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if reservation:
            reservation.status = "confirmed"
            db.commit()
            db.refresh(reservation)
        return reservation
