from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
import time
import uuid
from datetime import datetime
from app.db.session import get_db
from app.models import Model, UsageRecord, APIKey
from app.schemas import ChatCompletionRequest
from app.services.providers import get_provider_for_model
from app.core.templates import get_system_prompt
from app.core.security import verify_api_key
from app.services.api_keys import get_api_key_by_prefix

router = APIRouter(prefix="/chat", tags=["chat"])


def get_api_key_from_header(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    raw_key = authorization.split(" ", 1)[1]
    if not raw_key.startswith("nx_"):
        raise HTTPException(status_code=401, detail="Invalid API key format")
    prefix = raw_key[:12]
    api_key = get_api_key_by_prefix(db, prefix)
    if not api_key or not verify_api_key(raw_key, api_key.hashed_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="API key expired")
    return api_key


@router.post("/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    api_key: APIKey = Depends(get_api_key_from_header),
    db: Session = Depends(get_db),
):
    start = time.time()
    model = db.query(Model).filter(Model.id == request.model).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if model.status != "available":
        raise HTTPException(
            status_code=503,
            detail=f"Model '{request.model}' is currently {model.status}. Free inference capacity may be exhausted or backend not configured."
        )

    system_prompt = get_system_prompt(request.model)
    messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m.role, "content": m.content} for m in request.messages
    ]

    provider = get_provider_for_model(model)
    try:
        result = await provider.chat(model, messages, temperature=request.temperature, max_tokens=request.max_tokens)
        usage = UsageRecord(
            user_id=api_key.user_id,
            api_key_id=api_key.id,
            model_id=request.model,
            request_id=str(uuid.uuid4()),
            status="success",
            latency_ms=int((time.time() - start) * 1000),
        )
        db.add(usage)
        db.commit()
        return result
    except Exception as e:
        usage = UsageRecord(
            user_id=api_key.user_id,
            api_key_id=api_key.id,
            model_id=request.model,
            request_id=str(uuid.uuid4()),
            status="capacity_exhausted",
            latency_ms=0,
        )
        db.add(usage)
        db.commit()
        raise HTTPException(
            status_code=503,
            detail=str(e) or "Temporary free capacity exhausted or no backend configured."
        )