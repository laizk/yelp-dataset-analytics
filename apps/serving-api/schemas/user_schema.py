from typing import Optional

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: str = Field(..., description="Primary key")
    name: str = Field(..., description="User display name")
    review_count: int = Field(..., description="Total review count")
    yelping_since: str = Field(..., description="Account creation date")
    useful: int = Field(..., description="Useful vote count")
    funny: int = Field(..., description="Funny vote count")
    cool: int = Field(..., description="Cool vote count")
    fans: int = Field(..., description="Fan count")
    average_stars: float = Field(..., description="Average star rating")
    friends: Optional[str] = Field(default=None, description="Comma-separated friend IDs")
    elite: Optional[str] = Field(default=None, description="Comma-separated elite years")
    compliment_hot: int = Field(..., description="Hot compliment count")
    compliment_more: int = Field(..., description="More compliment count")
    compliment_profile: int = Field(..., description="Profile compliment count")
    compliment_cute: int = Field(..., description="Cute compliment count")
    compliment_list: int = Field(..., description="List compliment count")
    compliment_note: int = Field(..., description="Note compliment count")
    compliment_plain: int = Field(..., description="Plain compliment count")
    compliment_cool: int = Field(..., description="Cool compliment count")
    compliment_funny: int = Field(..., description="Funny compliment count")
    compliment_writer: int = Field(..., description="Writer compliment count")
    compliment_photos: int = Field(..., description="Photos compliment count")
