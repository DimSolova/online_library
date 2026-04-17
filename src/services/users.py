from src.repositories.users import UserRepository
from src.schemas.users import UserAdd
from src.services.base import BaseService


class UserService(BaseService):

    async def register_user(self, data):
        _data = UserAdd(
            **data.model_dump(),
            hashed_password=data.password,
            role_id=3
        )
        await UserRepository(self.session).add(_data)
        await self.session.commit()

        return data

