import os
from functools import lru_cache

class Settings:
    APP_NAME: str = "Yelp Serving API"
    
    # Kafka configuration
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
    KAFKA_TOPIC_BUSINESS: str = os.getenv("KAFKA_TOPIC_BUSINESS", "raw_data_business")
    KAFKA_TOPIC_USER: str = os.getenv("KAFKA_TOPIC_USER", "raw_data_user")
    KAFKA_TOPIC_REVIEW: str = os.getenv("KAFKA_TOPIC_REVIEW", "raw_data_review")

    # MongoDB configuration
    MONGO_HOST: str = os.getenv("MONGO_HOST", "mongodb")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", "27017"))
    MONGO_USER: str = os.getenv(
        "MONGO_USER",
        os.getenv("MONGO_INITDB_ROOT_USERNAME", "root"),
    )
    MONGO_PASSWORD: str = os.getenv(
        "MONGO_PASSWORD",
        os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password"),
    )
    MONGO_AUTH_DB: str = os.getenv("MONGO_AUTH_DB", "admin")
    MONGO_DB: str = os.getenv("MONGO_DB", "yelp")
    MONGO_COLLECTION_BUSINESS: str = os.getenv(
        "MONGO_COLLECTION_BUSINESS", "businesses"
    )
    MONGO_COLLECTION_USER: str = os.getenv("MONGO_COLLECTION_USER", "users")
    MONGO_COLLECTION_REVIEW: str = os.getenv("MONGO_COLLECTION_REVIEW", "reviews")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()
