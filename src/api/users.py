from fastapi import APIRouter, status

from src.api.dependencies import DBDep
from src.schemas.users import UserAddRequestDTO
from src.services.users import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db:DBDep, data:UserAddRequestDTO) -> dict:
    user = await UserService(db).register_user(data)
    return {
        "status": "success",
        "data": user
    }