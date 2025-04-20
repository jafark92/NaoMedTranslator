from app.database import fake_db
from fastapi import Request, WebSocket
from typing import Optional
from ably import AblyRest


def get_ably(request: Request) -> AblyRest:
    return request.app.state.ably


async def get_current_user(request: Request) -> Optional[dict]:
    """Dependency for HTTP request"""
    username = request.session.get("username")
    if not username:
        return None
    user = next((u for u in fake_db["users"] if u.username == username), None)
    return user
