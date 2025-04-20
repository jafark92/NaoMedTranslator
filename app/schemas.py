from typing import Optional
from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    DOCTOR = "doctor"
    PATIENT = "patient"


class User(BaseModel):
    username: str
    role: UserRole
    language: str
    password: str  # Store hashed password


class Message(BaseModel):
    sender: str
    recipient: str
    content: str
    timestamp: str
    translated_content: Optional[str] = None  # Add translated_content field
    audio_url: Optional[str] = None  # Add audio_url field


class SendMessageRequest(BaseModel):
    recipient: str
    content: str
