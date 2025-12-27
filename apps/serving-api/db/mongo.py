from pymongo import MongoClient

from core.config import get_settings


_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client
    if _client is None:
        settings = get_settings()
        uri = (
            f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}"
            f"@{settings.MONGO_HOST}:{settings.MONGO_PORT}/"
            f"{settings.MONGO_AUTH_DB}?authSource={settings.MONGO_AUTH_DB}"
        )
        _client = MongoClient(uri)
    return _client


def get_business_collection():
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.MONGO_DB][settings.MONGO_COLLECTION_BUSINESS]


def get_user_collection():
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.MONGO_DB][settings.MONGO_COLLECTION_USER]


def get_review_collection():
    settings = get_settings()
    client = get_mongo_client()
    return client[settings.MONGO_DB][settings.MONGO_COLLECTION_REVIEW]
