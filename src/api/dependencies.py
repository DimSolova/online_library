from typing import Annotated

from fastapi import Depends, Request, HTTPException
from starlette import status

from src.constants.roles import UserRole
from src.database import async_session_maker
from src.exceptions import TokenNotFoundHTTPException, InvalidTokenException, InvalidTokenHTTPException, \
    RoleForbiddenHTTPException
from src.schemas.users import UserTokenDTO
from src.services.users import UserService
from src.utils.db_manager import DBManager

async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]

def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise TokenNotFoundHTTPException
    return token

def get_current_user(token: str = Depends(get_token)):
    try:
        data = UserService().decode_token(token)
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    user = UserTokenDTO(
        id=data['id'],
        username=data['username'],
        email=data['email'],
        role=data['role'],
        exp=data['exp']
    )
    return user

UserIdDep = Annotated[UserTokenDTO, Depends(get_current_user)]


def require_role(allowed_roles: UserRole | list[UserRole]):
    """Проверка роли пользователя"""
    if isinstance(allowed_roles, UserRole):
        allowed_roles = [allowed_roles]

    allowed_ids = [role.value for role in allowed_roles]
    required_role_names = [role.name for role in allowed_roles]

    def role_checker(user: UserTokenDTO = Depends(get_current_user)) -> UserTokenDTO:
        if user.role not in allowed_ids:
            raise RoleForbiddenHTTPException(required_roles=required_role_names)
        return user
    return role_checker


AdminDep = Annotated[UserTokenDTO, Depends(require_role(UserRole.ADMIN))]
AuthorOrAdminDep = Annotated[UserTokenDTO, Depends(require_role([UserRole.ADMIN, UserRole.AUTHOR]))]
