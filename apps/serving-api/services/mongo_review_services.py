from typing import Any, Dict

from db.mongo import get_review_collection
from schemas.review_schema import ReviewSchema


def upsert_review(review: ReviewSchema) -> Dict[str, Any]:
    payload = review.model_dump()
    review_id = payload["review_id"]
    payload["_id"] = review_id

    collection = get_review_collection()
    result = collection.replace_one({"_id": review_id}, payload, upsert=True)

    return {
        "status": "success",
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }
