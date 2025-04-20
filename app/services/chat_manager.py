from typing import Dict, List, Tuple
from fastapi import WebSocket
from app.schemas import Message


class ChatManager:

    def __init__(self):
        self.chat_history: Dict[Tuple[str, str], List[Message]] = {}

    def add_message(self, message: Message):
        key = tuple(sorted([message.sender, message.recipient]))
        self.chat_history.setdefault(key, []).append(message)

    def get_history(self, u1: str, u2: str) -> List[Message]:
        key = tuple(sorted([u1, u2]))
        return self.chat_history.get(key, [])
