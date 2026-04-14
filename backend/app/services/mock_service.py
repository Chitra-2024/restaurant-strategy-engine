import random
from datetime import datetime, timedelta, timezone

PLATFORMS = ["reddit", "google", "twitter", "zomato"]
LOCATIONS = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad"]
PLATFORM_TEMPLATES = {
    "google": {
        "positive": [
            "{restaurant_name} food is amazing and the staff in {location} made the visit even better.",
            "Loved the ambience at {restaurant_name}; the meal was excellent.",
        ],
        "negative": [
            "{restaurant_name} service is slow and the wait felt too long.",
            "Expected better from {restaurant_name}; the meal arrived cold and overpriced.",
        ],
        "neutral": [
            "{restaurant_name} is okay overall for a quick meal in {location}.",
            "Tried {restaurant_name} today. Nothing special, nothing terrible.",
        ],
    },
    "reddit": {
        "positive": [
            "Had a great dinner at {restaurant_name}; the flavors really stood out.",
            "{restaurant_name} surprised me in a good way. Fresh food and friendly staff.",
        ],
        "negative": [
            "Delivery from {restaurant_name} was late again.",
            "{restaurant_name} looked busy, but the experience felt disorganized.",
        ],
        "neutral": [
            "{restaurant_name} felt average for the price point.",
            "The experience at {restaurant_name} was mixed but acceptable.",
        ],
    },
    "twitter": {
        "positive": [
            "Love the burger at {restaurant_name}. Tasty and quick.",
            "Amazing food at {restaurant_name} tonight.",
        ],
        "negative": [
            "Worst service at {restaurant_name}; support was poor.",
            "{restaurant_name} delivery was late and the order felt bad for the cost.",
        ],
        "neutral": [
            "{restaurant_name} is decent if you are nearby.",
            "Tried {restaurant_name}; it was fine overall.",
        ],
    },
    "zomato": {
        "positive": [
            "Ordered via Zomato from {restaurant_name}; the food was tasty and arrived on time.",
            "Excellent meal from {restaurant_name}. Great taste, good portion size, and smooth delivery.",
        ],
        "negative": [
            "Zomato order from {restaurant_name} was late and the meal felt overpriced.",
            "Poor delivery experience from {restaurant_name}; the food arrived cold.",
        ],
        "neutral": [
            "Zomato order from {restaurant_name} was average overall.",
            "The meal from {restaurant_name} was okay, though nothing stood out.",
        ],
    },
}
SENTIMENT_POOLS = ("positive", "positive", "negative", "neutral")


def _random_recent_timestamp(max_days: int) -> str:
    now = datetime.now(timezone.utc)
    offset = timedelta(
        days=random.randint(0, max_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return (now - offset).isoformat()


def _slugify(value: str) -> str:
    return value.lower().replace(" ", "-")


def _build_source_url(platform: str, restaurant_name: str) -> str:
    slug = _slugify(restaurant_name)
    review_id = random.randint(100, 999)

    if platform == "zomato":
        return f"https://zomato.com/restaurant/{slug}/reviews/{review_id}"
    if platform == "google":
        return f"https://example.com/google/{slug}/review/{review_id}"
    if platform == "twitter":
        return f"https://example.com/twitter/{slug}/status/{review_id}"
    return f"https://example.com/reddit/{slug}/review/{review_id}"


def _build_mock_record(
    restaurant_name: str,
    location: str | None,
    max_days: int,
) -> dict[str, str]:
    platform = random.choice(PLATFORMS)
    sentiment = random.choice(SENTIMENT_POOLS)
    review_location = location or random.choice(LOCATIONS)
    template = random.choice(PLATFORM_TEMPLATES[platform][sentiment])

    return {
        "platform": platform,
        "text": template.format(restaurant_name=restaurant_name, location=review_location),
        "timestamp": _random_recent_timestamp(max_days),
        "restaurant_name": restaurant_name,
        "location": review_location,
        "source_url": _build_source_url(platform, restaurant_name),
    }


async def generate_mock_reviews(
    restaurant_name: str,
    location: str | None = None,
    days: int | None = None,
) -> list[dict[str, str]]:
    record_count = random.randint(15, 25)
    max_days = max(1, min(days or 30, 30))
    return [
        _build_mock_record(
            restaurant_name=restaurant_name,
            location=location,
            max_days=max_days,
        )
        for _ in range(record_count)
    ]
