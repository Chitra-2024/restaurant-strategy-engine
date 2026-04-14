# Phase 4: Analytics and Strategic Scoring

## Aggregation Logic

The analytics layer reads from `processed_reviews` and groups records by:

- `aspect`
- `sentiment`

This produces a compact summary such as:

```json
{
  "food": {
    "positive": 10,
    "negative": 3,
    "neutral": 1
  }
}
```

## Aspect Scores

Each aspect now returns a richer structure:

```json
{
  "food": {
    "score": 0.77,
    "positive": 10,
    "negative": 3
  }
}
```

The score still uses the same ratio:

`score = positive / (positive + negative)`

- Positive-heavy aspects move closer to `1.0`
- Negative-heavy aspects move closer to `0.0`
- If an aspect has no positive or negative reviews, its score falls back to `0.0`
- Aspects are ordered by review volume so the most discussed topics appear first

## Health Score

The restaurant health score uses confidence-weighted sentiment:

`sum(sentiment_score * confidence) / sum(confidence)`

Sentiment is converted into numeric values:

- `positive = 1.0`
- `neutral = 0.5`
- `negative = 0.0`

The final value is normalized to a `0-100` scale.

## Insights

The service identifies:

- `strengths`: aspects with strong positive ratios
- `weaknesses`: aspects with strong negative ratios
- `insights`: human-readable statements for each aspect
- `summary`: a short business-friendly overview of overall performance

Insight rules:

- `score > 0.7` -> strong positive insight
- `score < 0.4` -> strong negative insight
- otherwise -> mixed sentiment insight

Strength and weakness lists remain simple:

- `strengths` use `score > 0.6`
- `weaknesses` use `score < 0.4`

The summary is generated from the health score plus the main strengths and weaknesses so non-technical users can quickly understand the result.
