# Nexora AI — Master Specification and Architecture

**Project Name:** Nexora AI  
**Version:** 0.1.0-alpha (Phase 1)  
**Status:** Architecture Defined — Implementation Starting  
**Free Access Policy:** All standard Nexora models are free for users. No paid tiers, no per-token billing for standard catalog. Fair-use rate limits and capacity controls apply.  
**Last Updated:** 2026-10-23  

## Core Mission
Nexora AI is a complete, free AI platform providing:
- Unified chat interface with specialized models
- Public developer API (OpenAI-compatible)
- Secure API key management
- Database-backed model registry
- Routing layer for self-hosted and optional external backends
- Developer portal and administrative console
- Persistent conversation history
- Usage tracking and capacity management

All 16 standard models follow the free-access policy. Models are only marked operational when a real, configured backend is available and verified.

## Free Access Principles
- No subscription or payment card required
- No per-token customer charges for standard models
- No premium-only models
- Transparent fair-use limits
- Honest capacity errors when free inference is exhausted
- Optional paid-provider adapters disabled by default and require explicit operator configuration with spending controls

## Model Catalog (16 Standard Models)
All models share the free-access policy. Status is tracked in the database.

1. nexora-chat — General-purpose conversational assistant
2. nexora-chat-fast — Low-latency for simple tasks
3. nexora-reasoner — Complex multi-step analysis
4. nexora-developer — General software development
5. nexora-builder — Application and project building
6. nexora-mc-developer — Minecraft mod/plugin development
7. nexora-mc-optimizer — Minecraft performance engineering
8. nexora-mc-shader — Minecraft shaders and rendering
9. nexora-mc-resourcepack — Minecraft resource packs
10. nexora-discord-developer — Discord bots and apps
11. nexora-discord-designer — Discord server architecture
12. nexora-web-developer — Websites and applications
13. nexora-ui-designer — UI/UX design assistance
14. nexora-data-analyst — Data analysis and charts
15. nexora-writer — Technical writing and editing
16. nexora-security-reviewer — Defensive security analysis

Priority for first operational models: nexora-chat, nexora-builder, nexora-developer, nexora-mc-developer, nexora-discord-developer.

## Architecture Overview

### High-Level Components
- **Frontend:** TypeScript + React (Vite) — dark, developer-focused UI
- **Backend:** Python (FastAPI) — API gateway, auth, routing, usage
- **Database:** PostgreSQL (with SQLite fallback for local development)
- **Inference Layer:** Provider adapters (self-hosted via Ollama/vLLM or optional external)
- **Auth:** JWT sessions + API keys (hashed)
- **Rate Limiting:** Redis or in-memory with DB persistence for distributed
- **Deployment:** Docker Compose (when available), environment templates

### Key Design Decisions
1. Model ID is independent of backend. Routing happens in a dedicated engine.
2. All secrets (API keys, provider credentials) are hashed or stored in secret management; never logged or exposed.
3. Models start as "unavailable" until a backend is configured and health-checked.
4. OpenAI-compatible `/v1/chat/completions` endpoint.
5. Streaming supported where backend allows.
6. Strict authorization: users only see their own data.
7. Audit logs for admin actions.
8. No automatic paid fallback.

### Technology Stack
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, passlib (bcrypt), python-jose
- Frontend: React 18, TypeScript, Vite, Tailwind CSS (or custom design system)
- Database: PostgreSQL 15+ / SQLite for dev
- Testing: pytest, httpx
- Container: Docker + docker-compose (documented; may not be available in all environments)

## Implementation Phases
See `PROGRESS.md` for checklist and status.

## Known Limitations (Phase 1)
- No real inference backends configured yet (sandbox has no GPU/Ollama/Docker).
- Models will be registered as unavailable until Phase 4-5.
- Local development uses SQLite until PostgreSQL is available.
- Full production deployment requires external infrastructure.

## Next Steps
Proceed to Phase 2: Database schema, migrations, and backend foundation.