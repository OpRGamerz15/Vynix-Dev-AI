from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.models import User, APIKey, Model, Conversation, Message, UsageRecord, Waitlist  # noqa
from app.api.v1 import auth, api_keys, models, chat, usage, admin, conversations, waitlist

app = FastAPI(
    title=settings.APP_NAME,
    description="Nexora AI — Free AI platform with its own API and specialized models. All standard models are free under fair-use limits.",
    version="0.1.0-alpha",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1")
app.include_router(api_keys.router, prefix="/v1")
app.include_router(models.router, prefix="/v1")
app.include_router(chat.router, prefix="/v1")
app.include_router(conversations.router, prefix="/v1")
app.include_router(usage.router, prefix="/v1")
app.include_router(admin.router, prefix="/v1")
app.include_router(waitlist.router, prefix="/v1")


@app.on_event("startup")
def startup():
    # Create tables for local development (use Alembic in production)
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "service": "nexora-ai", "free_access": True}


@app.get("/")
def root():
    return {
        "message": "Nexora AI API",
        "docs": "/docs",
        "models": "/v1/models",
        "note": "All standard models are free. See documentation for current availability and fair-use limits."
    }