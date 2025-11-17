FROM apache/spark:4.0.1-python3

USER root

# Set versions (match Spark / Hadoop / Delta)
ENV DELTA_VERSION=4.0.0
ENV HADOOP_AWS_VERSION=3.4.2
ENV AWS_SDK_VERSION=1.12.793
ENV KAFKA_VERSION=4.0.1
ENV SCALA_VERSION=2.13

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget ca-certificates netcat && \
    rm -rf /var/lib/apt/lists/*

# Download required JARs
RUN wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-spark_${SCALA_VERSION}/${DELTA_VERSION}/delta-spark_${SCALA_VERSION}-${DELTA_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${KAFKA_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${KAFKA_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_VERSION}/kafka-clients-${KAFKA_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_AWS_VERSION}/hadoop-aws-${HADOOP_AWS_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar && \
    wget -P /opt/spark/jars/ \
    https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# Install Python packages
RUN pip install --no-cache-dir delta-spark==${DELTA_VERSION} pyspark==${DELTA_VERSION} kafka-python boto3 great-expectations prometheus-client pytest


# Create app dir
WORKDIR /app

# Switch back to spark user for runtime
USER spark

# Spark env
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3
