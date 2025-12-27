FROM python:3.12-slim

COPY requirements.txt app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
