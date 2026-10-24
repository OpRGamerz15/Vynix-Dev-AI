"""
Seed the model registry with the 16 standard Nexora models.
All models start as unavailable until a backend is configured.
"""
from app.db.session import SessionLocal
from app.models import Model

MODELS = [
    {"id": "nexora-chat", "name": "Nexora Chat", "description": "Default general-purpose conversational assistant."},
    {"id": "nexora-chat-fast", "name": "Nexora Chat Fast", "description": "Low-latency model for simpler tasks."},
    {"id": "nexora-reasoner", "name": "Nexora Reasoner", "description": "Specialized model for complex multi-step analysis."},
    {"id": "nexora-developer", "name": "Nexora Developer", "description": "General software development assistant."},
    {"id": "nexora-builder", "name": "Nexora Builder", "description": "Application and project-building assistant."},
    {"id": "nexora-mc-developer", "name": "Nexora MC Developer", "description": "Minecraft mod and plugin development."},
    {"id": "nexora-mc-optimizer", "name": "Nexora MC Optimizer", "description": "Minecraft optimization and performance engineering."},
    {"id": "nexora-mc-shader", "name": "Nexora MC Shader", "description": "Minecraft shader and rendering assistant."},
    {"id": "nexora-mc-resourcepack", "name": "Nexora MC Resource Pack", "description": "Minecraft resource pack and asset development."},
    {"id": "nexora-discord-developer", "name": "Nexora Discord Developer", "description": "Discord application and bot development."},
    {"id": "nexora-discord-designer", "name": "Nexora Discord Designer", "description": "Discord server architecture and community management."},
    {"id": "nexora-web-developer", "name": "Nexora Web Developer", "description": "Websites and applications."},
    {"id": "nexora-ui-designer", "name": "Nexora UI Designer", "description": "UI and UX design assistance."},
    {"id": "nexora-data-analyst", "name": "Nexora Data Analyst", "description": "Data analysis, calculations, statistics and charts."},
    {"id": "nexora-writer", "name": "Nexora Writer", "description": "Technical documentation, writing and editing."},
    {"id": "nexora-security-reviewer", "name": "Nexora Security Reviewer", "description": "Defensive security analysis and secure coding."},
]


def seed_models():
    db = SessionLocal()
    try:
        for m in MODELS:
            existing = db.query(Model).filter(Model.id == m["id"]).first()
            if not existing:
                model = Model(
                    id=m["id"],
                    name=m["name"],
                    description=m["description"],
                    status="unavailable",
                    is_free=True,
                )
                db.add(model)
        db.commit()
        print(f"Seeded {len(MODELS)} models (all marked unavailable).")
    finally:
        db.close()


if __name__ == "__main__":
    seed_models()