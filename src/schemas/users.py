from datetime import date, datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserAddRequestDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserAddDTO(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    role_id: int | None
    is_active: bool
    created_at: datetime
