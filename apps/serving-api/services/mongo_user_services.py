from typing import Any, Dict, List

from db.mongo import get_user_collection
from schemas.user_schema import UserSchema


def upsert_user(user: UserSchema) -> Dict[str, Any]:
    payload = user.model_dump()
    user_id = payload["user_id"]
    payload["_id"] = user_id

    collection = get_user_collection()
    result = collection.replace_one({"_id": user_id}, payload, upsert=True)

    return {
        "status": "success",
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }


def list_users(limit: int = 20) -> List[Dict[str, Any]]:
    collection = get_user_collection()
    cursor = collection.find().sort("_id", -1).limit(limit)
    items = list(cursor)
    for item in items:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    return items
