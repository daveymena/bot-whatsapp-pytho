import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    # AI Configuration
    GROQ_API_KEYS: List[str] = [
        os.getenv("GROQ_API_KEY", ""),
        os.getenv("GROQ_API_KEY_2", ""),
        os.getenv("GROQ_API_KEY_6", "")
    ]
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    GROQ_MAX_TOKENS: int = int(os.getenv("GROQ_MAX_TOKENS", "1000"))
    GROQ_TIMEOUT: int = int(os.getenv("GROQ_TIMEOUT", "60000"))
    ENABLE_GROQ_ROTATION: bool = os.getenv("ENABLE_GROQ_ROTATION", "true").lower() == "true"
    
    # WhatsApp
    WHATSAPP_NUMBER: str = os.getenv("WHATSAPP_NUMBER", "")
    SESSION_PATH: str = os.getenv("SESSION_PATH", "./data/whatsapp-sessions")
    HEARTBEAT_INTERVAL: int = int(os.getenv("HEARTBEAT_INTERVAL", "10000"))
    RECONNECT_ATTEMPTS_MAX: int = int(os.getenv("RECONNECT_ATTEMPTS_MAX", "100"))
    ENABLE_TYPING_SIMULATION: bool = os.getenv("ENABLE_TYPING_SIMULATION", "true").lower() == "true"
    TYPING_SPEED_MIN: int = int(os.getenv("TYPING_SPEED_MIN", "40"))
    TYPING_SPEED_MAX: int = int(os.getenv("TYPING_SPEED_MAX", "100"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Business
    BUSINESS_NAME: str = os.getenv("BUSINESS_NAME", "Tecnovariedades D&S")
    BOT_NAME: str = os.getenv("BOT_NAME", "Tecnovariedades D&S Bot")
    BUSINESS_PHONE: str = os.getenv("BUSINESS_PHONE", "")
    BUSINESS_EMAIL: str = os.getenv("BUSINESS_EMAIL", "")
    BOT_LANGUAGE: str = os.getenv("BOT_LANGUAGE", "es")
    
    # Payment
    NEQUI_NUMBER: str = os.getenv("NEQUI_NUMBER", "")
    DAVIPLATA_NUMBER: str = os.getenv("DAVIPLATA_NUMBER", "")
    BANK_NAME: str = os.getenv("BANK_NAME", "Bancolombia")
    BANK_ACCOUNT_TYPE: str = os.getenv("BANK_ACCOUNT_TYPE", "Ahorros")
    BANK_ACCOUNT_NUMBER: str = os.getenv("BANK_ACCOUNT_NUMBER", "")
    BANK_ACCOUNT_HOLDER: str = os.getenv("BANK_ACCOUNT_HOLDER", "")
    
    # Mercado Pago
    MERCADOPAGO_ENABLED: bool = os.getenv("MERCADOPAGO_ENABLED", "true").lower() == "true"
    MERCADOPAGO_ACCESS_TOKEN: str = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")
    
    # PayPal
    PAYPAL_ENABLED: bool = os.getenv("PAYPAL_ENABLED", "true").lower() == "true"
    PAYPAL_MODE: str = os.getenv("PAYPAL_MODE", "sandbox")  # sandbox o live
    PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID", "")
    PAYPAL_CLIENT_SECRET: str = os.getenv("PAYPAL_CLIENT_SECRET", "")
    USD_TO_COP_RATE: float = float(os.getenv("USD_TO_COP_RATE", "4000"))
    
    # Delivery
    DELIVERY_ZONES: str = os.getenv("DELIVERY_ZONES", "Bogotá, Medellín, Cali")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:5000")
    
    # Dropshipping
    DROPI_ENABLED: bool = os.getenv("DROPI_ENABLED", "true").lower() == "true"
    DROPI_API_URL: str = os.getenv("DROPI_API_URL", "")
    DROPI_AGENT_TOKEN: str = os.getenv("DROPI_AGENT_TOKEN", "")
    
    # Features
    ENABLE_CONVERSATION_MEMORY: bool = os.getenv("ENABLE_CONVERSATION_MEMORY", "true").lower() == "true"
    PHOTOS_ENABLED: bool = os.getenv("PHOTOS_ENABLED", "true").lower() == "true"

settings = Settings()
