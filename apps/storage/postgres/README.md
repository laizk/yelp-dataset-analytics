# postgres

## Purpose
Local Postgres storage for analytics and (later) AI/RAG services.

## Structure
- initdb.d/: bootstrap SQL executed when the Postgres volume is created.

## Notes
- Analytics seed data lives in initdb.d/01_analytics_seed.sql.
- AI/RAG seed data can be added later in a separate SQL file.
