from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.schemas import Message
from app.dependencies import get_current_user, get_current_user_ws, get_chat_manager
from app.services.chat_manager import ChatManager
from app.services.audio import text_to_speech
from app.services.translator import translate_message
from app.database import fake_db

router = APIRouter()


@router.get("/chat/history/{recipient}", response_model=List[Message])
async def get_chat_history(recipient: str, current_user: dict = Depends(get_current_user), manager: ChatManager = Depends(get_chat_manager)):
    """
    GET endpoint to fetch chat history between the logged-in user and the recipient.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return manager.get_history(current_user.username, recipient)


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket, current_user: dict = Depends(get_current_user_ws), manager: ChatManager = Depends(get_chat_manager)):
    if not current_user:
        await websocket.close(code=1008)
        return
    # Accept the handshake here
    await websocket.accept()

    # Register connection
    manager.connect(current_user.username, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = Message(
                sender=current_user.username,
                recipient=data["recipient"],
                content=data["content"],
                timestamp=datetime.now(timezone.utc).isoformat()
            )

            # Translate message and generate audio
            recipient_user = next(
                (u for u in fake_db["users"] if u.username == message.recipient), None)
            if recipient_user and recipient_user.language != current_user.language:
                try:
                    # Translate using OpenAI
                    message.translated_content = await translate_message(
                        message.content, recipient_user.language
                    )
                    # Generate audio for the translated text
                    message.audio_url = await text_to_speech(
                        message.translated_content, recipient_user.language
                    )
                except Exception as e:
                    print(f"Translation or TTS error: {e}")
                    message.translated_content = None
                    message.audio_url = None

            # Save to history & broadcast to all sessions
            await manager.broadcast(message.sender, message)

    except WebSocketDisconnect:
        # We can log or ignore it
        pass
    finally:
        # Clean up connection
        manager.disconnect(current_user.username, websocket)
