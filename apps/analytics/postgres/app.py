import os
from typing import List, Any

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "analytics")

app = FastAPI(title="Postgres HTTP API", version="0.1.0")


class QueryRequest(BaseModel):
    sql: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/query")
def run_query(payload: QueryRequest) -> dict:
    sql = payload.sql.strip()
    if not sql:
        raise HTTPException(status_code=400, detail="SQL is required")

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
