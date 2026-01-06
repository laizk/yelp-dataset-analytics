import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from lib.spark_session import create_spark_session
from lib.streaming.enrichment import (
    load_users_df,
    load_businesses_df,
    start_enriched_stream,
)
from lib.streaming.kafka_reader import read_kafka_json
from lib.streaming.schemas import review_schema


def main() -> None:
    spark = create_spark_session(app_name="reviews-kafka-to-mongo-enriched")
    topic = os.getenv("KAFKA_TOPIC_REVIEW", "raw_data_review")

    reviews_stream = read_kafka_json(spark, topic, review_schema())
    users_df = load_users_df(spark)
    businesses_df = load_businesses_df(spark)

    query = start_enriched_stream(reviews_stream, users_df, businesses_df)
    query.awaitTermination()


if __name__ == "__main__":
    main()
