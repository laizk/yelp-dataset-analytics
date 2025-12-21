import os
from typing import List, Any

import clickhouse_connect
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "analytics")
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "clickhouse")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "clickhouse")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "clickhouse123")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "analytics")

app = FastAPI(title="Postgres HTTP API", version="0.1.0")


class QueryRequest(BaseModel):
    sql: str

    class Config:
        json_schema_extra = {
            "examples": [
                {"sql": "SELECT * FROM analytics.seed LIMIT 100"},
                {"sql": "SELECT name, created_at FROM analytics_seed LIMIT 5"},
            ]
        }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


def _validate_sql(sql: str) -> str:
    sql = sql.strip()
    if not sql:
        raise HTTPException(status_code=400, detail="SQL is required")
    return sql


@app.post("/query")
def run_query(payload: QueryRequest) -> dict:
    sql = _validate_sql(payload.sql)

    try:
        with psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                columns: List[str] = [col[0] for col in cursor.description] if cursor.description else []
                rows: List[Any] = cursor.fetchall() if columns else []
    except Exception as exc:  # pragma: no cover - simple guardrail
        raise HTTPException(status_code=400, detail=f"Query failed: {exc}") from exc

    data = [dict(zip(columns, row)) for row in rows] if columns else []
    return {"columns": columns, "rows": data}


@app.post("/query/postgres")
def run_query_postgres(payload: QueryRequest) -> dict:
    sql = _validate_sql(payload.sql)

    try:
        with psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                columns: List[str] = [col[0] for col in cursor.description] if cursor.description else []
                rows: List[Any] = cursor.fetchall() if columns else []
    except Exception as exc:  # pragma: no cover - simple guardrail
        raise HTTPException(status_code=400, detail=f"Query failed: {exc}") from exc

    data = [dict(zip(columns, row)) for row in rows] if columns else []
    return {"columns": columns, "rows": data}


@app.post("/query/clickhouse")
def run_query_clickhouse(payload: QueryRequest) -> dict:
    sql = _validate_sql(payload.sql)

    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
        )
        result = client.query(sql)
        columns: List[str] = list(result.column_names) if result.column_names else []
        rows: List[Any] = result.result_rows if columns else []
    except Exception as exc:  # pragma: no cover - simple guardrail
        raise HTTPException(status_code=400, detail=f"Query failed: {exc}") from exc

    data = [dict(zip(columns, row)) for row in rows] if columns else []
    return {"columns": columns, "rows": data}
