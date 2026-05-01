from datetime import datetime

from pydantic import BaseModel


class ReviewAddRequestDTO(BaseModel):
    rating: int
    text: str

class ReviewAddDTO(ReviewAddRequestDTO):

    book_id: int
    user_id: int

class ReviewDTO(ReviewAddRequestDTO):
    id: int

    created_at: datetime
    updated_at: datetime