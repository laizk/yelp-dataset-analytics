from __future__ import annotations

import os
from datetime import datetime

from airflow.sdk import dag
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


def _spark_conf() -> dict:
    mongo_host = os.getenv("MONGO_HOST", "mongodb")
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
    mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password")
    mongo_db = os.getenv("MONGO_DB", "yelp")

    split_dir = os.getenv("YELP_SPLIT_DIR", "/data/raw/split")
    bronze_base = os.getenv("BRONZE_BASE", "s3a://bronze")

    base_env = {
        "MONGO_HOST": mongo_host,
        "MONGO_PORT": mongo_port,
        "MONGO_INITDB_ROOT_USERNAME": mongo_user,
        "MONGO_INITDB_ROOT_PASSWORD": mongo_password,
        "MONGO_DB": mongo_db,
        "YELP_SPLIT_DIR": split_dir,
        "BRONZE_BASE": bronze_base,
    }

    conf = {
        "spark.submit.deployMode": "client",
    }

    for key, value in base_env.items():
        conf[f"spark.driverEnv.{key}"] = value
        conf[f"spark.executorEnv.{key}"] = value

    return conf


@dag(
    dag_id="spark_users_businesses_bronze_mongo",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    description="Spark batch load of users/businesses to bronze + MongoDB",
)
def spark_users_businesses_bronze_mongo():
    SparkSubmitOperator(
        task_id="submit_users_businesses_job",
        conn_id="spark_standalone_client",
        application="/app/jobs/users_businesses_to_bronze_mongo.py",
        name="users-businesses-bronze-mongo",
        verbose=True,
        conf=_spark_conf(),
    )


spark_users_businesses_bronze_mongo()
