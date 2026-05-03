from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.reviews import ReviewDTO


class BookAddRequestDTO(BaseModel):
    title: str
    description: str
    isbn: str
    author: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Идиот",
                "description": "Книга про идиота",
                "isbn": "9785389071278",
                "author": "Ф.М. Достоевский",
            }
        }
    )


class BookDTOAdd(BookAddRequestDTO):
    added_by_id: int


class BookPATCHDTO(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Идиот",
                "description": "Книга про идиота",
                "isbn": "9785389071278",
                "author": "Ф.М. Достоевский",
            }
        }
    )


class BookDTO(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    description: str
    added_by_id: int
    created_at: datetime
    updated_at: datetime


class BookWithRelsDTO(BookDTO):
    reviews: list[ReviewDTO] = []
