from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import User, Model, APIKey
from app.core.security import get_current_admin
from app.schemas import UserResponse, ModelResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def list_users(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/models/{model_id}/status")
def set_model_status(model_id: str, status: str, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    if status not in ["available", "unavailable", "disabled"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    model.status = status
    db.commit()
    return {"model_id": model_id, "status": status}


@router.get("/stats")
def admin_stats(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return {
        "total_users": db.query(User).count(),
        "total_api_keys": db.query(APIKey).count(),
        "total_models": db.query(Model).count(),
        "available_models": db.query(Model).filter(Model.status == "available").count(),
    }