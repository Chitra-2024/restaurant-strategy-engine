import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.analytics_service import analyze_reviews

router = APIRouter(tags=["analytics"])
logger = logging.getLogger(__name__)


class AnalyzeRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=1)


@router.post("/analyze")
async def analyze_data(payload: AnalyzeRequest) -> dict[str, object]:
    db = get_database()
    restaurant_name = payload.restaurant_name.strip()

    if not restaurant_name:
        raise HTTPException(status_code=400, detail="restaurant_name is required")

    try:
        processed_reviews = await db.processed_reviews.find(
            {"restaurant_name": restaurant_name}
        ).to_list(length=None)
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
