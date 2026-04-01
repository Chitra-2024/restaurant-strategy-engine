# Phase 1 Documentation

## Architecture Overview

Phase 1 sets up a simple full-stack foundation for the Restaurant Strategy Engine:

- `backend/` hosts a FastAPI API with modular route, service, and configuration layers.
- `frontend/` hosts a React application with Tailwind CSS for the UI.
- MongoDB is configured through environment variables and connected during backend startup.
- The frontend communicates with the backend through a dedicated service module.

## Folder Structure Explanation

```text
restaurant-strategy-engine/
|-- backend/
|   |-- app/
|   |   |-- config/      # environment settings and MongoDB connection
|   |   |-- models/      # reserved for future data models
|   |   |-- routes/      # FastAPI route definitions
|   |   |-- services/    # backend business logic
|   |   |-- utils/       # shared backend helpers
|   |   `-- main.py      # FastAPI application entry point
|   |-- .env.example     # sample backend environment variables
|   |-- README.md        # backend setup guide
|   `-- requirements.txt # Python dependencies
|-- frontend/
|   |-- src/
|   |   |-- components/  # reusable UI pieces
|   |   |-- pages/       # page-level views
|   |   |-- services/    # API communication layer
|   |   |-- App.jsx      # root React component
|   |   |-- index.css    # Tailwind entry styles
|   |   `-- main.jsx     # frontend entry point
|   |-- .env.example     # sample frontend environment variables
|   |-- README.md        # frontend setup guide
|   |-- index.html       # Vite HTML entry
|   |-- package.json     # Node dependencies and scripts
|   |-- postcss.config.js
|   |-- tailwind.config.js
|   `-- vite.config.js
`-- PHASE_1.md
```

## Tech Stack Used

- Backend: FastAPI, Uvicorn, Motor, Pydantic Settings
- Frontend: React, Vite, Tailwind CSS
- Database: MongoDB

## Frontend to Backend Communication

The frontend uses `frontend/src/services/api.js` to call the backend `GET /health` endpoint.

Workflow:

1. User clicks the "Check API Health" button.
2. The frontend sends a request to `http://localhost:8000/health` by default.
3. FastAPI returns:

```json
{
  "status": "ok"
}
```

4. The frontend displays the response on the page.

## MongoDB Configuration

MongoDB settings are loaded from backend environment variables:

- `MONGODB_URI`
- `MONGODB_DB_NAME`

These values are defined in `backend/.env`, read by `pydantic-settings`, and used in `backend/app/config/database.py`.

On backend startup:

1. The application loads settings.
2. It creates a MongoDB client.
3. It selects the configured database.
4. It sends a ping command to verify connectivity.

## Design Decisions

- Kept the health route minimal so Phase 1 only proves project wiring.
- Split route and service layers to preserve clean architecture from the start.
- Added environment-based configuration so local, staging, and production settings can diverge later.
- Used a dedicated frontend API service so future endpoints can be added without mixing networking into UI components.

## Setup Workflow

### Backend

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```
