# Project Journey

This document captures the end-to-end journey of building the Yelp Analytics platform,
including architectural choices, real engineering challenges, and the lessons learned while
iterating toward a production-like local data stack.

## 🎯 Motivation & Goals

The primary goal of this project was to design and implement a realistic data engineering
platform locally, without relying on managed cloud services, while preserving cloud parity.

Key objectives:

-   Reproduce real-world data pipelines:
    -   Streaming ingestion (event-driven)
    -   Batch ELT processing
    -   Lakehouse storage (Bronze / Silver / Gold)
-   Build everything locally-first, but in a way that can later be swapped with:
    -   MinIO → AWS S3 / ADLS
    -   Local Spark → EMR / Databricks
    -   Local Airflow → MWAA / Azure Data Factory
-   Use realistic datasets (Yelp Open Dataset) with:
    -   Large snapshots (business, users)
    -   High-volume append-only streams (reviews)
-   Embrace failure-driven learning by running the system end-to-end and debugging
    real infrastructure issues rather than relying on toy examples.

This project is not just about "making it work", but about understanding why things break
and how production data platforms are stabilized over time.

## 🧭 Key Questions and Decisions

-   **Client vs cluster deploy mode for Spark?**
    -   Decision: Client mode for easier local debugging with Airflow running the driver.
    -   Tradeoff: The Airflow image must carry Spark/Delta/S3A dependencies too.
-   **Where should dependencies live?**
    -   Decision: Bake critical JARs into Spark and Airflow images.
    -   Tradeoff: Larger images, but fewer runtime classpath surprises.
-   **How to standardize networking?**
    -   Decision: Use Docker service names inside containers and `localhost` for host access.
    -   Tradeoff: Documentation must be explicit about where a script runs.

## 🏗️ Architecture Decisions

The stack was intentionally chosen to reflect industry-standard data engineering patterns:

-   **Apache Spark + Delta Lake**
    -   Used for batch ELT and lakehouse modeling
    -   Implements Bronze / Silver / Gold layers
    -   Enables schema evolution, ACID guarantees, and replayable transformations
-   **MinIO (S3A-compatible storage)**
    -   Acts as a local replacement for cloud object storage
    -   Forces correct handling of S3A configs, credentials, and Hadoop dependencies
-   **Apache Airflow**
    -   Orchestrates Spark batch jobs
    -   Mimics real-world scheduler → compute separation
    -   Exposes operational concerns like logging, retries, and dependency management
-   **Apache Kafka**
    -   Handles streaming ingestion for append-only data (reviews)
    -   Enables replay, throttling, and backfill scenarios
    -   Forces explicit thinking about producer/consumer contracts and offsets

A key design principle throughout the project was swap-ability:
any local component should be replaceable by a managed cloud equivalent with minimal changes
to pipeline logic.

## 🚀 Key Milestones

1) **Local Lakehouse with Spark Batch Processing**
   -   Configured Spark to write Delta tables to `s3a://` paths backed by MinIO
   -   Implemented Bronze → Silver → Gold transformations
   -   Validated schema evolution and partitioning strategies

2) **Airflow-Orchestrated Spark Jobs**
   -   Integrated Airflow with Spark via SparkSubmitOperator
   -   Ran Spark jobs in client mode to reflect common on-prem and hybrid setups
   -   Debugged cross-container classpath and dependency propagation issues

3) **Kafka Producer Tooling for Streaming Data**
   -   Built a Kafka producer script to stream Yelp review JSONL files
   -   Added throttling, progress logging, flush intervals, and replayability for backfills
   -   Decoupled snapshot ingestion (batch) from high-velocity review streams (Kafka)

4) **Bronze + Mongo Dual Writes from Spark**
   -   Added a Spark job that loads Yelp users and businesses JSONL splits
   -   Writes raw snapshots to Bronze (`s3a://bronze/users`, `s3a://bronze/businesses`)
   -   Mirrors the same data into MongoDB collections for OLTP-style access

5) **Analytics Engine Shift (DuckDB → Postgres + ClickHouse)**
   -   Replaced DuckDB with Postgres for a production-like OLAP store
   -   Swapped dbt adapter to `dbt-postgres` and added Postgres service + seed data
   -   Added ClickHouse alongside Postgres to compare OLAP performance and UX
   -   Extended FastAPI analytics API to support `/query/postgres` and `/query/clickhouse`

6) **Dataset Split for Batch/Streaming Simulation**
   -   Wrote a JSONL splitter (`local/scripts/split_yelp_dataset.py`) to create
       part1/part2 files while preserving user/business/review relationships
   -   Split enables snapshot batch loads (part1) and change simulation (part2)

7) **Streamlit → Analytics API Integration**
   -   Streamlit reads from FastAPI analytics API and renders a basic chart
   -   Validates query-to-UI flow before modeling dashboards

8) **DuckDB UI Containerization (2025-09-25)**
   -   Moved DuckDB container assets into `apps/analytics/duckdb`
   -   Updated `docker-compose.yml` to reference the new path and run the UI automatically
   -   Switched to the official `duckdb/duckdb:latest` image for stable CLI/UI support
   -   Tried multiple install paths (Alpine package, pip on Alpine, pip on slim) before settling on the official image

9) **DuckDB Server + HTTP Debug API (date TBD)**
   -   Replaced the DuckDB service image with a custom build from `apps/analytics/duckdb`
   -   Starts the DuckDB server (`--listen`) and a FastAPI app for HTTP queries
   -   Added `/health` and `/query` endpoints for quick debugging from a browser or curl

10) **Standalone Spark Cluster + Airflow SparkSubmit**
    -   Split Spark into master + worker in `docker-compose.yml`
    -   Built custom Airflow image with Java + Spark + Spark provider
    -   Added SparkSubmit DAG to run batch ingestion jobs from Airflow

11) **Airflow ↔ Spark Connectivity Hardening (2025-12-22)**
    -   Fixed invalid Airflow log URLs by setting a hostname callable
    -   Pinned Spark master URL to `spark://spark-master:7077`
    -   Mounted `/data` into Airflow so client-mode drivers can read local files

12) **Delta Support in Airflow Client Mode (2025-12-23)**
    -   Added Delta jars + `delta-spark` into the Airflow image
    -   Kept Spark standalone in client deploy mode for Python jobs

13) **MongoDB Spark Connector Integration (2025-12-24)**
    -   Added MongoDB Spark Connector jars to both Spark and Airflow images
    -   Discovered and resolved missing BSON/driver dependency errors
    -   Implemented dual-write pattern: Bronze (Delta) + MongoDB (operational store)
    -   Created reusable Spark session builder with MongoDB URI configuration
    -   Validated read/write operations through Jupyter notebooks

## ⚠️ Challenges and Fixes

### Spark

-   **Spark S3A Filesystem Errors**
    -   Symptom: `ClassNotFoundException: org.apache.hadoop.fs.s3a.S3AFileSystem` during Delta writes.
    -   Root cause: Spark runtime was missing the Hadoop S3A filesystem implementation.
    -   What we tried: Added Delta jars first (fixed `delta.DefaultSource`), but S3A still failed.
    -   Why it failed: Delta depends on S3A; without `hadoop-aws` the filesystem class is missing.
    -   Fix (code): Added `hadoop-aws` JARs into the Spark and Airflow images.
        -   `apps/batch/spark/Dockerfile` adds `/opt/spark/jars/hadoop-aws-<ver>.jar`
        -   `apps/batch/airflow/Dockerfile` mirrors the same JARs for the driver

-   **AWS SDK Version Mismatch**
    -   Symptom: `ClassNotFoundException: software.amazon.awssdk.core.exception.SdkException`.
    -   Root cause: Hadoop 3.4.x expects AWS SDK v2 classes, but only v1 bundle existed.
    -   What we tried: Kept only `aws-java-sdk-bundle` (v1).
    -   Why it failed: Hadoop 3.4.x pulls v2 classes; v1 bundle cannot satisfy them.
    -   Fix (code): Added AWS SDK v2 bundle jars to both images and kept versions aligned.
        -   `apps/batch/spark/Dockerfile` adds `software/amazon/awssdk/bundle`
        -   `apps/batch/airflow/Dockerfile` adds the same bundle for the driver

-   **Spark Python Jobs in Cluster Deploy Mode**
    -   Symptom: `Cluster deploy mode is currently not supported for python applications on standalone clusters.`
    -   Root cause: Spark standalone does not support Python in cluster mode.
    -   Fix: switch to `spark.submit.deployMode=client` for Python jobs.

### Airflow

-   **Executor Crashes Due to JAR Shipping**
    -   Symptom: Netty transport errors while sending a 700MB AWS SDK bundle, followed by
        `Lost executor ... Unable to create executor`.
    -   Root cause: `jars=` in `SparkSubmitOperator` forced the driver (Airflow) to ship
        huge JARs to executors even though they were already baked into the image.
    -   What we tried: Passed S3A/SDK jars via `jars=` in the DAG.
    -   Why it failed: Driver had to stream very large jars to executors, causing instability.
    -   Fix (code): Removed `jars=` and relied on pre-baked `/opt/spark/jars`.
        -   `apps/batch/airflow/dags/spark_users_businesses_batch.py`

-   **Airflow Logs Not Loading**
    -   Symptom: Airflow UI showed log URLs like `http://:8793/log/...` (empty host).
    -   Root cause: Airflow could not resolve a hostname for task logs.
    -   What we tried: Restarted services without fixing hostname source.
    -   Why it failed: Airflow kept rendering empty host URLs.
    -   Fix (code): Set a deterministic hostname for the worker and log server host.
        -   `docker-compose.airflow.yml` adds `hostname: airflow-worker`
        -   `docker-compose.airflow.yml` sets
            `AIRFLOW__LOGGING__WORKER_LOG_SERVER_HOST=airflow-worker`
        -   `docker-compose.airflow.yml` sets
            `AIRFLOW__CORE__HOSTNAME_CALLABLE=airflow.utils.net.get_host_ip_address`

-   **SparkSubmitOperator + Standalone Master URL**
    -   Symptom: `Could not parse Master URL: 'spark-master:7077'`.
    -   Root cause: Airflow connection normalized the host and stripped the scheme.
    -   What we tried:
        -   `AIRFLOW_CONN_SPARK_DEFAULT` (conn-uri) and `conn-json` in compose
        -   Cluster deploy mode (failed for PySpark on standalone)
    -   Why it failed: `conn-json` stores host/port without scheme, which yielded
        `spark-master:7077` at submit time.
    -   Fix: explicitly set `spark.master` in the DAG conf so `spark-submit` gets
        `spark://spark-master:7077`.

-   **Airflow CLI Connection Creation in Compose**
    -   Symptom: `services.airflow-cli.environment.command must be a string...`
    -   Root cause: `command:` was nested under `environment:` in YAML.
    -   Fix: moved `command` to the correct level under `airflow-cli`.

-   **Airflow ↔ Spark Execution Dependencies**
    -   Symptom: `spark-submit` failed due to missing Java/Spark binaries.
    -   Root cause: SparkSubmitOperator runs `spark-submit` inside Airflow container.
    -   Fix: install OpenJDK + Spark in the Airflow image and set `SPARK_HOME`.

-   **Delta Format Not Found in Client Mode**
    -   Symptom: writes failed when using `df.write.format("delta")`.
    -   Root cause: Airflow driver image lacked Delta jars/extensions even though
        Spark worker image had them.
    -   Fix: added Delta jars + `delta-spark` to `apps/batch/airflow/Dockerfile`
        and kept client mode so the driver loads Delta.

-   **Local File Paths Not Found in Airflow Driver**
    -   Symptom: `PATH_NOT_FOUND` for `/data/raw/split/...` in client mode.
    -   Root cause: Airflow containers mounted data at `/opt/airflow/data`, not `/data`.
    -   Fix: added `./data:/data:ro` to `docker-compose.airflow.yml`.

### Kafka

-   **Kafka DNS Resolution Outside Docker**
    -   Symptom: `NoBrokersAvailable` when running producer on the host.
    -   Root cause: `broker:29092` only resolves inside Docker networks.
    -   What we tried: Used `broker:29092` from the host.
    -   Why it failed: Host DNS cannot resolve Docker service names.
    -   Fix (code/docs): Switched host examples to `localhost:9092`.
        -   `local/scripts/produce_reviews_to_kafka.py` example updated
        -   `.env.example` keeps Docker defaults for container runs

### DuckDB

-   **DuckDB Alpine Package Missing**
    -   Symptom: `apk add duckdb` failed (`no such package`).
    -   Root cause: Alpine repositories do not ship a DuckDB package.
    -   What we tried: `apk add --no-cache duckdb`.
    -   Why it failed: Package not available in Alpine repos.
    -   Fix: Switched away from Alpine-based installs and evaluated alternate approaches.

-   **PEP 668 and Build Failures on Alpine**
    -   Symptom: `externally-managed-environment` and missing `g++`/CMake during `pip install duckdb`.
    -   Root cause: Alpine Python enforces PEP 668 and requires a C++ toolchain to build from source.
    -   What we tried:
        -   `pip install duckdb` → blocked by PEP 668
        -   `pip install --break-system-packages duckdb` → attempted source build
        -   Added `build-base cmake ninja` → still required building from source on Alpine
    -   Why it failed: DuckDB sdist required a full C++ toolchain/build on Alpine; still brittle and slow.
    -   Fix: Moved to `python:*-slim` and ultimately to the official `duckdb/duckdb` image to avoid builds.

-   **DuckDB CLI Not Found in Container**
    -   Symptom: `duckdb: not found` when starting the UI.
    -   Root cause: Python package install does not always include the CLI binary.
    -   What we tried: `pip install duckdb` on `python:*-slim` base.
    -   Why it failed: CLI binary not on PATH for the container runtime.
    -   Fix: Use official `duckdb/duckdb` image (CLI included) for the UI service.

-   **Headless UI Browser Launch**
    -   Symptom: `xdg-open: not found` when UI tries to open a browser.
    -   Root cause: Container has no desktop/browser.
    -   Fix (config): Set `DUCKDB_NO_BROWSER=1` in compose to suppress auto-open.

-   **DuckDB Server Flag Not Recognized**
    -   Symptom: `Error: unknown option: -listen` when starting the DuckDB server.
    -   Root cause: cached `duckdb/duckdb:latest` image did not support `--listen`.
    -   What we tried: Running `duckdb --listen` directly in the container.
    -   Why it failed: the installed DuckDB CLI version lacked server-mode support.
    -   Fix: Build a custom DuckDB image from `apps/analytics/duckdb` with a pinned CLI version.

-   **No Built-In DuckDB Web UI**
    -   Symptom: Could not reach a DuckDB UI over HTTP.
    -   Root cause: the official DuckDB image only provides the CLI, not a web UI.
    -   What we tried: Exposing ports and expecting a UI on the DuckDB service.
    -   Why it failed: no HTTP server exists without an explicit wrapper.
    -   Fix: Added a minimal FastAPI wrapper (`/health`, `/query`) to provide an HTTP endpoint.

### MongoDB

-   **MongoDB Spark Connector ClassNotFoundException**
    -   Symptom: `java.lang.ClassNotFoundException: com.mongodb.spark.sql.connector.MongoTableProvider` when writing to MongoDB.
    -   Root cause: MongoDB Spark Connector JAR was missing from Spark classpath.
    -   What we tried: Added `mongo-spark-connector` JAR to Spark image.
    -   Why it initially failed: Connector alone wasn't enough; needed full driver stack.
    -   Fix (code): Added MongoDB Spark Connector + driver JARs to both Spark and Airflow images.
        -   `apps/batch/spark/Dockerfile` and `apps/batch/airflow/Dockerfile`

-   **MongoDB BSON Dependency Missing**
    -   Symptom: `java.lang.NoClassDefFoundError: org/bson/BsonValue` when executing MongoDB operations.
    -   Root cause: MongoDB Spark Connector depends on the MongoDB Java Driver, which includes BSON classes.
    -   What we tried: Only added the Connector JAR, assuming it was self-contained.
    -   Why it failed: The connector is not a fat JAR; it requires separate driver dependencies.
    -   Fix (code): Added three additional MongoDB driver JARs:
        -   `mongodb-driver-sync-5.6.2.jar`
        -   `mongodb-driver-core-5.6.2.jar`
        -   `bson-5.6.2.jar`
        -   Applied to both `apps/batch/spark/Dockerfile` and `apps/batch/airflow/Dockerfile`

-   **MongoDB Connection URI Configuration**
    -   Symptom: Connection failures or authentication errors when connecting to MongoDB from Spark.
    -   Root cause: Spark needs explicit MongoDB connection URI configuration for both read and write operations.
    -   What we tried: Set only `spark.mongodb.write.connection.uri`.
    -   Why it failed: Read operations also need explicit configuration; Spark doesn't infer from write config.
    -   Fix (code): Created centralized MongoDB URI builder and configured both read/write URIs.
        -   `apps/batch/spark/jobs/utils.py` - `_mongo_uri()` function
        -   `apps/batch/spark/jobs/spark_session.py` - sets both read and write URIs
        -   Format: `mongodb://{user}:{password}@{host}:{port}/{auth_db}?authSource={auth_db}`

-   **Environment Variable Propagation for MongoDB**
    -   Symptom: Spark jobs couldn't connect to MongoDB due to missing credentials in executor environment.
    -   Root cause: In client mode, environment variables set in DAG only affected the driver, not executors.
    -   What we tried: Set MongoDB env vars only in the DAG configuration.
    -   Why it failed: Executors run in separate JVMs and don't inherit driver environment by default.
    -   Fix (code): Propagate MongoDB environment variables to both driver and executor environments.
        -   `apps/batch/airflow/dags/spark_users_businesses_batch.py`
        -   Set `spark.driverEnv.*` AND `spark.executorEnv.*` for all MongoDB variables

These issues closely mirror production incidents seen in real data teams.

## ❓ Open Questions & Key Decisions

-   **Kafka topic contracts**: keep JSON payloads or formalize schemas (Avro/Protobuf)?
-   **Bronze write format**: Delta vs. Parquet, and what schema evolution rules apply?
-   **Mongo usage**: is it for OLTP serving, metadata storage, or both?
-   **Streaming sink**: when reviews stream in, do they land in Bronze only or also in a serving store?
-   **Environment split**: how to standardize host vs Docker defaults without drift?
-   **OLAP engine**: Postgres vs ClickHouse as the long-term analytics store
    -   Considerations: query latency, concurrency, ops complexity, dbt adapter maturity.
-   **Mongo serving strategy**: batch-only, or dual-write from streaming for app views?
    -   Considerations: eventual consistency, enrichment strategy, backfills.
    -   Current decision: Dual-write from batch (Bronze Delta + MongoDB) for users/businesses
    -   Future consideration: Should reviews also dual-write, or stay Bronze-only?
-   **Airflow Spark connection**: enforce via UI vs code-driven init
    -   Considerations: reproducibility, team onboarding, drift.
-   **Spark deploy mode**: client vs cluster for Python jobs
    -   Decision: client mode (standalone cluster does not support Python in cluster mode).
    -   Considerations: Airflow image must contain Delta/Spark deps and data mounts.

## 🧭 Recent Debugging Timeline (2025-12-22 → 2025-12-24)

-   **12/22** Log URLs invalid (`http://:8793/...`) → set hostname callable in Airflow.
-   **12/22** Spark master parsing failed (`spark-master:7077`) → pinned `spark.master` in DAG.
-   **12/22** Local data path missing in client mode → mounted `./data:/data:ro` into Airflow.
-   **12/22** Tried PySpark cluster mode on standalone → failed (unsupported).
-   **12/23** Delta format missing in client mode → added Delta jars + `delta-spark` to Airflow image.
-   **12/24** MongoDB Connector ClassNotFoundException → added `mongo-spark-connector` JAR to Spark/Airflow.
-   **12/24** MongoDB BSON dependency error → added MongoDB driver JARs (sync, core, bson) to both images.
-   **12/24** MongoDB connection failures → created centralized URI builder, configured both read/write URIs.
-   **12/24** MongoDB env vars not propagating → set both `spark.driverEnv.*` and `spark.executorEnv.*` in DAG.
-   **12/24** Successfully validated MongoDB dual-write pattern through Jupyter notebooks.

## 🔄 What I'd Do Differently

-   Lock dependency versions earlier (Spark, Hadoop, Delta Lake, AWS SDK, MongoDB drivers)
    to reduce classpath drift and runtime surprises.
-   Add environment-specific documentation upfront
    (host vs Docker networking, and where code is expected to run).
-   Introduce preflight validation checks for S3A, Kafka, MongoDB, and Spark configs.
-   Create a dependency matrix document early showing which JARs are needed for which features
    (Delta, S3A, Kafka, MongoDB) to avoid iterative troubleshooting.
-   Set up a test Spark job that validates all integrations (Delta write, S3A read, MongoDB read/write)
    as a smoke test before building complex pipelines.

## 🧱 Structure and Naming

-   Use role-based service names (`serving-api`, `analytics-api`) so the codebase maps cleanly
    onto the data architecture layers: ingestion + operational serving vs BI/OLAP querying.
-   Align top-level folders with pipeline stages (streaming, batch, storage, analytics, UI)
    to reflect data flow from raw events → lakehouse → serving + dashboards.
-   Treat naming as part of the architecture: clear paths reduce onboarding time and keep OLTP,
    batch, and BI responsibilities from bleeding into each other.
-   Consolidate and prune regularly (e.g., keep notebooks under analytics, remove stale roots)
    so the repository stays navigable as the platform grows.

## 🔮 Next Steps

-   Add Spark Structured Streaming consumers for Kafka review topics.
-   Persist streaming outputs into Bronze Delta tables.
-   Promote the Bronze users/businesses paths into Silver/Gold with dbt models.
-   Add MongoDB indexes and query patterns for operational serving use cases.
-   Integrate DataHub for metadata, lineage, and schema tracking.
-   Add exactly-once semantics discussion (Kafka offsets + Delta idempotency).
-   Expand troubleshooting runbooks into dedicated documentation.
-   Document the dual-write pattern and when to use Delta vs MongoDB for different access patterns.

## ✨ Final Reflection

This project evolved from a local demo into a realistic data engineering system that exposed
the same classes of problems faced in production: dependency drift, networking boundaries,
orchestration pitfalls, and operational observability.

The value of the project lies not only in the final architecture, but in the debugging journey
that shaped it. Each failure taught valuable lessons about distributed systems, dependency management,
and the importance of understanding the entire stack rather than relying on abstractions.

The addition of MongoDB integration highlighted the complexity of managing multiple storage systems
and the critical importance of understanding transitive dependencies in JVM-based ecosystems. This
experience reinforced that modern data platforms are not just about choosing the right tools, but
about deeply understanding how those tools interact at the infrastructure level.
