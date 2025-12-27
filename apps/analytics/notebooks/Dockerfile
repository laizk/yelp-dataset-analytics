FROM apache/spark:4.0.1-python3
USER root

# ===== Versions =====
ENV SPARK_VERSION=4.0.1
ENV DELTA_VERSION=4.0.0
ENV HADOOP_VERSION=3.4.0
ENV AWS_SDK_V1_VERSION=1.12.793
ENV AWS_SDK_V2_VERSION=2.40.13
ENV KAFKA_VERSION=4.0.1
ENV SCALA_VERSION=2.13

# ===== Mongo (Spark Connector + Java Driver deps) =====
# Connector jar alone is NOT enough; you also need bson + mongodb driver jars
ENV MONGO_SPARK_VERSION=10.5.0
ENV MONGO_JAVA_DRIVER_VERSION=5.6.2

# ===== OS deps =====
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ===== Core Spark extensions (Delta Lake) =====
RUN wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar

# ===== S3A (Hadoop AWS + AWS SDK v1) =====
RUN wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_V1_VERSION}/aws-java-sdk-bundle-${AWS_SDK_V1_VERSION}.jar

# ===== AWS SDK v2 (sometimes needed with Hadoop 3.4.x environments) =====
RUN wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/${AWS_SDK_V2_VERSION}/bundle-${AWS_SDK_V2_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/software/amazon/awssdk/url-connection-client/${AWS_SDK_V2_VERSION}/url-connection-client-${AWS_SDK_V2_VERSION}.jar

# ===== Kafka (optional) =====
RUN wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_VERSION}/kafka-clients-${KAFKA_VERSION}.jar

# ===== MongoDB Spark Connector + required Mongo Java driver jars =====
RUN wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_${SCALA_VERSION}/${MONGO_SPARK_VERSION}/mongo-spark-connector_${SCALA_VERSION}-${MONGO_SPARK_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-sync-${MONGO_JAVA_DRIVER_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/${MONGO_JAVA_DRIVER_VERSION}/mongodb-driver-core-${MONGO_JAVA_DRIVER_VERSION}.jar && \
    wget -q -P /opt/spark/jars/ \
      https://repo1.maven.org/maven2/org/mongodb/bson/${MONGO_JAVA_DRIVER_VERSION}/bson-${MONGO_JAVA_DRIVER_VERSION}.jar

# ===== Python deps =====
RUN pip install --no-cache-dir \
    jupyterlab \
    delta-spark==${DELTA_VERSION}

WORKDIR /workspace
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]
