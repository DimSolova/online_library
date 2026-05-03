from datetime import datetime

from pydantic import BaseModel, Field

class FavoriteAddDTO(BaseModel):

    user_id: int
    book_id: int

class FavoriteDTO(FavoriteAddDTO):
    id: int
