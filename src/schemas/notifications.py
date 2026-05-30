from datetime import datetime

from pydantic import BaseModel


class NotificationDTO(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    related_book_id: int
    related_review_id: int
    is_read: bool
    created_at: datetime

class NotificationAddDTO(BaseModel):
    user_id: int
    title: str
    message: str
    related_book_id: int
    related_review_id: int