import json
import logging
from typing import Any, Dict

from kafka import KafkaProducer
from schemas.business_schema import BusinessSchema
from schemas.user_schema import UserSchema
from schemas.review_schema import ReviewSchema
from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


producer: KafkaProducer | None = None

def get_producer() -> KafkaProducer:
    global producer
    if producer is None:
        logger.info("Creating KafkaProducer...")
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5
        )
    return producer


def _publish_to_kafka(payload_dict: Dict[str, Any], topic: str, entity: str) -> Dict[str, Any]:
    p = get_producer()
    logger.info("Publishing %s to Kafka topic '%s': %s", entity, topic, payload_dict)

    try:
        future = p.send(topic, payload_dict)
        # Block until the send is actually done (optional)
        record_metadata = future.get(timeout=10)

        logger.info(
            "Message sent to Kafka topic=%s partition=%s offset=%s",
            record_metadata.topic,
            record_metadata.partition,
            record_metadata.offset,
        )

        return {
            "status": "success",
            "topic": record_metadata.topic,
            "partition": record_metadata.partition,
            "offset": record_metadata.offset,
        }

    except Exception as exc:
        logger.exception("Failed to publish %s message to Kafka", entity)
        # Let caller decide what to do with the error
        raise exc


def publish_business_to_kafka(business: BusinessSchema) -> Dict[str, Any]:
    """
    Business logic: take a validated BusinessSchema and publish to Kafka.
    Return a small response dict (so routes can directly return it).
    """
    # Pydantic v2: model_dump(); if you're on v1, use .dict()
    payload_dict = business.model_dump()  # or business.dict() for pydantic v1
    return _publish_to_kafka(payload_dict, settings.KAFKA_TOPIC_BUSINESS, "business")


def publish_user_to_kafka(user: UserSchema) -> Dict[str, Any]:
    """
    User logic: take a validated UserSchema and publish to Kafka.
    Return a small response dict (so routes can directly return it).
    """
    payload_dict = user.model_dump()
    return _publish_to_kafka(payload_dict, settings.KAFKA_TOPIC_USER, "user")


def publish_review_to_kafka(review: ReviewSchema) -> Dict[str, Any]:
    """
    Review logic: take a validated ReviewSchema and publish to Kafka.
    Return a small response dict (so routes can directly return it).
    """
    payload_dict = review.model_dump()
    return _publish_to_kafka(payload_dict, settings.KAFKA_TOPIC_REVIEW, "review")
