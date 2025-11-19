from typing import Dict, List
from datetime import datetime, timedelta

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
        self.ttl = timedelta(hours=24)
    
    def add_message(self, phone: str, role: str, content: str):
        if phone not in self.conversations:
            self.conversations[phone] = []
        
        self.conversations[phone].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        
        self._cleanup_old_messages(phone)
    
    def get_history(self, phone: str, limit: int = 10) -> List[Dict[str, str]]:
        if phone not in self.conversations:
            return []
        
        messages = self.conversations[phone][-limit:]
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    
    def _cleanup_old_messages(self, phone: str):
        if phone not in self.conversations:
            return
        
        cutoff_time = datetime.now() - self.ttl
        self.conversations[phone] = [
            msg for msg in self.conversations[phone]
            if msg["timestamp"] > cutoff_time
        ]
    
    def clear_conversation(self, phone: str):
        if phone in self.conversations:
            del self.conversations[phone]

conversation_manager = ConversationManager()
