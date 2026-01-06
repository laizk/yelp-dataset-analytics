from pyspark.sql import functions as F

from . import config


def read_kafka_json(spark, topic: str, schema):
    options = {
        "kafka.bootstrap.servers": config.kafka_bootstrap(),
        "subscribe": topic,
        "startingOffsets": config.kafka_starting_offsets(),
    }

    max_offsets = config.kafka_max_offsets_per_trigger()
    if max_offsets:
        options["maxOffsetsPerTrigger"] = max_offsets

    df = spark.readStream.format("kafka").options(**options).load()
    return (
        df.selectExpr("CAST(value AS STRING) as json_str")
        .select(F.from_json("json_str", schema).alias("payload"))
        .select("payload.*")
    )
