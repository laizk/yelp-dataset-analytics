from fastapi import APIRouter, HTTPException
from schemas.business_schema import BusinessSchema
from schemas.user_schema import UserSchema
from schemas.review_schema import ReviewSchema
from services.kafka_producer_services import (
    publish_business_to_kafka,
    publish_user_to_kafka,
    publish_review_to_kafka,
)
from services.mongo_business_services import upsert_business
from services.mongo_user_services import upsert_user
from services.mongo_review_services import upsert_review

kafka_router = APIRouter(prefix="/kafka", tags=["kafka"])
business_router = APIRouter(prefix="/businesses", tags=["businesses"])
user_router = APIRouter(prefix="/users", tags=["users"])
review_router = APIRouter(prefix="/reviews", tags=["reviews"])


@kafka_router.post("/publish/business")
async def publish_business(payload: BusinessSchema):
    """
    Accepts a BusinessSchema JSON body and publishes it to Kafka via the service layer.

    Swagger:
    - Run the serving API, then open http://localhost:8010/docs
    - POST /api/kafka/publish/business with a JSON body like:
      {
        "business_id": "8wGISYjYkE2tSqn3cDMu8A",
        "name": "Nifty Car Rental",
        "address": "1241 Airline Dr",
        "city": "Kenner",
        "state": "LA",
        "postal_code": "70062",
        "latitude": 29.981183,
        "longitude": -90.2540123,
        "stars": 3.5,
        "review_count": 14,
        "is_open": 1,
        "attributes": null,
        "categories": "Automotive, Car Rental, Hotels & Travel, Truck Rental",
        "hours": {
          "Monday": "8:0-17:0",
          "Tuesday": "8:0-17:0",
          "Wednesday": "8:0-17:0",
          "Thursday": "8:0-17:0",
          "Friday": "8:0-17:0",
          "Saturday": "9:0-15:0",
          "Sunday": "9:0-12:0"
        }
      }

    Postman:
    - POST http://localhost:8010/api/kafka/publish/business
    - Body: raw JSON (same payload as above)
    """
    try:
        result = publish_business_to_kafka(payload)
        return {
            "message": "Business published successfully",
            "result": result,
        }
    except Exception as e:
        # Wrap any service error as HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


@kafka_router.post("/publish/user")
async def publish_user(payload: UserSchema):
    """
    Accepts a UserSchema JSON body and publishes it to Kafka via the service layer.

    Swagger:
    - Run the serving API, then open http://localhost:8010/docs
    - POST /api/kafka/publish/user with a JSON body like:
      {
        "user_id": "abc123",
        "name": "Jane Doe",
        "review_count": 12,
        "yelping_since": "2020-01-15",
        "useful": 3,
        "funny": 1,
        "cool": 2,
        "fans": 0,
        "average_stars": 4.2,
        "friends": "",
        "elite": "",
        "compliment_hot": 0,
        "compliment_more": 0,
        "compliment_profile": 0,
        "compliment_cute": 0,
        "compliment_list": 0,
        "compliment_note": 0,
        "compliment_plain": 0,
        "compliment_cool": 0,
        "compliment_funny": 0,
        "compliment_writer": 0,
        "compliment_photos": 0
      }

    Postman:
    - POST http://localhost:8010/api/kafka/publish/user
    - Body: raw JSON (same payload as above)
    """
    try:
        result = publish_user_to_kafka(payload)
        return {
            "message": "User published successfully",
            "result": result,
        }
    except Exception as e:
        # Wrap any service error as HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


@kafka_router.post("/publish/review")
async def publish_review(payload: ReviewSchema):
    """
    Accepts a ReviewSchema JSON body and publishes it to Kafka via the service layer.

    Swagger:
    - Run the serving API, then open http://localhost:8010/docs
    - POST /api/kafka/publish/review with a JSON body like:
      {
        "review_id": "KU_O5udG6zpxOg-VcAEodg",
        "user_id": "mh_-eMZ6K5RLWhZyISBhwA",
        "business_id": "XQfwVwDr-v0ZS3_CbbE5Xw",
        "stars": 3,
        "useful": 0,
        "funny": 0,
        "cool": 0,
        "text": "If you decide to eat here...",
        "date": "2018-07-07 22:09:11"
      }

    Postman:
    - POST http://localhost:8010/api/kafka/publish/review
    - Body: raw JSON (same payload as above)
    """
    try:
        result = publish_review_to_kafka(payload)
        return {
            "message": "Review published successfully",
            "result": result,
        }
    except Exception as e:
        # Wrap any service error as HTTP 500
        raise HTTPException(status_code=500, detail=str(e))


@business_router.post("")
async def register_business(payload: BusinessSchema):
    """
    Accepts a BusinessSchema JSON body and upserts it into MongoDB.
    """
    try:
        result = upsert_business(payload)
        return {
            "message": "Business stored successfully",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.post("")
async def register_user(payload: UserSchema):
    """
    Accepts a UserSchema JSON body and upserts it into MongoDB.
    """
    try:
        result = upsert_user(payload)
        return {
            "message": "User stored successfully",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@review_router.post("")
async def register_review(payload: ReviewSchema):
    """
    Accepts a ReviewSchema JSON body and upserts it into MongoDB.
    """
    try:
        result = upsert_review(payload)
        return {
            "message": "Review stored successfully",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
