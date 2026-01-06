import os
import sys

from pyspark.sql import SparkSession

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from lib.spark_session import create_spark_session
from lib.utils import _get_env, _mongo_uri, _load_jsonl, _write_bronze, _write_mongo

def main() -> None:
    # spark = (
    #     SparkSession.builder.appName("users-businesses-bronze-mongo")
    #     .config("spark.mongodb.write.connection.uri", _mongo_uri())
    #     .getOrCreate()
    # )
    
    spark = create_spark_session(app_name="users-businesses-bronze-mongo")

    split_dir = _get_env("YELP_SPLIT_DIR", "/data/raw/split")
    users_path = _get_env("USERS_PATH", os.path.join(split_dir, "yelp_academic_dataset_user_part1.jsonl"))
    businesses_path = _get_env(
        "BUSINESSES_PATH", os.path.join(split_dir, "yelp_academic_dataset_business_part1.jsonl")
    )

    bronze_base = _get_env("BRONZE_BASE", "s3a://bronze")
    bronze_users_path = _get_env("BRONZE_USERS_PATH", f"{bronze_base}/users")
    bronze_businesses_path = _get_env("BRONZE_BUSINESSES_PATH", f"{bronze_base}/businesses")
    bronze_mode = _get_env("BRONZE_MODE", "overwrite")

    mongo_db = _get_env("MONGO_APP_DB", "yelp")
    mongo_mode = _get_env("MONGO_MODE", "append")

    users_df = _load_jsonl(spark, users_path)
    businesses_df = _load_jsonl(spark, businesses_path)

    _write_bronze(users_df, bronze_users_path, bronze_mode)
    _write_bronze(businesses_df, bronze_businesses_path, bronze_mode)

    _write_mongo(users_df, mongo_db, "users", mongo_mode)
    _write_mongo(businesses_df, mongo_db, "businesses", mongo_mode)

    spark.stop()


if __name__ == "__main__":
    main()
