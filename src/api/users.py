from fastapi import APIRouter, status, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException,\
    InvalidCredentialsException, InvalidCredentialsHTTPException
from src.schemas.users import UserAddRequestDTO, UserLoginDTO
from src.services.users import UserService

router = APIRouter(prefix='/auth', tags=['Пользователи'])

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
    try:
        token = await UserService(db).login_user(data)
    except InvalidCredentialsException:
        raise InvalidCredentialsHTTPException()
    response.set_cookie("access_token", token)
    return {
        "status": "success",
        "data": {"access_token": token}
    }

@router.post("/logout")
async def logout(
        user:UserIdDep,
        response: Response
):
    response.delete_cookie(key="access_token")
    return {"status": "success",
            "data": {"message": "Вы успешно вышли"}
            }

@router.get("/me", description="проверяет есть ли в куках jwt токен и возвращает пользователя")
async def get_me(user: UserIdDep):
    print(user)
    return {
        "status": "success",
        "data": user
    }