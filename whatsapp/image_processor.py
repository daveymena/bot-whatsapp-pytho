"""
Image Processor - Análisis avanzado de imágenes
Incluye Vision AI, OCR y detección de comprobantes de pago
"""

import os
import openai
import base64
from PIL import Image
from io import BytesIO
import re
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            openai.api_key = self.openai_key
        
        self.temp_dir = Path('temp-media/images')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración
        self.vision_enabled = os.getenv('VISION_AI_ENABLED', 'true').lower() == 'true'
        self.ocr_enabled = os.getenv('OCR_ENABLED', 'true').lower() == 'true'
    
    async def analyze_image_with_ai(self, image_path):
        """
        Analizar imagen con GPT-4 Vision
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            str: Análisis de la imagen
        """
        if not self.vision_enabled or not self.openai_key:
            logger.warning("Vision AI not enabled or API key missing")
            return None
        
        try:
            # Leer y codificar imagen
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analiza esta imagen y describe qué ves. 
                                Si es un comprobante de pago, extrae:
                                - Monto
                                - Fecha
                                - Referencia/ID de transacción
                                - Método de pago
                                
                                Si es una foto de producto, describe el producto."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            logger.info(f"Image analyzed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing image with AI: {e}")
            return None

    
    async def extract_text_ocr(self, image_path):
        """
        Extraer texto de imagen con OCR (Tesseract)
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            str: Texto extraído
        """
        if not self.ocr_enabled:
            return None
        
        try:
            import pytesseract
            
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang='spa')
            
            logger.info(f"OCR extracted text: {len(text)} characters")
            return text
            
        except ImportError:
            logger.warning("pytesseract not installed. Install with: pip install pytesseract")
            return None
        except Exception as e:
            logger.error(f"Error in OCR: {e}")
            return None
    
    async def detect_payment_proof(self, image_path):
        """
        Detectar si la imagen es un comprobante de pago
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            dict: {
                'is_payment_proof': bool,
                'confidence': float,
                'amount': float or None,
                'reference': str or None,
                'date': str or None,
                'analysis': str,
                'extracted_text': str
            }
        """
        result = {
            'is_payment_proof': False,
            'confidence': 0.0,
            'amount': None,
            'reference': None,
            'date': None,
            'analysis': None,
            'extracted_text': None
        }
        
        try:
            # Analizar con IA
            analysis = await self.analyze_image_with_ai(image_path)
            result['analysis'] = analysis
            
            # Extraer texto con OCR
            ocr_text = await self.extract_text_ocr(image_path)
            result['extracted_text'] = ocr_text
            
            # Buscar palabras clave de pago
            payment_keywords = [
                'pago', 'transferencia', 'comprobante', 'transacción',
                'monto', 'referencia', 'aprobado', 'exitoso', 'successful',
                'bancolombia', 'nequi', 'daviplata', 'mercadopago', 'paypal'
            ]
            
            text_to_check = f"{analysis or ''} {ocr_text or ''}".lower()
            
            # Contar coincidencias
            matches = sum(1 for keyword in payment_keywords if keyword in text_to_check)
            result['confidence'] = min(matches / len(payment_keywords), 1.0)
            result['is_payment_proof'] = matches >= 2
            
            # Extraer monto
            amount = self._extract_amount(text_to_check)
            if amount:
                result['amount'] = amount
            
            # Extraer referencia
            reference = self._extract_reference(text_to_check)
            if reference:
                result['reference'] = reference
            
            logger.info(f"Payment detection: {result['is_payment_proof']} (confidence: {result['confidence']})")
            return result
            
        except Exception as e:
            logger.error(f"Error detecting payment proof: {e}")
            return result
    
    def _extract_amount(self, text):
        """Extraer monto de texto"""
        try:
            # Buscar patrones de dinero
            patterns = [
                r'\$\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)',  # $1,000.00
                r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*(?:cop|pesos|usd|dólares)',  # 1000 COP
                r'monto[:\s]+\$?\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)',  # Monto: $1000
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    amount_str = match.group(1).replace(',', '').replace('.', '')
                    return float(amount_str)
            
            return None
        except:
            return None
    
    def _extract_reference(self, text):
        """Extraer referencia/ID de transacción"""
        try:
            # Buscar patrones de referencia
            patterns = [
                r'referencia[:\s]+([A-Z0-9]{6,})',
                r'ref[:\s]+([A-Z0-9]{6,})',
                r'id[:\s]+([A-Z0-9]{6,})',
                r'transacci[oó]n[:\s]+([A-Z0-9]{6,})',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            return None
        except:
            return None
    
    async def process_image_message(self, phone, image_data):
        """
        Procesar mensaje de imagen completo
        
        Args:
            phone: Número de teléfono
            image_data: Datos binarios de la imagen
            
        Returns:
            dict: Resultado del procesamiento
        """
        try:
            # Guardar imagen temporalmente
            timestamp = datetime.now().timestamp()
            image_path = self.temp_dir / f"image_{phone}_{timestamp}.jpg"
            
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Image saved: {image_path}")
            
            # Detectar si es comprobante de pago
            payment_result = await self.detect_payment_proof(image_path)
            
            # Limpiar archivo temporal
            try:
                os.remove(image_path)
            except:
                pass
            
            return {
                'success': True,
                'is_payment_proof': payment_result['is_payment_proof'],
                'payment_data': payment_result,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Error processing image message: {e}")
            return {
                'success': False,
                'is_payment_proof': False,
                'payment_data': None,
                'error': str(e)
            }
