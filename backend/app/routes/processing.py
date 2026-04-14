import logging

from fastapi import APIRouter, HTTPException
from pymongo import DESCENDING
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.nlp_service import process_reviews

router = APIRouter(tags=["processing"])
logger = logging.getLogger(__name__)

PROCESSING_BATCH_SIZE = 20


@router.post("/process-data")
async def process_data() -> dict[str, int | str]:
    db = get_database()

    try:
        raw_reviews = await db.raw_reviews.find().sort(
            "timestamp",
            DESCENDING,
        ).limit(PROCESSING_BATCH_SIZE).to_list(length=PROCESSING_BATCH_SIZE)

        if not raw_reviews:
            return {
                "message": "Processed successfully",
                "count": 0,
            }

        raw_review_ids = [str(review["_id"]) for review in raw_reviews if review.get("_id")]

        existing_processed = await db.processed_reviews.find(
            {"raw_review_id": {"$in": raw_review_ids}},
            {"raw_review_id": 1},
        ).to_list(length=PROCESSING_BATCH_SIZE)
        processed_ids = {
            record["raw_review_id"]
            for record in existing_processed
            if record.get("raw_review_id")
        }

        reviews_to_process = [
            review for review in raw_reviews if str(review.get("_id")) not in processed_ids
        ]

        if not reviews_to_process:
            return {
                "message": "Processed successfully",
                "count": 0,
            }

        processed_data = process_reviews(reviews_to_process)
        await db.processed_reviews.insert_many(processed_data)

        return {
            "message": "Processed successfully",
            "count": len(processed_data),
        }
    except PyMongoError as error:
        logger.warning("Failed to process review data: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to process review data",
        ) from error
