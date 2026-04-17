from fastapi import APIRouter

from src.database import async_session_maker
from src.schemas.users import UserAddRequest
from src.services.users import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/register')
async def register_suer(data:UserAddRequest):
    async with async_session_maker() as session:

        res = await UserService(session).register_user(data)

        return {"status": "ok", "data": res}