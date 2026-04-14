from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.models.filters import DataFilterRequest


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    return cleaned or None


def build_filter_request(
    restaurant_name: str | None = None,
    location: str | None = None,
    days: int | None = None,
) -> DataFilterRequest:
    return DataFilterRequest(
        restaurant_name=normalize_text(restaurant_name),
        location=normalize_text(location),
        days=days,
    )


def build_review_query(filters: DataFilterRequest | None) -> dict[str, Any]:
    if filters is None:
        return {}

    query: dict[str, Any] = {}
    restaurant_name = normalize_text(filters.restaurant_name)
    location = normalize_text(filters.location)

    if restaurant_name:
        query["restaurant_name"] = restaurant_name

    if location:
        query["location"] = location

    if filters.days:
        cutoff = datetime.now(timezone.utc) - timedelta(days=filters.days)
        query["timestamp"] = {"$gte": cutoff.isoformat()}

    return query
