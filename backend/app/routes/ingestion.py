import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.filter_service import normalize_text
from app.services.mock_service import generate_mock_reviews

router = APIRouter(tags=["ingestion"])
logger = logging.getLogger(__name__)


class IngestDataRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=1)
    location: str | None = Field(default=None)
    days: int | None = Field(default=None, ge=1, le=365)


@router.post("/ingest-data")
async def ingest_data(payload: IngestDataRequest) -> dict[str, int | str]:
    restaurant_name = payload.restaurant_name.strip()
    location = normalize_text(payload.location)
    if not restaurant_name:
        raise HTTPException(status_code=400, detail="restaurant_name is required")

    # Reddit API temporarily disabled
    data = await generate_mock_reviews(
        restaurant_name=restaurant_name,
        location=location,
        days=payload.days,
    )

    try:
        db = get_database()

        print("Connected DB:", db.name)
        print(f"Generated {len(data)} records")

        if not data:
            print("No data generated")
        else:
            print("Inserting into MongoDB...")
            result = await db.raw_reviews.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} records")
    except PyMongoError as error:
        logger.warning("Failed to store ingested records: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to store ingested data",
        ) from error

    return {
        "message": "Data ingested",
        "count": len(data),
    }
