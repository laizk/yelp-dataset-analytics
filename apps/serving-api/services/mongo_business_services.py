from typing import Any, Dict

from db.mongo import get_business_collection
from schemas.business_schema import BusinessSchema


def upsert_business(business: BusinessSchema) -> Dict[str, Any]:
    payload = business.model_dump()
    business_id = payload["business_id"]
    payload["_id"] = business_id

    collection = get_business_collection()
    result = collection.replace_one({"_id": business_id}, payload, upsert=True)

    return {
        "status": "success",
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }
