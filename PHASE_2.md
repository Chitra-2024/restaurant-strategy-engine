# Phase 2 Data Ingestion Layer

## Ingestion Flow

1. `POST /ingest-data` receives a `restaurant_name`.
2. The API calls the mock data service.
3. The mock service generates realistic multi-platform review-like records.
4. The records are inserted into MongoDB collection `raw_reviews`.
5. The API returns a success message with the inserted record count.

## Sources Used

- Simulated Reddit posts.
- Simulated Google reviews.
- Simulated Twitter posts.
- Simulated Zomato reviews.

## Normalized Shape

All records include:

```json
{
  "platform": "reddit | google | twitter | zomato",
  "text": "review or discussion text",
  "timestamp": "ISO-8601 timestamp",
  "restaurant_name": "restaurant name"
}
```

## Mock Strategy

- Each ingestion request generates 15 to 25 records.
- Platforms are randomly selected from Reddit, Google, Twitter, and Zomato.
- Text varies across positive, negative, and neutral sentiment patterns.
- Timestamps are randomized across recent dates to mimic fresh incoming data.

## Limitations

- All data in this phase is simulated and intended only to validate the ingestion pipeline.
- Record generation is randomized, so exact counts and wording vary between requests.
- This phase only stores raw text data in MongoDB. NLP, sentiment analysis, scoring, and trend detection are intentionally not included yet.
