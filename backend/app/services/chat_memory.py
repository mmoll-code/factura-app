import redis.asyncio as redis
import json
from typing import List, Dict, Any, Optional

class ChatMemoryService:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self._redis = None

    async def connect(self):
        if not self._redis:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)

    async def add_message(self, chat_id: str, message: Dict[str, Any]) -> None:
        await self.connect()
        key = f"chat_history:{chat_id}"
        await self._redis.rpush(key, json.dumps(message))

    async def get_history(self, chat_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        await self.connect()
        key = f"chat_history:{chat_id}"
        if limit:
            messages = await self._redis.lrange(key, -limit, -1)
        else:
            messages = await self._redis.lrange(key, 0, -1)
        return [json.loads(m) for m in messages]

    async def clear_history(self, chat_id: str) -> None:
        await self.connect()
        key = f"chat_history:{chat_id}"
        await self._redis.delete(key)

    async def set_state(self, chat_id: str, state: Dict[str, Any]) -> None:
        await self.connect()
        key = f"chat_state:{chat_id}"
        await self._redis.set(key, json.dumps(state))

    async def get_state(self, chat_id: str) -> Optional[Dict[str, Any]]:
        await self.connect()
        key = f"chat_state:{chat_id}"
        value = await self._redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def clear_state(self, chat_id: str) -> None:
        await self.connect()
        key = f"chat_state:{chat_id}"
        await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
            self._redis = None

# Example usage (to be used in endpoints or services):
# chat_memory = ChatMemoryService(redis_url="redis://localhost:6379/0")
# await chat_memory.add_message(chat_id, message)
# history = await chat_memory.get_history(chat_id)
