# Phase 5: Strategy and Business Recommendations

## Traceability

The pipeline now carries review source metadata end-to-end.

- Mock reviews include `location` and `source_url`
- `source_url` is stored in both `raw_reviews` and `processed_reviews`
- Analytics insights attach source references so business users can trace each finding back to sample reviews

This keeps strategic output explainable instead of opaque.

## Filtering Logic

Strategy and analytics endpoints support optional filters:

- `restaurant_name`
- `location`
- `days`

Filtering is applied before analytics or strategy generation:

- `restaurant_name` narrows results to one restaurant
- `location` narrows results to one market when provided
- `days` limits reviews to the latest N days using review timestamps
- If no filters are provided, the system falls back to all available matching data

## SWOT Logic

The strategy layer uses the existing analytics output as input.

- `strengths` are taken directly from the analytics strengths list
- `weaknesses` are taken directly from the analytics weaknesses list
- `opportunities` are generated from weaknesses as improvement areas
- `threats` are generated from weaknesses as business risks

Example opportunity:

- `Improve delivery to increase customer satisfaction`

Example threat:

- `Poor delivery experience may lead to customer churn`

## 4Ps Logic

The strategy output now includes a simple 4Ps framework:

- `Product` maps to `food`
- `Price` maps to `price`
- `Place` maps to delivery and location experience
- `Promotion` maps to social mentions, especially Reddit and Twitter activity

Rules stay lightweight:

- high score -> positive business statement
- low score -> improvement suggestion
- no data -> neutral fallback

## Recommendations Logic

Recommendations are rule-based and business-friendly.

- Each weakness produces one improvement recommendation
- Each strength produces one reinforcement recommendation

Examples:

- `Maintain strong food performance as a competitive advantage`
- `Optimize delivery operations to address customer concerns`

## Output Structure

`POST /strategy` returns:

```json
{
  "global_score": 78,
  "swot": {
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "threats": []
  },
  "4ps": {
    "product": "",
    "price": "",
    "place": "",
    "promotion": ""
  },
  "insights": [],
  "recommendations": []
}
```

## PDF Export Workflow

`GET /export-pdf` uses the same strategy pipeline and returns a downloadable report.

Flow:

1. Accept `restaurant_name`, optional `location`, and optional `days`
2. Build filtered strategy output
3. Generate a PDF with ReportLab
4. Return the file as a downloadable response

The PDF includes:

- Restaurant Strategy Report title
- Restaurant name
- Global score
- SWOT
- 4Ps
- Insights
- Recommendations
