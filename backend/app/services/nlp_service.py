from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

POSITIVE_WORDS = ["good", "great", "amazing", "excellent", "love", "tasty"]
NEGATIVE_WORDS = ["bad", "slow", "poor", "worst", "late", "overpriced"]
ASPECT_KEYWORDS = {
    "food": ["food", "taste", "pizza", "burger", "meal"],
    "service": ["service", "staff", "wait", "support"],
    "delivery": ["delivery", "late", "time"],
    "price": ["price", "expensive", "cheap", "cost"],
    "ambience": ["ambience", "atmosphere", "environment"],
}
PLATFORM_CONFIDENCE = {
    "google": 0.9,
    "zomato": 0.85,
    "reddit": 0.6,
    "twitter": 0.5,
}


def _normalize_text(text: str) -> str:
    return text.lower().strip()


def _contains_keyword(text: str, keyword: str) -> bool:
    pattern = rf"\b{re.escape(keyword.lower())}\b"
    return re.search(pattern, text) is not None


def analyze_sentiment(text: str) -> dict[str, str]:
    normalized_text = _normalize_text(text)
    has_positive = any(
        _contains_keyword(normalized_text, word) for word in POSITIVE_WORDS
    )
    has_negative = any(
        _contains_keyword(normalized_text, word) for word in NEGATIVE_WORDS
    )

    if has_positive and has_negative:
        sentiment = "neutral"
    elif has_positive:
        sentiment = "positive"
    elif has_negative:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"sentiment": sentiment}


def extract_aspect(text: str) -> dict[str, str]:
    normalized_text = _normalize_text(text)

    for aspect, keywords in ASPECT_KEYWORDS.items():
        if any(_contains_keyword(normalized_text, keyword) for keyword in keywords):
            return {"aspect": aspect}

    return {"aspect": "service"}


def assign_confidence(platform: str) -> dict[str, float]:
    confidence = PLATFORM_CONFIDENCE.get(platform.lower(), 0.5)
    return {"confidence": confidence}


def process_reviews(reviews: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    processed_data: list[dict[str, Any]] = []

    for review in reviews:
        text = str(review.get("text", ""))
        platform = str(review.get("platform", ""))

        sentiment = analyze_sentiment(text)
        aspect = extract_aspect(text)
        confidence = assign_confidence(platform)

        processed_review = {
            "platform": platform,
            "text": text,
            "aspect": aspect["aspect"],
            "sentiment": sentiment["sentiment"],
            "confidence": confidence["confidence"],
            "restaurant_name": review.get("restaurant_name", ""),
            "timestamp": review.get("timestamp", ""),
        }

        if review.get("_id") is not None:
            processed_review["raw_review_id"] = str(review["_id"])

        processed_data.append(processed_review)

    return processed_data
