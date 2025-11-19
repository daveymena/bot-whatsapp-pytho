import re
from typing import Optional

def format_phone(phone: str) -> str:
    """Formatea número de teléfono"""
    phone = re.sub(r'\D', '', phone)
    if not phone.startswith('57'):
        phone = '57' + phone
    return phone

def format_currency(amount: float) -> str:
    """Formatea moneda en COP"""
    return f"${amount:,.0f} COP"

def extract_email(text: str) -> Optional[str]:
    """Extrae email de un texto"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extrae teléfono de un texto"""
    pattern = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def clean_message(message: str) -> str:
    """Limpia un mensaje de caracteres especiales"""
    return message.strip().replace('\n\n\n', '\n\n')
