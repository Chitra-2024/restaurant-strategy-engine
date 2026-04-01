def get_health_status() -> dict[str, str]:
    return {"status": "ok"}


async def insert_test_document(database) -> str:
    result = await database.test_collection.insert_one(
        {"message": "mongo is working"}
    )
    return str(result.inserted_id)
