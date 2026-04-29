from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserAddRequestDTO(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginDTO(BaseModel):
    """Схема для логина пользователя"""

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "user@example.com", "password": "string"}
        }
    )


class UserAddDTO(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int


class UserTokenDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: int
    is_active: bool
    exp: int


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    role_id: int | None
    is_active: bool
    created_at: datetime

    # Позволяет не прокидывать None
    model_config = ConfigDict(
        from_attributes=True,  # позволяет принимать SQLAlchemy объекты
    )


class UserWithHashDTO(UserDTO):
    hashed_password: str


class ChangeRoleRequest(BaseModel):
    role_id: int


class ChangeActiveRequest(BaseModel):
    is_active: bool
