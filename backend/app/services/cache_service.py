from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.models.filters import DataFilterRequest

CACHE_TTL_MINUTES = 10
_strategy_cache: dict[str, dict[str, Any]] = {}


def build_cache_key(filters: DataFilterRequest | None) -> str:
    restaurant_name = (filters.restaurant_name if filters else None) or "all"
    location = (filters.location if filters else None) or "all"
    days = (filters.days if filters else None) or "all"
    return f"{restaurant_name.lower()}::{location.lower()}::{days}"


def get_cached_strategy(filters: DataFilterRequest | None) -> dict[str, Any] | None:
    key = build_cache_key(filters)
    entry = _strategy_cache.get(key)
    if not entry:
        return None

    if datetime.now(timezone.utc) - entry["created_at"] > timedelta(minutes=CACHE_TTL_MINUTES):
        _strategy_cache.pop(key, None)
        return None

    return entry["value"]


def set_cached_strategy(filters: DataFilterRequest | None, value: dict[str, Any]) -> None:
    key = build_cache_key(filters)
    _strategy_cache[key] = {
        "value": value,
        "created_at": datetime.now(timezone.utc),
    }
