# Multimodal Emergency Agent — Starter Repository

Overview
--------
This repository contains a starter implementation for a multimodal emergency agent:
- Text prompt / Voice wake-word / offline fallback -> ingest emergency request
- Nearest responder lookup using OpenStreetMap + placeholder for government '108' API
- Dispatch via SMS + WhatsApp (Twilio) and Push (FCM)
- Cloud Run compatible backend, Cloud SQL (Postgres) for encrypted logs
- Vertex AI intent classifier integration (sample)
- Escalation via Cloud Tasks (sample)
- Supports up to 3 emergency contacts

What's included
---------------
- `backend/` — FastAPI app, DB models, integrations (Twilio, FCM, OSM helpers).
- `vertex/` — sample intent classifier call (Vertex AI placeholder).
- `client/` — minimal demo single-file web client that triggers `/api/emergency`.
- `infra/` — SQL schema, Cloud Run & Cloud SQL notes, IAM and environment variable checklist.
- `docs/IMPACT.md` — impact analysis for Emergency Response in Healthcare.
- `Dockerfile`, `cloudbuild.yaml` — Cloud Run deployment artifacts.

Important
---------
This is a starter/demo. **Do not** deploy to production without:
- Replacing placeholder API calls and secrets with secure values.
- Proper authentication, rate limiting, and security review.
- Compliance checks for storing and transmitting emergency data.

Environment variables (examples)
--------------------------------
See `infra/env.example` for a complete list. Key variables:
- `DATABASE_URL` (Postgres, Cloud SQL connection string)
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`
- `FCM_SERVER_KEY` or service account JSON (preferred)
- `VERTEX_PROJECT`, `VERTEX_REGION`, `VERTEX_MODEL_ID` (if using Vertex)
- `FERNET_KEY` (for encrypting logs)
- `CLOUD_TASKS_QUEUE` (for escalation scheduling)

Zip
---
A zip of this repo is included with this notebook output.

