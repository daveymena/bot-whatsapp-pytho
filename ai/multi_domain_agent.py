"""
Agente Multi-Dominio
Maneja: Productos, Servicios, Agendamiento, Info General
"""
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DomainType(Enum):
    """Tipos de dominio que el bot puede manejar"""
    PRODUCT_SALES = "product_sales"           # Venta de productos físicos/digitales
    SERVICE_BOOKING = "service_booking"       # Agendamiento de servicios
    INFORMATION = "information"               # Información general
    SUPPORT = "support"                       # Soporte técnico
    COMPLAINT = "complaint"                   # Quejas/reclamos

@dataclass
class ServiceSlot:
    """Slot de tiempo para servicios"""
    date: datetime
    duration_minutes: int
    service_type: str
    available: bool = True
    price: float = 0.0

class MultiDomainAgent:
    """Agente que maneja múltiples dominios de conversación"""
    
    def __init__(self):
        self.domain_patterns = {
            DomainType.PRODUCT_SALES: [
                'comprar', 'producto', 'precio', 'stock', 'disponible',
                'catálogo', 'envío', 'pago', 'orden'
            ],
            DomainType.SERVICE_BOOKING: [
                'cita', 'agendar', 'reservar', 'turno', 'horario',
                'disponibilidad', 'consulta', 'sesión', 'servicio'
            ],
            DomainType.INFORMATION: [
                'información', 'horario', 'ubicación', 'contacto',
                'quiénes son', 'qué hacen', 'cómo funciona'
            ],
            DomainType.SUPPORT: [
                'problema', 'ayuda', 'no funciona', 'error',
                'soporte', 'falla', 'cómo usar'
            ],
            DomainType.COMPLAINT: [
                'queja', 'reclamo', 'molesto', 'insatisfecho',
                'mal servicio', 'no llegó', 'mala calidad'
            ]
        }
        
        # Horarios disponibles para servicios (ejemplo)
        self.service_hours = {
            'weekday': {'start': 9, 'end': 18},  # 9am - 6pm
            'saturday': {'start': 9, 'end': 14},  # 9am - 2pm
            'sunday': None  # Cerrado
        }
    
    def detect_domain(self, message: str, context: Dict) -> DomainType:
        """Detecta el dominio de la conversación"""
        message_lower = message.lower()
        
        scores = {}
        for domain, patterns in self.domain_patterns.items():
            score = sum(1 for pattern in patterns if pattern in message_lower)
            if score > 0:
                scores[domain] = score
        
        if not scores:
            return DomainType.INFORMATION
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def handle_service_booking(self, message: str, context: Dict) -> Dict:
        """Maneja agendamiento de servicios"""
        
        # Extraer información de la solicitud
        service_info = self._extract_booking_info(message)
        
        # Obtener slots disponibles
        available_slots = self._get_available_slots(
            service_info.get('service_type'),
            service_info.get('preferred_date')
        )
        
        return {
            'domain': DomainType.SERVICE_BOOKING,
            'service_info': service_info,
            'available_slots': available_slots,
            'next_action': 'present_slots' if available_slots else 'no_availability'
        }
    
    def _extract_booking_info(self, message: str) -> Dict:
        """Extrae información de agendamiento del mensaje"""
        info = {
            'service_type': None,
            'preferred_date': None,
            'preferred_time': None,
            'duration': 60  # Default 1 hora
        }
        
        # Detectar tipo de servicio
        service_keywords = {
            'consulta': 'Consulta General',
            'asesoría': 'Asesoría Especializada',
            'instalación': 'Instalación',
            'mantenimiento': 'Mantenimiento',
            'capacitación': 'Capacitación'
        }
        
        message_lower = message.lower()
        for keyword, service in service_keywords.items():
            if keyword in message_lower:
                info['service_type'] = service
                break
        
        # Detectar fecha (simplificado)
        date_keywords = {
            'hoy': 0,
            'mañana': 1,
            'pasado mañana': 2
        }
        
        for keyword, days_ahead in date_keywords.items():
            if keyword in message_lower:
                info['preferred_date'] = datetime.now() + timedelta(days=days_ahead)
                break
        
        return info
    
    def _get_available_slots(self, service_type: Optional[str], 
                            preferred_date: Optional[datetime]) -> List[ServiceSlot]:
        """Obtiene slots disponibles para un servicio"""
        
        if not preferred_date:
            preferred_date = datetime.now() + timedelta(days=1)
        
        # Verificar si es día laborable
        weekday = preferred_date.weekday()
        
        if weekday == 6:  # Domingo
            return []
        
        hours = self.service_hours['saturday'] if weekday == 5 else self.service_hours['weekday']
        
        # Generar slots cada hora
        slots = []
        for hour in range(hours['start'], hours['end']):
            slot_time = preferred_date.replace(hour=hour, minute=0, second=0)
            
            # Solo slots futuros
            if slot_time > datetime.now():
                slots.append(ServiceSlot(
                    date=slot_time,
                    duration_minutes=60,
                    service_type=service_type or 'General',
                    available=True,
                    price=50000  # Precio ejemplo
                ))
        
        return slots[:5]  # Máximo 5 slots
    
    def format_booking_response(self, slots: List[ServiceSlot]) -> str:
        """Formatea respuesta de agendamiento"""
        
        if not slots:
            return """
Lo siento, no tenemos disponibilidad para esa fecha 😔

¿Te gustaría ver opciones para otro día?
"""
        
        response = "📅 *Horarios Disponibles*\n\n"
        
        for i, slot in enumerate(slots, 1):
            date_str = slot.date.strftime("%d/%m/%Y")
            time_str = slot.date.strftime("%I:%M %p")
            
            response += f"{i}. {date_str} - {time_str}\n"
            response += f"   ⏱ Duración: {slot.duration_minutes} min\n"
            response += f"   💰 Valor: ${slot.price:,.0f}\n\n"
        
        response += "¿Cuál horario prefieres? 😊"
        
        return response
    
    def handle_multi_product_inquiry(self, message: str, 
                                     products: List[Dict]) -> Dict:
        """Maneja consultas sobre múltiples productos"""
        
        # Detectar si pregunta por varios productos
        product_mentions = []
        for product in products:
            if product['name'].lower() in message.lower():
                product_mentions.append(product)
        
        if len(product_mentions) > 1:
            return {
                'type': 'multi_product',
                'products': product_mentions,
                'action': 'compare_products'
            }
        elif len(product_mentions) == 1:
            return {
                'type': 'single_product',
                'product': product_mentions[0],
                'action': 'present_product'
            }
        else:
            return {
                'type': 'general_inquiry',
                'action': 'show_catalog'
            }
    
    def format_product_comparison(self, products: List[Dict]) -> str:
        """Formatea comparación de productos"""
        
        if len(products) > 3:
            products = products[:3]  # Máximo 3 productos
        
        response = "📊 *Comparación de Productos*\n\n"
        
        for i, product in enumerate(products, 1):
            response += f"{i}. *{product['name']}*\n"
            response += f"   💰 ${product['price']:,.0f}\n"
            response += f"   📦 Stock: {product['stock']} unidades\n"
            
            # Destacar diferencias clave
            if product.get('is_digital'):
                response += "   ⚡ Entrega inmediata (digital)\n"
            else:
                response += "   🚚 Envío físico\n"
            
            response += "\n"
        
        response += "¿Cuál te interesa más? 😊"
        
        return response

multi_domain_agent = MultiDomainAgent()
