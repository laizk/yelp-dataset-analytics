import os
from functools import lru_cache

class Settings:
    APP_NAME: str = "Yelp Serving API"
    
    # Kafka configuration
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "broker:29092")
    KAFKA_TOPIC_BUSINESS: str = os.getenv("KAFKA_TOPIC_BUSINESS", "raw_data_business")
    KAFKA_TOPIC_USER: str = os.getenv("KAFKA_TOPIC_USER", "raw_data_user")
    KAFKA_TOPIC_REVIEW: str = os.getenv("KAFKA_TOPIC_REVIEW", "raw_data_review")
    
@lru_cache
def get_settings() -> Settings:
    return Settings()
