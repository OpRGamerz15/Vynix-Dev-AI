# Nexora JARVIS

**Status:** Coming Soon (Premium Product)  
**Tagline:** Your AI. Your Devices. Your Commands.

Nexora JARVIS is a planned premium personal AI assistant under the Nexora AI brand. It is not yet available.

## Current State
- Dedicated product page in the frontend
- Product card on the home dashboard
- Official logo used
- Real waitlist endpoint (`POST /v1/waitlist`) that validates email, prevents duplicates, and stores submissions
- No payment, no checkout, no prices, no launch date
- Existing free Nexora models remain unchanged and free

## Planned Features (not yet implemented)
- Natural voice conversations
- Wake-word activation (with explicit permission)
- Cross-device assistant
- Device integrations (authorized only)
- Smart automation
- Context memory (user-controlled)
- Developer integrations
- Voice responses
- Permission and privacy controls

JARVIS will not claim the ability to power on a completely off device, bypass locks, or control unsupported hardware.

## Backend
Waitlist table is created on startup via SQLAlchemy. Emails are stored securely in the database. No secrets exposed.