import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from typing import Dict, Any

class GoogleSheetsIntegration:
    """Integración con Google Sheets para guardar ventas y datos"""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.client = None
        self.sheet = None
    
    def connect(self, spreadsheet_name: str):
        """Conecta con Google Sheets"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope
            )
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open(spreadsheet_name)
            
            print(f"✅ Conectado a Google Sheets: {spreadsheet_name}")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Google Sheets: {e}")
            return False
    
    def log_sale(self, order_data: Dict[str, Any]):
        """Registra una venta en Google Sheets"""
        try:
            worksheet = self.sheet.worksheet("Ventas")
            
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                order_data.get("order_number"),
                order_data.get("user_phone"),
                order_data.get("user_name"),
                order_data.get("products"),
                order_data.get("total"),
                order_data.get("payment_method"),
                order_data.get("status")
            ]
            
            worksheet.append_row(row)
            print(f"✅ Venta registrada en Google Sheets: {order_data.get('order_number')}")
            
        except Exception as e:
            print(f"❌ Error registrando venta: {e}")
    
    def log_lead(self, lead_data: Dict[str, Any]):
        """Registra un lead en Google Sheets"""
        try:
            worksheet = self.sheet.worksheet("Leads")
            
            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                lead_data.get("phone"),
                lead_data.get("name"),
                lead_data.get("interest"),
                lead_data.get("stage"),
                lead_data.get("source")
            ]
            
            worksheet.append_row(row)
            print(f"✅ Lead registrado: {lead_data.get('phone')}")
            
        except Exception as e:
            print(f"❌ Error registrando lead: {e}")

# Instancia global
sheets_integration = GoogleSheetsIntegration()
