#!/bin/bash

echo "Creating project folder structure..."

# Root folders
mkdir -p apps
mkdir -p pipelines
mkdir -p infra
mkdir -p libs
mkdir -p data
mkdir -p docs
mkdir -p assets
mkdir -p tests

# Apps subfolders
mkdir -p apps/ui/streamlit
mkdir -p apps/ui/react

mkdir -p apps/api/fastapi

mkdir -p apps/ai/embeddings
mkdir -p apps/ai/llm
mkdir -p apps/ai/vectordb
mkdir -p apps/ai/retriever

mkdir -p apps/streaming/kafka
mkdir -p apps/streaming/spark_streaming

mkdir -p apps/batch/spark
mkdir -p apps/batch/airflow
mkdir -p apps/batch/dbt

mkdir -p apps/storage/minio
mkdir -p apps/storage/mongodb

mkdir -p apps/analytics/duckdb
mkdir -p apps/analytics/notebooks

mkdir -p apps/datahub

# Pipelines
mkdir -p pipelines/ingestion
mkdir -p pipelines/streaming
mkdir -p pipelines/batch
mkdir -p pipelines/embeddings
mkdir -p pipelines/training

# Infra
mkdir -p infra/docker
mkdir -p infra/compose
mkdir -p infra/terraform
mkdir -p infra/configs

# Libs
mkdir -p libs/utils
mkdir -p libs/logging
mkdir -p libs/monitoring
mkdir -p libs/common_schemas

# Data
mkdir -p data/raw
mkdir -p data/bronze
mkdir -p data/silver
mkdir -p data/gold

# Docs
mkdir -p docs/architecture
mkdir -p docs/data-models
mkdir -p docs/rag-design

# Tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/e2e

echo "Done!"
