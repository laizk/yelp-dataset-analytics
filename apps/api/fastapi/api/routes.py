from fastapi import APIRouter, HTTPException
from schemas.business_schema import BusinessSchema

router = APIRouter()

@router.post('/kafka/publish/business')
async def publish_business(payload: BusinessSchema):
    # You now have a fully validated payload
    # Example: payload.name, payload.business_id, etc.

    try:
        # TODO: send to Kafka
        # kafka_producer.send("business_topic", payload.dict())

        return {"message": "Business published successfully", "data": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

