from fastapi import APIRouter

from src.schemas.users import UserAddRequest
from src.services.users import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/register')
async def register_suer(data:UserAddRequest):
    res = await UserService().register_user(data)
    return {"status": "ok", "data": res}