from typing import Dict, List, Tuple
from fastapi import WebSocket
from app.schemas import Message


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.chat_history: Dict[Tuple[str, str], List[Message]] = {}

    def connect(self, user: str, websocket: WebSocket):
        self.active_connections.setdefault(user, []).append(websocket)

    def disconnect(self, user: str, websocket: WebSocket):
        conns = self.active_connections.get(user, [])
        if websocket in conns:
            conns.remove(websocket)
            if not conns:
                del self.active_connections[user]

    async def broadcast(self, sender: str, message: Message):
        # Save the message
        key = tuple(sorted([message.sender, message.recipient]))
        self.chat_history.setdefault(key, []).append(message)
        # Send to sender and recipient
        for user in [message.sender, message.recipient]:
            for ws in self.active_connections.get(user, []):
                await ws.send_json(message.dict())

    def get_history(self, u1: str, u2: str) -> List[Message]:
        key = tuple(sorted([u1, u2]))
        return self.chat_history.get(key, [])
