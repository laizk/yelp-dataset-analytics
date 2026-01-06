# Spark cluster image (master/worker/driver) with Delta + Kafka + Mongo + S3A (MinIO/S3)
FROM apache/spark:4.0.1-python3

USER root

# ----------------------------
# Versions (aligned with Jupyter image)
# ----------------------------
ENV SPARK_VERSION=4.0.1
ENV SCALA_VERSION=2.13

ENV DELTA_VERSION=4.0.0

# S3A / Hadoop
ENV HADOOP_VERSION=3.4.0
ENV AWS_SDK_V1_VERSION=1.12.793
ENV AWS_SDK_V2_VERSION=2.40.13

# Kafka (match Spark)
ENV KAFKA_VERSION=4.0.1

# Mongo (match Jupyter)
ENV MONGO_SPARK_VERSION=10.5.0
ENV MONGO_JAVA_DRIVER_VERSION=5.6.2

ENV SPARK_HOME=/opt/spark

# ----------------------------
# OS deps
# ----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget ca-certificates netcat curl && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------
# JARs: Delta, Kafka, S3A, AWS SDK, Mongo (+ driver deps)
# ----------------------------
RUN set -eux; \
  \
  # Delta
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar; \
  \
  # Kafka
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_VERSION}/kafka-clients-${KAFKA_VERSION}.jar; \
  \
  # S3A (MinIO/S3)
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_V1_VERSION}/aws-java-sdk-bundle-${AWS_SDK_V1_VERSION}.jar; \
  \
  # AWS SDK v2 (kept aligned with Jupyter image)
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_V2_VERSION}/bundle-${AWS_SDK_V2_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/${AWS_SDK_V2_VERSION}/url-connection-client-${AWS_SDK_V2_VERSION}.jar; \
  \
  # Optional helper jar you already had (safe to keep)
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar; \
  \
  # Mongo Spark Connector
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_${SCALA_VERSION}/${MONGO_SPARK_VERSION}/mongo-spark-connector_${SCALA_VERSION}-${MONGO_SPARK_VERSION}.jar; \
  \
  # Mongo Java Driver deps (fix NoClassDefFoundError: org/bson/BsonValue)
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-sync-${MONGO_JAVA_DRIVER_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-core-${MONGO_JAVA_DRIVER_VERSION}.jar; \
  wget -q -P ${SPARK_HOME}/jars/ \
    https://repo1.maven.org/maven2/org/mongodb/bson/${MONGO_JAVA_DRIVER_VERSION}/bson-${MONGO_JAVA_DRIVER_VERSION}.jar

# ----------------------------
# Python deps (keep what you need for cluster jobs)
# NOTE: pyspark is already provided by the base image; reinstalling can cause mismatches.
# ----------------------------
RUN pip install --no-cache-dir \
  delta-spark==${DELTA_VERSION} \
  kafka-python \
  boto3 \
  great-expectations \
  prometheus-client \
  pytest

# ----------------------------
# App directory
# ----------------------------
WORKDIR /app

# Switch back to spark user for runtime
USER spark

ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
