from pydantic import BaseModel, EmailStr


class UserAddRequest(BaseModel):

    username: str
    email: EmailStr
    password: str

