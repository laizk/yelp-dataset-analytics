FROM python:3.12-slim

# Lightweight HTTP API deps for Postgres
RUN pip install --no-cache-dir fastapi uvicorn[standard] psycopg2-binary clickhouse-connect

WORKDIR /app
COPY app.py /app/app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

# Command is set in docker-compose.yml to start the UI and keep the container alive
