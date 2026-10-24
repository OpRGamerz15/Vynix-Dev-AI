# Nexora AI Deployment Guide

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt email-validator
PYTHONPATH=. python scripts/seed_models.py
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker Compose
```bash
docker compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

## Production Notes
- Switch DATABASE_URL to PostgreSQL
- Use Alembic for migrations (not yet fully configured)
- Set strong SECRET_KEY and JWT_SECRET_KEY
- Configure a free/self-hosted inference backend (Ollama, vLLM, etc.) and update model status to "available" via admin endpoint
- ENABLE_PAID_PROVIDERS remains false by default
- Put behind HTTPS reverse proxy (nginx, Caddy, etc.)
- Implement full rate limiting with Redis for production scale

## Inference Setup (required for real responses)
1. Install Ollama or compatible server
2. Pull a suitable open-weight model
3. Update model backend_config in the database
4. Set model status to "available" via admin API
5. Implement the provider adapter call in `app/api/v1/chat.py` (currently returns honest 503)

All models stay free. No per-token charges for standard catalog.