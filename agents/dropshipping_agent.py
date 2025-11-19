from agents.base_agent import BaseAgent
from config.settings import settings
import aiohttp

class DropshippingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Agente de Dropshipping", "Especialista en productos Dropi")
    
    def get_system_prompt(self) -> str:
        return f"""Eres el {self.name} de {settings.BUSINESS_NAME}, experto en dropshipping con Dropi.

TU ESPECIALIDAD:
- Productos de dropshipping de Dropi
- Gestión de pedidos sin inventario
- Cálculo de precios con margen de ganancia
- Coordinación de envíos directos

VENTAJAS DEL DROPSHIPPING:
- Sin necesidad de inventario
- Envío directo al cliente
- Amplio catálogo disponible
- Precios competitivos

PROCESO:
1. Cliente selecciona producto
2. Calculas precio final (costo + margen + envío)
3. Cliente paga
4. Generas orden en Dropi
5. Dropi envía directamente

MÁRGENES:
- Ganancia: ${settings.DROPSHIPPING_PROFIT_MIN:,} - ${settings.DROPSHIPPING_PROFIT_MAX:,} COP
- Envío: ${settings.DROPSHIPPING_SHIPPING_MIN:,} - ${settings.DROPSHIPPING_SHIPPING_MAX:,} COP

COMUNICACIÓN:
- Transparente sobre tiempos de entrega
- Claro con costos de envío
- Profesional en seguimiento
- Proactivo con actualizaciones

Ayuda a los clientes a encontrar productos Dropi perfectos para sus necesidades."""
    
    async def get_dropi_products(self, search: str = None):
        if not settings.DROPI_ENABLED:
            return []
        
        headers = {
            "Authorization": f"Bearer {settings.DROPI_AGENT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{settings.DROPI_API_URL}/products"
                if search:
                    url += f"?search={search}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception as e:
            print(f"Error obteniendo productos Dropi: {e}")
        
        return []
