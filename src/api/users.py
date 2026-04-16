from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get('')
async def get_me():
    return {"status": "ok"}