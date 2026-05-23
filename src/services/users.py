"""
Сервисный слой для работы с пользователями.
Содержит всю бизнес-логику, связанную с User.
"""

from datetime import UTC, datetime, timedelta

import jwt
from jwt import PyJWTError
from pwdlib import PasswordHash

from src.config import setting
from src.exceptions import (
    ForeignKeyException,
    InvalidCredentialsException,
    InvalidRoleException,
    InvalidTokenException,
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.schemas.users import ChangeActiveRequest, ChangeRoleRequest, UserAddDTO, UserDTO
from src.services.base import BaseService
from src.tasks.tasks import send_emails_to_users_with_favorites_books

# PasswordHash с рекомендованными настройками — он будет использоваться для хэширования и проверки паролей.
password_hash = PasswordHash.recommended()


class UserService(BaseService):
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        return encoded_jwt

    def get_password_hash(self, password: str) -> str:
        return password_hash.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    def decode_token(self, token):
        try:
            return jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        except PyJWTError:
            raise InvalidTokenException

    async def register_user(self, data):
        hashed_password = self.get_password_hash(data.password)
        token_data = UserAddDTO(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
            role_id=3,
        )
        try:
            user = await self.db.users.add(token_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        return user

    async def login_user(self, data):
        """Получаем пользователя и далее делаем проверку на
        Существующего пользователя и на верный пароль и оборачиваем в одно исключение
        Лучше возвращать одну ошибку на email и password"""
        user = await self.db.users.get_user_with_hashed_password(data.email)
        if not user or not self.verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsException

        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role_id,
            "is_active": user.is_active,
        }
        send_emails_to_users_with_favorites_books.delay(user.id)  # type: ignore[attr-defined]
        token = self.create_access_token(data)
        return token

    async def change_role(self, user_id: int, data: ChangeRoleRequest) -> UserDTO:
        try:
            user: UserDTO = await self.db.users.edit(data, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        except ForeignKeyException:
            raise InvalidRoleException

        await self.db.commit()
        return user

    async def change_active(self, user_id: int, data: ChangeActiveRequest) -> UserDTO:
        try:
            user: UserDTO = await self.db.users.edit(data, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        await self.db.commit()
        return user
