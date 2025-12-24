# Airflow image with Spark binaries + Delta + S3A (MinIO/S3) + Mongo jars
FROM apache/airflow:3.1.3

USER root

# ----------------------------
# Versions (aligned with Jupyter/Spark)
# ----------------------------
ENV SPARK_VERSION=4.0.1
ENV HADOOP_PROFILE=bin-hadoop3

ENV SCALA_VERSION=2.13
ENV DELTA_VERSION=4.0.0

# S3A / Hadoop (align)
ENV HADOOP_VERSION=3.4.0
ENV AWS_SDK_V1_VERSION=1.12.793
ENV AWS_SDK_V2_VERSION=2.40.13

# Mongo (align)
ENV MONGO_SPARK_VERSION=10.5.0
ENV MONGO_JAVA_DRIVER_VERSION=5.6.2

ENV SPARK_HOME=/opt/spark

# ----------------------------
# OS deps
# ----------------------------
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     openjdk-17-jdk-headless \
     curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# ----------------------------
# Install Spark distribution (spark-submit used by SparkSubmitOperator)
# ----------------------------
RUN curl -L -o /tmp/spark.tgz \
    https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-${HADOOP_PROFILE}.tgz \
  && tar -xzf /tmp/spark.tgz -C /opt \
  && mv /opt/spark-${SPARK_VERSION}-${HADOOP_PROFILE} ${SPARK_HOME} \
  && rm /tmp/spark.tgz

# ----------------------------
# JARs: Delta + S3A + Mongo (+ driver deps)
# ----------------------------
RUN set -eux; \
  # Delta
  curl -L -o ${SPARK_HOME}/jars/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar \
    https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar; \
  curl -L -o ${SPARK_HOME}/jars/delta-storage-${DELTA_VERSION}.jar \
    https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar; \
  \
  # S3A
  curl -L -o ${SPARK_HOME}/jars/hadoop-aws-${HADOOP_VERSION}.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar; \
  curl -L -o ${SPARK_HOME}/jars/aws-java-sdk-bundle-${AWS_SDK_V1_VERSION}.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_V1_VERSION}/aws-java-sdk-bundle-${AWS_SDK_V1_VERSION}.jar; \
  \
  # AWS SDK v2 (optional but consistent with your other images)
  curl -L -o ${SPARK_HOME}/jars/awssdk-bundle-${AWS_SDK_V2_VERSION}.jar \
    https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_V2_VERSION}/bundle-${AWS_SDK_V2_VERSION}.jar; \
  curl -L -o ${SPARK_HOME}/jars/awssdk-url-connection-client-${AWS_SDK_V2_VERSION}.jar \
    https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/${AWS_SDK_V2_VERSION}/url-connection-client-${AWS_SDK_V2_VERSION}.jar; \
  \
  # Mongo Spark Connector
  curl -L -o ${SPARK_HOME}/jars/mongo-spark-connector_${SCALA_VERSION}-${MONGO_SPARK_VERSION}.jar \
    https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_${SCALA_VERSION}/${MONGO_SPARK_VERSION}/mongo-spark-connector_${SCALA_VERSION}-${MONGO_SPARK_VERSION}.jar; \
  \
  # Mongo Java Driver deps (fix org/bson/BsonValue)
  curl -L -o ${SPARK_HOME}/jars/mongodb-driver-sync-${MONGO_JAVA_DRIVER_VERSION}.jar \
    https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-sync-${MONGO_JAVA_DRIVER_VERSION}.jar; \
  curl -L -o ${SPARK_HOME}/jars/mongodb-driver-core-${MONGO_JAVA_DRIVER_VERSION}.jar \
    https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-core-${MONGO_JAVA_DRIVER_VERSION}.jar; \
  curl -L -o ${SPARK_HOME}/jars/bson-${MONGO_JAVA_DRIVER_VERSION}.jar \
    https://repo1.maven.org/maven2/org/mongodb/bson/${MONGO_JAVA_DRIVER_VERSION}/bson-${MONGO_JAVA_DRIVER_VERSION}.jar

# Ensure spark-submit is on PATH
ENV PATH="${SPARK_HOME}/bin:${PATH}"

USER airflow

# ----------------------------
# Airflow provider + optional pyspark for local testing
# ----------------------------
RUN pip install --no-cache-dir \
  apache-airflow-providers-apache-spark==5.4.1 \
  pyspark==${SPARK_VERSION} \
  delta-spark==${DELTA_VERSION}
