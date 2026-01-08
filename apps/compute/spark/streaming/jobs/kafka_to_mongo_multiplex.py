import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from lib.spark_session import create_spark_session
from lib.streaming.bronze import read_kafka_raw
from lib.streaming.mongo_multiplex import start_multiplex_stream


def main() -> None:
    spark = create_spark_session(app_name="kafka-to-mongo-multiplex")
    topic_pattern = os.getenv("KAFKA_MONGO_TOPIC_PATTERN", "raw_data_.*")

    kafka_stream = read_kafka_raw(spark, topic_pattern)
    query = start_multiplex_stream(kafka_stream)
    query.awaitTermination()


if __name__ == "__main__":
    main()
