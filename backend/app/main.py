from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import connect_to_mongo, disconnect_from_mongo
from app.routes.analytics import router as analytics_router
from app.routes.compare import router as compare_router
from app.routes.export import router as export_router
from app.routes.health import router as health_router
from app.routes.ingestion import router as ingestion_router
from app.routes.processing import router as processing_router
from app.routes.reviews import router as reviews_router
from app.routes.strategy import router as strategy_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    yield
    await disconnect_from_mongo()


app = FastAPI(
    title="Restaurant Strategy Engine API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "healthy", "message": "Restaurant Strategy Engine API is running"}

app.include_router(health_router)
app.include_router(ingestion_router)
app.include_router(processing_router)
app.include_router(analytics_router)
app.include_router(strategy_router)
app.include_router(export_router)
app.include_router(reviews_router)
app.include_router(compare_router)

import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
