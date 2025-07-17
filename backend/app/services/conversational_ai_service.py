from app.clients.openai_client.base_client import OpenAIBaseClient
from typing import List, Dict

class ConversationalAIService:
    def __init__(self, openai_api_key: str):
        self.openai_client = OpenAIBaseClient(api_key=openai_api_key)

    def get_ai_response(self, history: List[Dict], user_id: str) -> str:
        messages = self._format_history_for_openai(history, user_id)
        return self.openai_client.chat_completion(messages)

    def _format_history_for_openai(self, history: List[Dict], user_id: str) -> List[Dict]:
        messages = []
        for msg in history:
            if msg["from"] == user_id:
                messages.append({"role": "user", "content": msg["body"]})
            else:
                messages.append({"role": "assistant", "content": msg["body"]})
        return messages 