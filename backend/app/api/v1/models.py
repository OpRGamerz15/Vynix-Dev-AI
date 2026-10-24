from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import Model
from app.schemas import ModelResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=List[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    return db.query(Model).all()


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model