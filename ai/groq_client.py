from groq import Groq
from config.settings import settings
import random
from typing import List, Dict

class GroqClient:
    def __init__(self):
        self.api_keys = [key for key in settings.GROQ_API_KEYS if key]
        self.current_key_index = 0
        self.client = Groq(api_key=self.api_keys[0])
        
    def _rotate_key(self):
        if settings.ENABLE_GROQ_ROTATION and len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            self.client = Groq(api_key=self.api_keys[self.current_key_index])
    
    async def generate_response(self, messages: List[Dict[str, str]], max_tokens: int = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                max_tokens=max_tokens or settings.GROQ_MAX_TOKENS,
                temperature=0.7,
                top_p=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error en GROQ: {e}")
            self._rotate_key()
            raise

groq_client = GroqClient()
