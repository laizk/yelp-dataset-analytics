from typing import Dict, Optional
from pydantic import BaseModel, Field


class BusinessHours(BaseModel):
    """
    Opening hours for each day of the week.
    All fields optional because some businesses may not open daily.
    """
    Monday: Optional[str] = None
    Tuesday: Optional[str] = None
    Wednesday: Optional[str] = None
    Thursday: Optional[str] = None
    Friday: Optional[str] = None
    Saturday: Optional[str] = None
    Sunday: Optional[str] = None


class BusinessSchema(BaseModel):
    business_id: str = Field(..., description="Primary key")
    name: str = Field(..., description="Business name")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    postal_code: str = Field(..., description="Postal code")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    stars: float = Field(..., description="Average rating")
    review_count: int = Field(..., description="Number of reviews")
    is_open: int = Field(..., description="1 = open, 0 = closed")

    attributes: Optional[Dict[str, object]] = Field(
        default=None, description="Business attributes"
    )
    
    categories: str = Field(
        ..., description="Comma-separated list of categories"
    )
    
    hours: Optional[BusinessHours] = Field(
        default=None, description="Business hours for each day"
    )
