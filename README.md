# Nexora AI

**A free AI platform with its own API and specialized models.**

All standard Nexora models are free for users. No paid tiers. No per-token billing for the standard catalog. Fair-use limits apply to protect shared infrastructure.

## Status
Phases 1–7 and core of 8/9/11 implemented.  
Model registry, authentication, API keys, public OpenAI-compatible API, and usage tracking are functional.  
Real AI responses require a configured free or self-hosted inference backend (not present in the current environment). Models correctly report as unavailable and return honest capacity errors.

## Quick Start (Local Development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
# Optional: copy ../.env.example to .env and edit
PYTHONPATH=. python scripts/seed_models.py   # seed 16 free models
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 for the basic dashboard and http://localhost:8000/docs for the API.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Progress Checklist](docs/PROGRESS.md)
- [Known Issues](docs/KNOWN_ISSUES.md)

## Free Access
Every enabled model in the Nexora catalog is available without payment. See the dashboard and API docs for current rate limits and capacity status. All models start unavailable until a backend is configured.

## Models
16 specialized models (nexora-chat, nexora-developer, nexora-mc-developer, nexora-discord-developer, etc.).  
Models are only marked available when a real backend is configured and health-checked.

## License
Provided as open source. All code created for this project follows the free-access principles defined in the specification.