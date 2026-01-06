from pyspark.sql import types as T


def review_schema() -> T.StructType:
    return T.StructType(
        [
            T.StructField("review_id", T.StringType(), True),
            T.StructField("user_id", T.StringType(), True),
            T.StructField("business_id", T.StringType(), True),
            T.StructField("stars", T.IntegerType(), True),
            T.StructField("useful", T.IntegerType(), True),
            T.StructField("funny", T.IntegerType(), True),
            T.StructField("cool", T.IntegerType(), True),
            T.StructField("text", T.StringType(), True),
            T.StructField("date", T.StringType(), True),
        ]
    )


def user_schema() -> T.StructType:
    return T.StructType(
        [
            T.StructField("user_id", T.StringType(), True),
            T.StructField("name", T.StringType(), True),
            T.StructField("review_count", T.IntegerType(), True),
            T.StructField("yelping_since", T.StringType(), True),
            T.StructField("useful", T.IntegerType(), True),
            T.StructField("funny", T.IntegerType(), True),
            T.StructField("cool", T.IntegerType(), True),
            T.StructField("fans", T.IntegerType(), True),
            T.StructField("average_stars", T.DoubleType(), True),
        ]
    )


def business_schema() -> T.StructType:
    return T.StructType(
        [
            T.StructField("business_id", T.StringType(), True),
            T.StructField("name", T.StringType(), True),
            T.StructField("address", T.StringType(), True),
            T.StructField("city", T.StringType(), True),
            T.StructField("state", T.StringType(), True),
            T.StructField("postal_code", T.StringType(), True),
            T.StructField("latitude", T.DoubleType(), True),
            T.StructField("longitude", T.DoubleType(), True),
            T.StructField("stars", T.DoubleType(), True),
            T.StructField("review_count", T.IntegerType(), True),
            T.StructField("is_open", T.IntegerType(), True),
            T.StructField("attributes", T.MapType(T.StringType(), T.StringType()), True),
            T.StructField("categories", T.StringType(), True),
            T.StructField("hours", T.MapType(T.StringType(), T.StringType()), True),
        ]
    )
