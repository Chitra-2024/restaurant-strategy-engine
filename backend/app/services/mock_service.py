import random
from datetime import datetime, timedelta, timezone

PLATFORMS = ["reddit", "google", "twitter", "zomato"]
POSITIVE_TEMPLATES = [
    "{restaurant_name} food is amazing.",
    "Loved the ambience at {restaurant_name}.",
    "Had a great dinner at {restaurant_name}; the flavors really stood out.",
    "{restaurant_name} surprised me in a good way. Fresh food and friendly staff.",
    "Really enjoyed my visit to {restaurant_name}. I'd happily go back.",
]
NEGATIVE_TEMPLATES = [
    "{restaurant_name} service is slow.",
    "Delivery from {restaurant_name} was late.",
    "Expected better from {restaurant_name}; the meal arrived cold.",
    "Waited too long for a table at {restaurant_name}.",
    "{restaurant_name} looked busy, but the experience felt disorganized.",
]
NEUTRAL_TEMPLATES = [
    "{restaurant_name} is okay overall.",
    "Tried {restaurant_name} today. Nothing special, nothing terrible.",
    "{restaurant_name} felt average for the price point.",
    "The experience at {restaurant_name} was mixed but acceptable.",
    "{restaurant_name} is decent if you are nearby.",
]
SENTIMENT_POOLS = (
    POSITIVE_TEMPLATES,
    POSITIVE_TEMPLATES,
    NEGATIVE_TEMPLATES,
    NEUTRAL_TEMPLATES,
)


def _random_recent_timestamp() -> str:
    now = datetime.now(timezone.utc)
    offset = timedelta(
        days=random.randint(0, 14),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return (now - offset).isoformat()


def _build_mock_record(restaurant_name: str) -> dict[str, str]:
    templates = random.choice(SENTIMENT_POOLS)
    template = random.choice(templates)

    return {
        "platform": random.choice(PLATFORMS),
        "text": template.format(restaurant_name=restaurant_name),
        "timestamp": _random_recent_timestamp(),
        "restaurant_name": restaurant_name,
    }


async def generate_mock_reviews(restaurant_name: str) -> list[dict[str, str]]:
    record_count = random.randint(15, 25)
    return [_build_mock_record(restaurant_name=restaurant_name) for _ in range(record_count)]
