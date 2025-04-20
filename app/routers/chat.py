from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.schemas import Message, SendMessageRequest
from app.dependencies import get_current_user, get_current_user_ws, get_chat_manager
from app.services.chat_manager import ChatManager
from app.services.audio import text_to_speech
from app.services.translator import translate_message
from app.database import fake_db
from ably import AblyRest
import os

router = APIRouter()

# Initialize Ably client
ably = AblyRest(os.getenv("ABLY_API_KEY"))


@router.get("/chat/history/{recipient}", response_model=List[Message])
async def get_chat_history(recipient: str, current_user: dict = Depends(get_current_user), manager: ChatManager = Depends(get_chat_manager)):
    """
    GET endpoint to fetch chat history between the logged-in user and the recipient.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return manager.get_history(current_user.username, recipient)


# Ably instead of direct WebSocket connections
# Native WebSockets won’t work directly on Vercel’s serverless infrastructure.
@router.get("/chat/ably/token")
async def get_ably_token(current_user: dict = Depends(get_current_user)):
    """GET Endpoint, generates a token tied to the current user's username, which the frontend will use to connect to Ably"""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        token_request = ably.auth.create_token_request(
            {'clientId': current_user['username']})
        return token_request
    except Exception as e:
        print(f"Error generating Ably token: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate Ably token: {str(e)}")


@router.post("/chat/send")
async def send_message(
    request: SendMessageRequest,
    current_user: dict = Depends(get_current_user),
    manager: ChatManager = Depends(get_chat_manager)
):
    """
    POST endpoint to receive messages from clients, process them, and publish to Ably
    Backend publishes messages to Ably channels, and clients subscribe to those channels directly
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    message = Message(
        sender=current_user['username'],
        recipient=request.recipient,
        content=request.content,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

    # Translate message and generate audio if needed
    recipient_user = next(
        (u for u in fake_db["users"] if u.username == request.recipient), None)
    if recipient_user and recipient_user.language != current_user.language:
        try:
            message.translated_content = await translate_message(request.content, recipient_user.language)
            message.audio_url = await text_to_speech(message.translated_content, recipient_user.language)
        except Exception as e:
            print(f"Translation or TTS error: {e}")
            message.translated_content = None
            message.audio_url = None

    # Save to chat history
    manager.add_message(message)

    # Publish to Ably channel
    channel_name = f"chat:{':'.join(sorted([current_user['username'], request.recipient]))}"
    channel = ably.channels.get(channel_name)
    await channel.publish("message", message.model_dump())

    return {"status": "success"}
