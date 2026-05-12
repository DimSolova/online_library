from fastapi import APIRouter, Response, status

from src.api.dependencies import AdminDep, DBDep, UserIdDep
from src.exceptions import (
    InvalidCredentialsException,
    InvalidCredentialsHTTPException,
    InvalidRoleException,
    InvalidRoleHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.schemas.users import (
    ChangeActiveRequest,
    ChangeRoleRequest,
    UserAddRequestDTO,
    UserDTO,
    UserLoginDTO,
)
from src.services.users import UserService
from src.tasks.tasks import test_task

router = APIRouter(prefix="/auth", tags=["Пользователи"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: DBDep, data: UserAddRequestDTO) -> dict:
    try:
        user = await UserService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException()
    return {"status": "success", "data": user}


@router.post("/login")
async def login_user(response: Response, db: DBDep, data: UserLoginDTO):
    try:
        token = await UserService(db).login_user(data)
    except InvalidCredentialsException:
        raise InvalidCredentialsHTTPException()
    response.set_cookie("access_token", token)
    return {"status": "success", "data": {"access_token": token}}


@router.post("/logout")
async def logout(user: UserIdDep, response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "success", "data": {"message": "Вы успешно вышли"}}


@router.get("/me", description="проверяет есть ли в куках jwt токен и возвращает пользователя")
async def get_me(user: UserIdDep):
    test_task.delay()
    return {"status": "success", "data": user}


@router.patch("/{user_id}/role")
async def change_user_role(user_id: int, data: ChangeRoleRequest, admin: AdminDep, db: DBDep) -> dict:
    try:
        user: UserDTO = await UserService(db).change_role(user_id, data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except InvalidRoleException:
        raise InvalidRoleHTTPException
    return {
        "status": "success",
        "data": f"у пользователя c id:{user.id} изменена роль на {user.role_id}",
    }


@router.patch("/{user_id}/active")
async def change_user_active(user_id: int, data: ChangeActiveRequest, admin: AdminDep, db: DBDep) -> dict:
    try:
        user: UserDTO = await UserService(db).change_active(user_id, data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return {
        "status": "success",
        "data": f"у пользователя c id:{user_id} is_active {user.is_active}",
    }
