from pydantic import BaseModel, Field


class ReviewSchema(BaseModel):
    review_id: str = Field(..., description="Primary key")
    user_id: str = Field(..., description="User ID")
    business_id: str = Field(..., description="Business ID")
    stars: int = Field(..., description="Star rating")
    useful: int = Field(..., description="Useful vote count")
    funny: int = Field(..., description="Funny vote count")
    cool: int = Field(..., description="Cool vote count")
    text: str = Field(..., description="Review text")
    date: str = Field(..., description="Review date timestamp")
