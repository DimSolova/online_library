from pydantic import EmailStr
from sqlalchemy import select

from src.models import UserOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import UserDataMapper, UserHashDataMapper


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res = await self.session.execute(query)
        model = res.scalars().one_or_none()
        if not model:
            return None
        return UserHashDataMapper.map_to_domain_entity(model)
