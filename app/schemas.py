from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    sender: str
    recipient: str
    content: str
    timestamp: str
    translated_content: Optional[str] = None  # Add translated_content field
    audio_url: Optional[str] = None  # Add audio_url field
