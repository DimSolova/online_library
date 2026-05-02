from src.exceptions import ObjectAlreadyExistsException, ReviewAlreadyExistsException, ForeignKeyException, \
    BookNotFoundException
from src.schemas.reviews import ReviewAddRequestDTO, ReviewAddDTO
from src.services.base import BaseService


class ReviewsService(BaseService):
    async def add_review(
            self,
            user,
            book_id,
            data: ReviewAddRequestDTO
    ):
        add_review = ReviewAddDTO(
            **data.model_dump(),
            user_id=user.id,
            book_id=book_id
        )
        try:
            res = await self.db.review.add(add_review)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise ReviewAlreadyExistsException
        except ForeignKeyException:
            raise BookNotFoundException

        return res
