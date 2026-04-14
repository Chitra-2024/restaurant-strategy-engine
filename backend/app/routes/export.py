import logging

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pymongo.errors import PyMongoError

from app.config.database import get_database
from app.services.filter_service import build_filter_request
from app.services.query_service import build_strategy_output
from app.services.report_service import generate_strategy_pdf

router = APIRouter(tags=["export"])
logger = logging.getLogger(__name__)


@router.get("/export-pdf")
async def export_pdf(
    restaurant_name: str | None = Query(default=None),
    location: str | None = Query(default=None),
    days: int | None = Query(default=None, ge=1, le=365),
):
    db = get_database()
    filters = build_filter_request(
        restaurant_name=restaurant_name,
        location=location,
        days=days,
    )

    try:
        strategy_output = await build_strategy_output(db, filters)
        if strategy_output is None:
            raise HTTPException(status_code=404, detail="No data found for this restaurant")

        pdf_buffer = generate_strategy_pdf(
            restaurant_name=filters.restaurant_name or "All Restaurants",
            filters=filters,
            strategy_output=strategy_output,
        )
        filename = f"{(filters.restaurant_name or 'restaurant-strategy').replace(' ', '-').lower()}-strategy-report.pdf"

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except PyMongoError as error:
        logger.warning("Failed to export strategy PDF: %s", error)
        raise HTTPException(
            status_code=503,
            detail="Failed to export strategy PDF",
        ) from error
