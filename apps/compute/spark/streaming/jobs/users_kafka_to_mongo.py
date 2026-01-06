import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from lib.spark_session import create_spark_session

from lib.streaming.kafka_reader import read_kafka_json
from lib.streaming.mongo_writer import start_stream_to_mongo
from lib.streaming.schemas import user_schema


def main() -> None:
    spark = create_spark_session(app_name="users-kafka-to-mongo")
    topic = os.getenv("KAFKA_TOPIC_USER", "raw_data_user")
    collection = os.getenv("MONGO_COLLECTION_USER", "users")

    users_stream = read_kafka_json(spark, topic, user_schema())
    query = start_stream_to_mongo(
        users_stream,
        collection=collection,
        checkpoint_env="KAFKA_USERS_CHECKPOINT",
        default_checkpoint="/tmp/users_checkpoint",
    )
    query.awaitTermination()


if __name__ == "__main__":
    main()
