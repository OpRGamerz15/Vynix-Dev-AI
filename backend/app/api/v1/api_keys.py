from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import User, APIKey
from app.schemas import APIKeyCreate, APIKeyResponse, APIKeyCreated
from app.core.security import get_current_user
from app.services.api_keys import create_api_key

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.post("", response_model=APIKeyCreated)
def create_key(key_in: APIKeyCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_key, raw_key = create_api_key(db, current_user, key_in.name, key_in.expires_in_days)
    response = APIKeyCreated.from_orm(api_key)
    response.raw_key = raw_key
    return response


@router.get("", response_model=List[APIKeyResponse])
def list_keys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(APIKey).filter(APIKey.user_id == current_user.id).all()


@router.delete("/{key_id}")
def revoke_key(key_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    key = db.query(APIKey).filter(APIKey.id == key_id, APIKey.user_id == current_user.id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    key.is_active = False
    db.commit()
    return {"status": "revoked"}