# Phase 3: Rule-Based NLP Processing

## Sentiment Logic

The sentiment layer is keyword-based and does not use any external API or ML model.

- Positive words: `good`, `great`, `amazing`, `excellent`, `love`, `tasty`
- Negative words: `bad`, `slow`, `poor`, `worst`, `late`, `overpriced`
- If positive and negative words both appear in the same review, the result is `neutral`
- If no tracked keyword appears, the result also falls back to `neutral`

## Aspect Extraction

The aspect extractor uses first-match keyword mapping.

- `food`: `food`, `taste`, `pizza`, `burger`, `meal`
- `service`: `service`, `staff`, `wait`, `support`
- `delivery`: `delivery`, `late`, `time`
- `price`: `price`, `expensive`, `cheap`, `cost`
- `ambience`: `ambience`, `atmosphere`, `environment`

The first matching aspect is selected as the review's primary aspect.

## Confidence Scoring

Confidence is assigned from the platform source.

- `google` -> `0.9`
- `zomato` -> `0.85`
- `reddit` -> `0.6`
- `twitter` -> `0.5`

## Processing Flow

`POST /process-data`:

1. Reads the latest raw reviews from `raw_reviews`
2. Skips reviews that already exist in `processed_reviews`
3. Enriches each review with sentiment, aspect, and confidence
4. Stores the result in `processed_reviews`
