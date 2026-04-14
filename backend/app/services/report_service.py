from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.models.filters import DataFilterRequest


def _draw_section(
    pdf: canvas.Canvas,
    title: str,
    items: list[str],
    y_position: int,
) -> int:
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y_position, title)
    y_position -= 18
    pdf.setFont("Helvetica", 10)

    if not items:
        pdf.drawString(60, y_position, "- None")
        return y_position - 20

    for item in items:
        if y_position < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y_position = 750
        pdf.drawString(60, y_position, f"- {item}")
        y_position -= 16

    return y_position - 12


def generate_strategy_pdf(
    restaurant_name: str,
    filters: DataFilterRequest | None,
    strategy_output: dict[str, object],
) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y_position = height - 50

    pdf.setTitle("Restaurant Strategy Report")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y_position, "Restaurant Strategy Report")
    y_position -= 30

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y_position, f"Restaurant Name: {restaurant_name or 'All Restaurants'}")
    y_position -= 18

    if filters and filters.location:
        pdf.drawString(50, y_position, f"Location: {filters.location}")
        y_position -= 18

    if filters and filters.days:
        pdf.drawString(50, y_position, f"Days Filter: Last {filters.days} days")
        y_position -= 18

    pdf.drawString(50, y_position, f"Global Score: {strategy_output.get('global_score', 0)}")
    y_position -= 28

    swot = strategy_output.get("swot", {})
    y_position = _draw_section(pdf, "Strengths", list(swot.get("strengths", [])), y_position)
    y_position = _draw_section(pdf, "Weaknesses", list(swot.get("weaknesses", [])), y_position)
    y_position = _draw_section(pdf, "Opportunities", list(swot.get("opportunities", [])), y_position)
    y_position = _draw_section(pdf, "Threats", list(swot.get("threats", [])), y_position)

    four_ps = strategy_output.get("4ps", {})
    four_p_lines = [
        f"Product: {four_ps.get('product', '')}",
        f"Price: {four_ps.get('price', '')}",
        f"Place: {four_ps.get('place', '')}",
        f"Promotion: {four_ps.get('promotion', '')}",
    ]
    y_position = _draw_section(pdf, "4Ps Framework", four_p_lines, y_position)

    insight_items = [
        f"{insight.get('text', '')} | Sources: {', '.join(insight.get('source_urls', []))}"
        for insight in strategy_output.get("insights", [])
    ]
    y_position = _draw_section(pdf, "Insights", insight_items, y_position)
    _draw_section(
        pdf,
        "Recommendations",
        list(strategy_output.get("recommendations", [])),
        y_position,
    )

    pdf.save()
    buffer.seek(0)
    return buffer
