#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
from typing import Iterable, Set, Tuple, TextIO


def _stable_bucket(value: str, ratio: float) -> int:
    digest = hashlib.md5(value.encode("utf-8")).hexdigest()
    bucket = int(digest, 16) / (16 ** 32)
    return 1 if bucket < ratio else 2


def _iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _write_jsonl(path: Path, rows: Iterable[dict]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True))
            handle.write("\n")
            count += 1
    return count


def _write_row(handle: TextIO, row: dict) -> None:
    handle.write(json.dumps(row, ensure_ascii=True))
    handle.write("\n")


def _split_entities_stream(
    rows: Iterable[dict],
    id_key: str,
    ratio: float,
    out_part1: TextIO,
    out_part2: TextIO,
) -> Tuple[Set[str], int, int]:
    part1_ids: Set[str] = set()
    part1_count = 0
    part2_count = 0

    for row in rows:
        entity_id = row.get(id_key)
        if not entity_id:
            continue
        if _stable_bucket(entity_id, ratio) == 1:
            part1_ids.add(entity_id)
            _write_row(out_part1, row)
            part1_count += 1
        else:
            _write_row(out_part2, row)
            part2_count += 1

    return part1_ids, part1_count, part2_count


def _split_reviews(
    rows: Iterable[dict],
    user_ids_part1: Set[str],
    business_ids_part1: Set[str],
    out_part1: TextIO,
    out_part2: TextIO,
) -> Tuple[int, int, int]:
    part1_count = 0
    part2_count = 0
    missing_refs = 0

    for row in rows:
        user_id = row.get("user_id")
        business_id = row.get("business_id")
        if not user_id or not business_id:
            missing_refs += 1
            _write_row(out_part2, row)
            part2_count += 1
            continue
        if user_id in user_ids_part1 and business_id in business_ids_part1:
            _write_row(out_part1, row)
            part1_count += 1
        else:
            _write_row(out_part2, row)
            part2_count += 1

    return part1_count, part2_count, missing_refs


def main() -> None:
    parser = argparse.ArgumentParser(description="Split Yelp JSONL files into two consistent batches.")
    parser.add_argument("--business", required=True, type=Path, help="Path to yelp business JSONL file")
    parser.add_argument("--user", required=True, type=Path, help="Path to yelp user JSONL file")
    parser.add_argument("--review", required=True, type=Path, help="Path to yelp review JSONL file")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory")
    parser.add_argument("--ratio", type=float, default=0.5, help="Ratio for part1 (default: 0.5)")
    args = parser.parse_args()

    if not (0.0 < args.ratio < 1.0):
        raise ValueError("ratio must be between 0 and 1")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    business_part1_path = args.out_dir / "yelp_academic_dataset_business_part1.jsonl"
    business_part2_path = args.out_dir / "yelp_academic_dataset_business_part2.jsonl"
    user_part1_path = args.out_dir / "yelp_academic_dataset_user_part1.jsonl"
    user_part2_path = args.out_dir / "yelp_academic_dataset_user_part2.jsonl"
    review_part1_path = args.out_dir / "yelp_academic_dataset_review_part1.jsonl"
    review_part2_path = args.out_dir / "yelp_academic_dataset_review_part2.jsonl"

    with business_part1_path.open("w", encoding="utf-8") as business_part1_out, \
        business_part2_path.open("w", encoding="utf-8") as business_part2_out, \
        user_part1_path.open("w", encoding="utf-8") as user_part1_out, \
        user_part2_path.open("w", encoding="utf-8") as user_part2_out, \
        review_part1_path.open("w", encoding="utf-8") as review_part1_out, \
        review_part2_path.open("w", encoding="utf-8") as review_part2_out:
        user_part1_ids, user_part1_count, user_part2_count = _split_entities_stream(
            _iter_jsonl(args.user), "user_id", args.ratio, user_part1_out, user_part2_out
        )
        business_part1_ids, business_part1_count, business_part2_count = _split_entities_stream(
            _iter_jsonl(args.business), "business_id", args.ratio, business_part1_out, business_part2_out
        )
        review_part1_count, review_part2_count, missing_refs = _split_reviews(
            _iter_jsonl(args.review),
            user_part1_ids,
            business_part1_ids,
            review_part1_out,
            review_part2_out,
        )

    print("Split complete:")
    print(f"  businesses: part1={business_part1_count}, part2={business_part2_count}")
    print(f"  users: part1={user_part1_count}, part2={user_part2_count}")
    print(f"  reviews: part1={review_part1_count}, part2={review_part2_count}")
    if missing_refs:
        print(f"  reviews with missing refs routed to part2: {missing_refs}")


if __name__ == "__main__":
    main()
