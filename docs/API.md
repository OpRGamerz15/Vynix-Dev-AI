# Nexora AI API Reference

Base URL: configurable (default http://localhost:8000)

All standard models are free under fair-use limits. No payment required.

## Authentication
- Register: POST /v1/auth/register
- Login: POST /v1/auth/login (form data: username=email, password)
- Me: GET /v1/auth/me (Bearer JWT)

## API Keys
- Create: POST /v1/api-keys (Bearer JWT) → returns raw key once
- List: GET /v1/api-keys
- Revoke: DELETE /v1/api-keys/{id}

## Models
- List: GET /v1/models
- Get: GET /v1/models/{model_id}

## Chat Completions (OpenAI-compatible)
POST /v1/chat/completions
Authorization: Bearer nx_...

```json
{
  "model": "nexora-chat",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}
```

Returns 503 with clear message if model is unavailable or free capacity is exhausted.

## Usage
GET /v1/usage (Bearer JWT)

## Admin (requires is_admin=true)
- GET /v1/admin/users
- GET /v1/admin/stats
- POST /v1/admin/models/{id}/status?status=available

## Health
GET /health

Interactive docs: /docs