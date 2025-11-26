from fastapi import APIRouter, HTTPException
from schemas.business_schema import BusinessSchema
from services.kafka_producer_services import publish_business_to_kafka

router = APIRouter(prefix="/kafka", tags=["kafka"])


@router.post("/publish/business")
async def publish_business(payload: BusinessSchema):
    """
    Accepts a BusinessSchema JSON body and publishes it to Kafka via the service layer.
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
