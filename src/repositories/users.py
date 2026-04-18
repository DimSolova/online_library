from pydantic import EmailStr
from sqlalchemy import select

from src.models import UserOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserDTO, UserWithHashDTO


class UserRepository(BaseRepository):
    model = UserOrm
    schema = UserDTO

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = (
            select(self.model)
            .filter_by(email=email)
        )
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashDTO.model_validate(model)
