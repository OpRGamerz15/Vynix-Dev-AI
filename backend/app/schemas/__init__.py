from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class APIKeyCreate(BaseModel):
    name: str
    expires_in_days: Optional[int] = None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key_prefix: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    requests_per_minute: int
    requests_per_day: int

    class Config:
        from_attributes = True


class APIKeyCreated(APIKeyResponse):
    raw_key: str  # shown only once


class ModelResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    is_free: bool
    backend_type: Optional[str]

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: Optional[dict] = None