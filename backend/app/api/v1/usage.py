from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import UsageRecord, User
from app.core.security import get_current_user

router = APIRouter(prefix="/usage", tags=["usage"])


@router.get("")
def get_usage(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(UsageRecord).filter(UsageRecord.user_id == current_user.id).order_by(UsageRecord.created_at.desc()).limit(100).all()
    return {
        "total_requests": len(records),
        "records": [
            {
                "id": r.id,
                "model_id": r.model_id,
                "status": r.status,
                "latency_ms": r.latency_ms,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]
    }