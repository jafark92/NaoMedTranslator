from app.database import fake_db
from fastapi import Request, WebSocket
from typing import Optional
from app.services.chat_manager import ChatManager

chat_manager = ChatManager()


def get_chat_manager() -> ChatManager:
    return chat_manager


async def get_current_user(request: Request) -> Optional[dict]:
    """Dependency for HTTP request"""
    username = request.session.get("username")
    if not username:
        return None
    user = next((u for u in fake_db["users"] if u.username == username), None)
    return user


async def get_current_user_ws(websocket: WebSocket) -> Optional[dict]:
    """Dependency for WebSocket"""
    username = websocket.session.get("username") if hasattr(
        websocket, "session") else None
    if not username:
        return None
    user = next((u for u in fake_db["users"] if u.username == username), None)
    return user
