from . import config


def write_to_mongo(batch_df, batch_id: int, collection: str) -> None:
    if batch_df.rdd.isEmpty():
        return

    (batch_df.write.format("mongodb")
        .mode("append")
        .option("database", config.mongo_database())
        .option("collection", collection)
        .save())


def start_stream_to_mongo(stream_df, collection: str, checkpoint_env: str, default_checkpoint: str):
    checkpoint = config.checkpoint_path(checkpoint_env, default_checkpoint)
    trigger_seconds = config.kafka_trigger_seconds()

    writer = (
        stream_df.writeStream
        .foreachBatch(lambda df, batch_id: write_to_mongo(df, batch_id, collection))
        .outputMode("append")
        .option("checkpointLocation", checkpoint)
    )

    if trigger_seconds:
        writer = writer.trigger(processingTime=f"{trigger_seconds} seconds")

    return writer.start()
