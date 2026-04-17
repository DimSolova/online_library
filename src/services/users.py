"""
Сервисный слой для работы с пользователями.
Содержит всю бизнес-логику, связанную с User.
"""

from pwdlib import PasswordHash

from src.schemas.users import UserAddDTO
from src.services.base import BaseService

#PasswordHash с рекомендованными настройками — он будет использоваться для хэширования и проверки паролей.
password_hash = PasswordHash.recommended()


class UserService(BaseService):

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)


    async def register_user(self, data):
        hashed_password = self.get_password_hash(data.password)
        _data = UserAddDTO(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
            role_id=3
        )
        user = await self.db.users.add(_data)
        await self.db.commit()
        return user

