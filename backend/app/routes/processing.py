import logging

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from app.models.filters import DataFilterRequest
from app.config.database import get_database
from app.services.query_service import process_reviews_on_demand

router = APIRouter(tags=["processing"])
logger = logging.getLogger(__name__)


@router.post("/process-data")
async def process_data(payload: DataFilterRequest | None = None) -> dict[str, int | str]:
    db = get_database()

    try:
        count = await process_reviews_on_demand(
            db,
            payload or DataFilterRequest(),
        )

        return {
            "message": "Processed successfully",
            "count": count,
        }
    except PyMongoError as error:
        logger.warning("Failed to process review data: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to process review data",
        ) from error
