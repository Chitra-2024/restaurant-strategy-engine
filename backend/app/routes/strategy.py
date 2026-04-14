import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.analytics_service import analyze_reviews
from app.services.strategy_service import build_strategy

router = APIRouter(tags=["strategy"])
logger = logging.getLogger(__name__)


class StrategyRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=1)


@router.post("/strategy")
async def generate_strategy(payload: StrategyRequest) -> dict[str, object]:
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

        analytics_output = analyze_reviews(processed_reviews)
        return build_strategy(analytics_output)
    except PyMongoError as error:
        logger.warning("Failed to generate strategy output: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to generate strategy output",
        ) from error
