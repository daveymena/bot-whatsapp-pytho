import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from whatsapp.baileys_client import baileys_client
from whatsapp.message_handler import message_handler
from database.connection import init_db
from config.settings import settings
from admin.panel_routes import router as admin_router
from admin.auth_routes import router as auth_router
from admin.stats_routes import router as stats_router
from services.scheduler import start_scheduler
from ai.context_manager import context_manager
import os

app = FastAPI(
    title="WhatsApp Sales Bot Pro",
    version="2.0.0",
    description="Bot de ventas inteligente con IA, multi-agente y panel de administración"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
static_path = os.path.join(os.path.dirname(__file__), "admin", "static")
if os.path.exists(static_path):
    app.mount("/admin/static", StaticFiles(directory=static_path), name="static")

# Registrar routers
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(stats_router)

# Importar y registrar rutas de pago
from admin.payment_routes import router as payment_router
app.include_router(payment_router)

# Importar y registrar rutas de productos
from admin.products_routes import router as products_router
app.include_router(products_router)

# Importar y registrar rutas de IA de ventas
from admin.ai_sales_routes import router as ai_sales_router
app.include_router(ai_sales_router)

# Importar y registrar rutas de la tienda pública
from admin.shop_routes import router as shop_router
app.include_router(shop_router)

class MessageRequest(BaseModel):
    phone: str
    message: str

class HumanTakeoverRequest(BaseModel):
    phone: str
    agent_id: str
    action: str

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🚀 INICIANDO BOT DE VENTAS WHATSAPP PRO")
    print("=" * 60)
    print(f"🏢 Negocio: {settings.BUSINESS_NAME}")
    print(f"📱 Número: {settings.WHATSAPP_NUMBER}")
    
    init_db()
    print("✅ Base de datos lista")
    
    await baileys_client.initialize()
    baileys_client.on_message(handle_incoming_message)
    asyncio.create_task(baileys_client.start_heartbeat())
    
    start_scheduler()
    asyncio.create_task(cleanup_contexts_periodically())
    
    print("\n✅ BOT COMPLETAMENTE OPERATIVO")
    print(f"🌐 Panel Admin: http://localhost:5000/admin/dashboard\n")

async def handle_incoming_message(phone: str, message: str):
    try:
        response = await message_handler.handle_message(phone, message)
        if response:
            await baileys_client.send_message(phone, response)
    except Exception as e:
        print(f"❌ Error: {e}")

async def cleanup_contexts_periodically():
    while True:
        await asyncio.sleep(3600)
        context_manager.cleanup_old_contexts()

@app.get("/")
async def root():
    return {
        "status": "online",
        "bot": settings.BOT_NAME,
        "version": "2.0.0",
        "features": ["Multi-agente", "NLP", "AIDA", "Anti-spam", "Panel Admin"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "whatsapp_connected": baileys_client.connected,
        "active_conversations": len(context_manager.contexts)
    }

@app.post("/send-message")
async def send_message(request: MessageRequest):
    await baileys_client.send_message(request.phone, request.message)
    return {"status": "sent"}

@app.post("/human-takeover")
async def human_takeover(request: HumanTakeoverRequest):
    if request.action == "enable":
        result = message_handler.enable_human_takeover(request.phone, request.agent_id)
    else:
        result = message_handler.disable_human_takeover(request.phone)
    return {"status": "success", "message": result}

@app.get("/context/{phone}")
async def get_user_context(phone: str):
    return context_manager.get_summary(phone)

@app.post("/webhook/message")
async def webhook_message(request: dict):
    """Webhook para recibir mensajes desde Baileys"""
    phone = request.get("phone")
    message = request.get("message")
    
    if not phone or not message:
        raise HTTPException(status_code=400, detail="Phone and message required")
    
    try:
        response = await message_handler.handle_message(phone, message)
        return {"reply": response}
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
