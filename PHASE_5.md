# Phase 5: Strategy and Business Recommendations

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
  "swot": {
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "threats": []
  },
  "recommendations": []
}
```
