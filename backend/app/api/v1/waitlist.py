from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.models import Waitlist

router = APIRouter(prefix="/waitlist", tags=["waitlist"])


class WaitlistRequest(BaseModel):
    email: EmailStr
    product: str = "nexora-jarvis"


@router.post("")
def join_waitlist(data: WaitlistRequest, db: Session = Depends(get_db)):
    existing = db.query(Waitlist).filter(Waitlist.email == data.email, Waitlist.product == data.product).first()
    if existing:
        raise HTTPException(status_code=400, detail="This email is already on the waitlist for this product.")
    entry = Waitlist(email=data.email, product=data.product)
    db.add(entry)
    db.commit()
    return {"status": "added", "message": "You have been added to the Nexora JARVIS waitlist. We will notify you at launch."}


@router.get("/status")
def waitlist_status():
    return {
        "product": "nexora-jarvis",
        "status": "coming_soon",
        "waitlist_open": True,
        "note": "Premium product. No payment required to join the waitlist. Existing Nexora AI models remain free."
    }