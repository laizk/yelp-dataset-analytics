from pyspark.sql import functions as F

from . import config
from .schemas import review_schema, user_schema, business_schema
from .mongo_writer import write_to_mongo


def _with_record_type(df):
    record_type = F.regexp_extract(F.col("topic"), r"raw_data_([A-Za-z0-9_-]+)", 1)
    return df.withColumn("record_type", record_type)


def _parse_payload(df, schema):
    return (
        df.selectExpr("CAST(value AS STRING) as json_str")
        .select(F.from_json("json_str", schema).alias("payload"))
        .select("payload.*")
    )


def write_multiplex_batch(batch_df, batch_id: int) -> None:
    """Split a mixed Kafka batch by record_type and write to Mongo collections."""
    if batch_df.rdd.isEmpty():
        return

    typed = _with_record_type(batch_df)

    reviews = typed.filter(F.col("record_type") == "review")
    users = typed.filter(F.col("record_type") == "user")
    businesses = typed.filter(F.col("record_type") == "business")

    if not reviews.rdd.isEmpty():
        review_df = _parse_payload(reviews, review_schema())
        write_to_mongo(
            review_df,
            batch_id,
            config.get_env("MONGO_COLLECTION_REVIEW", "reviews"),
        )

    if not users.rdd.isEmpty():
        user_df = _parse_payload(users, user_schema())
        write_to_mongo(
            user_df,
            batch_id,
            config.get_env("MONGO_COLLECTION_USER", "users"),
        )

    if not businesses.rdd.isEmpty():
        business_df = _parse_payload(businesses, business_schema())
        write_to_mongo(
            business_df,
            batch_id,
            config.get_env("MONGO_COLLECTION_BUSINESS", "businesses"),
        )


def start_multiplex_stream(kafka_stream):
    checkpoint = config.checkpoint_path(
        "KAFKA_MONGO_MULTIPLEX_CHECKPOINT",
        "/tmp/mongo_multiplex_checkpoint",
    )
    trigger_seconds = config.kafka_trigger_seconds()

    writer = (
        kafka_stream.writeStream
        .foreachBatch(write_multiplex_batch)
        .outputMode("append")
        .option("checkpointLocation", checkpoint)
    )

    if trigger_seconds:
        writer = writer.trigger(processingTime=f"{trigger_seconds} seconds")

    return writer.start()
