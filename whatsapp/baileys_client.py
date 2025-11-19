import asyncio
import json
import os
from typing import Callable
import aiohttp
from config.settings import settings

class BaileysClient:
    """
    Cliente de WhatsApp usando Baileys (Node.js)
    Esta es una interfaz Python que se comunica con un proceso Node.js
    """
    
    def __init__(self):
        self.session_path = settings.SESSION_PATH
        self.connected = False
        self.reconnect_attempts = 0
        self.message_handler = None
        self.baileys_url = "http://localhost:3002"
        
    async def initialize(self):
        """Inicializa la conexión con WhatsApp"""
        os.makedirs(self.session_path, exist_ok=True)
        print(f"📱 Inicializando cliente WhatsApp...")
        print(f"📂 Sesión: {self.session_path}")
        
        # Verificar conexión con Baileys
        await self._check_baileys_connection()
        
    async def _check_baileys_connection(self):
        """Verifica la conexión con el servidor Baileys"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.baileys_url}/status", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.connected = data.get("connected", False)
                        if self.connected:
                            print("✅ Conectado a WhatsApp via Baileys")
                        else:
                            print("⚠️ Baileys activo pero WhatsApp no conectado")
                            print("📱 Escanea el QR code en la terminal de Node.js")
        except Exception as e:
            print(f"⚠️ No se pudo conectar con Baileys: {e}")
            print("💡 Asegúrate de ejecutar: npm start")
        
    async def send_message(self, phone: str, message: str):
        """Envía un mensaje de WhatsApp"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "phone": phone,
                    "message": message,
                    "simulateTyping": settings.ENABLE_TYPING_SIMULATION
                }
                async with session.post(
                    f"{self.baileys_url}/send-message",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        print(f"📤 Mensaje enviado a {phone}")
                    else:
                        error = await response.text()
                        print(f"❌ Error enviando mensaje: {error}")
        except Exception as e:
            print(f"❌ Error en send_message: {e}")
        
    async def send_image(self, phone: str, image_url: str, caption: str = ""):
        """Envía una imagen por WhatsApp"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "phone": phone,
                    "imageUrl": image_url,
                    "caption": caption
                }
                async with session.post(
                    f"{self.baileys_url}/send-image",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        print(f"📸 Imagen enviada a {phone}")
                    else:
                        error = await response.text()
                        print(f"❌ Error enviando imagen: {error}")
        except Exception as e:
            print(f"❌ Error en send_image: {e}")
        
    async def _simulate_typing(self, phone: str, message: str):
        """Simula que el bot está escribiendo"""
        import random
        typing_time = len(message) / random.randint(
            settings.TYPING_SPEED_MIN,
            settings.TYPING_SPEED_MAX
        )
        delay = random.randint(
            settings.TYPING_DELAY_MIN,
            settings.TYPING_DELAY_MAX
        ) / 1000
        
        await asyncio.sleep(min(typing_time + delay, 5))
        
    def on_message(self, handler: Callable):
        """Registra el manejador de mensajes entrantes"""
        self.message_handler = handler
        
    async def start_heartbeat(self):
        """Mantiene la conexión activa"""
        while self.connected:
            await asyncio.sleep(settings.HEARTBEAT_INTERVAL / 1000)
            # Verificar estado de conexión
            
    async def reconnect(self):
        """Reconecta al servidor de WhatsApp"""
        if self.reconnect_attempts >= settings.RECONNECT_ATTEMPTS_MAX:
            print("❌ Máximo de intentos de reconexión alcanzado")
            return False
        
        self.reconnect_attempts += 1
        delay = min(
            settings.RECONNECT_DELAY_BASE * (2 ** self.reconnect_attempts),
            settings.RECONNECT_DELAY_MAX
        ) / 1000
        
        print(f"🔄 Reconectando en {delay}s (intento {self.reconnect_attempts})...")
        await asyncio.sleep(delay)
        
        try:
            await self.initialize()
            self.reconnect_attempts = 0
            return True
        except Exception as e:
            print(f"❌ Error en reconexión: {e}")
            return False

baileys_client = BaileysClient()
