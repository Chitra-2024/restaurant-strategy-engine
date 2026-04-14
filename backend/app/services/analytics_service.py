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
) -> list[str]:
    insights: list[str] = []

    for aspect, details in aspect_scores.items():
        score = float(details["score"])
        aspect_name = aspect.capitalize()

        if score > 0.7:
            insights.append(
                f"{aspect_name} is a strong point with consistently positive feedback"
            )
        elif score < 0.4:
            insights.append(
                f"{aspect_name} is a major weakness with frequent complaints"
            )
        else:
            insights.append(f"{aspect_name} shows mixed customer sentiment")

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
    aspect_scores = calculate_aspect_scores(aggregated_data)
    insight_groups = identify_insights(aggregated_data, aspect_scores)
    health_score = calculate_health_score(review_list)
    insights = generate_insights(aspect_scores)
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
    }
