# Nexora AI — Known Issues and Limitations

## Current Environment Constraints (Sandbox)
- No Docker available
- No Ollama or local LLM inference servers
- No GPU
- Limited ability to run long-running services
- PostgreSQL not pre-installed (SQLite used for local development; intermittent I/O observed)

## Product Limitations
- All 16 models are registered in the database and marked **unavailable** until a real free or self-hosted backend is configured and health-checked.
- Chat completions return honest 503 capacity/backend-not-configured errors. No fabricated responses.
- Email verification and password reset require SMTP configuration (not yet implemented).
- Full distributed rate limiting, streaming, admin console UI, and conversation history UI are scaffolded but not complete.
- Production deployment requires external hosting with suitable inference resources.

## Security Notes
- API keys are generated securely and stored hashed (bcrypt).
- Raw key shown only once at creation.
- No secrets in frontend.
- Provider credentials kept in environment; paid providers disabled by default.
- User data isolated by ownership checks.

## Nexora JARVIS
- Product is Coming Soon only. No functional assistant yet.
- Waitlist is real (stores validated emails, prevents duplicates).
- All planned features are labeled as planned. No fake capabilities claimed.