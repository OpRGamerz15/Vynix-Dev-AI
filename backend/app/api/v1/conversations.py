from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.session import get_db
from app.models import Conversation, Message, User, Model
from app.core.security import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/conversations", tags=["conversations"])


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    model_id: str = "nexora-chat"


class MessageCreate(BaseModel):
    content: str
    role: str = "user"


class ConversationResponse(BaseModel):
    id: int
    title: str
    model_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("", response_model=ConversationResponse)
def create_conversation(data: ConversationCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == data.model_id).first()
    if not model:
        raise HTTPException(404, "Model not found")
    conv = Conversation(user_id=user.id, title=data.title, model_id=data.model_id)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("", response_model=List[ConversationResponse])
def list_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc()).all()


@router.get("/{conv_id}/messages", response_model=List[MessageResponse])
def get_messages(conv_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == user.id).first()
    if not conv:
        raise HTTPException(404, "Conversation not found")
    return conv.messages


@router.post("/{conv_id}/messages", response_model=MessageResponse)
def add_message(conv_id: int, data: MessageCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == user.id).first()
    if not conv:
        raise HTTPException(404, "Conversation not found")
    msg = Message(conversation_id=conv.id, role=data.role, content=data.content)
    db.add(msg)
    conv.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(msg)
    return msg


@router.delete("/{conv_id}")
def delete_conversation(conv_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == user.id).first()
    if not conv:
        raise HTTPException(404, "Conversation not found")
    db.delete(conv)
    db.commit()
    return {"status": "deleted"}