from fastapi import APIRouter, status, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException
from src.schemas.users import UserAddRequestDTO, UserLoginDTO
from src.services.users import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db:DBDep, data:UserAddRequestDTO) -> dict:
    try:
        user = await UserService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException()
    return {
        "status": "success",
        "data": user
    }

@router.post("/login")
async def login_user(
        response: Response,
        db:DBDep,
        data:UserLoginDTO):
    token = await UserService(db).login_user(data)
    response.set_cookie("access_token", token)
    return {
        "status": "success",
        "user": token
    }

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "success"}

@router.get("/me", description="проверяет есть ли в куках jwt токен и возвращает пользователя")
async def get_me(user: UserIdDep):
    return user