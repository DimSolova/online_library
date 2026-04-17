from datetime import date

from pydantic import BaseModel, EmailStr


class UserAddRequest(BaseModel):

    username: str
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    role_id: int

class User:
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    created_at: date
    role_id: int