import os
from pyspark.sql import SparkSession
from utils import _mongo_uri

def create_spark_session(app_name: str = "My Spark App") -> SparkSession:
    # Optional: set master via env (leave empty to let spark-submit decide)
    spark_master = os.getenv("SPARK_MASTER_URL", "")  # e.g. spark://spark-master:7077

    builder = (
        SparkSession.builder
        .appName(app_name)
        # Delta
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
        # MinIO / S3A from env (falls back to docker service name)
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("DATA_LAKE_ENDPOINT", "http://minio:9000"))
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("DATA_LAKE_ACCESS_KEY_ID", "minioadmin"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("DATA_LAKE_SECRET_ACCESS_KEY", "minioadmin"))
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        # Mongo (set BOTH)
        .config("spark.mongodb.read.connection.uri", _mongo_uri())
        .config("spark.mongodb.write.connection.uri", _mongo_uri())
    )

    if spark_master:
        builder = builder.config("spark.master", spark_master)

    spark = builder.getOrCreate()
    return spark
