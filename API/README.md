# Caseira API

FastAPI backend service for Caseira.

## Run with Docker Compose (from project root)

```bash
docker compose up --build
```

This starts:
- PostgreSQL (`db`)
- FastAPI backend (`backend`) on port `8000`
- UI frontend (`frontend`) on port `80`

## API Container Details

- Working directory: `/app`
- Entrypoint: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- Exposed port: `8000`

## Environment

The backend reads `DATABASE_URL` from the root `.env` file when run through Docker Compose.

Example value:

```env
DATABASE_URL=postgresql://postgres:1234@db:5432/caseira
```

## Local Development (without Docker)

From this `API` folder:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
