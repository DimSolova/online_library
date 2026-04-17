from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.users import UserAddRequest
from src.services.users import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/register')
async def register_user(db:DBDep, data:UserAddRequest):
    res = await UserService(db).register_user(data)
    return {"status": "ok", "data": res}