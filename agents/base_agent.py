from abc import ABC, abstractmethod
from typing import Dict, Any
from ai.groq_client import groq_client
from ai.conversation_manager import conversation_manager

class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    async def process_message(self, user_phone: str, message: str, context: Dict[str, Any] = None) -> str:
        system_prompt = self.get_system_prompt()
        history = conversation_manager.get_history(user_phone)
        
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        messages.extend(history)
        messages.append({"role": "user", "content": message})
        
        response = await groq_client.generate_response(messages)
        
        conversation_manager.add_message(user_phone, "user", message)
        conversation_manager.add_message(user_phone, "assistant", response)
        
        return response
