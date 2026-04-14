import logging

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.models.filters import DataFilterRequest
from app.services.analytics_service import analyze_reviews
from app.services.query_service import fetch_processed_reviews

router = APIRouter(tags=["analytics"])
logger = logging.getLogger(__name__)


@router.post("/analyze")
async def analyze_data(payload: DataFilterRequest | None = None) -> dict[str, object]:
    db = get_database()

    try:
        processed_reviews = await fetch_processed_reviews(db, payload)
        if not processed_reviews:
            return {
                "message": "No data found for this restaurant",
            }

        return analyze_reviews(processed_reviews)
    except PyMongoError as error:
        logger.warning("Failed to analyze processed review data: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to analyze processed review data",
        ) from error
