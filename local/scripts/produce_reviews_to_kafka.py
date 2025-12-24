#!/usr/bin/env python3
"""
Stream Yelp review JSONL records into Kafka with safety and progress controls.

Usage example (from repo root):
  python local/scripts/produce_reviews_to_kafka.py \
    --bootstrap localhost:9092 \
    --topic raw_data_review \
    --max-records 10000 \
    --sleep-seconds 2 \
    --log-every 1
"""
import argparse
import json
import logging
import os
import time
from pathlib import Path
from typing import Optional

from kafka import KafkaProducer


def _default_bootstrap() -> str:
    """Pick the Kafka server address from env; fall back to the local default."""
    return (
        os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        or os.getenv("KAFKA_BOOTSTRAP")
        or "broker:29092"
    )


def _default_topic() -> str:
    """Choose the Kafka topic name for reviews; use the project default if unset."""
    return os.getenv("KAFKA_TOPIC_REVIEW") or "raw_data_review"


def _iter_jsonl(path: Path, start_line: int) -> tuple[int, dict]:
    """Read the JSONL file line by line and return each row as a Python dict."""
    with path.open("r", encoding="utf-8") as handle:
        for idx, line in enumerate(handle, start=1):
            if idx < start_line:
                continue
            line = line.strip()
            if not line:
                continue
            yield idx, json.loads(line)


def _send_reviews(
    producer: KafkaProducer,
    topic: str,
    path: Path,
    start_line: int,
    max_records: Optional[int],
    flush_interval: int,
    log_every: int,
    sleep_seconds: float,
) -> int:
    """
    Send review rows to Kafka with progress logs and periodic flushes.

    Features:
    - start_line: resume from a specific line in the file.
    - max_records: limit how many rows to send in a single run.
    - flush_interval: push buffered messages regularly so memory doesn't grow.
    - log_every: print progress updates for long runs.
    """
    logging.info(
        "Starting producer: file=%s topic=%s start_line=%d max_records=%s",
        path,
        topic,
        start_line,
        str(max_records) if max_records is not None else "all",
    )
    sent = 0
    failures = 0
    start_time = time.time()

    for line_no, row in _iter_jsonl(path, start_line):
        review_id = row.get("review_id")
        try:
            producer.send(topic, key=review_id, value=row)
            sent += 1
        except Exception:  # noqa: BLE001 - want to keep sending
            failures += 1

        if sent and sent % flush_interval == 0:
            # Flush forces buffered messages out to Kafka and waits for acks.
            # This uses local process memory; flush makes sure records are sent
            # and acknowledged instead of sitting in the producer buffer.
            producer.flush()

        if sent and sent % log_every == 0:
            elapsed = time.time() - start_time
            rate = sent / elapsed if elapsed else 0.0
            sample_text = str(row.get("text", ""))[:120].replace("\n", " ")
            logging.info(
                "Sent %d records (failures=%d, line=%d, rate=%.1f msg/s, sample=%s)",
                sent,
                failures,
                line_no,
                rate,
                sample_text,
            )

        if max_records and sent >= max_records:
            break

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    producer.flush()
    logging.info("Done. Sent %d records (failures=%d).", sent, failures)
    return sent


def main() -> None:
    """
    Parse CLI args, connect to Kafka, and stream review records.

    Features:
    - CLI overrides for file path, topic, and bootstrap servers.
    - Start-line and max-records controls for partial loads or retries.
    - Tunable flush/log intervals for throughput vs. observability.
    """
    parser = argparse.ArgumentParser(
        description="Produce Yelp review part1 JSONL records into Kafka."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/split/yelp_academic_dataset_review_part1.jsonl"),
        help="Path to review JSONL part1 file",
    )
    parser.add_argument(
        "--bootstrap",
        default=_default_bootstrap(),
        help="Kafka bootstrap servers (env KAFKA_BOOTSTRAP_SERVERS or KAFKA_BOOTSTRAP)",
    )
    parser.add_argument(
        "--topic",
        default=_default_topic(),
        help="Kafka topic (env KAFKA_TOPIC_REVIEW)",
    )
    parser.add_argument(
        "--start-line",
        type=int,
        default=1,
        help="Line number to start from (1-based)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=None,
        help="Max records to send (default: send all)",
    )
    parser.add_argument(
        "--flush-interval",
        type=int,
        default=1000,
        help="Flush producer every N records",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=5000,
        help="Log progress every N records",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Pause after each record to throttle send rate",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        key_serializer=lambda v: v.encode("utf-8") if v else None,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=True).encode("utf-8"),
        retries=5,
        acks="all",
    )

    _send_reviews(
        producer=producer,
        topic=args.topic,
        path=args.input,
        start_line=max(args.start_line, 1),
        max_records=args.max_records,
        flush_interval=max(args.flush_interval, 1),
        log_every=max(args.log_every, 1),
        sleep_seconds=max(args.sleep_seconds, 0.0),
    )


if __name__ == "__main__":
    main()
