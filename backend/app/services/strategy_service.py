from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _format_aspect(aspect: str) -> str:
    return aspect.replace("_", " ")


def _build_varied_messages(aspects: list[str], templates: list[str]) -> list[str]:
    messages: list[str] = []

    for index, aspect in enumerate(aspects):
        template = templates[index % len(templates)]
        messages.append(template.format(aspect=_format_aspect(aspect)))

    return messages


def generate_opportunities(
    strengths: Iterable[str],
    weaknesses: Iterable[str],
) -> list[str]:
    weakness_list = list(weaknesses)
    if weakness_list:
        return _build_varied_messages(
            weakness_list,
            [
                "Capitalize on improvements in {aspect} to increase customer satisfaction",
                "Build upon operational fixes in {aspect} to strengthen the customer experience",
                "Use targeted progress in {aspect} to improve guest loyalty",
                "Expand performance gains in {aspect} to attract new customers",
            ],
        )

    strength_list = list(strengths)
    if strength_list:
        return _build_varied_messages(
            strength_list,
            [
                "Capitalize on strong {aspect} to attract new customers",
                "Build upon excellent {aspect} to increase repeat business",
                "Use standout {aspect} to improve customer retention",
                "Expand using strong {aspect} as a clear market differentiator",
            ],
        )

    return ["Build upon current operational stability to unlock new growth opportunities"]


def generate_threats(
    strengths: Iterable[str],
    weaknesses: Iterable[str],
) -> list[str]:
    weakness_list = list(weaknesses)
    if weakness_list:
        return _build_varied_messages(
            weakness_list,
            [
                "Continued issues in {aspect} may lead to customer churn",
                "Weakness in {aspect} could damage brand trust over time",
                "Poor performance in {aspect} may reduce repeat visits",
                "Ongoing problems in {aspect} could create a competitive disadvantage",
            ],
        )

    strength_list = list(strengths)
    if strength_list:
        return _build_varied_messages(
            strength_list,
            [
                "Competitors may attempt to replicate high-performing {aspect} offerings",
                "Maintaining consistency in {aspect} during high demand may be challenging",
                "Strong {aspect} expectations may become harder to sustain as the business grows",
                "Rivals could narrow the gap by matching the current {aspect} experience",
            ],
        )

    return ["Maintaining consistency as demand grows may be challenging"]


def generate_recommendations(
    strengths: Iterable[str],
    weaknesses: Iterable[str],
) -> list[str]:
    recommendations = [
        f"Maintain strong {_format_aspect(strength)} performance as a competitive advantage"
        for strength in strengths
    ]

    recommendations.extend(
        f"Optimize {_format_aspect(weakness)} operations to address customer concerns"
        for weakness in weaknesses
    )

    return recommendations


def _describe_aspect(
    aspect_scores: dict[str, dict[str, float | int]],
    aspect_name: str,
    positive_text: str,
    improvement_text: str,
    neutral_text: str,
) -> str:
    details = aspect_scores.get(aspect_name)
    if not details:
        return neutral_text

    score = float(details.get("score", 0.0))
    if score > 0.7:
        return positive_text
    if score < 0.4:
        return improvement_text
    return neutral_text


def build_four_ps(analytics_output: dict[str, Any]) -> dict[str, str]:
    aspect_scores = analytics_output.get("aspect_scores", {})
    platform_counts = analytics_output.get("platform_counts", {})
    locations = analytics_output.get("locations", [])
    social_mentions = int(platform_counts.get("reddit", 0)) + int(platform_counts.get("twitter", 0))

    if social_mentions >= 4:
        promotion = "Social mentions are active, giving the brand visible promotion momentum"
    elif social_mentions > 0:
        promotion = "Social discussion exists, but promotion can be strengthened with more consistent visibility"
    else:
        promotion = "Promotion visibility is limited, so broader awareness efforts may help"

    place_neutral = (
        f"Place performance is stable across {locations[0]}"
        if locations
        else "Place performance is neutral with limited delivery or location feedback"
    )

    return {
        "product": _describe_aspect(
            aspect_scores,
            "food",
            "Product is a clear strength with strong food quality feedback",
            "Product needs attention, especially around food consistency and customer satisfaction",
            "Product sentiment is balanced, with room to sharpen the menu experience",
        ),
        "price": _describe_aspect(
            aspect_scores,
            "price",
            "Price perception is favorable and supports value positioning",
            "Price perception is weak, so improving value communication may be necessary",
            "Price sentiment is mixed, suggesting value expectations are not yet consistent",
        ),
        "place": _describe_aspect(
            aspect_scores,
            "delivery",
            "Place performance is strong, with reliable delivery and access experience",
            "Place performance needs improvement, especially around delivery reliability and convenience",
            place_neutral,
        ),
        "promotion": promotion,
    }


def build_strategy(analytics_output: dict[str, Any]) -> dict[str, Any]:
    strengths = list(analytics_output.get("strengths", []))
    weaknesses = list(analytics_output.get("weaknesses", []))

    swot = {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunities": generate_opportunities(strengths, weaknesses),
        "threats": generate_threats(strengths, weaknesses),
    }

    return {
        "global_score": analytics_output.get("health_score", 0),
        "swot": swot,
        "4ps": build_four_ps(analytics_output),
        "insights": analytics_output.get("insights", []),
        "aspect_scores": analytics_output.get("aspect_scores", {}),
        "summary": analytics_output.get("summary", ""),
        "recommendations": generate_recommendations(strengths, weaknesses),
    }
