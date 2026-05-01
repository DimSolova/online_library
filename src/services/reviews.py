from src.schemas.reviews import ReviewAddRequestDTO
from src.services.base import BaseService


class ReviewsService(BaseService):
    async def add_review(
            self,
            book_id: int,
            data: ReviewAddRequestDTO
    ):

        print(book_id)
        print(data)
        return book_id
