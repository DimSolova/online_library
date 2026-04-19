from typing import Annotated

from fastapi import Depends, Request
from src.database import async_session_maker
from src.exceptions import TokenNotFoundHTTPException, InvalidTokenException, InvalidTokenHTTPException
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
    return data




UserIdDep = Annotated[str, Depends(get_current_user)]