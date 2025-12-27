# Project Checklist

## Serving API
- [x] Create serving API service with health endpoint.
- [x] Add Kafka publish endpoints for business/user/review.
- [x] Add MongoDB upsert endpoints for business/user/review.
- [x] Configure Mongo connection settings via env.
- [ ] Add basic validation and clearer error responses per endpoint.
- [ ] Add MongoDB index strategy for `businesses`, `users`, `reviews`.
- [ ] Add read endpoints for recent `businesses`, `users`, `reviews` to support UI lists.
- [ ] Add API request logging and correlation IDs.
- [ ] Document `SERVING_API_URL` and Mongo env vars in README.

## Analytics API
- [x] Health check endpoint.
- [x] Analytics API service exists (Postgres/ClickHouse query endpoints).
- [ ] Document analytics API endpoints and usage in README.
- [ ] Add ClickHouse query endpoint examples to docs.
- [ ] Define analytics API authentication strategy.

## Streamlit UI
- [x] Business registration page wired to serving API (Mongo).
- [x] User registration page wired to serving API (Mongo).
- [x] Review registration page wired to serving API (Mongo).
- [ ] Add pages to list recent businesses/users/reviews from MongoDB.
- [ ] Add success/pending state after form submissions.
- [ ] Add environment switcher (local vs docker endpoints).
- [ ] Add basic input validation before submit.

## Streaming (Kafka + Spark Streaming)
- [x] Kafka topics defined for business/user/review.
- [ ] Define topic contracts for business/user/review in `docs/data-models/`.
- [ ] Implement Kafka-first review ingestion pipeline.
- [ ] Build streaming job to enrich reviews with user/business info.
- [ ] Define enriched review schema and timestamp strategy for MongoDB.

## Batch (Spark + Airflow + dbt)
- [x] Airflow + Spark + dbt services provisioned in compose.
- [ ] Add smoke test job to validate S3A, Delta, Mongo integrations.
- [ ] Document batch job inputs/outputs in `apps/batch/README.md`.
- [ ] Add dbt models for Silver/Gold from Bronze tables.

## Storage (MongoDB + MinIO + Postgres/ClickHouse)
- [x] MongoDB, MinIO, Postgres, ClickHouse services provisioned in compose.
- [ ] Define collection/table naming conventions (Bronze/Silver/Gold).
- [ ] Add indexes for high-traffic query fields.
- [ ] Add retention policy for raw Kafka replay data.

## Infra (Docker + Compose)
- [x] Docker Compose wiring for serving API, analytics API, and Streamlit.
- [ ] Update README Kafka env section to reflect `raw_data_business` + `raw_data_user`.
- [ ] Confirm Compose exposes required ports for UI + APIs.
- [ ] Add compose profiles for minimal vs full stack.

## Docs
- [x] Architecture diagram included in README.
- [ ] Add architecture note separating OLTP vs BI APIs in `docs/architecture/`.
- [ ] Add data contracts for business/user/review in `docs/data-models/`.
- [ ] Add runbooks for local dev + troubleshooting.

## AI / RAG
- [ ] Add embeddings pipeline roadmap in `apps/ai/README.md`.
- [ ] Define vector DB choice and schema.
- [ ] Add retrieval evaluation plan.

## Testing
- [ ] Add API startup + health check smoke tests.
- [ ] Add integration tests for Mongo upsert endpoints.
- [ ] Add streaming job tests for review enrichment.
