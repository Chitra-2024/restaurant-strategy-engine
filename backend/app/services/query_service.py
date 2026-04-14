from __future__ import annotations

from typing import Any

from pymongo import DESCENDING

from app.models.filters import DataFilterRequest
from app.services.analytics_service import analyze_reviews
from app.services.filter_service import build_review_query
from app.services.mock_service import generate_mock_reviews
from app.services.nlp_service import process_reviews
from app.services.strategy_service import build_strategy

PROCESSING_BATCH_SIZE = 20


async def fetch_raw_reviews(
    db: Any,
    filters: DataFilterRequest | None,
    *,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    query = build_review_query(filters)
    cursor = db.raw_reviews.find(query).sort("timestamp", DESCENDING)
    if limit is not None:
        cursor = cursor.limit(limit)
    return await cursor.to_list(length=limit)


async def fetch_processed_reviews(
    db: Any,
    filters: DataFilterRequest | None,
) -> list[dict[str, Any]]:
    query = build_review_query(filters)
    return await db.processed_reviews.find(query).sort("timestamp", DESCENDING).to_list(length=None)


async def ingest_reviews_on_demand(
    db: Any,
    filters: DataFilterRequest,
) -> int:
    restaurant_name = (filters.restaurant_name or "").strip()
    if not restaurant_name:
        return 0

    data = await generate_mock_reviews(
        restaurant_name=restaurant_name,
        location=filters.location,
        days=filters.days,
    )

    if not data:
        return 0

    result = await db.raw_reviews.insert_many(data)
    return len(result.inserted_ids)


async def process_reviews_on_demand(
    db: Any,
    filters: DataFilterRequest,
) -> int:
    raw_reviews = await fetch_raw_reviews(
        db,
        filters,
        limit=PROCESSING_BATCH_SIZE,
    )
    if not raw_reviews:
        return 0

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
        return 0

    processed_data = process_reviews(reviews_to_process)
    await db.processed_reviews.insert_many(processed_data)
    return len(processed_data)


async def ensure_processed_reviews(
    db: Any,
    filters: DataFilterRequest | None,
) -> list[dict[str, Any]]:
    processed_reviews = await fetch_processed_reviews(db, filters)
    if processed_reviews:
        return processed_reviews

    if filters is None or not (filters.restaurant_name or "").strip():
        return []

    await ingest_reviews_on_demand(db, filters)
    await process_reviews_on_demand(db, filters)
    return await fetch_processed_reviews(db, filters)


async def build_strategy_output(
    db: Any,
    filters: DataFilterRequest | None,
) -> dict[str, Any] | None:
    processed_reviews = await ensure_processed_reviews(db, filters)
    if not processed_reviews:
        return None

    analytics_output = analyze_reviews(processed_reviews)
    return build_strategy(analytics_output)
