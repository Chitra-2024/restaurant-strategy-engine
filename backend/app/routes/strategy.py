import logging

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.models.filters import DataFilterRequest
from app.services.query_service import build_strategy_output

router = APIRouter(tags=["strategy"])
logger = logging.getLogger(__name__)


@router.post("/strategy")
async def generate_strategy(payload: DataFilterRequest | None = None) -> dict[str, object]:
    db = get_database()

    try:
        strategy_output = await build_strategy_output(db, payload)
        if strategy_output is None:
            return {
                "message": "Unable to fetch sufficient data for this restaurant",
            }

        return strategy_output
    except PyMongoError as error:
        logger.warning("Failed to generate strategy output: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to generate strategy output",
        ) from error
