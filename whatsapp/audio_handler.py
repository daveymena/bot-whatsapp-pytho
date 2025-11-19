"""
Audio Handler - Procesamiento de mensajes de voz
Transcripción con Whisper y síntesis de voz con TTS
"""

import os
import openai
from gtts import gTTS
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AudioHandler:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            openai.api_key = self.openai_key
        
        self.temp_dir = Path('temp-media/audio')
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración
        self.tts_enabled = os.getenv('TTS_ENABLED', 'false').lower() == 'true'
        self.tts_language = os.getenv('TTS_LANGUAGE', 'es')
    
    async def transcribe_audio(self, audio_path):
        """
        Transcribir audio a texto usando Whisper API
        
        Args:
            audio_path: Ruta al archivo de audio
            
        Returns:
            str: Texto transcrito o None si hay error
        """
        if not self.openai_key:
            logger.warning("OpenAI API key not configured")
            return None
        
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="es"
                )
            
            logger.info(f"Audio transcribed successfully: {transcript.text[:50]}...")
            return transcript.text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    async def text_to_speech(self, text, language=None):
        """
        Convertir texto a audio usando gTTS
        
        Args:
            text: Texto a convertir
            language: Idioma (default: español)
            
        Returns:
            str: Ruta al archivo de audio generado
        """
        if not self.tts_enabled:
            return None
        
        lang = language or self.tts_language
        
        try:
            timestamp = datetime.now().timestamp()
            output_path = self.temp_dir / f"tts_{timestamp}.mp3"
            
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(output_path))
            
            logger.info(f"TTS audio generated: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None

    
    async def process_audio_message(self, phone, audio_data, audio_format='ogg'):
        """
        Procesar mensaje de audio completo
        
        Args:
            phone: Número de teléfono del remitente
            audio_data: Datos binarios del audio
            audio_format: Formato del audio (ogg, mp3, etc)
            
        Returns:
            dict: {
                'text': texto transcrito,
                'success': bool,
                'error': mensaje de error si aplica
            }
        """
        try:
            # Guardar audio temporalmente
            timestamp = datetime.now().timestamp()
            audio_path = self.temp_dir / f"audio_{phone}_{timestamp}.{audio_format}"
            
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Audio saved: {audio_path}")
            
            # Transcribir
            text = await self.transcribe_audio(audio_path)
            
            # Limpiar archivo temporal
            try:
                os.remove(audio_path)
            except:
                pass
            
            if text:
                return {
                    'text': text,
                    'success': True,
                    'error': None
                }
            else:
                return {
                    'text': None,
                    'success': False,
                    'error': 'No se pudo transcribir el audio'
                }
                
        except Exception as e:
            logger.error(f"Error processing audio message: {e}")
            return {
                'text': None,
                'success': False,
                'error': str(e)
            }
    
    async def generate_audio_response(self, text, language=None):
        """
        Generar respuesta en audio
        
        Args:
            text: Texto de la respuesta
            language: Idioma
            
        Returns:
            str: Ruta al archivo de audio o None
        """
        if not self.tts_enabled:
            return None
        
        return await self.text_to_speech(text, language)
    
    def cleanup_old_files(self, max_age_hours=24):
        """
        Limpiar archivos de audio antiguos
        
        Args:
            max_age_hours: Edad máxima en horas
        """
        try:
            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in self.temp_dir.glob('*'):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        logger.info(f"Removed old audio file: {file_path}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old files: {e}")
