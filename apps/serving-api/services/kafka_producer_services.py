import json
import logging
from typing import Any, Dict

from kafka import KafkaProducer
from schemas.business_schema import BusinessSchema
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


def publish_business_to_kafka(business: BusinessSchema) -> Dict[str, Any]:
    """
    Business logic: take a validated BusinessSchema and publish to Kafka.
    Return a small response dict (so routes can directly return it).
    """
    # Pydantic v2: model_dump(); if you're on v1, use .dict()
    payload_dict = business.model_dump()  # or business.dict() for pydantic v1
    
    p = get_producer()  # <-- created only now    
    
    print('business payload_dict:', payload_dict)

    logger.info(
        "Publishing business to Kafka topic '%s': %s",
        settings.KAFKA_TOPIC_BUSINESS,
        payload_dict,
    )

    try:
        future = p.send(settings.KAFKA_TOPIC_BUSINESS, payload_dict)
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
        logger.exception("Failed to publish message to Kafka")
        # Let caller decide what to do with the error
        raise exc
