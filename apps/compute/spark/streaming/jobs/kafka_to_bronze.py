import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from lib.spark_session import create_spark_session
from lib.streaming.bronze import build_bronze_df, read_kafka_raw, write_bronze


def main() -> None:
    spark = create_spark_session(app_name="kafka-to-bronze")
    topic_pattern = os.getenv("KAFKA_BRONZE_TOPIC_PATTERN", "raw_data_.*")

    raw_stream = read_kafka_raw(spark, topic_pattern)
    bronze_stream = build_bronze_df(raw_stream)
    query = write_bronze(bronze_stream)
    query.awaitTermination()


if __name__ == "__main__":
    main()
