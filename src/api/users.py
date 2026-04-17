from fastapi import APIRouter

from src.schemas.users import UserAddRequest

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('')
async def register_suer(data:UserAddRequest):
    return {"status": "ok", "data": data}