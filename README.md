# IT Release Readiness & Governance

A React + TypeScript single page app served next to a FastAPI backend,
wired for containerised deployment.

## Stack

| Layer | Choice |
| --- | --- |
| Frontend | React 18, TypeScript and Vite |
| Backend | FastAPI on Python 3.12 (uvicorn) |
| Database | none yet - items are held in memory |
| Tests | pytest + ruff (backend), `tsc --noEmit` and `vite build` (frontend) |
| Deploy | Docker Compose: nginx serves the SPA, uvicorn runs the API |

## Layout

```
backend/app/main.py     FastAPI application (/health, /api/v1/items)
backend/tests/          pytest suite
frontend/src/           React entry point and application component
frontend/nginx.conf     SPA and API reverse proxy for the container
docker-compose.yml      frontend + backend services
```

## Run locally

```bash
# terminal 1 - API
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000

# terminal 2 - web app
cd frontend
npm install
npm run dev        # http://localhost:5173, proxies /api and /health to :8000
```

## Test

```bash
cd backend && ruff check . && pytest -q
cd frontend && npm run build
```

## Configuration

`cp .env.example .env` and fill in the values you need; every variable is
documented in that file. `.env` is git-ignored and must never be committed.

## Deployment

`docker compose up --build -d` builds `frontend/` (nginx) and `backend/`
(uvicorn). The SPA is published on port 5173 and the API on 8000; terminate
TLS in front of the frontend and keep the API off the public internet. The
backend exposes `GET /health`, which compose and the platform use as the
liveness/readiness probe. CI (`.github/workflows/ci.yml`) runs ruff, pytest,
the frontend build and a docker build without publishing an image.
