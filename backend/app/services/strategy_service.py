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
        "swot": swot,
        "recommendations": generate_recommendations(strengths, weaknesses),
    }
