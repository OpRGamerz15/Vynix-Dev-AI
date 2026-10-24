import secrets
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import APIKey, User
from app.core.security import hash_api_key

def generate_api_key() -> str:
    alphabet = string.ascii_letters + string.digits
    return "nx_" + "".join(secrets.choice(alphabet) for _ in range(48))

def create_api_key(db: Session, user: User, name: str, expires_in_days: int = None) -> tuple[APIKey, str]:
    raw_key = generate_api_key()
    key_prefix = raw_key[:12]
    hashed = hash_api_key(raw_key)
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None

    api_key = APIKey(
        name=name,
        key_prefix=key_prefix,
        hashed_key=hashed,
        user_id=user.id,
        expires_at=expires_at,
        requests_per_minute=20,
        requests_per_day=500,
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key, raw_key

def get_api_key_by_prefix(db: Session, prefix: str) -> APIKey | None:
    return db.query(APIKey).filter(APIKey.key_prefix == prefix, APIKey.is_active == True).first()