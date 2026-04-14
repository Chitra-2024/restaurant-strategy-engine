import logging

from fastapi import APIRouter, HTTPException, Query
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.filter_service import build_filter_request
from app.services.query_service import fetch_processed_reviews

router = APIRouter(tags=["reviews"])
logger = logging.getLogger(__name__)


@router.get("/reviews")
async def get_reviews(
    restaurant_name: str | None = Query(default=None),
    location: str | None = Query(default=None),
    days: int | None = Query(default=None, ge=1, le=365),
    limit: int = Query(default=8, ge=1, le=10),
) -> dict[str, object]:
    db = get_database()
    filters = build_filter_request(
        restaurant_name=restaurant_name,
        location=location,
        days=days,
    )

    try:
        reviews = await fetch_processed_reviews(db, filters)
        sample_reviews = reviews[:limit]

        return {
            "reviews": [
                {
                    "platform": review.get("platform", ""),
                    "text": review.get("text", ""),
                    "timestamp": review.get("timestamp", ""),
                    "source_url": review.get("source_url", ""),
                }
                for review in sample_reviews
            ]
        }
    except PyMongoError as error:
        logger.warning("Failed to fetch review feed: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to fetch reviews",
        ) from error
