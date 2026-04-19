"""
Сервисный слой для работы с пользователями.
Содержит всю бизнес-логику, связанную с User.
"""
from datetime import timedelta, datetime, timezone

import jwt
from pwdlib import PasswordHash

from src.config import setting
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException
from src.schemas.users import UserAddDTO
from src.services.base import BaseService

#PasswordHash с рекомендованными настройками — он будет использоваться для хэширования и проверки паролей.
password_hash = PasswordHash.recommended()


class UserService(BaseService):

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)

    def verify_password(self,plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    def decode_token(self, token):
        return jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])


    async def register_user(self, data):
        hashed_password = self.get_password_hash(data.password)
        _data = UserAddDTO(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
            role_id=3
        )
        try:
            user = await self.db.users.add(_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        return user

    async def login_user(self, data):
        """Получаем юзера по email, даже если пароль не верный,
         а далее делаем проверку на пароль
        Если прошло то возвращаем пользователя"""
        user = await self.db.users.get_user_with_hashed_password(data.email)
        if not self.verify_password(data.password, user.hashed_password):
            raise Exception
        data = {
            "id":user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role_id
        }
        token = self.create_access_token(data)
        return token

