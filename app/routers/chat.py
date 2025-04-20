from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from typing import List
from ably import AblyRest
from app.schemas import Message, SendMessageRequest
from app.services.audio import text_to_speech
from app.services.translator import translate_message
from app.dependencies import get_current_user
from app.database import fake_db
from app.dependencies import get_current_user, get_ably

router = APIRouter()


@router.get("/chat/history/{recipient}", response_model=List[Message])
async def get_chat_history(
    recipient: str,
    current_user: dict = Depends(get_current_user),
    ably: AblyRest = Depends(get_ably),
):
    """
    GET endpoint to fetch chat history between the logged-in user and the recipient.
    Now using Ably's built-in message history instead of local storage.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    channel_name = f"chat:{':'.join(sorted([current_user.username, recipient]))}"
    channel = ably.channels.get(channel_name)
    history = await channel.history(limit=50)
    print(channel_name)
    print(channel)
    print(history)
    return [Message(**msg.data) for msg in history.items]


@router.get("/chat/ably/token")
async def get_ably_token(
    current_user: dict = Depends(get_current_user),
    ably: AblyRest = Depends(get_ably),
):
    """
    Generate a secure token for Ably. This allows frontend to connect to Ably using token auth.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        capabilities = {
            f"chat:{current_user.username}:*": ["publish", "subscribe"],
            f"chat:*:{current_user.username}": ["publish", "subscribe"]
        }
        print(current_user.username)
        token_request = await ably.auth.request_token({
            'clientId': current_user.username,
            'ttl': 3600 * 1000,  # Optional: Token valid for 1 hour
            'capability': capabilities,
        })
        print("=====================================")
        print("Returning", token_request.token)
        return token_request.token  # Safely serialize token
    except Exception as e:
        print(f"Ably token generation error: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create Ably token")


@router.post("/chat/send")
async def send_message(
    request: SendMessageRequest,
    current_user: dict = Depends(get_current_user),
    ably: AblyRest = Depends(get_ably),
):
    """
    Receive a message, translate if needed, generate audio, and publish to Ably.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        sender = current_user.username
        recipient = request.recipient
        message = Message(
            sender=sender,
            recipient=recipient,
            content=request.content,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

        # Translate message and generate audio if needed
        recipient_user = next(
            (u for u in fake_db["users"] if u.username == recipient), None)
        if recipient_user and recipient_user.language != current_user.language:
            try:
                message.translated_content = await translate_message(request.content, recipient_user.language)
                message.audio_url = await text_to_speech(message.translated_content, recipient_user.language)
            except Exception as e:
                print(f"Translation or TTS error: {e}")
                message.translated_content = None
                message.audio_url = None

        # Publish to Ably channel
        channel_name = f"chat:{':'.join(sorted([sender, recipient]))}"
        channel = ably.channels.get(channel_name)
        await channel.publish("message", message.model_dump())

        return {"status": "success"}
    except Exception as e:
        print(f"Error generating Ably token: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate Ably token: {str(e)}")
