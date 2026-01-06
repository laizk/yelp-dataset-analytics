import os

from pyspark.sql import SparkSession

def _get_env(name: str, default: str) -> str:
    value = os.getenv(name, default)
    return value


def _mongo_uri() -> str:
    host = _get_env("MONGO_HOST", "mongodb")
    port = _get_env("MONGO_PORT", "27017")
    user = _get_env("MONGO_INITDB_ROOT_USERNAME", "root")
    password = _get_env("MONGO_INITDB_ROOT_PASSWORD", "password")
    auth_db = _get_env("MONGO_AUTH_DB", "admin")
    return f"mongodb://{user}:{password}@{host}:{port}/{auth_db}?authSource={auth_db}"


def _load_jsonl(spark: SparkSession, path: str):
    return spark.read.json(path)


def _write_bronze(df, path: str, mode: str) -> None:
    df.write.format("delta").mode(mode).save(path)


def _write_mongo(df, database: str, collection: str, mode: str) -> None:
    (df.write.format("mongodb")
       .mode(mode)
       .option("connection.uri", _mongo_uri())
       .option("database", database)
       .option("collection", collection)
       .save())

def _read_mongo(spark: SparkSession, database: str, collection: str):
    return (spark.read.format("mongodb")
            .option("connection.uri", _mongo_uri())
            .option("database", database)
            .option("collection", collection)
            .load())
