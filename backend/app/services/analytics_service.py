from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import Any

SENTIMENT_WEIGHTS = {
    "positive": 1.0,
    "neutral": 0.5,
    "negative": 0.0,
}


def aggregate_by_aspect_and_sentiment(
    reviews: Iterable[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    aggregation: dict[str, dict[str, int]] = defaultdict(
        lambda: {"positive": 0, "negative": 0, "neutral": 0}
    )

    for review in reviews:
        aspect = str(review.get("aspect", "service"))
        sentiment = str(review.get("sentiment", "neutral"))

        if sentiment not in aggregation[aspect]:
            aggregation[aspect][sentiment] = 0

        aggregation[aspect][sentiment] += 1

    return {aspect: counts for aspect, counts in aggregation.items()}


def collect_aspect_sources(
    reviews: Iterable[dict[str, Any]],
) -> dict[str, list[str]]:
    source_map: dict[str, list[str]] = defaultdict(list)

    for review in reviews:
        aspect = str(review.get("aspect", "service"))
        source_url = str(review.get("source_url", "")).strip()
        if source_url and source_url not in source_map[aspect]:
            source_map[aspect].append(source_url)

    return {aspect: urls for aspect, urls in source_map.items()}


def collect_platform_counts(
    reviews: Iterable[dict[str, Any]],
) -> dict[str, int]:
    platform_counts: dict[str, int] = defaultdict(int)

    for review in reviews:
        platform = str(review.get("platform", "unknown"))
        platform_counts[platform] += 1

    return dict(platform_counts)


def collect_locations(reviews: Iterable[dict[str, Any]]) -> list[str]:
    locations = []

    for review in reviews:
        location = str(review.get("location", "")).strip()
        if location and location not in locations:
            locations.append(location)

    return locations


def collect_all_sources(reviews: Iterable[dict[str, Any]]) -> list[str]:
    sources = []

    for review in reviews:
        source_url = str(review.get("source_url", "")).strip()
        if source_url and source_url not in sources:
            sources.append(source_url)

    return sources


def _aspect_review_count(counts: dict[str, int]) -> int:
    return (
        counts.get("positive", 0)
        + counts.get("negative", 0)
        + counts.get("neutral", 0)
    )


def calculate_aspect_scores(
    aggregated_data: dict[str, dict[str, int]],
) -> dict[str, dict[str, float | int]]:
    aspect_scores: dict[str, dict[str, float | int]] = {}

    sorted_aspects = sorted(
        aggregated_data.items(),
        key=lambda item: _aspect_review_count(item[1]),
        reverse=True,
    )

    for aspect, counts in sorted_aspects:
        positive = counts.get("positive", 0)
        negative = counts.get("negative", 0)
        total = positive + negative

        score = positive / total if total else 0.0
        aspect_scores[aspect] = {
            "score": round(score, 2),
            "positive": positive,
            "negative": negative,
        }

    return aspect_scores


def calculate_health_score(reviews: Iterable[dict[str, Any]]) -> int:
    weighted_total = 0.0
    confidence_total = 0.0

    for review in reviews:
        sentiment = str(review.get("sentiment", "neutral"))
        confidence = float(review.get("confidence", 0.0))
        sentiment_score = SENTIMENT_WEIGHTS.get(sentiment, 0.5)

        weighted_total += sentiment_score * confidence
        confidence_total += confidence

    if confidence_total == 0:
        return 0

    normalized_score = (weighted_total / confidence_total) * 100
    return round(normalized_score)


def identify_insights(
    aggregated_data: dict[str, dict[str, int]],
    aspect_scores: dict[str, dict[str, float | int]],
) -> dict[str, list[str]]:
    strengths = sorted(
        (
            aspect
            for aspect, details in aspect_scores.items()
            if aggregated_data.get(aspect, {}).get("positive", 0) > 0
            and float(details["score"]) > 0.6
        ),
        key=lambda aspect: float(aspect_scores[aspect]["score"]),
        reverse=True,
    )
    weaknesses = sorted(
        (
            aspect
            for aspect, details in aspect_scores.items()
            if aggregated_data.get(aspect, {}).get("negative", 0) > 0
            and float(details["score"]) < 0.4
        ),
        key=lambda aspect: float(aspect_scores[aspect]["score"]),
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
    }


def generate_insights(
    aspect_scores: dict[str, dict[str, float | int]],
    source_map: dict[str, list[str]],
    fallback_sources: list[str],
) -> list[dict[str, Any]]:
    insights: list[dict[str, Any]] = []

    for aspect, details in aspect_scores.items():
        score = float(details["score"])
        aspect_name = aspect.capitalize()
        source_urls = source_map.get(aspect, [])[:2] or fallback_sources[:1]

        if score > 0.7:
            text = f"{aspect_name} is a strong point with consistently positive feedback"
        elif score < 0.4:
            text = f"{aspect_name} is a major weakness with frequent complaints"
        else:
            text = f"{aspect_name} shows mixed customer sentiment"

        insights.append(
            {
                "aspect": aspect,
                "text": text,
                "source_urls": source_urls,
            }
        )

    return insights


def generate_summary(
    health_score: int,
    strengths: list[str],
    weaknesses: list[str],
) -> str:
    if health_score >= 75:
        performance = "Overall performance is above average"
    elif health_score >= 50:
        performance = "Overall performance is steady but has room for improvement"
    else:
        performance = "Overall performance is below average and needs attention"

    summary_parts = [performance]

    if strengths:
        strength_text = ", ".join(strengths[:2])
        summary_parts.append(f"Strong areas include {strength_text}")

    if weaknesses:
        weakness_text = ", ".join(weaknesses[:2])
        summary_parts.append(f"Key issues are visible in {weakness_text}")

    return ". ".join(summary_parts) + "."


def analyze_reviews(reviews: Iterable[dict[str, Any]]) -> dict[str, Any]:
    review_list = list(reviews)
    aggregated_data = aggregate_by_aspect_and_sentiment(review_list)
    source_map = collect_aspect_sources(review_list)
    platform_counts = collect_platform_counts(review_list)
    locations = collect_locations(review_list)
    fallback_sources = collect_all_sources(review_list)
    aspect_scores = calculate_aspect_scores(aggregated_data)
    insight_groups = identify_insights(aggregated_data, aspect_scores)
    health_score = calculate_health_score(review_list)
    insights = generate_insights(aspect_scores, source_map, fallback_sources)
    summary = generate_summary(
        health_score,
        insight_groups["strengths"],
        insight_groups["weaknesses"],
    )

    return {
        "health_score": health_score,
        "strengths": insight_groups["strengths"],
        "weaknesses": insight_groups["weaknesses"],
        "aspect_scores": aspect_scores,
        "insights": insights,
        "summary": summary,
        "platform_counts": platform_counts,
        "locations": locations,
    }
