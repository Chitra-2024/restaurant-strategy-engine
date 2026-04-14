import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.models.filters import DataFilterRequest
from app.services.query_service import build_strategy_output

router = APIRouter(tags=["comparison"])
logger = logging.getLogger(__name__)


class CompareRequest(BaseModel):
    restaurants: list[str] = Field(..., min_length=2)
    location: str | None = None
    days: int | None = Field(default=None, ge=1, le=365)


def _build_comparison_summary(comparisons: list[dict[str, object]]) -> str:
    if len(comparisons) < 2:
        return "Not enough restaurants were available for comparison."

    ranked = sorted(comparisons, key=lambda item: int(item.get("global_score", 0)), reverse=True)
    leader = ranked[0]
    runner_up = ranked[1]

    leader_strength = (leader.get("strengths") or ["overall experience"])[0]
    runner_weakness = (runner_up.get("weaknesses") or ["overall consistency"])[0]

    return (
        f"{leader['restaurant']} outperforms {runner_up['restaurant']} overall, "
        f"especially in {leader_strength}, while {runner_up['restaurant']} shows weaker {runner_weakness} performance."
    )


@router.post("/compare")
async def compare_restaurants(payload: CompareRequest) -> dict[str, object]:
    db = get_database()
    restaurants = [restaurant.strip() for restaurant in payload.restaurants if restaurant.strip()]
    if len(restaurants) < 2:
        raise HTTPException(status_code=400, detail="At least two restaurants are required")

    try:
        comparisons: list[dict[str, object]] = []

        for restaurant in restaurants:
            filters = DataFilterRequest(
                restaurant_name=restaurant,
                location=payload.location,
                days=payload.days,
            )
            strategy_output = await build_strategy_output(db, filters)
            if strategy_output is None:
                continue

            comparisons.append(
                {
                    "restaurant": restaurant,
                    "global_score": strategy_output.get("global_score", 0),
                    "strengths": strategy_output.get("swot", {}).get("strengths", []),
                    "weaknesses": strategy_output.get("swot", {}).get("weaknesses", []),
                }
            )

        return {
            "comparisons": comparisons,
            "comparison_summary": _build_comparison_summary(comparisons),
        }
    except PyMongoError as error:
        logger.warning("Failed to compare restaurants: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to compare restaurants",
        ) from error
