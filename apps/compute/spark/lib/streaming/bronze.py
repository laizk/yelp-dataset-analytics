from pyspark.sql import functions as F

from . import config


def read_kafka_raw(spark, topic_pattern: str):
    options = {
        "kafka.bootstrap.servers": config.kafka_bootstrap(),
        "subscribePattern": topic_pattern,
        "startingOffsets": config.kafka_starting_offsets(),
    }

    max_offsets = config.kafka_max_offsets_per_trigger()
    if max_offsets:
        options["maxOffsetsPerTrigger"] = max_offsets

    return spark.readStream.format("kafka").options(**options).load()


def with_record_type(df):
    # Expect topic names like raw_data_review/raw_data_user/raw_data_business.
    record_type = F.regexp_extract(F.col("topic"), r"raw_data_([A-Za-z0-9_-]+)", 1)
    return df.withColumn("record_type", record_type)


def build_bronze_df(df):
    return (
        df.transform(with_record_type)
        .withColumn("ingest_ts", F.current_timestamp())
        .select(
            "record_type",
            "topic",
            F.col("partition").alias("kafka_partition"),
            F.col("offset").alias("kafka_offset"),
            F.col("timestamp").alias("kafka_timestamp"),
            F.col("ingest_ts"),
            F.col("key").cast("string").alias("key"),
            F.col("value").cast("string").alias("raw_payload"),
        )
    )


def write_bronze(df):
    path = config.get_env("BRONZE_STREAM_PATH", "s3a://bronze/kafka")
    checkpoint = config.checkpoint_path("KAFKA_BRONZE_CHECKPOINT", "/tmp/bronze_kafka_checkpoint")
    trigger_seconds = config.kafka_trigger_seconds()

    writer = (
        df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint)
        .option("path", path)
    )

    if trigger_seconds:
        writer = writer.trigger(processingTime=f"{trigger_seconds} seconds")

    return writer.start()
