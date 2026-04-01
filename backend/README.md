# Backend Setup

## Overview

The backend is a FastAPI service with a modular structure:

- `app/main.py`: FastAPI app entry point
- `app/routes/`: API route definitions
- `app/services/`: business logic
- `app/config/`: settings and MongoDB connection

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create an environment file:

```bash
copy .env.example .env
```

4. Start the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Example Endpoint

`GET /health`

Response:

```json
{
  "status": "ok"
}
```

