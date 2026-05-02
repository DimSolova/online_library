from datetime import datetime

from pydantic import BaseModel, Field


class ReviewAddRequestDTO(BaseModel):
    rating: int = Field(ge=1, le=5)
    text: str

class ReviewAddDTO(ReviewAddRequestDTO):

    book_id: int
    user_id: int

class ReviewDTO(ReviewAddRequestDTO):
    id: int

    created_at: datetime
    updated_at: datetime