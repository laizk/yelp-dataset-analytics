from pyspark.sql import functions as F

from lib.utils import _read_mongo
from . import config


def load_users_df(spark):
    """Load users dimension from MongoDB."""
    db = config.mongo_database()
    collection = config.get_env("MONGO_COLLECTION_USER", "users")
    return _read_mongo(spark, db, collection)


def load_businesses_df(spark):
    """Load businesses dimension from MongoDB."""
    db = config.mongo_database()
    collection = config.get_env("MONGO_COLLECTION_BUSINESS", "businesses")
    return _read_mongo(spark, db, collection)


def prep_dims(users_df, businesses_df):
    """Select only needed columns and drop duplicate IDs."""
    users_clean = (
        users_df.select(F.col("user_id"), F.col("name").alias("user_name"))
        .dropDuplicates(["user_id"])
    )
    businesses_clean = (
        businesses_df.select(F.col("business_id"), F.col("name").alias("business_name"))
        .dropDuplicates(["business_id"])
    )
    return users_clean, businesses_clean


def build_enriched_reviews_df(reviews_stream, users_clean, businesses_clean):
    """Join streaming reviews with user/business dims and shape enriched schema."""
    reviews_pruned = reviews_stream.select(
        "review_id",
        "user_id",
        "business_id",
        "stars",
        "useful",
        "funny",
        "cool",
        "text",
        "date",
    )

    joined = (
        reviews_pruned
        .join(users_clean, on="user_id", how="left")
        .join(businesses_clean, on="business_id", how="left")
    )

    return joined.select(
        F.col("review_id"),
        F.col("user_id"),
        F.col("business_id"),
        F.col("date").alias("timestamp"),
        F.struct("stars", "useful", "funny", "cool", "text", "date").alias("review"),
        F.struct(F.col("user_name").alias("name")).alias("user_info"),
        F.struct(F.col("business_name").alias("name")).alias("business_info"),
    )


def write_enriched_to_mongo(batch_df, batch_id: int) -> None:
    """Append enriched reviews to MongoDB (reviews_enriched)."""
    if batch_df.rdd.isEmpty():
        return

    # Optional: reduce write parallelism for smaller local clusters.
    # batch_df = batch_df.coalesce(8)

    collection = config.get_env("MONGO_COLLECTION_REVIEWS_ENRICHED", "reviews_enriched")
    (batch_df.write.format("mongodb")
        .mode("append")
        .option("database", config.mongo_database())
        .option("collection", collection)
        .save())


def start_enriched_stream(reviews_stream, users_df, businesses_df):
    """Start streaming write to MongoDB (reviews_enriched)."""
    users_clean, businesses_clean = prep_dims(users_df, businesses_df)
    enriched = build_enriched_reviews_df(reviews_stream, users_clean, businesses_clean)

    checkpoint = config.checkpoint_path(
        "KAFKA_REVIEWS_ENRICHED_CHECKPOINT",
        "/tmp/reviews_enriched_checkpoint",
    )
    trigger_seconds = config.kafka_trigger_seconds()

    writer = (
        enriched.writeStream
        .foreachBatch(write_enriched_to_mongo)
        .outputMode("append")
        .option("checkpointLocation", checkpoint)
    )

    if trigger_seconds:
        writer = writer.trigger(processingTime=f"{trigger_seconds} seconds")

    return writer.start()
